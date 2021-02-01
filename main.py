import secrets
import base_blockchain
from agents import (AgentData, update_contribution_amount)
from circle import (initialise_circle_state, update_circle_state, get_total_active_balance)
from chain import(create_block)
from utils import (pounds_to_eth, eth_to_pounds)

blockchain = base_blockchain.BlockChain()

# Create an array of `AgentData` objects


def get_initial_deposits(n):
    agent = [AgentData(secrets.token_bytes(48), pounds_to_eth(300), i, 0, False, 0)
             for i in range(n)]
    return agent


# creates circle
circle_ = initialise_circle_state("Circle C", get_initial_deposits(10))

# create initial block
genesis_state = create_block(circle_)

# check moneypool balance
get_total_active_balance(circle_)

# initate monthly contributions
def intitiate_monthly_deposits(genesis_state):
    month_sum = 0.0
    block_agent_data = genesis_state.data[0]['data']

    for x in range(0, len(block_agent_data)):
        agent_contribution = float(block_agent_data[x].amount)
        month_sum += eth_to_pounds(agent_contribution) # c - from differential eq
        block_agent_data[x].contributed_amt += agent_contribution # update agent contributed amount

    print("Deposited amount: GBP" + str(month_sum))
    return month_sum    # todo: validate sum at later stage

# Allocate to agent according to standing
def allocate_pool(genesis_state, timestep, duration):
    block_agent_data = genesis_state.data[0]['data']
    pool_amount = intitiate_monthly_deposits(genesis_state)

    for x in range(0, len(block_agent_data)):
        if(block_agent_data[x].standing == timestep and block_agent_data[x].taken == False):
            allocation_amt = (duration*block_agent_data[x].amount) # a - from differential eq
            block_agent_data[x].balance += allocation_amt
            block_agent_data[x].taken = True
            print("Allocating agent: " + str(block_agent_data(x).pubkey) + " amount: ETH" + str(allocation_amt))
            pool_amount -= eth_to_pounds(allocation_amt)
    return pool_amount


## UPDATE CIRCLE STATE and create + add block to chain
def new_pool_state(timestep, duration):    
    updateCircle_ = update_circle_state(genesis_state.data[0]['name'], timestep+1, allocate_pool(genesis_state, timestep, duration), genesis_state.data[0]['data'])
    new_block = create_block(updateCircle_) # create block
    print("Pool amount: GBP" + str(get_total_active_balance(updateCircle_)))
    return updateCircle_

new_state = new_pool_state(0, 10)