# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 19:13:03 2016

@author: kurner
"""

def simple_gen():  
    yield "white"
    yield "yellow" #<---
    yield "green"
    yield "orange"
    yield "purple"
    yield "blue"
    yield "brown"
    yield "red"
    yield "black"
    
def driver():
    g = simple_gen()
    for color in g:
        print(color)

def fibs(a=0, b=1, max=10000):
    while True:
        if a > max:
            return a
        yield a
        newb = a + b
        a = b
        b = newb

def test_fibs():
    f = fibs()
    while True:
        try:
            next(f)
        except StopIteration as ev:
            return ev.value
    
class Fibs:
    """
    Another way to write an iterator
    """ 
    def __init__(self, a=0, b=1, max=10000):
        self.a = a
        self.b = b
        self.max = max
        
    def __next__(self):  # <-- needed for iterators
        answer = self.a
        newb = self.a + self.b
        self.a = self.b
        self.b = newb
        if answer > self.max:
            raise StopIteration(answer)
        return answer
        
    def __iter__(self):  # <-- needed for iterators
        return self
        

def test_Fibs():
    f = Fibs()
    while True:
        try:
            next(f)
        except StopIteration as ev:
            return ev.value