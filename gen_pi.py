# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 16:08:49 2015

@author: kurner

Another generator example:  converging to Pi

https://mail.python.org/pipermail/edu-sig/2015-September/date.html

"""

def pi():

    k, a, b, a1, b1 = 2, 4, 1, 12, 4
    while True:
        p, q, k = k*k, 2*k+1, k+1
        a, b, a1, b1 = a1, b1, p*a+q*a1, p*b+q*b1
        d, d1 = a/b, a1/b1
        while d == d1:
            yield int(d)
            a, a1 = 10*(a%b), 10*(a1%b1)
            d, d1 = a/b, a1/b1

if __name__ == "__main__":                    
    the_gen = pi()
    for _ in range(20000):
        print(next(the_gen),end="")
    print()

  
  
 
