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