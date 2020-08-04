from mpmath import *
import re

# Opens file of Zeta Zeros, formats each Zero, returns list of mp.mpf objects (floats)
def parsefile(file_name):
    output = []
    pattern = "[0-9]*\.[0-9\n\s]*\s{3}"
    
    # Parses the text file for matches of the regex pattern
    with open(file_name, 'r') as infile:
        data = infile.read()
        matches = re.findall(pattern, data)
        
        for i in matches:
            # Removes all whitespace and line-breaks
            i = i.replace("\n","").replace(" ","")
            # Creates an mpmath float object of each zero, adds it to the output list
            output.append(mp.mpf(i))
        infile.close()
    return output


# Takes a Zeta Zero and computes its' standard continued fraction
# s= Img. Component of each Zeta Zero (mpmath float obj)
# t= Precision level (Default:30)
def zeta_scf(s, t=30):
    cf = []
    It = 0
    while It < t:
        cf.append(int(floor(s/mp.mpf(1))))
        y = s - floor(s/mp.mpf(1))
        try:
            s = mp.mpf(1)/y
        except ZeroDivisionError:
            return cf
        It += 1
    return cf


# Computes the SCF for all provided Zeta Zeros up to the amount of characters in each Zero:
Zeros_CF = list((zeta_scf(i,len(str(i))) for i in ZetaZeros))


# Decode a standard continued fraction
# (with mpmath float objects*)
def CF_decode(cf):
    h1,h2 = 1,0
    k1,k2 = 0,1
    for a in cf:
        h = mp.mpf(a*h1+h2)
        k = mp.mpf(a*k1+k2)
        #print([a,h,k,h/k])
        try:
            hk = h/k
        except ZeroDivisionError:
            hk = 0
        h2,k2 = h1,k1
        h1,k1 = h,k
    return h/k


# Returns a list of the deltas for each item in two closely-related lists of floats (or mpmath float objects)
def delta(a,b):
    n = 0
    deltas = []
    for i in a:
        d = (i-b[n])/(i*100)
        deltas.append(d)
        n+=1
    return deltas



if __name__ == "__main__":
    # Set decimal precision, get list of Zeta Zeros
    d = int(input("9 or 1024 dps?\n> "))
        
    if d == 9:
        mp.dps = 12
    elif d == 1024:
        mp.d = 1026

    ZetaZeros = parsefile("ZetaZeros_"+d+".txt")
    
    # Computes the SCF for all provided Zeta Zeros up to the amount of characters in each Zero:
    Zeros_CF = list((zeta_scf(i,len(str(i))) for i in ZetaZeros))
    # Return the HK values of CF_decode for the zeros
    Zeros_HK = list((CF_decode(i) for i in Zeros_CF))
    # Return the delta between the original values and HK values
    deltas_HK = delta(ZetaZeros, Zeros_HK)
