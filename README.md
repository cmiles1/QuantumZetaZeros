# Quantum Zeta Zeros

This is my first repository, meant for studying the Riemann Hypothesis and the link between the zeta function's zeros and the spacing of prime numbers.
## Index
1) Continuedfractions.py
## Files

### continuedfractions.py
Converts a float, (and a max iteration) and turns it into a CF.\
Converts a CF into an float

####  CF_encode(x,maxIt)
Where float 'x' is the real number to encode, and integer 'maxIt' is the maximum iterations (accuracy, maximum length) of the standard continued fraction.\
Returns a list best representing the continued fraction of x

####  CF_decode(cf)
Where 'cf' is the continued fraction in the form of a list\
Returns a touple of :\
0) the numerator of the best-fitting "h" values\
1) the denominator of the best-fitting "k" values\
2) the integer form of the fraction\

#### Examples:
```
  >>> import continuedfractions
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
