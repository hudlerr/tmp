import time
from utils import (pounds_to_eth, eth_to_pounds)

# Contains everything building or altering the rosca circle related

class CircleState:
    def __init__(self, name, timestep, collected_amt, balance, data): # intialise
        self.name = name
        self.timestep = timestep
        self.collected_amt = collected_amt
        self.balance = balance
        self.data = data

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)    

def initialise_circle_state(name, data):
    # creates circle saving data 
    circle = CircleState(name, 0, 0.0, 0.0, data)
    print("New ROSCA circle created - " + name)
    return circle

def get_total_active_balance(circle):
    return circle.balance

def get_total_montly_contribution(block_agent_data):
    max_sum = 0.0

    for x in range(0, len(block_agent_data)):
        agent_contribution = eth_to_pounds(block_agent_data[x].amount)
        max_sum += agent_contribution
    return max_sum  

def update_circle_state(name, timestep, collected_amt, balance, data):
    circle = CircleState(name, timestep, collected_amt, balance, data)
    print("Updating circle state.." )
    return circle
