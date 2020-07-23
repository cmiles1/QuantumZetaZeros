# Quantum Zeta Zeros
This is my first repository, meant for collaborating on the study of the Riemann Zeta Zeros and their theoretical relationships.
## Index
1. Dependencies
2. Files
   - Continuedfractions.py
   - Zetafunc.py
   - ZetaSCF.py
   - LRSS.py

<br></br>

## Dependencies
List of every imported module (and what was used from each) in the repo:
1) mpmath  (mp.dps, mp.mpf)
2) collections  (defaultdict)
3) re  (findall)
4) itertools  (islice)

<br></br>

## Files



### Continuedfractions.py
Converts a float, (and takes on a max iteration amount for precision) into a CF. with ```CF_encode(x,maxIt)``` \
Converts a CF into an float with ```CF_decode(cf)```

####  CF_encode(x,maxIt)
Where float 'x' is the real number to encode, and integer 'maxIt' is the maximum iterations (accuracy, maximum length) of the standard continued fraction.\
Returns a list best representing the continued fraction of x

####  CF_decode(cf)
Where 'cf' is the continued fraction in the form of a list\
Returns a list of :

0) the numerator of the best-fitting "h" values
1) the denominator of the best-fitting "k" values
2) the integer form of the fraction

#### Examples:
```
  >>> CF_encode(8.255,12)
  [8, 3, 1, 11, 1, 2, 1]
  >>> CF_decode([8, 3, 1, 11, 1, 2, 1])
  [1651, 200, 8.255]
  >>> CF_decode([8, 3, 1, 11, 1, 2, 1])[2]
  8.255
  >>> CF_decode([8, 3, 1, 11, 1, 2, 1])[:2]
  [1651, 200]
  >>> CF_decode(CF_encode(4.44564,12))
  [4684937111563, 1053827370539, 4.44564]
```
<br></br>

### Zetafunc.py
Computes the Zeta function, in terms of Eta, for a real/complex number. Whereas the real component of s > 0 and not equal to one.\
Note: The complex component of 's' is written in the form 'a+bj'. Where 'J' is the Pythonic form of 'i', used to denote an imaginary number.

#### eta(s, t=100000)
Computes the Eta function (the alternating Zeta function) for a real or complex number ('s') greater than 0 and not equal to one.\
Takes on an argument, "t", as the amount of iterations (terms) to be computed. Default : 100,000 \
Returns the Eta of 's'.

#### zeta(s, t=100000)
Computes the Zeta function, in terms of the Eta function. This should only be used for positive real components of complex numbers, as the domain of the Eta function is all real components greater than 0 and not equal to one.\
Takes an optional argument, "t", as the amount of iterations (terms) to be computed. Default : 100,000 \
Returns the Zeta of 's'.

#### Examples:
```
  >>> print(abs(zeta(1))) # Returns Infinity
  inf
  >>> print(abs(zeta(2))) # Returns (Pi^2) / 6
  1.64493406674819
  >>> (math.pi ** 2)/6
  1.6449340668482264

  >>> print(abs(zeta(3))) # Returns Apery's Constant
  1.2020569031595831

  >>> print(abs(zeta(.5+14.134725141734693790457251983562470270784257115699243175685567460149j))) # Calculates the first known Zeta Zero
  0.0006661155883749823
  
  >>> print(abs(zeta(.5+21.022039638771554992628479593896902777334340524902781754629520403587j))) # Calculates the second known Zeta Zero
  0.0007724462154547514
```
<br></br>

### ZetaSCF.py
Computes the best standard continued fraction from a provided list of re-formatted Zeta Zeros, out to 1024 digits. \(`Zeta_Zeros_1024.txt`)\
Uses the mpmath and re modules.

#### parsefile(file_name)
Takes on the string of a file name and parses the file for the following regular expression:
```
    [0-9]*\.[0-9\n\s]*\s{3}
    
    a) [0-9]*\.
    b) [0-9\n\s]*
    c) \s{3}
    
    a) Numbers 0-9 (greedy) until a decimal
    b) Numbers 0-9, line-breaks, or whitespace characters (greedy), until 
    c) A set of three whitespace characters (The spaces in-between each zero)
```
For each match in the regular expression, any white-space characters or line-breaks are removed, and the output is converted to an mpmath float object (mp.mpf). \
All zeros are returned in the form of a list of mpmath floats (to the precision of mp.dps, which is set to 1025)

#### zeta_scf(s, t=30)
Takes on the imaginary part of a Zeta Zero, `s` (as an mpmath float), and returns its standard continued fraction, (as a list of integers). \
Optionally, takes on an integer, `t`, for the amount-of-terms to output in the continued fraction. (Default: 30)

#### CF_decode(cf)
Decodes a continued fraction using the H/K algorithm, returns an mpmath float object. \
Identical to `Continuedfractions.CF_decode`, but uses mpmath float objects for higher arbitrary precision.

#### delta(a,b)
Returns the delta of each pair of items at the same index of two lists

#### Examples:
```
>>> ZetaZeros = readfile("ZetaZeros_1024.txt")
```
Find the SCF of the Nth Zero to 30 terms:
```
>>> x = N-1
>>> Nth_Zero = zeta_scf(ZetaZeros[x])
```
Find the SCF for the Nth Zero to 500 terms:
```
>>> x = N-1
>>> Nth_Zero_500 = zeta_scf(ZetaZeros[x], 500)
```
Find the SCF for the 1st Zero up to 500 terms:
```
>>> First_Zero_500 = zeta_scf(ZetaZeros[0], 500)
```
Find the best-fitting SCF for all provided Zeta Zeros up to 500 terms :
```
>>> Zeros_CF = list((zeta_scf(i,len(str(i))) for i in ZetaZeros))
```
Get the H/K values of each CF
```
>>> Zeros_HK = list((CF_decode(i) for i in Zeros_CF))
```
Get the Delta of the `Zeros_HK` list ('b'), compared to the `ZetaZeros` list ('a')
```
>>> delta(ZetaZeros, Zeros_HK)
```
<br></br>

### LRSS.py
Finds Longest Recurring Subsequence terms inside a list \
By default, this outputs the LRSS' of each of the CFs of the Zeta Zeros from ZetaSCF.py
Uses "defaultdict" from the "collections" module \

#### getsubs(i,r)
Generates a list of subsequences in a given list \
Returns each of the subsequences in a list

#### CreateSfxArr(r)
For each sequence (of any length) in a list, counts the occurences of the subsequence (`getsubs`) \
Returns a Suffix Array for the specified list ("r").

#### LRSS(z)
Creates a Suffix Array of every subsequence in a list, (`CreateSfxArr`) \
Filters the array's values to only include repeated substrings (value >= 2), (`repeated`) \
Finds the longest-length subsequence that occurs more than once in the string.  \
Returns the longest repeating subsequence of the Suffix Array (as a list)

#### get_all_LRSS(cflist,x)
Generates the LRSS for every term (list) in a list of lists. \
Takes an integer, "x", as the amount of terms to compute in each list. (Default: -1, which is all terms in each CF)\
Returns a list of the LRSS (prior to the 'x'th term), for each list.

#### Examples:
Find the longest recurring subsequence of the first 500 terms of each zeta zero's continued fraction.
```
>>> LRSS_30t = get_all_LRSS(Zeros_CF,500)
>>> n= 0
>>> for i in LRSS_30t:
     print("Zero #", n, "\n", "LRSS :", i)
     n +=1
```
Use all terms:
```
>> LRSS_all = get_all_LRSS(Zeros_CF)
```
Find the LRSS of [<b>1,1,10</b>,4,2,7,<b>1,1,10</b>,3,1,1,1]
```
>>> lrs = LRSS([1, 1, 10, 4, 2, 7, 1, 1, 10, 3, 1, 1, 1])
[1, 1, 10]
```


