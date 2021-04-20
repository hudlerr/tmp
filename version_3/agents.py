# Contains anything Agent (participant) related

class AgentData:
    def __init__(self, pubkey, amount, standing, balance, taken, contributed_amt, defaulted, rating, contribute_strategy, allocate_strategy, borrowed):
        self.pubkey = pubkey
        self.amount = amount # amount agreed to contribute monthly
        self.standing = standing # standing within group, indicates your turn
        self.balance = balance # amount recived from rosca circle (should be duration * amount)
        self.taken = taken # indicates whether you've taken or not
        self.contributed_amt = contributed_amt # amount contributed so far
        self.rating = rating # trust-rating based on agents actions
        self.defaulted = defaulted # whether agent has stolen pool
        self.contribute_strategy = contribute_strategy # contributing strategy (honest OR influenced OR broke)
        self.allocate_strategy = allocate_strategy # allocate strategy (honest OR greedy)
        self.borrowed = borrowed # amount agent has/hasn't borrowed from pool

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

def get_monthly_default_count(participants, agent):
    count = 0
    for x in range(0, len(participants)):
        if(participants[agent].defaulted == True):
            count += 1
    return count    

def calculate_agent_amount(agent, month, duration):
    expected_contribution = month * agent.amount
    exepcted_allocation = duration * agent.amount
    missing = expected_contribution - agent.contributed_amt
    print("calculate_agent_amount: " + str(expected_contribution) + " " + str(agent.contributed_amt) + " missing: " + str(missing))

    if(expected_contribution != agent.contributed_amt) :
        return exepcted_allocation - missing
    else : 
        return exepcted_allocation
