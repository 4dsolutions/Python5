# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 21:15:06 2016

@author: kurner

Keywords Quiz
Can you think of them all?

An idea I picked up at a Python User Group...

"""

import keyword
all_kw = keyword.kwlist[:] # make a copy
found = [ ]

while len(all_kw) > 0:
    print("{} keywords left to guess".format(len(all_kw)))
    guess = input("What is your guess? (q to quit): ")
    if guess == 'q':
        print("You gave up!")
        print("Unguessed: ", all_kw)
        print("Guessed: ", found)
        break
    if guess in all_kw:
        print("Yes, that's one of them")
        all_kw.remove(guess)
        found.append(guess)
    elif guess in found:
        print("You got that one already")
        print("Found:", found)
    else:
        print("{} is not a keyword in Python.".format(guess))
else:
    print("Congratulations; you got them all!")


