import time

# Contains everything building or altering the rosca circle related

class CircleState:
    def __init__(self, name, timestep, balance, data): # intialise
        self.name = name
        self.timestep = timestep
        self.balance = balance
        self.data = data

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)    

def initialise_circle_state(name, data):
    # creates circle saving data 
    circle = CircleState(name, 0, 0.0, data)
    name_ = name
    print("New ROSCA circle created - " + name)
    return circle

def get_total_active_balance(circle):
    return circle.balance

def update_circle_state(name, timestep, balance, data):
    circle = CircleState(name, timestep, balance, data)
    print("Updating circle state.." )
    return circle
