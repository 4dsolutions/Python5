# -*- coding: utf-8 -*-
"""
Created on Tue Feb 14 00:19:17 2017

@author: Kirby Urner (programmer)

CoverA and CoverB by David Koski

A book with triangular book covers lies open on a table.
One triangular page flaps back and forth, its tip defining
two complementary tetrahedrons, the page a shared face.

They have equal volume, though unless the page is straight
up, one will have the longer edge twixt page tip and 
cover tip.

This program marches the page tip tetrahedron through
'station stops' with volumes at sqrt(n/9) n=0...9.
The functions get the page-tip to cover-tip lengths 
which get fed to a Tetrahedron type with a volume method
based on six edges for input.  Getting back the expected
volume for output shows the functions are getting the 
right lengths.

The station stops are important especially for the 
last two: a regular and right tetrahedron respectively,
each volume 1 depending on whether XYZ or IVM mensuration
is used, S3 or sqrt(9/8) being the conversion factor 
between them.

http://controlroom.blogspot.com/2017/01/page-turner.html

"""
from math import sqrt
from tetravolume import Tetrahedron

sqrt2 = sqrt(2)

def coverA(n):
    # Cover A to Tip when Tetrahedron volume = sqrt(n/9)
    acute = sqrt(6-(2*(sqrt(9-n))))
    return acute

def coverB(n):
    # Cover B to Tip when Tetrahedron volume = sqrt(n/9)
    obtuse = sqrt(6+(2*(sqrt(9-n))))
    return obtuse
    
def chart():
    """
    >>> chart()
    Vol.   IVM      XYZ      check
    √(0/9) 0.000000 0.000000 0.000000
    √(1/9) 0.353553 0.333333 0.333333
    √(2/9) 0.500000 0.471405 0.471405
    √(3/9) 0.612372 0.577350 0.577350
    √(4/9) 0.707107 0.666667 0.666667
    √(5/9) 0.790569 0.745356 0.745356
    √(6/9) 0.866025 0.816497 0.816497
    √(7/9) 0.935414 0.881917 0.881917
    √(8/9) 1.000000 0.942809 0.942809
    √(9/9) 1.060660 1.000000 1.000000
    """
    print("Vol.   IVM      XYZ      check")
    for n in range(10):
        # coverA or coverB will give the same answers as the 
        # complementary tetrahedrons have the same volume
        tet = Tetrahedron(1, 1, 1, 1, 1, coverA(n)/2)
        print("√({}/9) {:6f} {:6f} {:6f}".format(
            n, tet.ivm_volume(), tet.xyz_volume(), sqrt(n/9)))
    
if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
