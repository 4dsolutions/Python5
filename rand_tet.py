#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  4 09:56:18 2020

@author: mac
"""

import tetravolume as tv
from itertools import permutations
from qrays import Qvector
from random import choice
from gmpy2 import mpfr, get_context

ccp_spokes = [Qvector(p) for p in set(permutations((0,1,1,2)))]

get_context().precision=1000
zero = mpfr('0.0')

def rand_vert():
    vert = Qvector((zero, zero, zero, zero))
    for _ in range(1000):
        vert += choice(ccp_spokes)
    return vert

# vertexes
A = rand_vert()
B = rand_vert()
C = rand_vert()
D = rand_vert()

#edges
a = (A-B).length()
b = (A-C).length()
c = (A-D).length()
d = (B-C).length()
e = (C-D).length()
f = (D-B).length()

lengths = (a,b,c,d,e,f)
# print(lengths)

tet = tv.Tetrahedron(*lengths)
vol = tet.ivm_volume()
print(vol)
