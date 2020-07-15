from mpmath import *
import re

# Sets precision for mpmath objects
mp.dps = 1028

# Opens file of Zeta Zeros, formats each Zero, returns list of mp.mpf objects (floats)
def readfile(file_name):
    output = []
    pattern = "[0-9]*\.[0-9\n\s]*\s{3}"
    
    # Parses the text file for matches of the regex pattern
    with open(file_name, 'r') as infile:
        data = infile.read()
        matches = re.findall(pattern, data)
        
        for i in matches:
            # Removes all whitespace and line-breaks
            i = i.replace(" ","").replace("\n","")
            # Creates an mpmath float object of each zero, adds it to the output list
            output.append(mp.mpf(i))
            
    return output
    

# Takes a Zeta Zero and computes its' standard continued fraction
# s= ZetaZero
# t= Precision
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
        
# Returns list of mp floats from a given text file in the same directory
ZetaZeros = readfile("ZetaZeros_1024.txt")

# Computes the SCF for all provided Zeta Zeros up to 500 terms:
Zeros_CF = list((zeta_scf(i,500) for i in ZetaZeros))

