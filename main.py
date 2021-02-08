import secrets
import random
import base_blockchain
from agents import (AgentData, update_contribution_amount, verify_allocated_amount, get_monthly_default_count)
from circle import (initialise_circle_state, update_circle_state, get_total_active_balance, get_total_montly_contribution)
from chain import(create_block)
from utils import (pounds_to_eth, eth_to_pounds)

blockchain = base_blockchain.BlockChain()

# Create an array of `AgentData` objects
def get_initial_deposits(n):
    agent = [AgentData(secrets.token_bytes(48), pounds_to_eth(300), i, 0, False, 0, False)
             for i in range(n)]       
    return agent

# creates circle
circle_ = initialise_circle_state("Circle C", get_initial_deposits(10))

# create initial block
genesis_state = create_block(circle_)
print("print gs -> " + str(genesis_state))

# check moneypool balance
get_total_active_balance(circle_)

# player decision
def randomised_agent_contribution(agent, amount):
    if random.random() < 0.4: # 10% chance player will default
        agent.defaulted = True
        # print("Agent defaulted. Amount: " + str(amount) + " agent: " + str(agent))
        return False
    else :
        agent.defaulted = False
        return True  

# initate monthly contributions
def p_intitiate_monthly_deposits(genesis_state):
    month_sum = 0.0
    pool = genesis_state
    block_agent_data = pool.data[0]['data']
    
    print("\n" + "STARTING ROSCA MONTH " + str(pool.data[0]['timestep']))
    
    # for each agent add their monthly contribution to the collected pool
    for x in range(0, len(block_agent_data)):
        agent_contribution = eth_to_pounds(block_agent_data[x].amount)
        # player decision
        if(randomised_agent_contribution(block_agent_data[x], agent_contribution) == True):
            month_sum += agent_contribution # c - from differential eq
            block_agent_data[x].contributed_amt += agent_contribution # update agent contributed amount
    print("Total deposited amount: GBP" + str(month_sum))
    return month_sum  # todo: validate sum at later stage

# Allocate to agent according to standing
def allocate_pool(genesis_state, timestep, duration):
    block_agent_data = genesis_state.data[0]['data']
    pool_amount = p_intitiate_monthly_deposits(genesis_state)

    for x in range(0, len(block_agent_data)):
        if(block_agent_data[x].standing == timestep and block_agent_data[x].taken == False):
            allocation_amt = eth_to_pounds(duration*block_agent_data[x].amount) # a - from differential eq
            
            if(verify_allocated_amount(block_agent_data[x], allocation_amt, pool_amount) == True):
                print("allocation_amt " + str(allocation_amt) + ", pool_amount" + str(pool_amount))
                block_agent_data[x].taken = True
                pool_amount -= allocation_amt
            else :
                print("Not enough money in pool to allocate agent full amount of: " + str(allocation_amt) + "\n")    
                allocation_amt = pool_amount
                block_agent_data[x].taken = False
                pool_amount = 0.0

            print("Allocating agent: " + str(block_agent_data[x].pubkey) + ", standing: " + str(block_agent_data[x].standing) + ", amount: GBP" + str(allocation_amt))
            block_agent_data[x].balance += allocation_amt
    return pool_amount

## UPDATE CIRCLE STATE and create + add block to chain
def new_pool_state(timestep, duration):    
    calc_timestep = genesis_state.data[0]['timestep']
    pool_amt = allocate_pool(genesis_state, calc_timestep, duration)
    collected_amt = p_intitiate_monthly_deposits(genesis_state)

    updateCircle_ = update_circle_state(genesis_state.data[0]['name'], calc_timestep, collected_amt, pool_amt, genesis_state.data[0]['data'])
    new_block = create_block(updateCircle_) # create block
    print("Pool amount: GBP" + str(get_total_active_balance(updateCircle_)) + "\n")
    print(blockchain)
    return new_block


new_state = new_pool_state(0, 10)
print("DEFAULT : " + str(get_monthly_default_count(new_state.data[0]['data'])))