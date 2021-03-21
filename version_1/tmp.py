# print agent array
for x in range(0, len(agents_)):
    print(str(x), ':', str(agents_[x]))

# find agent
def filterFunction(a):
    if a.standing == 2:
        print(a)
list(filter(filterFunction, agents_))    

# str to int
int(float(tmp))

def allocate_pool(genesis_state, timestep, duration, p_collected_amt):
    block_agent_data = genesis_state.data[0]['data']
    pool_amount = intitiate_monthly_deposits(genesis_state)

    for x in range(0, len(block_agent_data)):
        if(block_agent_data[x].standing == timestep and block_agent_data[x].taken == False):
            allocation_amt = (duration*block_agent_data[x].amount) # a - from differential eq
            block_agent_data[x].balance += allocation_amt
            block_agent_data[x].taken = True
            print("Allocating agent: " + str(block_agent_data[x].pubkey) + ", standing: " + str(block_agent_data[x].standing) + ", amount: GBP" + str(eth_to_pounds(allocation_amt)))
            pool_amount -= eth_to_pounds(allocation_amt)
    return pool_amount