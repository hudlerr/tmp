from agents import get_monthly_default_count
import random

# # approve requests to change turn in which agent recieves pot based on partcipants history
# def approve_standing(state, agent, standing):
#     # threshold for a vote to be approved
#     threshold = (state['Participants'] * 0.8)
#     participants = state['agent_data']
#     approve = False

#     if(get_monthly_default_count(agent) != 0):
#         message = "Agent changing turn not approved: Has a defaulting record."
#     else:
#         message = "Agent changing turn approved: Old position - " + \
#             str(agent.standing) + " New position - " + standing
#         approve = True

#     rejected_count = partcipant_vote(participants)

#     if(state['Participants'] - rejected_count < threshold):
#         return (False, message)
#     else:
#         return (approve, message)


# def partcipant_vote(participants):
#     rejected_count = 0

#     for i in participants:
#         rejected_chance = 0.05  #  5%
#         if(random.random() > rejected_chance):
#             rejected_count+1
#     return rejected_count


# def check_agent_debt(agent):
#     if(agent.borrowed != 0):
#         print("***************************************************************************")
#         print("Agent at standing: " + str(agent.standing) + " repays borrowed amount: £" + str(agent.borrowed))
#         agent_data[x].borrowed = 0
#     return agent.borrowed    
