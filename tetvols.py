#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 14:36:27 2019

@author: Kirby Urner
"""

from operator import mul
from math import sqrt as rt2
from qrays import Qvector, Vector
import sys

Syn3    = pow(9/8, 0.5)
root2 = rt2(2)
root3 = rt2(3)
root5 = rt2(5)
root6 = rt2(6)
PHI = (1 + root5)/2.0

def ivm_volume(edges):
    """
    Takes six edges of tetrahedron with faces
    (a,b,d)(b,c,e)(c,a,f)(d,e,f) 
    
    returns tetravolumes
    """
    
    a2, b2, c2, d2, e2, f2 = map(mul, edges, edges)

    def addopen():
        sumval =   f2 * a2 * b2
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

    def addclosed():
        sumval =   a2 * b2 * d2
        sumval +=  d2 * e2 * f2
        sumval +=  b2 * c2 * e2
        sumval +=  a2 * c2 * f2
        return sumval

    def addopposite():
        sumval =  a2 * e2 * (a2 + e2)
        sumval += b2 * f2 * (b2 + f2)
        sumval += c2 * d2 * (c2 + d2)
        return sumval
    
    ivmvol = ((addopen() - addclosed() - addopposite())/2) ** 0.5
    
    return ivmvol
    
def xyz_volume(edges):
    return (1/Syn3) * ivm_volume(edges)

def make_tet(v0,v1,v2):
    """
    three edges from any corner, remaining three edges computed
    """
    a,b,c = v0.length(), v1.length(), v2.length()
    d,e,f = (v0-v1).length(), (v1-v2).length(), (v2-v0).length()
    edges = a,b,c,d,e,f
    return ivm_volume(edges), xyz_volume(edges)

R = 0.5
D = 1.0

import unittest
class Test_Tetrahedron(unittest.TestCase):

    def test_unit_volume(self):
        tet = ivm_volume((D, D, D, D, D, D))
        self.assertEqual(tet, 1, "Volume not 1")

    def test_e_module(self):
        e0 = D
        e1 = root3 * PHI**-1
        e2 = rt2((5 - root5)/2)
        e3 = (3 - root5)/2
        e4 = rt2(5 - 2*root5)
        e5 = 1/PHI
        tet = ivm_volume((e0, e1, e2, e3, e4, e5))
        self.assertTrue(1/23 > tet/8 > 1/24, "Wrong E-mod")
        
    def test_unit_volume2(self):
        tet = xyz_volume((R, R, R, R, R, R))
        self.assertAlmostEqual(tet, 0.117851130)

    def test_phi_edge_tetra(self):
        tet = ivm_volume((D, D, D, D, D, PHI))
        self.assertAlmostEqual(float(tet), 0.70710678)

    def test_right_tetra(self):
        e = pow((root3/2)**2 + (root3/2)**2, 0.5)  # right tetrahedron
        tet = xyz_volume((D, D, D, D, D, e))
        self.assertAlmostEqual(tet, 1)

    def test_quadrant(self):
        qA = Qvector((1,0,0,0))
        qB = Qvector((0,1,0,0))
        qC = Qvector((0,0,1,0))
        tet = make_tet(qA, qB, qC) 
        self.assertAlmostEqual(tet[0], 0.25) 

    def test_octant(self):
        x = Vector((0.5, 0,   0))
        y = Vector((0  , 0.5, 0))
        z = Vector((0  , 0  , 0.5))
        tet = make_tet(x,y,z)
        self.assertAlmostEqual(tet[1], 1/6, 5) # good to 5 places

    def test_quarter_octahedron(self):
        a = Vector((1,0,0))
        b = Vector((0,1,0))
        c = Vector((0.5,0.5,root2/2))
        tet = make_tet(a, b, c)
        self.assertAlmostEqual(tet[0], 1, 5) # good to 5 places  

    def test_xyz_cube(self):
        a = Vector((0.5, 0.0, 0.0))
        b = Vector((0.0, 0.5, 0.0))
        c = Vector((0.0, 0.0, 0.5))
        R_octa = make_tet(a,b,c) 
        self.assertAlmostEqual(6 * R_octa[1], 1, 4) # good to 4 places  

    def test_s3(self):
        D_tet = xyz_volume((D, D, D, D, D, D))
        a = Vector((0.5, 0.0, 0.0))
        b = Vector((0.0, 0.5, 0.0))
        c = Vector((0.0, 0.0, 0.5))
        R_cube = 6 * make_tet(a,b,c)[1]
        self.assertAlmostEqual(D_tet * Syn3, R_cube, 4)

    def test_martian(self):
        p = Qvector((2,1,0,1))
        q = Qvector((2,1,1,0))
        r = Qvector((2,0,1,1))
        result = make_tet(5*q, 2*p, 2*r)
        self.assertAlmostEqual(result[0], 20, 7)
        
    def test_phi_tet(self):
        "edges from common vertex: phi, 1/phi, 1"
        p = Vector((1, 0, 0))
        q = Vector((1, 0, 0)).rotz(60) * PHI
        r = Vector((0.5, root3/6, root6/3)) * 1/PHI
        result = make_tet(p, q, r)
        self.assertAlmostEqual(result[0], 1, 7)
        
    def test_phi_tet_2(self):
        p = Qvector((2,1,0,1))
        q = Qvector((2,1,1,0))
        r = Qvector((2,0,1,1))
        result = make_tet(PHI*q, (1/PHI)*p, r)
        self.assertAlmostEqual(result[0], 1, 7)
        
    def test_phi_tet_3(self):
        T = ivm_volume((PHI, 1/PHI, 1.0, 
                        root2, root2/PHI, root2))
        self.assertAlmostEqual(T, 1, 7)

    def test_koski(self):
        a = 1 
        b = PHI ** -1
        c = PHI ** -2
        d = (root2) * PHI ** -1 
        e = (root2) * PHI ** -2
        f = (root2) * PHI ** -1       
        T = ivm_volume((a,b,c,d,e,f))
        self.assertAlmostEqual(T, PHI ** -3, 7)       

def command_line():
    args = sys.argv[1:]
    try:
        args = [float(x) for x in args] # floats
        print(ivm_volume(args))
        print(xyz_volume(args)) 
    except TypeError:
        edges = 1,1,1,1,1,1
        print("defaults used")
        print(ivm_volume(args))
        print(xyz_volume(edges)) 

        
if __name__ == "__main__":
    if len(sys.argv)==7:
        command_line()  
    else:
        unittest.main()
        