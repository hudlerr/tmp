from datetime import timedelta
import random

import secrets
from circle import initialise_circle_state
from chain import create_block
from agents import (AgentData, update_contribution_amount, verify_allocated_amount, get_monthly_default_count, calculate_agent_amount)

"""
    GENESIS STATES
"""
def get_initial_deposits(n):
    agent = [AgentData(secrets.token_bytes(48), 300, i, 0, False, 0, False, 0)
             for i in range(n)]       
    return agent

agent_genesis = get_initial_deposits(10)

genesis_state = {
    'Contributers_On': True, # contributers are active
    'Cheaters_On': False, # cheaters are inactive
    'Total_Volume': 0, # total volume of pool activity (GBP)
    'Honest_Volume': 0, # volume of honest (contributed) activity (GBP)
    'Dishonest_Volume': 0, # volume of dishonest (non-contributed) activity (GBP)
    'Cheats_Volume': 0, # volume of cheater activity (GBP)
    'Contributers_Rating': 0, # total ratings of contributing agent
    'Contributers_Cost': 0, # cost incurred by contributers
    'Contributers_Reward': 0, # rewards collected by contributers
    'Cheaters_Cost': 0, # costs incurred by cheaters
    'Cheater_Reward': 0, # rewards (profit) achieved by cheating 
    'timestep': 0,
    'agent_data': agent_genesis,
    'Duration': 10
}

"""
  POLICIES + BEHAVIOUR GROUPS DEFINITION
  1. Monthly collection policy
  2. Monthly allocation policy
  3. Contributer decision
  4. Cheater decision   
"""
def p_intitiate_monthly_deposits(genesis_state):
    month_sum = 0.0
    expected_month_sum = 0.0
    agent_data = genesis_state['agent_data']
    month = genesis_state['timestep']

    print("\n" + "STARTING ROSCA MONTH " + str(month))
    
    # for each agent add their monthly contribution to the collected pool
    for x in range(0, len(agent_data)):
        agent_contribution = agent_data[x].amount
        expected_month_sum += agent_contribution

        # player decision - initiate contributers behaviour
        if(p_contributer(genesis_state, agent_data[x]) == True):
            month_sum += agent_contribution # c - from differential eq
        else :
            print("Contributer default: GBP" + str(agent_contribution))

    genesis_state['Total_Volume'] = expected_month_sum
    genesis_state['Honest_Volume'] = month_sum
    genesis_state['Dishonest_Volume'] = expected_month_sum - month_sum

    print("Total deposited amount: GBP" + str(genesis_state['Honest_Volume']) + " - Defaulted amount: " + str(genesis_state['Dishonest_Volume']))

    return month_sum 

def p_allocate_pool(state):
    block_agent_data = state['agent_data']
    pool_amount = state['Honest_Volume']
    timestep = genesis_state['timestep']

    for x in range(0, len(block_agent_data)):
        if(block_agent_data[x].standing == timestep and block_agent_data[x].taken == False):
            allocation_amt = calculate_agent_amount(block_agent_data[x], timestep+1, state['Duration']) # a - from differential eq

            print("verify: allocation_amt: " + str(allocation_amt) + ", pool_amount" + str(pool_amount))
            if(verify_allocated_amount(block_agent_data[x], allocation_amt, pool_amount) == True):    
                block_agent_data[x].taken = True
                pool_amount -= allocation_amt

                print("Allocating agent: " + str(block_agent_data[x].pubkey) + ", standing: " + str(block_agent_data[x].standing) + ", amount: GBP" + str(allocation_amt))
                
            else :
                print("Not enough money in pool to allocate agent full amount of: " + str(allocation_amt) + "\n")    
                allocation_amt = pool_amount
                block_agent_data[x].taken = False
                pool_amount = 0.0

            # player decision - initiate cheater behaviour
            if(p_cheater(state, block_agent_data[x], allocation_amt) == True):
                state['Contributers_Cost'] = contributer_cost(state)
                state['Cheaters_On'] = True
                print("Allocator default: GBP" + str(state['Cheater_Reward']))
                block_agent_data[x].defaulted = True

            block_agent_data[x].balance += allocation_amt
    return pool_amount

"""
    AGENT BEHAVIOUR DEFINITION
"""
# contributer motivated to contributed to contribute share if reward > cost of other agents stealing 
def p_contributer(state, agent):
    act = False
    cost = contributer_cost(state)
    reward = contributers_reward(agent, state)

    contributer_strategies = [honest_contributer, influenced_contributer, broke_contributer]
    choose_strategy = random.choice(contributer_strategies)
    
    if(agent.defaulted):
        return act

    print("Shall I contribute? reward: " + str(reward) + " cost: " + str(0.25 * cost) + " strategy: " + str(choose_strategy))
    if (choose_strategy(reward, cost)):
        act = True
        agent.rating += 0.2 # increase rating 
        state['Contributers_Rating'] += 0.2
        agent.contributed_amt += agent.amount # update agent contributed amount

    return act

# cheater motivated to steal the pot if reward > amount contributed so far + agent takes the risk of being caught
def p_cheater(state, agent, allocation_amt):
    act = False
    risk = random.random()
    reward = cheater_reward(agent, allocation_amt)
    cost = cheater_cost(agent, allocation_amt)

    strategies = [honest_allocator, greedy_allocator]
    choose_strategy = random.choice(strategies)
    print("Shall I steal? reward: " + str(reward) + " cost: " + str(cost) + " strategy: " + str(choose_strategy))

    if(choose_strategy(reward, cost)):
        print("YESSSS - YOLO")
        act = True
        state['Cheats_Volume'] += reward 
        state['Cheater_Reward'] = reward
        state['Cheaters_Cost'] = cost

    return act

"""
    AGENT STATEGIES DEFINITION
"""

# three types of contributers
def honest_contributer(reward, cost):
    if(cost > reward): # contributes just as long as cost isnt greater than reward 
       return False
    else :
        return True    


def influenced_contributer(reward, cost):
    if((0.25 * cost) > reward): # gets discouraged from contributing if cost > 25% of reward
       return False
    else :
        return True 

def broke_contributer(reward, cost):       
    if(random.random() < 0.1): # 10% chance this contributer doesn't have enough money to contribute
       return False
    else :
        return True 

# two types of 'cheater'
def honest_allocator(reward, cost):   
    if(cost > reward): # doesn't steal pot as long as cost isnt greater than reward 
       return False
    else :
        return True    

def greedy_allocator(reward, cost):   
    risk = random.random()
    if((reward > cost) and risk < 0.05): # if reward is greater than cost and agent accepts risk of not being caught
        return True
    else:
        return False    

"""
    AGENT REWARD + COST DEFINITION
"""
# contributers's reward per round contributed => amount agreed
def contributers_reward(data, s):
    return calculate_agent_amount(data, s['timestep'], s['Duration'])

# Contributer's cost per round cheater acts => amount defaulted if at all
def contributer_cost(s):
    share = 0.1
    return (share * s['Cheats_Volume'])

# Cheater's reward per cheat
def cheater_reward(s, allocation_amt):
    print("check allocation_amt: " + allocation_amt + " contributed: " + s.contributed_amt)
    return allocation_amt - s.contributed_amt # Pot amount - Contributed amount

# Cheater's cost per cheat caught
delta = 0.05
def cheater_cost(s, allocation_amt):
    return (delta * allocation_amt) + allocation_amt - s.contributed_amt

"""
    STATE UPDATE LOGIC
"""
def s_updatepool(genesis_state, duration):    
    for x in range(0, duration):
        collected_amt = p_intitiate_monthly_deposits(genesis_state) ## initiate contributers behaviour
        pool_amt = p_allocate_pool(genesis_state) ## initiate cheaters behaviour

        genesis_state['timestep'] += 1
        print("Pool amount: GBP" + str(pool_amt) + "\n")


s_updatepool(genesis_state, 10)