# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 16:08:49 2015

@author: kurner

Another generator example:  converging to Phi

Shows eval( ) in action

"""

def continued():
    
    patt = "+ 1/(1"
    the_expr = ''  # empty
    n = 1
    
    while True:
        the_expr = the_expr + patt
        the_frac = "1 " + the_expr + ")" * n
        
        yield eval(the_frac)  # or show the_frac
        
        n += 1
                
the_gen = continued()
for _ in range(20):
    print(next(the_gen))  # <-- is a callable
  
  
 
