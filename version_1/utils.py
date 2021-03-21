
# ether conversions
def eth_to_gwei(eth):
    return eth * (10 ** 9)

def gwei_to_eth(gwei):
    return float(gwei) / (10 ** 9)  

def eth_to_pounds(eth):
    return eth * 1000    

def pounds_to_eth(pounds):
    return pounds / 1000        