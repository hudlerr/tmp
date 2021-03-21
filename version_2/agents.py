# Contains anything Agent (participant) related

class AgentData:
    def __init__(self, pubkey, amount, standing, balance, taken, contributed_amt, defaulted, rating):
        self.pubkey = pubkey
        self.amount = amount # amount agreed to contribute monthly
        self.standing = standing # standing within group, indicates your turn
        self.balance = balance # amount recived from rosca circle (should be duration * amount)
        self.taken = taken # indicates whether you've taken or not
        self.contributed_amt = contributed_amt # amount contributed so far
        self.rating = rating # trust-rating based on agents actions
        self.defaulted = defaulted # whether agent has stolen pool

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)    

    def increase_balance(self, amount):
        self.balance += amount

def update_contribution_amount(self, month_sum):
    self.contributed_amt += month_sum    

def verify_allocated_amount(agent, allocated_amt, pool_amt):
    if(allocated_amt <= pool_amt): 
        return True
    else :
        return False    

def get_monthly_default_count(agent):
    count = 0
    for x in range(0, len(agent)):
        if(agent[x].defaulted == True):
            count += 1
    return count    

def calculate_agent_amount(agent, month, duration):
    expected_contribution = month * agent.amount
    exepcted_allocation = duration * agent.amount
    print("calculate_agent_amount: " + str(expected_contribution) + " " + str(agent.contributed_amt))

    if(expected_contribution != agent.contributed_amt) :
        return exepcted_allocation - agent.contributed_amt
    else : 
        return exepcted_allocation
