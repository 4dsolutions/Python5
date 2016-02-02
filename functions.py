# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:00:44 2016

SESSION 04:  PDX CODE GUILD
Accelerated Programming with Python

RECAP:

Students comfortable with the content so far, with or
without laptops, were permitted to stay with my 
accelerated curriculum, however those wishing more 
of a clinic and recap of the basics were admitted 
to a separate more remedial section.

This edition of Intro to Programming @ <guild />
did not include the usual Labs and no homework was 
expected, so a Course + Clinic design became 
necessary to make up for the accelerated schedule.  

Some students already had some prior knowledge of 
programming, just maybe not in Python in particular.

Those who stayed with the accelerated version learned
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

* functions passed to other functions
* function that return functions
* preview of how def F(*args, **kwargs) allows any
  number of positional and keyword (named) arguments 
  to be passed to a function F.

@author: Kirby Urner
"""

def eat(food):
    print("I love", food)

def eats(*foods): # gather positional args in a tuple 
    print(foods)  # foods is a tuple now

print("Tuple of positional arguments to eats:")
print(eats("Spaghetti", "Oysters", "Chili", "Crackers", "Rice"))
    
def pretty(*names):
    print(names)        # show me the tuple
    for name in names:  # looping over the tuple
        print("Name: {:^20}".format(name))

print("Some US presidential candidates:")
print(pretty("Bernie Sanders", "Donald Trump", "Hillary Clinton", 
             "Ted Cruz"))
        
def example(*args, **kwargs): # gather keyword args in a dict
    print(args)   # tuple
    print(kwargs) # dict
    for arg in args:  # loop over the tuple
        print(arg)  
    for key, value in kwargs.items(): # ...now the dict
        print("Arg name:",key,"Value: ", value)

print("Adding a dict-parameter")

# positional + keyword (named) arguments
print(example(1,2,3,4, on_vacation=True, at_work=False ))

#=== functions that return and/or eat functions...
        
def addLetter(letters): # <-- pass in a string
    """
    A function factory that builds and returns 
    function objects.  L is a function that will
    add whatever letters are passed in to be the
    ending letters.
    """
    def L(s):
        return s + letters # <--- concatenation!
    return L
    
add_s  = addLetter("s")
add_ed = addLetter("ed")
print("addS('cat')", addS('cat'))
print("addD('show')", addD('show'))


def compose(g, f):
    """Take two functions as inputs and return a
    function that's their composition"""
    def newfunc(x):
        return g(f(x))
    return newfunc

# input function
def G(n):
    return n + 2

# input function
def F(n):
    return n * 2

# compare:
H = compose(G, F) # build a 3rd function from 1 & 2
print("G(F(x)):", H(100))  # G(F(x))

# ... now with 
H = compose(F, G)
print("F(G(x)):", H(100))  # F(G(x))

# ====== GNU Math section ========
#
# (a pun on New Math ala Tom Lehrer Youtube
# see: make_links_v2.py)

def gcd(a, b):
    """
    Euclid's Method for finding the GCD
    """
    while b:  # <--- while loop!
        a, b = b, a%b
    return a
    
def totient(N):
    """
    Returns the number of numbers between (1, N) that 
    have no factors in common with N:  called the 'totient
    of N -- called the totient of N.
    """
    # list comprehension!
    return len([x for x in range(1,N) if gcd(x,N)==1])

# note:  the int( ) type *is* "base aware"
print("Convert from Base  2:", int("1001010",2))
print("Convert from Base 16:", int("AFF2", 16))




