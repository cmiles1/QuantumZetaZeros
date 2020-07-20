from itertools import islice
#import math


# Zeta.py
# Calculates Zeta function in terms of Eta(s), where Re(s) > 0, Re(s) != 1

def count(firstval=0, step=1):
    x = firstval
    while 1:
        yield x
        x += step

# Calculates Eta(s) of a complex/real positive number, s
def eta(s,t=100000):
    if s ==1:
        return float("inf")
    term = (((-1) **(n-1))/(n**s) for n in count(1))
    return sum(islice(term,t))

# Calculates Zeta(s) in terms of Eta(s)
def zeta(s,t=100000):
    if s == 1:
        return float("inf")
    else:
        return eta(s)/ (2**(1-s)-1)
    return eta(s,t)/ (2**(1-s)-1)
