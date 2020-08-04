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

def encode_gcf(z,a0,b0,Ai,Bi,Ci,Di,Ei,t=100):
    # Takes a number, z, and the coefficients of a GCF and computes its delta
    # (*These coefficients are being treated as the form of a quadratic term over a linear term)
    # Mathematical representation : a0+ b0/(An**2+Bn+C/(Dn+E))
    # Returns the term with the closest delta to 'z', and its delta

    # args:
    # z= a given number (mpmath float obj)
    # a0 = First A value
    # b0 = First B value
    # Ai -> Ei = Each coefficient in the generalized continued fraction

    # kwargs:
    # t= Terms in the to compute the minimum gcf delta (Default: 100), range from 0 to 'n' value
    
    h1,h2 = 1,0
    k1,k2 = 0,1
    an,bn = a0,b0
    b1 = 1

    delta_min = z - floor(z)

    n,n_min = 0,1
    
    while n < t:

        hn = mp.mpf(an * h1 + b1 * h2)
        kn = mp.mpf(an * k1 + b1 * k2)

        try:
            est = hn / kn
        except ZeroDivisionError:
            est = 0
        delta = abs(z - est)

        if delta <= delta_min:
            delta_min = delta
            n_min = n
            

        h2,k2 = h1,k1
        h1,k1 = hn,kn
        b1 = bn
        n+=1
        an = Di * n + Ei
        bn = Ai * (n * n) + Bi * n + Ci
        
    return (delta_min, n_min)



def brute_search(z,ss,t=100,len_gcfs=10,ss_0=[],best_gcfs=[]):
    # Brute Search
    #
    # Brute-force searches for the best GCF of a value in the (range, or list) of the given values, from mn and mx.
    # Passes arguments to encode_gcf()
    # Returns the closest term in GCF (n_min), with the delta, as well as the coefficients of the GCF
    # Excepts keyboard interrupt and still returns the current smallest delta in the search space
    #
    # Cycles through a0,b0,Ai->Ei = range(min,...,max) to find the best GCF for a term 'z'
    # mn= -9  mx= 9 -> 893,871,739,000 total combinations
    # time complexity: O(m*n)
    #
    # args: z,ss
    # z= a given number (mpmath float obj w/ arbitrary prec)
    # ss = list of potential values for Ai->Ei values in the coefficients
    
    # kwargs: ss_0, t, best_gcfs
    # t = terms per gcf to try (kwarg of encode_gcf), default:100
    # len_gcfs = amount of candidates to print (output size), the length of 'bestgcfs', default: 10
    # ss_0 = list of potential values for a0,b0 values, (same as 'ss' if left blank*)
    # best_gcfs = List of the best candidate GCFs, used after a CTL+C interrupt to continue at a current point
    


    if len(ss_0) == 0:
        ss_0 = ss

    # Set a variable to hold the starting range for the best guess (Anything less than 1 will be logged)
    sm_v = 1,1

    try:
        # Enumerate for each of the seven coefficients of the GCF
        for a0 in ss_0:
            #print("\n########\na0 search space:",a0)
            for b0 in ss_0:
                #print("\n#\nb0 search space:",b0)
                for Ai in ss:
                    for Bi in ss:
                        for Ci in ss:
                            for Di in ss:
                                for Ei in ss:
                                    
                                    coeffs = [a0,b0,Ai,Bi,Ci,Di,Ei]
                                    # Encodes the GCFs for each of the a0,b0,Ai->Ei combinations
                                    gcf_est = encode_gcf(z,a0,b0,Ai,Bi,Ci,Di,Ei,t)
                                    
                                    if len(best_gcfs) == 0:
                                        best_gcfs.append([gcf_est,coeffs])
                                    elif gcf_est[0] < best_gcfs[-1][0][0]:
                                        best_gcfs.append([gcf_est,coeffs])
                                        best_gcfs.sort(key=lambda x: x[0][0])

                                        if len(best_gcfs) > len_gcfs:
                                            best_gcfs.remove(best_gcfs[-1])

                                            # The coeffs should become more accurate with more iterations
                                            #print('\n####','\nBest found estimate:',best_gcfs[0][1],'\nDelta:',float(best_gcfs[0][0][0]))
  
    # Allows for CTL+C to see where the search range ended
    # Repeat the search with the ss_0 (search space for a0,b0) being less than the last tested coefficients printed below
    # And repeat the "brute_search" function with the "ss_0" and "best_gcfs" kwargs reflecting this change
    # Shows where the search stopped, best items so far
    except KeyboardInterrupt:
        print("[Interrupt] Last tested coefficients:",[a0,b0,Ai,Bi,Ci,Di,Ei])
        
    return best_gcfs

###################################################
# Test 1
# First tested search space for Zeta Zero 1 at 1024 digits of precision for 15 terms
# Search space a0,b0,Ai-Ei Z{-9,9}
# Best found GCF in range :
"""
>>> z = ZetaZeros[0]
>>> ss = list(range(-9,9))
>>> ZetaZero1_GCFs = brute_search(z,ss,15,1)
>>> print('Coeffs:\n',[i[0] for i in ZetaZero1_GCFs])

"""

##########################

# Test 2
# First tested search space for Zeta Zero 1 at 9 digits of precision to 15 terms
# Search space Ai-Ei: {-19 < All primes (and their negative conjugates), and -1,0,1 > 19}
# Search space a0, b0: {All primes, and 1 < 20}
# Best found GCFs in range :
"""
>>> z = ZetaZeros[0]
>>> ss = [-19, -17, -13, -11, -7, -5, -3, -2, -1, 0, 1, 2, 3, 5, 7, 11, 13, 17, 19]
>>> ss_0 = [1, 2, 3, 5, 7, 11, 13, 17, 19]
>>> ZetaZero1_GCFs = brute_search(z,ss,15,10,ss_0)
>>> print('Coeffs:\n',[i[0] for i in ZetaZero1_GCFs])
Coeffs:
[[17, 19, 19, 2, 13, -3, -1],
[13, 11, -19, 1, -7, 11, 0],
[11, 3, 17, -2, 7, -7, 19],
[11, 19, 1, -5, -13, -5, 5],
[13, 13, 5, -13, 11, -7, 17],
[13, 19, -3, -7, -11, 1, 17],
[13, 13, -19, 11, -7, 17, -5],
[17, 17, 0, 11, 7, -3, -1],
[17, 13, 11, -5, -1, -3, -1],
[13, 1, 17, 7, 19, 7, -11]]

>>> print('Deltas:\n',[i[1] for i in ZetaZero1_GCFs])
Closest term / Deltas:
(mpf('3.82642610929906e-8'), 5)
(mpf('8.28586053103209e-8'), 6)
(mpf('8.32242221804336e-8'), 9)
(mpf('1.16675437311642e-7'), 8)
(mpf('1.48294930113479e-7'), 7)
(mpf('1.58815964823589e-7'), 14)
(mpf('1.73648004420102e-7'), 5)
(mpf('1.82262738235295e-7'), 8)
(mpf('2.07608536584303e-7'), 11)
(mpf('2.45318005909212e-7'), 12)
"""
# First tested search space for Zeta Zero 1 at 1024 digits of precision to 300 terms
# Search space Ai-Ei: -19 < All primes (and their negative conjugates) > 19
# Search space a0, b0: All primes < 20
# Best found GCF in range :
"""
>>> z = ZetaZeros[0]
>>> coeffs = [c[0] for c in ZetaZero1_GCFs]
>>> for n in coeffs:
	ZetaZero1_deltas.append(encode_gcf(z,n[0],n[1],n[2],n[3],n[4],n[5],n[6],300))
>>> for i in ZetaZero1_deltas:
	print(i[0],"\n")

3.8000253956432355e-08 

8.259322817508208e-08 

8.295972513481071e-08 

1.1641043841254518e-07 

1.4803119694967077e-07 

1.5908122604566105e-07 

1.7338267065431938e-07 

1.8252653802004958e-07 

2.0734424789523712e-07 

2.4558576728992743e-07 
"""
# Returned roughly the same result as the first part of the test.
# For trying to encode this zeta sum to a high precision, this did not yield an extremely
# accurate result.
###################################################



if __name__ == "__main__":
    # Set decimal precision, get list of Zeta Zeros
    dps = input("9 or 1024 dps?\n> ")
        
    if int(dps) == 9:
        mp.dps = 12
    elif int(dps) == 1024:
        mp.dps = 1026

    ZetaZeros = parsefile("ZetaZeros_"+dps+".txt")


