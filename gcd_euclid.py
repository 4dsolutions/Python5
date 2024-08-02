#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 09:36:45 2024

@author: kirbyurner
"""

def gcd(n, m):
    """
    Euclid's Method
    """
    # if n < m then r will be n e.g. 5 % 100 returns 5
    r = n % m   # dividing n by m leaves how many?
    if r == 0:  # no remainder, m is gold
        return m
    else:
        # see if m and r have a gcd > 1
        # if r == 1, then r==0 next call, current m returned
        return gcd(m, r) 

def test_me():
    m = 100; n = 20
    print(f"gcd({m}, {n}) = {gcd(m,n)}")
    m = 113; n = 20
    print(f"gcd({m}, {n}) = {gcd(m,n)}")
    m = 17; n = 31
    print(f"gcd({m}, {n}) = {gcd(m,n)}")
    m = 270; n = 192
    print(f"gcd({m}, {n}) = {gcd(m,n)}")
    
    
if __name__ == "__main__":
    test_me()