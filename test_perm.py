# -*- coding: utf-8 -*-
"""
Created on Thu Nov 19 10:48:49 2015

@author: kurner

Testing the Permutation class in px_class.py
"""

import unittest
from px_class import P

class Test_Permutation(unittest.TestCase):
    
    def test_1(self):
        """
        any p * ~p should give Identity
        """
        p = P() # identity permutation
        new_p = p.shuffle()
        inv_p = ~new_p 
        self.assertEqual(p, inv_p * new_p, "expected identity fails")
        
    def test_2(self):
        """
        encrypt and decrypt are inverse operations on string
        """
        p = P().shuffle() # arbitrary permutation
        s = "the rain in spain stays mainly in the plain"
        c = p.encrypt(s)
        self.assertEqual(p.decrypt(c), s, "decrypted phrase differs")

    def test_3(self):
        """
        lets have a division operation!  a / b == a * ~b
        or equivalently a / b == a * b**-1
        """
        p = P().shuffle() # arbitrary permutation
        q = P().shuffle() # arbitrary permutation
        r = p / q
        # if r = p / q then r * q = p
        self.assertEqual(p, r * q, "expected identity fails")
        r = q / p
        # if r = q / p then r * p = q
        self.assertEqual(q, r * p, "expected identity fails")
                
    def test_4(self):
        self.assertRaises(TypeError, P, 3)
        
if __name__ == "__main__":
    unittest.main()
