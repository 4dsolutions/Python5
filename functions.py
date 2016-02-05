# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 20:00:44 2016

Functions in Python

@author: Kirby Urner
"""

def section(title):
    """center in a string 60 wide padded with ="""
    return "\n{:=^60}\n.".format(title)

print(section("<<<< local, nonlocal, global variables >>>>"))

# globals
STAR = "Sirius"   # Polaris
Favorites = [ ]
X = 100

def setStar(name):
    global STAR
    STAR = name
    Favorites.append(name)

print("STAR: ", STAR)
setStar("Polaris")
print("STAR: ", STAR)

def outerF():
    X = 10
    print("Inside outerF:", X)
    def innerF():
        nonlocal X  # global or nonlocal?
        print("Inside InnerF, X:", X)    # expect 10
        X = "Infinity"
        print("Inside InnerF, X:", X)
    innerF()
    return X

print("Returned from outerF: ", outerF())
print("            Global X: ", X)

print(section("<<<< Scattering and Gathering with * and ** >>>>"))

def eats(*foods): # gather positional args in a tuple 
    print("foods: ", foods)  # foods is a tuple now

print("Tuple of positional arguments to eats():")

# open-ended number of positional arguments passed in...
eats("Spaghetti", "Oysters", "Chili", "Crackers", "Rice")
    
def pretty(*names):
    for name in names:  # looping over the tuple
        print("Name: {:>20}".format(name))

print("Some US presidential candidates:")
print(pretty("Bernie Sanders", "Donald Trump", "Hillary Clinton", 
             "Ted Cruz"))
       
def example(*args, **kwargs): # gather keyword args in a dict
    """
    (* ) convert positionals --> tuple
    (**) convert keyword args --> dict
    """
    for arg in args:  # loop over the tuple
        print(arg, sep=", ", end="")
    print()
    for key, value in kwargs.items(): # ...now the dict
        print("Arg name:",key,"Value: ", value)

# positional + keyword (named) arguments
example( 1,2,3,4, on_vacation=True, at_work=False )

# same thing using "exploders" * and **
example( *(1,2,3,4), **dict(on_vacation=False, at_work=True) )

print(section("<<<< GNU Math section >>>>"))

# note:  the int( ) type *is* "base aware"
print("======= int as multi-base ========")
print("Convert from Base  2:", int("1001010",2))
print("Convert from Base 16:", int("AFF2", 16))

print("======= Top-Level Functions ========")
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

print("add_s('cat')", add_s('cat'))
print("add_ed('show')", add_ed('show'))

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


print("======= Totient / Totatives ========")
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

def totatives(N):
    # list comprehension!
    return [x for x in range(1,N) if gcd(x,N)==1]
    
def totient(N):
    """
    Returns the number of numbers between (1, N) that 
    have no factors in common with N:  called the 'totient
    of N -- called the totient of N.
    """
    return len(totatives(N))

print("Totient of  100:", totient(100))
print("Totient of 1000:", totient(1000))






