#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 08:52:51 2020

@author: mac
"""


from math import sqrt as rt2
from qrays import Qvector

S3    = pow(9/8, 0.5)
root2 = rt2(2)
root3 = rt2(3)
root5 = rt2(5)
root6 = rt2(6)
PHI = (1 + root5)/2.0

class Tetrahedron:
    
    def __init__(self, A, B, C, D):
        #onboarding
        self.A = A
        self.B = B
        self.C = C
        self.D = D

    @property 
    def AB(self):
        return (self.A - self.B).length()

    @property 
    def AC(self):
        return (self.A - self.C).length()

    @property 
    def AD(self):
        return (self.A - self.D).length()

    @property 
    def BC(self):
        return (self.B - self.C).length()

    @property 
    def CD(self):
        return (self.C - self.D).length()

    @property 
    def BD(self):
        return (self.B - self.D).length()

    @property
    def volume(self):
        a2 = self.AB ** 2
        b2 = self.AC ** 2
        c2 = self.AD ** 2
        d2 = self.BC ** 2
        e2 = self.CD ** 2
        f2 = self.BD ** 2

        def _addopen():
            sumval = f2*a2*b2
            sumval +=  d2 * a2 * c2
            sumval +=  a2 * b2 * e2
            sumval +=  c2 * b2 * d2
            sumval +=  e2 * c2 * a2
            sumval +=  f2 * c2 * b2
            sumval +=  e2 * d2 * a2
            sumval +=  b2 * d2 * f2
            sumval +=  b2 * e2 * f2
            sumval +=  d2 * e2 * c2
            sumval +=  a2 * f2 * e2
            sumval +=  d2 * f2 * c2
            return sumval

        def _addclosed():
            sumval =   a2 * b2 * d2
            sumval +=  d2 * e2 * f2
            sumval +=  b2 * c2 * e2
            sumval +=  a2 * c2 * f2
            return sumval

        def _addopposite():
            sumval =  a2 * e2 * (a2 + e2)
            sumval += b2 * f2 * (b2 + f2)
            sumval += c2 * d2 * (c2 + d2)
            return sumval
        
        return ((_addopen() - _addclosed() - _addopposite())/2) ** 0.5

    @property
    def xyz_volume(self):
        return 1/S3 * self.volume


#===================================================    
import unittest

class TetTest(unittest.TestCase):
    
    def setUp(self):
        q1 = Qvector((1,0,0,0))
        q2 = Qvector((0,1,0,0))
        q3 = Qvector((0,0,1,0))
        q4 = Qvector((0,0,0,1))
        self.the_tet = Tetrahedron(q1,q2,q3,q4)
        
    def test_init(self):
        self.assertEqual(self.the_tet.AB, 1, "Houston, we've got a problem")
        self.assertEqual(self.the_tet.AC, 1, "Houston, we've got a problem")
        self.assertEqual(self.the_tet.AD, 1, "Houston, we've got a problem")
        self.assertEqual(self.the_tet.BC, 1, "Houston, we've got a problem")
        self.assertEqual(self.the_tet.CD, 1, "Houston, we've got a problem")
        self.assertEqual(self.the_tet.BD, 1, "Houston, we've got a problem")

    def test_volume(self):
        self.assertEqual(self.the_tet.volume, 1, "Houston, we've got a problem")
        
def test():
    unittest.main()
    

if __name__ == "__main__":
    test()