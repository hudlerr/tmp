# Contains anything Agent (participant) related

class AgentData:
    def __init__(self, pubkey, amount, standing, balance, taken, contributed_amt):
        self.pubkey = pubkey
        self.amount = amount # amount agreed to contribute monthly
        self.standing = standing # standing within group, indicates your turn
        self.balance = balance # amount recived from rosca circle (should be duration * amount)
        self.taken = taken # indicates whether you've taken or not
        self.contributed_amt = contributed_amt # amount contributed so far

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)    

    def increase_balance(self, amount):
        self.balance += amount

def update_contribution_amount(self, month_sum):
    self.contributed_amt += month_sum    

