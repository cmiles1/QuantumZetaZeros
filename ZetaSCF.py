from mpmath import *
import re

# Sets precision for mpmath objects
mp.dps = 1025


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

        
# Returns list of mp floats from a given text file in the same directory
ZetaZeros = parsefile("ZetaZeros_1024.txt")


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

# Return HK values of CF_decode
Zeros_HK = list((CF_decode(i) for i in Zeros_CF))

# CF Rounding (Error Removing) Utility
# Compares the number of accurate digits in original zero to the returned HK value of the standard CF
# Remove the last number of terms in the CF, for each inaccurate digit between the Zero and the HK

# Note: this function does not get a more accurate value for the CF,
# The function is for accurate pattern-detection in the string of each CF
def RoundZerosCF(ZetaZeros, Zeros_HK):
    n = 0
    Rnd_CF = []
    for i in ZetaZeros:
        # Check that each zero is equal to the decoded CF of the Zero
        if i != Zeros_HK[n]:
            #print(str(i).split(".")[0])
            # If the two items are not equal, count the 'k' number of digits backward
            for k in range(1, len(str(ZetaZeros[n]))-1):
                # If everything before the 'k'th last item is equal in both lists, remove the last "k" items from the CF
                if str(i)[:-k] == str(Zeros_HK[n])[:-k]:
                    Rnd_CF.append(Zeros_CF[n][:-k])
                    break
                # Or, if everything before 'k' is equal to everything before 1+k (from the last digit) in the returned HK value
                elif str(i)[:-k] == str(Zeros_HK[n])[:-k-1]:
                    Rnd_CF.append(Zeros_CF[n][:-k-1])
                    break
        else:
            Rnd_CF.append(Zeros_CF[n])
        n+=1
    return Rnd_CF

Rnd_CF = RoundZerosCF(ZetaZeros, Zeros_HK)
