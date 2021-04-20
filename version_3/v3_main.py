from system import (p_allocate_pool, p_intitiate_monthly_deposits, get_initial_deposits)
import base_blockchain
from circle import (update_circle_state, initialise_circle_state)
from chain import create_block
from network_helper_functions import (choose_amount, approve_standing, partcipant_vote)
from agents import (get_monthly_default_count)
import random

# intialise our blockchain
blockchain = base_blockchain.BlockChain()
# genesis state
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
    'Timestep': 0,
    'Agent_Data': get_initial_deposits(max_amount, participants),
    'Duration': 10,
    'Participants': 10,
    'Surplus_Amout': 0
}
# create initial block
intial_block = create_block(genesis_state)

## approve borrowing based on partcipants history
def approve_borrowing(state, agent_no, amount):

    ## threshold for a vote to be approved
    threshold = (state['Participants'] * 0.8)
    participants = state['Agent_Data']
    approve = False

    if(get_monthly_default_count(participants, agent_no) != 0):
        print("1")
        message = "Agent borrowing not approved: Has a defaulting record."
    elif(amount > participants[agent_no].amount):
        message = "Agent borrowing not approved: Amount requested to high for agent."
        print("2")
    else:           
        message = "Agent borrowing approved: Amount - " + str(amount)
        print("3")
        participants[agent_no].borrowed = amount
        approve = True

    rejected_count = partcipant_vote(participants)
    
    if(state['Participants'] - rejected_count < threshold) :
        return { "approve": False, "message": "Agent borrowing denied: Participants vote" }
    else:
        return {approve, message}

def agent_borrow_request(state):
    amount = choose_amount()
    agent_pos = random.randint(0, state['Participants'])
    borrowed_amt = 0

    if(random.random() < 0.5): # 10% chance of certain agent asking to borrow from pool
        print("****************************************************************************")
        print("Agent at standing: " + str(agent_pos) + " intiates request to borrow: " + str(amount))
        
        approved, message = approve_borrowing(state, agent_pos, amount)
        if(approved):
            borrowed_amt = amount
        print(message)  
        
    return borrowed_amt
              
"""
    STATE UPDATE LOGIC
"""
def s_updatepool(intial_block):  
    state = intial_block.data[0]['data']
    duration = state['Duration']

    for x in range(0, duration):
        # collected_amt = p_intitiate_monthly_deposits(genesis_state) ## initiate contributers behaviour
        collected_amt = 10000
        # pool_amt = p_allocate_pool(genesis_state) ## initiate cheaters behaviour
        pool_amt = 500

        ## intiate borrowers behaviour
        if(pool_amt != 0 and state['Timestep'] > 2): 
            borrowed_amt = agent_borrow_request(state)
            pool_amt -= borrowed_amt

        state['Timestep'] += 1
        print("Pool amount: GBP" + str(pool_amt) + "\n")
        new_block = create_block(genesis_state) # create block    


s_updatepool(intial_block)