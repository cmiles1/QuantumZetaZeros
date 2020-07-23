from collections import defaultdict
from ZetaSCF import Zeros_CF

# Take a subsequence and count the number of occurences
def getsubs(i,r):
    substr = r[i:]
    n = -1
    while substr:
        yield substr
        substr = r[i:n]
        n -= 1


# Generate a suffix array of all possible combinations and the amount they are repeated
def CreateSfxArr(r):
    occ = defaultdict(int)
    for i in range(len(r)):
        # Count the rate of occurence per subsequence
        for sub in getsubs(i,r):
            key = str(sub)[1:-1]
            try:
                occ[key] += 1
            # The suffix array is very memory-intensive for larger values
            except MemoryError as error:
                print(error,'\n',i,r[0])
                # Return whatever could be calculated
                return occ
    return occ


# Get the longest recurring subsequence in the list
def LRSS(z):
    sfxar = CreateSfxArr(z)
    # Remove all subsequences with only 1 occurence
    repeated = [k for k,v in sfxar.items() if v >= 2]
    # Make sure there is at least one subsequence with more than 1 occurence
    if repeated:
        # Find the key with the largest length, format as list of integers
        mk = [int(i) for i in max(repeated, key=len).split(', ')]
        return mk

#lrs = LRSS([1, 1, 10, 4, 2, 7, 1, 1, 10, 3, 1, 1, 1])
## output => [1, 1, 10]

# Get all the LRSS' for each item in a given list, for the first x terms in each item (Default: all)
# Beware, larger x values are more memory-intensive (see CreateSfxArr func)
def get_all_LRSS(cflist,x=-1):
    out = []
    for cf in cflist:
        out.append(LRSS(cf[:x]))
    return out


#############

# Print the longest repeating subsequence in the first 500 terms of each
# continued fraction
if __name__ == "__main__":
    
    out = get_all_LRSS(Zeros_CF,-500)
    n = 1
    print(len(out))
    for i in out:
        print("Zero #",n)
        print("LRSS :",i)
        n+=1


