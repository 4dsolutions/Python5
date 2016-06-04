# -*- coding: utf-8 -*-
"""
Created on Sat Jun  4 09:07:22 2016

@author:  K. Urner, 4D Solutions, (M) MIT License

 Aug 29, 2000: added extra-class, class dependent methods for
    dot and cross as alternative syntax
 July 8,2000: added method for rotation around any axis vector
 May 27,2000: shortend several methods thanks to Peter Schneider-Kamp
 May 24,2000: added unit method, tweaks
 May 8, 2000: slight tweaks re rounding values
 May 7, 2000: enhanced the Qvector subclass with native
    length, dot, cross methods -- keeps coords as a 4-tuple
    -- generalized Vector methods to accommodate 4-tuples
    if Qvector subclass, plus now returns vector of whatever
    type invokes method (i.e. Qvector + Qvector = Qvector)
 Mar 23, 2000
 added spherical coordinate subclass
 added quadray coordinate subclass
 Mar 5: added angle function
"""

import math
from math import pi as π, radians, degrees
from operator import add, sub, mul, neg

deg2rad = π/180
rad2deg = 180/π
root2   = 2.0**0.5

class Vector:

    def __init__(self, arg, *flag):
        """Initialize a vector at an (x,y,z) tuple (= arg)."""
        self.coords = tuple(map(float,arg))
        self.xyz = self.coords

    def __repr__(self):
        return "Vector " + str(self.coords)
    
    def __mul__(self,scalar):
        """Return vector (self) * scalar."""
        newcoords = map(mul,len(self.coords)*[scalar],self.coords)
        return self.__class__(newcoords)

    __rmul__ = __mul__ # allow scalar * vector

    def __div__(self,scalar):
        """Return vector (self) * 1/scalar"""        
        return self.__mul__(1.0/scalar)
    
    def __add__(self,v1):
        """Add a vector object to this object (self)"""        
        return self.__class__(map(add,v1.xyz,self.xyz),1)
        
    def __sub__(self,v1):
        """Subtract a vector object from this object (self).
        
        return a new vector"""
        return self.__add__(-v1)
    
    def __neg__(self):      
        """Return a new vector, the negative of this one."""
        return self.__class__(map(neg,self.coords),1)

    def unit(self):
        return self.__mul__(1./self.length())

    def dot(self,v1):
        """Return the dot product of self with another vector.

        return a scalar"""
        return sum(map(mul,v1.xyz,self.xyz))
        # return reduce(add,map(mul,v1.xyz,self.xyz))

    def cross(self,v1):
        """Return the cross product of self with another vector

        return a vector"""
        newcoords = [0,0,0]
        newcoords[0] = self.xyz[1]*v1.xyz[2]-self.xyz[2]*v1.xyz[1]
        newcoords[1] = self.xyz[2]*v1.xyz[0]-self.xyz[0]*v1.xyz[2]
        newcoords[2] = self.xyz[0]*v1.xyz[1]-self.xyz[1]*v1.xyz[0]
        return self.__class__(newcoords,1)
    
    def length(self):
        """Return this vector's length"""
        return self.dot(self) ** 0.5

    def angle(self,v1):
       """Return angle between self and v1, in decimal degrees"""
       costheta = round(self.dot(v1)/(self.length() * v1.length()),10)
       theta = math.acos(costheta) * rad2deg
       return round(theta,10)

    def rotaxis(self,vAxis,deg):
        """Rotate around vAxis by deg

        realign rotation axis with Z-axis, realign self accordingly,
        rotate by deg (counterclockwise) around Z, resume original
        orientation (undo realignment)"""
        r,phi,theta = vAxis.spherical()
        newv  = self.rotz(-theta).roty(phi)
        newv  = newv.rotz(-deg)
        newv  = newv.roty(-phi).rotz(theta)
        return self.__class__(newv.xyz,1)        

    def rotx(self,deg):
        rad    = deg*deg2rad
        newy   = math.cos(rad)*self.xyz[1] - math.sin(rad)*self.xyz[2]
        newz   = math.sin(rad)*self.xyz[1] + math.cos(rad)*self.xyz[2]
        newxyz = map(lambda x: round(x,8),(self.xyz[0],newy,newz))
        return self.__class__(newxyz,1)
   
    def roty(self,deg):
        rad    = deg*deg2rad
        newx   = math.cos(rad)*self.xyz[0] - math.sin(rad)*self.xyz[2]
        newz   = math.sin(rad)*self.xyz[0] + math.cos(rad)*self.xyz[2]
        newxyz = map(lambda x: round(x,8),(newx,self.xyz[1],newz))
        return self.__class__(newxyz,1)

    def rotz(self,deg):
        rad    = deg*deg2rad
        newx   = math.cos(rad)*self.xyz[0] - math.sin(rad)*self.xyz[1]
        newy   = math.sin(rad)*self.xyz[0] + math.cos(rad)*self.xyz[1]
        newxyz = map(lambda x: round(x,8),(newx,newy,self.xyz[2]))
        return self.__class__(newxyz,1)
    
    def spherical(self):
        """Return (r,phi,theta) spherical coords based on current (x,y,z)"""
        r = self.length()

        if self.xyz[0]==0:
            if   self.xyz[1]==0: theta =   0.0
            elif self.xyz[1]<0:  theta = -90.0
            else:                theta =  90.0
            
        else:            
            theta = math.atan(self.xyz[1]/self.xyz[0]) * rad2deg
            if   self.xyz[0]<0 and self.xyz[1]==0:  theta =    180
            elif self.xyz[0]<0 and self.xyz[1]<0:   theta =    180 - theta
            elif self.xyz[0]<0 and self.xyz[1]>0:   theta = - (180 + theta)

        if r==0: phi=0.0
        else: phi = math.acos(self.xyz[2]/r) * rad2deg
        
        return (r,phi,theta)

    def quadray(self):
        """return (a,b,c,d) quadray based on current (x,y,z)"""
        x=self.xyz[0]
        y=self.xyz[1]
        z=self.xyz[2]
        a = (2/root2) * ((x>=0)*x   + (y>=0)*y   + (z>=0)*z)
        b = (2/root2) * ((x<0)*(-x) + (y<0)*(-y) + (z>=0)*z)
        c = (2/root2) * ((x<0)*(-x) + (y>=0)*y   + (z<0)*(-z))
        d = (2/root2) * ((x>=0)*x   + (y<0)*(-y) + (z<0)*(-z))
        return self.norm((a,b,c,d))

    def norm(self,plist):
        """Normalize such that 4-tuple all non-negative members."""
        return tuple(map(sub,plist,[min(plist)]*4)) 
    
    def norm0(self):
        """Normalize such that sum of 4-tuple members = 0"""
        q = self.quadray()
        return tuple(map(sub,q,[sum(q)/4.0]*4))
        
class Qvector(Vector):
    """Subclass of Vector that takes quadray coordinate args"""
    
    def __init__(self,arg,*flag):
        """Initialize a vector at an (a,b,c,d) tuple (= arg).
        
        NOTE: in accompanying essay, xyz units = sphere diameter
        i.e. Vector((1,0,0)).length() is 1 D, therefore quadray
        inputs must be scaled by 1/2 to fit this context, i.e.
        tetra edge defined by 2 basis quadrays = 1 D."""
        
        arg = tuple(arg) # in case was map object
        if len(arg)==3:  arg = Vector(arg).quadray() # if 3-tuple passed
            
        self.coords = self.norm(arg)

        a,b,c,d     =  self.coords
        self.xyz    = ((0.5/root2) * (a - b - c + d),
                       (0.5/root2) * (a - b + c - d),
                       (0.5/root2) * (a + b - c - d))

    def __repr__(self):
        return "Qvector " + str(self.coords)
                    
    def dot(self,v1):
        """Return the dot product of self with another vector.

        return a scalar"""
        scalar = 0
        return 0.5*sum(map(mul,self.norm0(),v1.norm0()))

    def cross(self,v1):
        """Return the cross product of self with another vector.

        return a Qvector"""
        A=Qvector((1,0,0,0))
        B=Qvector((0,1,0,0))
        C=Qvector((0,0,1,0))
        D=Qvector((0,0,0,1))
        a1,b1,c1,d1 = v1.quadray()
        a2,b2,c2,d2 = self.quadray()
        k= (2.0**0.5)/4.0
        sum =   (A*c1*d2 - A*d1*c2 - A*b1*d2 + A*b1*c2
               + A*b2*d1 - A*b2*c1 - B*c1*d2 + B*d1*c2 
               + b1*C*d2 - b1*D*c2 - b2*C*d1 + b2*D*c1 
               + a1*B*d2 - a1*B*c2 - a1*C*d2 + a1*D*c2
               + a1*b2*C - a1*b2*D - a2*B*d1 + a2*B*c1 
               + a2*C*d1 - a2*D*c1 - a2*b1*C + a2*b1*D)
        return k*sum
    
    def quadray(self):
        return self.coords


class Svector(Vector):
    """Subclass of Vector that takes spherical coordinate args."""
    
    def __init__(self,arg,isxyz=None):
        # if returning from Vector calc method, spherical is true
        if isxyz:
            arg = Vector(arg).spherical()
            
        # initialize a vector at an (r,phi,theta) tuple (= arg)
        r     = arg[0]
        phi   = deg2rad * arg[1]
        theta = deg2rad * arg[2]
        self.coords = tuple(map(lambda x:round(x,15),
                      (r * math.cos(theta) * math.sin(phi),
                       r * math.sin(theta) * math.sin(phi),
                       r * math.cos(phi))))
        self.xyz = self.coords

    def __repr__(self):
        return "Svector " + str(self.spherical())

def dot(a,b):
    return a.dot(b)

def cross(a,b):
    return a.cross(b)

def angle(a,b):
    return a.angle(b)

def length(a):
    return a.length()

