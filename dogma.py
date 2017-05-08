#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 14:27:35 2017

@author: Kirby Urner

https://youtu.be/ZdvpNaWwx24 (useful talk by Simeon Franklin)

Descriptors:
    data: __set__ and __get__
    non-data: __get__ only
    
Rules of access:

    1. obj.x returns obj.__dict__['x'] unless there's an
       type(obj).x with a __get__ method
    2. type(obj).x
    3. x with __get__ in ancestral tree, or regular x attr
    4. __getattr__ triggered
    
    5. obj.x = y sets obj.__dict__['y'] unless there's a
    data descriptor named x (with a __set__ method)
    
"""
class Nondata:

    def __init__(self, f):
        if type(f) == str:
            self.attr = f
        else:
            self.attr = f.__name__
        
    def __get__(self, obj, cls):
        print("in __get__", obj, cls)
        return 42
    
class Data:
    
    def __init__(self, f):
        if type(f) == str:
            self.attr = f
        else:
            self.attr = f.__name__
        
    def __set__(self, obj, value):
        print("in __set__", obj, value)
        obj.__dict__[self.attr] = value
        
    def __get__(self, obj, cls):
        print("in __get__", obj, cls)
        if self.attr in obj.__dict__:
            return obj.__dict__[self.attr]

class Creature:
    color = Data("color") # override
    age = Nondata("age")
        
class Dog(Creature):
    # color = "Green"

    def __init__(self, nm):
        self.name = nm
        self.color = "brown" # triggers __get__
        self.age = 10  # stores to self.__dict__
        
class Cat:

    def __init__(self, nm):
        self.name = nm
        
    @Data
    def color(self, color):
        pass
    
    @Nondata
    def age(self, age):
        self.age = age
        