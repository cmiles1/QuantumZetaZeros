# Quantum Zeta Zeros

This is my first repository, meant for collaborating on the study of the Riemann Zeta Zeros and their possible, theoretical relationships.
## Index
1) Continuedfractions.py
2) Zetafunc.py
3) ZetaSCF.py
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

### ZetaSCF.py
Computes the best standard continued fraction from a provided list of re-formatted Zeta Zeros, out to 1024 digits. \(`Zeta_Zeros_1024.txt`)\
Uses the mpmath and re modules.

#### readfile(file_name)
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
All zeros are returned in the form of a list of mpmath floats (to the precision of mp.dps, which is set to 1028)

#### zeta_scf(s, t=30)
Takes on the imaginary part of a Zeta Zero, `s` (as an mpmath float), and returns its standard continued fraction, (as a list of integers). \
Optionally, takes on an integer, `t`, for the amount-of-terms to output in the continued fraction. (Default: 30)

#### Examples:
```
ZetaZeros = readfile("ZetaZeros_1024.txt")
x = N-1
```
Find the SCF of the Nth Zero to 30 terms:
```
Nth_Zero = zeta_scf(ZetaZeros[x])
```
Find the SCF for the Nth Zero to 500 terms:
```
Nth_Zero_500 = zeta_scf(ZetaZeros[x], 500)
```
Find the SCF for the 1st Zero up to 500 terms:
```
First_Zero_500 = zeta_scf(ZetaZeros[0], 500)
```
Find the SCF for all provided Zeta Zeros up to 500 terms :
```
Zeros_CF = list((zeta_scf(i,500) for i in ZetaZeros))
```

