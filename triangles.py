# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 19:39:20 2017

@author: Kirby Urner

Simple Triangle class the initializes 
using 3 vertexes A, B, C using (x,y) tuples

a, b, c are sides opposite A, B, C. 
Angles are BAC, ABC, ACB or alpha, beta, gamma

These edge lengths as well as the three angles are available
as read-only attributes, along with other boolean attributes:

is_scalene (all edges different length), is_obtuse, 
is_equiangular (all angles & edges equal)
is_right (Pythagorean Theorem checks out) 
is_acute (all angles < 90) 
is_iscosceles (defined as not scalene)

https://en.wikipedia.org/wiki/Triangle#Types_of_triangle

Given floating point numbers are used, comparison of edges
and angles to 90 are within a set tolerance. Angles may be
expressed in either radius or degrees depending on in_radians
"""

from math import sqrt as rt2, acos as arc_cosine, degrees
import unittest

class Triangle:
    in_radians = True
    tolerance = 1e-5
    
    def __init__(self, Axy, Bxy, Cxy, in_radians=True):
        self._Axy = Axy
        self._Bxy = Bxy
        self._Cxy = Cxy
        Triangle.in_radians = in_radians
                
    @property
    def a(self):
        Bx, By = self._Bxy
        Cx, Cy = self._Cxy
        return rt2((Bx - Cx)**2 + (By - Cy)**2)

    @property
    def b(self):
        Ax, Ay = self._Axy
        Cx, Cy = self._Cxy
        return rt2((Ax - Cx)**2 + (Ay - Cy)**2)

    @property
    def c(self):
        Ax, Ay = self._Axy
        Bx, By = self._Bxy
        return rt2((Ax - Bx)**2 + (Ay - By)**2)
        
    @property
    def is_right(self):
        if not self.hypotenuse:
            return False
        return True
        
    @property
    def is_obtuse(self):
        return (self.ABC > 90) or (self.BAC > 90) or (self.ACB > 90)

    @property
    def is_acute(self):
        return (self.ABC < 90) and (self.BAC < 90) and (self.ACB < 90)

    @property
    def is_oblique(self):
        return self.is_acute or self.is_obtuse
        
    @property 
    def is_scalene(self):
        """
        All sides different to within margin
        """
        return ((abs(self.a - self.b) > self.tolerance) 
                and (abs(self.a - self.c) > self.tolerance) 
                and (abs(self.b - self.c) > self.tolerance))

    @property 
    def is_isosceles(self):
        return not self.is_scalene
        
    @property 
    def is_equiangular(self):
        """
        All sides different to within margin
        """
        return ((abs(self.a - self.b) <= self.tolerance) 
                and (abs(self.a - self.c) <= self.tolerance) 
                and (abs(self.b - self.c) <= self.tolerance))
                
    @property
    def area(self):
        """
        Heron's formula
        """
        s = (self.a + self.b + self.c)/2
        return rt2(s*(s-self.a)*(s-self.b)*(s-self.c)) # Heron's formula
    
    @property
    def ivm_area(self):
        return self.area/rt2(3)
        
    @property
    def perimeter(self):
        return self.a + self.b + self.c
                             
    @property
    def hypotenuse(self):
        if   abs((self.c**2 + self.b**2) - self.a**2) < self.tolerance:
            return "a"
        elif abs((self.c**2 + self.a**2) - self.b**2) < self.tolerance:
            return "b"
        elif abs((self.b**2 + self.a**2) - self.c**2) < self.tolerance:
            return "c"
        else:
            return None

    @property
    def BAC(self):  # alpha
        a,b,c = self.a, self.b, self.c
        rads = arc_cosine((b**2 + c**2 - a**2)/(2*b*c))
        if not self.in_radians:
            return degrees(rads)
        return rads

    alpha = BAC
       
    @property
    def ABC(self):  # beta
        a,b,c = self.a, self.b, self.c
        rads = arc_cosine((a**2 + c**2 - b**2)/(2*a*c))
        if not self.in_radians:
            return degrees(rads)
        return rads

    beta = ABC
                
    @property
    def ACB(self): # gamma
        a,b,c = self.a, self.b, self.c
        rads = arc_cosine((a**2 + b**2 - c**2)/(2*a*b))
        if not self.in_radians:
            return degrees(rads)
        return rads
        
    gamma = ACB
    
class TestTriangle(unittest.TestCase):
    
    def test_pythagoras(self):
        t = Triangle((0,0), (4,0), (0,3))
        self.assertEqual(t.c, 4)
        self.assertEqual(t.b, 3)
        self.assertEqual(t.a, 5)
        self.assertAlmostEqual(t.a, 5.0)
        self.assertEqual(t.is_right, True)

    def test_right(self):
        t = Triangle((3,3), (2,6), (3,2))
        self.assertEqual(t.is_right, False)
        
        t = Triangle((3,3), (2,6), (-1,5))
        self.assertEqual(t.is_right, True) 
        self.assertTrue(t.is_isosceles)
        self.assertAlmostEqual(t.area, 5)
        
        t = Triangle((3,3), (2,6), (7,4))
        self.assertEqual(t.is_right, False)
        self.assertTrue(t.is_scalene)
        
        t = Triangle((3,3), (2,6), (0,3))
        self.assertEqual(t.is_right, False)

    def test_angles(self):        
        t = Triangle((3,3), (2,6), (-1,5))
        t.in_radians = False
        self.assertAlmostEqual(t.ABC, 90)
    
    def test_equilateral(self):
        t = Triangle((0,0), (10,0), (5, 5*rt2(3)))        
        t.in_radians = False
        self.assertAlmostEqual(t.ABC, 60)
        self.assertAlmostEqual(t.BAC, 60)
        self.assertAlmostEqual(t.ACB, 60)
        self.assertTrue(t.is_equiangular)
        
    def test_ivm(self):
        t = Triangle((-1,0),(1,0),(0,rt2(3))) # book cover
        self.assertAlmostEqual(t.ivm_area, 1.0)
        
if __name__ == "__main__":
    unittest.main()
    