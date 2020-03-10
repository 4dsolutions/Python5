# -*- coding: utf-8 -*-
"""
Last updated Mar 10, 2020

@author: Kirby Urner
(c) MIT License

Fun for Group Theory + Python
https://github.com/4dsolutions/Python5/blob/master/px_class.py

"""

from random import shuffle 
from string import ascii_lowercase  # all lowercase letters

class P:
    """
    A Permutation
    
    self._code: a dict, is a mapping of iterable elements 
    to themselves in any order.

    start out with Identity, or directly inject the mapping as
    a dict or use an inversions table to construct the permutation
    """   

    def __init__(self, 
        the_code = None,   # direct inject
        inv_table = None,  # construct 
        iterable = ascii_lowercase + ' '): # default domain

        if the_code:
            self._code = the_code
            
        elif inv_table:
            values = []
            for key in sorted(inv_table, reverse=True):
                if inv_table[key] >= len(values):
                    values.append(key)
                else:
                    values.insert(inv_table[key], key)
            self._code = dict(zip(sorted(inv_table), values))
            
        elif iterable:    
            try:
              # create two iterators for zipping together
              iter1 = iter(iterable)
              iter2 = iter(iterable)
            except:
                raise TypeError
                
            self._code = dict(zip(iter1, iter2))
        
    def shuffle(self):
        """
        return a random permutation of this permutation
        """
        # use shuffle
        # something like
        the_keys = list(self._code.keys()) # grab keys
        shuffle(the_keys)  # shuffles copied one
        newP = P()
        # old keys point to new ones
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
 
    def __getitem__(self, key):
        return self._code.get(key, None)
               
    def __repr__(self):
        return "P class: " + str(tuple(self._code.items())[:3]) + "..."

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

    def __mul__(self, other): 
        """
        look up my keys to get values that serve
        as keys to get others "target" values
        """
        new_code = {}
        for c in self._code:  # going through my keys
            target = other._code[ self._code[c] ]
            new_code[c] = target
        new_P = P(' ') 
        new_P._code = new_code
        return new_P
        
    def __truediv__(self, other):
        return self * ~other
                
    def __pow__(self, exp):
        """
        multiply self * self the right number of times
        """
        if exp == 0:
            output = P()
        else:
            output = self

        for x in range(1, abs(exp)):
            output *= self
        
        if exp < 0:
            output = ~output
            
        return output

    def __call__(self, s): 
        """
        another way to encrypt
        """
        return self.encrypt(s)  

    def __invert__(self):
        """
        create new P with reversed dict
        """
        newP = P(' ')
        newP._code = dict(zip(self._code.values(), self._code.keys()))
        return newP
        
    def __eq__(self, other):
        """
        are these permutation the same?  
        Yes if self._code == other._code
        """
        return self._code == other._code
        
    def inversion_table(self):
        invs = {}
        invP = ~self
        keys = sorted(self._code)
        for key in keys:
            x = invP[key] # position of key
            cnt = 0
            for left_of_key in keys: # in order up to position
                if left_of_key == x: # none more to left
                    break
                if self._code[left_of_key] > key:
                    cnt += 1
            invs[key] = cnt
        return invs
        
if __name__ == "__main__":
    p = P() # identity permutation
    new_p = p.shuffle()
    inv_p = ~new_p 
    try:
        assert p == inv_p * new_p   # should be True
        print("First Test Succeeds")
    except AssertionError:
        print("First Test Fails")
    #==========    
    p = P().shuffle()
    try:
        assert p ** -1 == ~p
        assert p ** -2 == ~(p * p)
        assert p ** -2 == (~p * ~p)
        print("Second Test Succeeds")
    except AssertionError:
        print("Second Test Fails")
    #========== 
    p = P().shuffle()
    s = "able was i ere i saw elba"
    c = p(s)
    print("Plain:  ", s)
    print("Cipher: ", c)
    try:
        assert p.decrypt(c) == s
        print("Third Test Succeeds")
    except AssertionError:
        print("Third Test Fails")
    #========== 
    knuth = {1:5, 2:9, 3:1, 4:8, 5:2, 6:6, 7:4, 8:7, 9:3} # vol 3 pg. 12
    expected = {1:2, 2:3, 3:6, 4:4, 5:0, 6:2, 7:2, 8:1, 9:0} # Ibid
    k = P(the_code=knuth)
    try: 
        assert k.inversion_table() == expected
        print("Fourth Test Succeeds")
    except AssertionError:
        print("Fourth Test Fails")
    #========== 
    p = P(inv_table = expected)
    try: 
        assert p == k
        print("Fifth Test Succeeds")
    except AssertionError:
        print("Fifth Test Fails")
    #========== 
    p = P().shuffle()
    inv = p.inversion_table()
    print("Perm:", p._code)
    print("Inv table:", inv)
    new_p = P(inv_table = inv)
    try: 
        assert p == new_p
        print("Sixth Test Succeeds")
    except AssertionError:
        print("Sixth Test Fails")    
  