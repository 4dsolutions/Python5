#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Sep  2 09:41:08 2017

@author: Kirby Urner
"""

from math import gcd
from string import ascii_lowercase
from random import shuffle
import unittest

def totatives(n):
    return {x for x in range(n) if gcd(x, n) == 1}

def totient(n):
    return len(totatives(n))

class M:  # for "modulo"
    
    modulus = 10  # class level
    
    def __init__(self, val, modulus=None):
        if modulus:
            self.modulus = M.modulus = modulus # resettable
        else:
            self.modulus = M.modulus # default
        self.val = val % self.modulus
        
    def __add__(self, other):
        if self.modulus != other.modulus:
            raise ValueError
        return M(self.val + other.val, self.modulus)
    
    def __mul__(self, other):
        if self.modulus != other.modulus:
            raise ValueError
        return M(self.val * other.val, self.modulus)
    
    def _bingcd(self, a, b):
        """Extended version of Euclid's Algorithm (binary GCD)
        Returns (m,n,gcd) such that  m*a + n*b = gcd(a,b)"""
        g,u,v = [b,a],[1,0],[0,1]
        while g[1] != 0:
            y = g[0] // g[1]
            g[0],g[1] = g[1],g[0] % g[1]
            u[0],u[1] = u[1],u[0] - y*u[1]
            v[0],v[1] = v[1],v[0] - y*v[1]
        m = v[0]%b
        gcd = (m*a)%b
        n = (gcd - m*a)/b
        return (m,n,gcd)

    def __invert__(self):
        """
        If gcd(a,b)=1, then (inverse(a, b) * a) mod b = 1,
        otherwise, if gcd(a,b)!=1, return 0
    
        Useful in RSA encryption, for finding d such that
        e*d mod totient(n) == 1
        """
        inva,n,gcd = self._bingcd(self.val, self.modulus)
        return M((gcd==1) * inva, self.modulus)
    
    def __pow__(self, exp):  # pow() and ** both trigger this method
        output = self
        if exp < 0:
            exp = abs(exp)
            output = ~self
        elif exp == 0:
            output = M(1)
        elif exp == 1:
            output = self    
        if exp > 1:
            for _ in range(1, exp):
                output = output * self       
        return output
    
    def __repr__(self):
        return "(" + str(self.val) + " mod " + str(M.modulus)+ ")"
        
class P_base:
    """
    A Permutation
    
    self._code: a dict, is a mapping of iterable elements 
    to themselves in any order.
    """   

    def __init__(self, iterable = ascii_lowercase + ' '): # default domain
        """
        start out with Identity
        """  
        try:
            seq1 = iter(iterable)
            seq2 = iter(iterable)
        except:
            raise TypeError

        self._code = dict(zip(seq1, seq2))
 
    def __getitem__(self, key):
        return self._code.get(key, None)
               
    def __repr__(self):
        return "P class: " + str(tuple(self._code.items())[:3]) + "..."

    def __mul__(self, other): 
        """
        look up my keys to get values that serve
        as keys to get others "target" values
        """
        new_code = {}
        for c in self._code:  # going through my keys
            target = other._code[ self._code[c] ]
            new_code[c] = target
        new_P = P() 
        new_P._code = new_code
        return new_P
   
    def __eq__(self, other):
        """
        are these permutation the same?  
        Yes if self._cod==e  other._code
        """
        return self._code == other._code
    
class P(P_base):  # first use of inheritance
        
    def __invert__(self):
        """
        create new P with reversed dict
        """
        newP = P()
        newP._code = dict(zip(self._code.values(), self._code.keys()))
        return newP
    
    def shuffle(self):
        """
        return a random permutation of this permutation
        """
        # use shuffle
        # something like
        the_keys = list(self._code.keys()) # grab keys
        shuffle(the_keys)  # shuffles 'em
        newP = P()
        # inject dict directly...
        newP._code = dict(zip(self._code.keys(), the_keys))
        return newP
        
    def encrypt(self, plain):
        """
        turn plaintext into cyphertext using self._code
        """
        output = ""  # empty string
        for c in plain:
            output = output + self._code.get(c, c) 
        return output
            
    def decrypt(self, cypher):
        """
        Turn cyphertext into plaintext using ~self
        """
        reverse_P = ~self  # invert me!
        output = ""
        for c in cypher:
            output = output + reverse_P._code.get(c, c)
        return output

    def cyclic(self):
        """
        cyclic notation, a compact view of a group
        """
        output = []
        the_dict = self._code.copy()
        while the_dict:
            start = tuple(the_dict.keys())[0]
            the_cycle = [start]
            the_next = the_dict.pop(start)
            while the_next != start:
                the_cycle.append(the_next)
                the_next = the_dict.pop(the_next)
            output.append(tuple(the_cycle))
        return tuple(output)
    
    def from_cyclic(self, incoming):
        """
        create a P-type object from incoming cyclic view
        
        Think of zipping ('a', 'c', 'q', 'k') with 
        ('c', 'q', 'k', 'a') -- the pairs ('a', 'c'),
        ('c', 'q'), ('q', 'k') and ('k', 'a') are what
        dict() will then consume.  We go through each 
        subgroup, updating the final dict with the results
        of each loop.  When done, dump the dict into _code.
        """
        output = {} 
        for subgroup in incoming:
            output.update(dict(zip(subgroup, subgroup[1:] + tuple(subgroup[0]))))
        newP = P()
        newP._code = output
        return newP
 
class Test_M(unittest.TestCase):
    
    def test_Perm(self):
        pass
    
    def test_M(self):
        N = 3 * 47
        m = M(93, N)                # original message, N product of 2 primes
        e = 7                       # raise to power
        c = m ** e                  # encrypted
        d = ~M(e, totient(N))       # inverse of c mod 40
        self.assertEqual(m.val, pow(c.val, d.val, N)) # getting our message back
    
if __name__ == "__main__":
    unittest.main()