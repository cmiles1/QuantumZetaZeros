from collections import defaultdict
from ZetaSCF import Rnd_CF
######################################################
# Take a substring and count the occurences
def getsubs(i,r):
    substr = r[i:]
    n = -1
    while substr:
        yield substr
        substr = r[i:n]
        n -= 1

# Create a suffix array of a string
def CreateSfxArr(r):
    occ = defaultdict(int)
    
    for i in range(len(r)):
        # Count the rate of occurence per substring
        for sub in getsubs(i,r):
            occ[sub] += 1
    return occ

# Get the longest recurring substring in the string
def LRSS(a):
    sfxar = CreateSfxArr(a)
    # Strip any substrings with only 1 occurence
    filtered = [k for k,v in sfxar.items() if v >= 2]
    # Make sure there is at least one substring with more than 1 occurence
    if filtered:
        maxkey = max(filtered, key=len)
        if maxkey[0] == ',':
            maxkey = maxkey[2:]
        if maxkey[-2] == ',':
            maxkey = maxkey[:-2]
    else:
        maxkey = "None"
    return maxkey




# Get all the LRSS' for each item in the list of Zeros, for the first x terms
# With the list of Zeta Zeros, a number ~= 550 effectively ran out of memory
def get_all_LRSS(cflist,x):
    out = []
    for cf in cflist:
        out.append(LRSS(str(cf[:x])))
    return out


# Print the longest recurring substring in the first 500 terms of each
# continued fraction
if __name__ == "__main__":
    out = get_all_LRSS(Rnd_CF,10)
    n = 1
    for i in out:
        print("Zero #",n)
        print("LRSS :",i)
        n+=1




