from datetime import timedelta
import secrets
from network_helper_functions import (order_agent_standing, choose_amount, check_agent_debt)
from agents import (AgentData, update_contribution_amount, verify_allocated_amount, get_monthly_default_count, calculate_agent_amount)
import random

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
    if(cost > reward and reward < 500): # doesn't steal pot as long as cost isnt greater than reward 
       return True
    else :
        return False    

def greedy_allocator(reward, cost):   
    risk = random.random()
    print("SHALL I CHEAT? REWARD " + str(reward) + " COST: " + str(3*cost) + " RISK: " + str(risk))
    if((reward >= (3*cost)) and (risk < 0.5 and reward != 0)): # if reward is greater than double the cost or agent accepts risk of not being caught
        return True
    else:
        return False  

"""
    GENESIS STATES
"""
def assign_contributing_strategy(i):
    """ ASSIGN CONTRIBUTING STRATEGY """
    contributer_strategies = [honest_contributer, influenced_contributer, broke_contributer]
    tmp = random.choice(contributer_strategies)
    print("AGENT " + str(i) + "\n" + "Contribution strategy: " + str(tmp))
    return tmp

def assign_allocating_strategy(i):
    """ ASSIGN ALLOCATING POOL STRATEGY """
    strategies = [honest_allocator, greedy_allocator]
    tmp = random.choice(strategies)
    print("Allocation strategy: " + str(tmp) + "\n")
    return tmp   

def get_initial_deposits(max_amount, n):
    print("AGENTS ARRIVAL")
    # count = n[0] if len(n) > 0 else n
    agent = [AgentData(secrets.token_bytes(48), choose_amount(max_amount), i, 0, False, 0, False, 0, assign_contributing_strategy(i), assign_allocating_strategy(i), 0)
             for i in range(n)]

    ordered = order_agent_standing(agent)             
    return ordered

"""
  POLICIES + BEHAVIOUR GROUPS DEFINITION
  1. Monthly collection policy
  2. Monthly allocation policy
  3. Contributer decision
  4. Cheater decision   
"""
def p_intitiate_monthly_deposits(params, substep, state_history, previous_state):
    state = previous_state['pool_state'].data[0]['data']
    month_sum = 0.0
    expected_month_sum = 0.0
    agent_data = state['Agent_Data']
    month = previous_state['timestep']

    print("\n" + "STARTING ROSCA MONTH " + str(month) + " - POOL AMOUNT: " + str(state['Surplus_Volume']) + " - MAX_A: " + str(params['max_amount']) + " - PARTIC: " + str(params['participants']))

    # for each agent add their monthly contribution to the collected pool
    for x in range(0, len(agent_data)):
        agent_contribution = agent_data[x].amount
        expected_month_sum += agent_contribution

        # player decision - initiate contributers behaviour
        if(p_contributer(params, state, agent_data[x], month) == True):
            month_sum += agent_contribution # c - from differential eq
            debt = check_agent_debt(state, agent_data[x])
            if(debt != 0):
                month_sum += debt
        else :
            print("Contributer default: GBP" + str(agent_contribution))

    state['Honest_Volume'] = month_sum
    state['Dishonest_Volume'] = expected_month_sum - month_sum
    state['Total_Volume'] = state['Honest_Volume'] + state['Surplus_Volume'] + state['Dishonest_Volume']

    print("Total deposited amount: GBP" + str(state['Honest_Volume']) + " - Defaulted amount: " + str(state['Dishonest_Volume']))

    return { 'collected_amount': month_sum }

def p_allocate_pool(params, substep, state_history, previous_state):
    state = previous_state['pool_state'].data[0]['data']
    agent_data = state['Agent_Data']
    timestep = previous_state['timestep']
    pool_amount = state['Total_Volume'] - state['Dishonest_Volume']

    for x in range(0, len(agent_data)):
        if(agent_data[x].standing == timestep and agent_data[x].taken == False):

            allocation_amt = calculate_agent_amount(agent_data[x], timestep+1, params['duration']) # a - from differential eq

            if(verify_allocated_amount(agent_data[x], allocation_amt, pool_amount) == True):    
                agent_data[x].taken = True
                pool_amount -= allocation_amt

                print("Allocating agent: " + str(agent_data[x].pubkey) + ", standing: " + str(agent_data[x].standing) + ", amount: GBP" + str(allocation_amt))
                
            else :
                print("Not enough money in pool to allocate agent full amount of: " + str(allocation_amt) + "\n")    
                allocation_amt = pool_amount
                agent_data[x].taken = False
                pool_amount = 0.0

            # reset variables
            state['Cheaters_Cost'] = 0
            state['Cheats_Volume'] = 0  
            state['Cheater_Reward'] = 0

            # player decision - initiate cheater behaviour
            if(p_cheater(state, agent_data[x], allocation_amt) == True):
                state['Contributers_Cost'] = contributer_cost(state)
                state['Cheaters_On'] = True
                print("Allocator default: GBP" + str(state['Cheater_Reward']))
                agent_data[x].defaulted = True 

            agent_data[x].balance += allocation_amt
    
    state['Surplus_Volume'] = pool_amount    
    print("Pool amount: GBP" + str(pool_amount) + "\n")
    
    return { 'pool_amount': pool_amount }

"""
   AGENT BEHAVIOUR DEFINITION
"""
# contributer motivated to contributed to contribute share if reward > cost of other agents stealing 
def p_contributer(params, state, agent, timestep):
    act = False
    cost = contributer_cost(state)
    reward = contributers_reward(params, agent, timestep)

    agent_strategy = agent.contribute_strategy
    
    if(agent.defaulted):
        return act

    print("Shall I contribute? reward: " + str(reward) + " cost: " + str(0.25 * cost) + " strategy: " + str(agent_strategy))
    if (agent_strategy(reward, cost)):
        act = True
        agent.rating += 0.2 # increase rating 
        state['Contributers_Rating'] += 0.2
        agent.contributed_amt += agent.amount # update agent contributed amount

    return act

# cheater motivated to steal the pot if reward > amount contributed so far + agent takes the risk of being caught
def p_cheater(state, agent, allocation_amt):
    act = False
    reward = cheater_reward(agent, allocation_amt)
    cost = cheater_cost(agent, allocation_amt)

    if(reward == 0): return act

    agent_strategy = agent.allocate_strategy

    if(agent_strategy(reward, cost)):
        act = True
        state['Cheats_Volume'] += reward 
        state['Cheater_Reward'] = reward
        state['Cheaters_Cost'] = cost
    else :
        state['Contributers_Reward'] = reward    

    return act

"""
    AGENT REWARD + COST DEFINITION
"""
# contributers's reward per round contributed => amount agreed
def contributers_reward(params, data, timestep):
    return calculate_agent_amount(data, timestep, params['duration'])

# Contributer's cost per round cheater acts => amount defaulted if at all
def contributer_cost(s):
    share = 0.1
    return (share * s['Cheats_Volume'])

# Cheater's reward per cheat
def cheater_reward(s, allocation_amt):
    if(s.contributed_amt >= allocation_amt):
        return 0.0
    else :    
        return allocation_amt - s.contributed_amt # Pot amount - Contributed amount

# Cheater's cost per cheat caught
delta = 0.05
def cheater_cost(s, allocation_amt):
    # return (delta * allocation_amt) + allocation_amt - s.contributed_amt
    return s.contributed_amt
