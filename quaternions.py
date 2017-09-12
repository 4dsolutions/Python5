#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 07:31:01 2017

@author: Kirby Urner

Youtubes about Quaternions:
https://youtu.be/jlskQDR8-bY Mathoma
https://youtu.be/KdW9ALJMk7s
https://youtu.be/3BR8tK-LuB0

α:  rotation angle
uV: normalized rotation axis

newpointQ = rotationQ * pointQ * ~rotationQ

alpha = cos(α/2) + uV * sin(α/2)
"""

from math import cos, sin, radians, pi
from qrays import Vector
import unittest

class Quaternion:
    
    def __init__(self, w, x, y, z):
        """
        w is the scalar part;
        x,y,z comprise a vector part as 
        the coefficients of i,j,k respectively
        where i,j,k are the three basis vectors
        described by Hamilton such that 
        i**2 == j**2 == k**2 == -1, and 
        i * j * k == -1 as well.
        """
        self.w = w
        self.x = x
        self.y = y
        self.z = z
            
    def __mul__(self, other):
        """
        Derived by inter-multiplying all four terms in 
        each Quaternion to get 16 products and then 
        simplifying according to such rules as ij = k,
        ji = -k.
        
        See:  https://youtu.be/jlskQDR8-bY Mathoma
        'Quaternions explained briefly'
        """
        a, b, c, d = self.w, self.x, self.y, self.z
        e, f, g, h = other.w, other.x, other.y, other.z
        w = (a*e - b*f - c*g - d*h)
        x = (a*f + b*e + c*h - d*g)
        y = (a*g - b*h + c*e + d*f)
        z = (a*h + b*g - c*f + d*e)
        return Quaternion(w, x, y, z)
    
    def __invert__(self):
        return Quaternion( self.w,
                          -self.x,
                          -self.y,
                          -self.z)
        
    def vector(self):
        return Vector((self.x, self.y, self.z))
        
    def __eq__(self, other):
        tolerance = 1e-8
        return (abs(self.w - other.w) < tolerance and
                abs(self.x - other.x) < tolerance and 
                abs(self.y - other.y) < tolerance and
                abs(self.z - other.z) < tolerance)
         
    def __repr__(self):
        return "Quaternion({},{},{},{})".format(self.w, 
                          self.x,
                          self.y,
                          self.z)

def rotator(uV, α):
    w = cos(α/2)
    x = uV.x * sin(α/2)
    y = uV.y * sin(α/2)
    z = uV.z * sin(α/2)
    return Quaternion(w, x, y, z)
    
class TestQuaternion(unittest.TestCase):
    
    def test_inverse(self):
        Q = Quaternion(0, 0, -1, 0)
        inverse = ~Q
        self.assertEqual(Q * inverse, Quaternion(1,0,0,0))
        
    def test_x(self):
        rV = Quaternion(0,1,0,0)
        rQ = rotator(Vector((0,1,0)), pi)
        newQ = rQ * rV * ~rQ
        self.assertTrue(newQ.vector() == Vector((-1, 0, 0)))
        
    def test_360(self):
        rV = Quaternion(0,1,0,0)
        one_deg = radians(1)
        rQ = rotator(Vector((0,1,0)), one_deg)
        for _ in range(360):
            rV = rQ * rV * ~rQ
        self.assertTrue(rV.vector() == Vector((1, 0, 0)))
        
if __name__ == "__main__":
    unittest.main()
    