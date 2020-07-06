#!/usr/bin/python3

# continuedfractions.py
# Takes on an integer, (and a max iteration) and turns it into a CF

def CF_encode(x,maxIt):
    cf = []
    It=0
    y=1
    while y > 1e-9 and It < maxIt:
        cf.append(int(x//1))
        y = x - (x//1)
        try:
            x = 1/y
        except ZeroDivisionError:
            return cf
        #print(y,x,(x//1))
        It += 1
    return cf

# Or, takes a CF and converts it to a fraction (approximately) representing
# An integer, and the decimal value of the fraction

def CF_decode(cf):
    h1,h2 = 1,0
    k1,k2 = 0,1
    for a in cf:
        h = a*h1+h2
        k = a*k1+k2
        #print([a,h,k,h/k])
        try:
            hk = h/k
        except ZeroDivisionError:
            hk = 0
        h2,k2 = h1,k1
        h1,k1 = h,k
    out = [h,k,h/k]
    return out



