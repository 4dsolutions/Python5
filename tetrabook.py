# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 21:41:28 2017

@author: kurner
"""

from math import sqrt as rt2, asin, pi, degrees
from tetravolume import Tetrahedron

# CONSTANTS
phi       = (1 + rt2(5))/2
rt2_3     = rt2(3)
long_diag = 2*rt2_3     # cover tip to cover tip, diagonal of rhomb
rt2_8     = rt2(8)
rt2_9     = rt2(9)      # = 3
rt2_6     = rt2(6)      # cover tip to page tip, page vertical
Syn3      = rt2(9/8)    # synergetics constant (to 3rd power)
xyz_base  = rt2_3

class TetraBook:
    
    radians = True
    
    def __init__(self, L = long_diag):
        self.long_edge = L

    @property
    def long_edge(self):
        return self._long_edge
        
    @long_edge.setter
    def long_edge(self, value):
        self._long_edge = value
        self._short_edge = rt2(long_diag**2 - self._long_edge**2)
        self._altitude = self.xyz_volume * rt2_3
        
    @property
    def short_edge(self):
        return self._short_edge
        
    @short_edge.setter
    def short_edge(self, value):
        self._short_edge = value
        self._long_edge = rt2(long_diag**2 - self._short_edge**2)
        self._altitude = self.xyz_volume * rt2_3
        
    @property
    def ivm_volume(self):
        tet = Tetrahedron(1, 1, 1, 1, 1, self._long_edge/2) # D units
        return tet.ivm_volume()
        
    @ivm_volume.setter
    def ivm_volume(self, vol):
        self._altitude = vol*(1/Syn3)*rt2_3
        self.short_edge = self._short() # resets long too
        
    @property
    def xyz_volume(self):
        tet = Tetrahedron(1, 1, 1, 1, 1, self._long_edge/2) # D units
        return tet.xyz_volume()

    @xyz_volume.setter
    def xyz_volume(self, vol):
        self._altitude = vol * rt2_3
        self.short_edge = self._short() # resets long too
        
    def _long(self):
        return rt2(6+(rt2(12)*rt2(3-self._altitude**2)))
 
    def _short(self):  
        return rt2(6-(rt2(12)*rt2(3-self._altitude**2)))
              
    @property
    def altitude(self):
        return self._altitude

    @altitude.setter
    def altitude(self, v):
        self._altitude = v
        self.short_edge = self._short() # resets long too

    @property         
    def angle_s(self):
        angle = asin(self._altitude/rt2_3)
        return (angle if self.radians 
                else degrees(angle))
        
    @property         
    def angle_l(self): 
        angle = asin(self._altitude/rt2_3)          
        return (pi - angle if self.radians 
                else 180 - degrees(angle))
        
    def __str__(self):
        return ("L: {:7.5f} S: {:7.5f} A: {:7.5f} " 
                "XYZvol: {:7.5f} IVMvol: {:7.5f}").format(
                           self.long_edge, 
                           self.short_edge, 
                           self.altitude, 
                           self.xyz_volume,
                           self.ivm_volume)
                           
    def __repr__(self):
        return "TetraBook({})".format(self.long_edge)

def tests():
    book = TetraBook() # a tetrabook is born
    
    book.long_edge = rt2_6  # set long edge, internal adjustments made
    print("Long edge = rt2_6")
    print(book)             # tell us all about it
    
    book.ivm_volume = 1.0   # setting volume this time
    print("IVM volume=1")
    print(book)             # tell us all about it
    
    book.xyz_volume = 1.0   # ... now xyz_volume
    print("XYZ volume=1")
    
    xyzvol = (1/3) * xyz_base * book.altitude
    try:
        assert abs(book.xyz_volume - xyzvol) < 0.0001
    except AssertionError:
        print("Error: ", "{:7.5f}  {:7.5f}".format(book.xyz_volume, xyzvol))
    
    print(book)             # tell us all about it
    
    book.altitude = rt2_3   # ... now altitude
    print("altitude=1")
    print(book)             # tell us all about it

def volumes():
    book = TetraBook()
    book.radians = False
    print("ALT     IVM     XYZ     Long    Short   AngleL     AngleS")
    for vol in [rt2(x)/rt2_8 for x in range(0,10)]:
        book.ivm_volume = vol
        xyzvol = (1/3) * xyz_base * book.altitude
        # fancy volume formula jibes with simple (1/3 base * height)
        try:
            assert abs(book.xyz_volume - xyzvol) < 0.0001
        except AssertionError:
            print("Error: ", "{:7.5f}  {:7.5f}".format(book.xyz_volume, xyzvol))
                   
        print("{:7.5f} {:7.5f} {:7.5f} {:7.5f} {:7.5f} {:9.5f} {:9.5f}".format(
                                               book.altitude,
                                               book.ivm_volume, 
                                               book.xyz_volume,
                                               book.long_edge,
                                               book.short_edge,
                                               book.angle_l,
                                               book.angle_s))    
    
def vary_altitude():
    book = TetraBook()
    book.radians = False
    print("ALT     IVM     XYZ     Long    Short   AngleL  AngleS")
    for alt in [(n/9)*rt2_3 for n in range(0,10)]:
        book.altitude = alt
        xyzvol = (1/3) * xyz_base * book.altitude
        # fancy volume formula jibes with simple (1/3 base * height)
        try:
            assert abs(book.xyz_volume - xyzvol) < 0.0001
        except AssertionError:
            print("Error: ", "{:7.5f}  {:7.5f}".format(book.xyz_volume, xyzvol))
                   
        print("{:7.5f} {:7.5f} {:7.5f} {:7.5f} {:7.5f} {:10.5f} {:10.5f}".format(
                                               book.altitude,
                                               book.ivm_volume, 
                                               book.xyz_volume,
                                               book.long_edge,
                                               book.short_edge,
                                               book.angle_l,
                                               book.angle_s))
                                               
if __name__ == "__main__":
    #tests()
    #vary_altitude()
    volumes()
    
    