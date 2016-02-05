# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:00:44 2016

SESSION 04:  PDX CODE GUILD

RECAP:

Students comfortable with the content so far, with or
without laptops, were permitted to stay with my 
curriculum, however those wishing more of a clinic 
and recap of the basics were admitted to a separate
more remedial section.

This edition of Intro to Programming @ <guild />
did not include the usual Labs and no homework was 
expected, so a Course + Clinic design became 
necessary.  Some students already had advanced 
knowledge of programming, just not of Python in
particular.

Those who stayed with the non-clinic version learned
about namedtuples as a bridge from the tuple to class
construct i.e. tuples are allowed to have attributes
by means of this collection.namedtuple subclass.

We also learned about how str.format will take names
corresponding to named arguments i.e.:

"He lives in {city}, {state}".format(city="Portland,
state="OR")

We looked at madlibs_v2.py as an example of this 
pattern.

Finally, we took a deeper look at functions, including:
* functions passed to other function
* function the return functions
* preview of how def F(*args, **kwargs) allows any
number of positional and keyword (named) arguments 
to be passed to a function F.

@author: Kirby Urner
"""

def eat(food):
    print("I love", food)

def eats(*foods):
    print(foods)
    
def pretty(*names):
    print(names)
    for name in names:
        print("Name: {:^20}".format(name))
        
def example(*args, **kwargs):
    print(args)
    print(kwargs)
    for arg in args:
        print(arg)
    for key, value in kwargs.items():
        print("Arg name:",key,"Value: ", value)
        
def addLetter(letter):
    def L(s):
        return s + letter
    return L

def L(s):
    return s + "D"

def compose(g, f):
    def newfunc(x):
        return g(f(x))
    return newfunc

def G(n):
    return n + 2

def F(n):
    return n * 2

def gcd(a, b):
    while b:
        a, b = b, a%b
    return a
    
def totient(N):
    return len([x for x in range(1,N) if gcd(x,N)==1])
    
    





