# -*- coding: utf-8 -*-
"""
Created on Sat Feb 11 16:55:10 2017

@author: Kirby Urner

Grayham Forscutt constructs phrases that file
by letter sum. Examples below.  Sometimes add
or subtract 'the' for plus/minus 33.

intelligent infinity + the = 266
focus on visualising the angelic fleet habitation - the = 466
"""

from string import ascii_lowercase

# expecting 433
phrases = \
"""\
the light entities of the higher evolution
hyperspace metropolis design blueprint
the collective vehicle generated from thought
focus on visualising the angelic fleet habitation
mentally construct the triacontahedron
collectively visualize a triacontahedron
create one hundred and forty four lightbodies
spun all hundred and forty four triaconta
become fully realized integrated ascended master
stationed inside the rhombic triacontahedron
the intergeometrical approach of the chakra vajra
liquid crystal thought structures
principle resonant phase conjugate cavity
volumes inside the rhombic triacontahedron\
""".split("\n")

# this overwrites the above -- just paste in phrases
# expecting 266
phrases = """\
quantized fractal volume
pre cosmic unified fractal field
disdyakis triacontahedron
the rhombic triacontahedron
modelling consciousness
universal language of light
this is template reality
the original divine matrix
intelligent infinity
fractal dynamics of phi ratio
prepare for first contact
oneness consciousness
full access to the higher self
compound quasicrystal
supersymmetric plasma
basic building block of reality
the underlying unified field
superluminal scalar waves
golden ratio symmetries
the collective oversoul
packing rhombic triacontahedra
triacontahedral clusters
plasma cavitation membranes
protective plasma membrane
programming the lightbody
phase conjugate mirroring
survived compression
collapsing quantum wave
implosive compression\
""".split("\n")

def sumphrase(s):
    # a=1, b=2... skips non-ascii characters
    return sum([ord(c)-96 for c in s if c in ascii_lowercase])
    
for p in phrases:
    print(sumphrase(p), p)

        
    
    