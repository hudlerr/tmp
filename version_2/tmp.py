from datetime import timedelta
from cadCAD import configs
from cadCAD.configuration import Configuration
from cadCAD.configuration.utils import exo_update_per_ts, proc_trigger, bound_norm_random, ep_time_step

import secrets
from version_1.circle import initialise_circle_state
from version_1.chain import create_block
from agents import (AgentData, update_contribution_amount, verify_allocated_amount, get_monthly_default_count)

# Create Circle
def get_initial_deposits(n):
    agent = [AgentData(secrets.token_bytes(48), 300, i, 0, False, 0, False)
             for i in range(n)]       
    return agent

circle_ = initialise_circle_state("Circle C", get_initial_deposits(10))
genesis_state = create_block(circle_)    

# REWARDS + COST
# contributers's reward per round => rating + interest
def contributers_reward(s):
    block_agent_data = s.data[0]['data']
    if(block_agent_data.defaulted == False):
        block_agent_data.rating += 0.4
    return block_agent_data.rating

## STATE UPDATE ##
def s_commit_to_cheating(genesis_state):
    cheater_behaviour = p_cheater(genesis_state)
    return 'Cheaters_On', cheater_behaviour

def s_commit_to_contributing(genesis_state):
    contributer_behaviour = p_intitiate_monthly_deposits(genesis_state)
    return 'Contributers_On', contributer_behaviour

# Contributer's cost per transaction verified
alfa = 0.001
def contributer_cost(s):
    return alfa * (s['Total_Volume'])

# Cheater's reward per transaction sent successfully
gamma = 1
def cheater_reward(s):
    return gamma * (s['Cheats_Volume'])

# Cheater's cost per cheat caught
delta = 5
def cheater_cost(s):
    return delta * s['Cheats_Caught_Volume']