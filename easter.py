# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 11:03:05 2016

Generates Easter dates:
Sun 04-23-2000
Sun 04-15-2001
Sun 03-31-2002
Sun 04-20-2003
Sun 04-11-2004
Sun 03-27-2005
Sun 04-16-2006
Sun 04-08-2007
Sun 03-23-2008
Sun 04-12-2009
Sun 04-04-2010
Sun 04-24-2011
Sun 04-08-2012
Sun 03-31-2013
Sun 04-20-2014
Sun 04-05-2015
Sun 03-27-2016
Sun 04-16-2017
Sun 04-01-2018
Sun 04-21-2019
Sun 04-12-2020

Using:
http://aa.usno.navy.mil/faq/docs/easter.php

@author: kurner
"""
import datetime

def from_year(y):
    """Please note the following: This is an integer calculation. 
    All variables are integers and all remainders from division 
    are dropped. For example, 7 divided by 3 is equal to 2 in 
    integer arithmetic.
    """
    c = y // 100
    n = y - 19 * ( y // 19 )
    k = ( c - 17 ) // 25
    i = c - c // 4 - ( c - k ) // 3 + 19 * n + 15
    i = i - 30 * ( i // 30 )
    i = i - ( i // 28 ) * ( 1 - ( i // 28 ) * ( 29 // ( i + 1 ) )
        * ( ( 21 - n ) // 11 ) )
    j = y + y // 4 + i + 2 - c + c // 4
    j = j - 7 * ( j // 7 )
    l = i - j
    m = 3 + ( l + 40 ) // 44
    d = l + 28 - 31 * ( m // 4 )
    return datetime.datetime(y, m, d)

for yr in [2000 + x for x in range(21)]:
    easter = from_year(yr)
    print(easter.strftime("%a %m-%d-%Y"))