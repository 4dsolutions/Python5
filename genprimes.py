# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 14:40:53 2016

@author: kurner
"""
def Primes():
    """generate successive prime numbers (trial by division)"""
    candidate = 1
    _primes_so_far = [2]  # first prime, only even prime
    yield _primes_so_far[-1]
    while True:
        candidate += 2           # check odds only from now on
        for prev in _primes_so_far:
            if prev**2 > candidate:
                yield candidate
                _primes_so_far.append(candidate)
                break
            if not divmod(candidate, prev)[1]: # no remainder!
                break                          # done looping


p = Primes()
print([next(p) for _ in range(3000)])  # next 30 primes please!  
