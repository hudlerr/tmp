import random
from agents import get_monthly_default_count

# approve requests to change turn in which agent recieves pot based on partcipants history
def approve_standing(state, agent, standing):
    # threshold for a vote to be approved
    threshold = (state['Participants'] * 0.8)
    participants = state['Agent_Data']
    approve = False

    if(get_monthly_default_count(agent) != 0):
        message = "Agent changing turn not approved: Has a defaulting record."
    else:
        message = "Agent changing turn approved: Old position - " + str(agent.standing) + " New position - " + standing
        approve = True

    rejected_count = partcipant_vote(participants)

    if(state['Participants'] - rejected_count < threshold):
        return (False, message)
    else:
        return (approve, message)

def partcipant_vote(participants):
    rejected_count = 0

    for i in participants:
        rejected_chance = 0.05  #  5%
        if(random.random() > rejected_chance):
            rejected_count+1
    return rejected_count


def check_agent_debt(state, agent):
    if(agent.borrowed != 0):
        print("***************************************************************************")
        print("Agent at standing: " + str(agent.standing) + " repays borrowed amount: £" + str(agent.borrowed))
        state['Borrowed_Volume'] -= agent.borrowed
        state['Honest_Volume'] += agent.borrowed # increment global pool value
        agent.borrowed = 0
    return agent.borrowed    

# def order_agent_standing(agent): # according to their rating
#     new_agent_list = sorted(agent, key=lambda x: x.rating, reverse=True)
#     return new_agent_list


def order_agent_standing(agent): 
    agent.sort(key=lambda x: x.rating, reverse=True) # according to their rating
    new_agent_list = sorted(agent, key=lambda x: x.amount, reverse=False) # according to decreasing amount
    
    # for x in range(0, len(new_agent_list)): # rewrite standing according to new ordering
    #     print("Old standing - " + str(agent[x].standing) + " New: " + str(x))
    #     new_agent_list[x].standing = x
    return new_agent_list

def choose_amount(max_amount):
    # amount = max_amount[0] if len(max_amount) > 0 else max_amount
    tmp = random.randint(1, max_amount) * 100
    print("AMOUNT: " + str(tmp))
    return tmp