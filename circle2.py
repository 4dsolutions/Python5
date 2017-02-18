# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 15:43:14 2016

@author: Kirby Urner

toggle the import model_property on and off to see
the example works the same either way.  model_property
contains a pure Python emulator of the built in
property type.

Related reading:
https://mail.python.org/pipermail/edu-sig/2016-October/011548.html
"""

# from model_property import Property as property
import math

class Circle:
    """setting either the radius or area attribute sets the other
       as a dependent value.  Initialized with radius only, unit
       circle by default.
    """

    def __init__(self, radius = 1):
        self.radius = radius

    @property
    def area(self):
        return self._area

    @property
    def radius(self):
        return self._radius

    @property
    def circumference(self):
        return self._circum
        
    @circumference.setter
    def circumference(self, value):
        self.radius = value / (2 * math.pi)
        
    @area.setter
    def area(self, value):
        self._area = value
        self._radius = math.sqrt(self._area / math.pi)
        self._circum = 2 * math.pi * self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value
        self._area = math.pi * (self._radius ** 2)
        self._circum = 2 * math.pi * self._radius
        
    def __repr__(self):
        return "Circle(radius = {})".format(self.radius)

the_circle = Circle(5)
print("the_circle:", the_circle)
print("Area: ", the_circle.area)
the_circle.area = 50
print("Radius when Area=50:", the_circle.radius)