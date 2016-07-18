# -*- coding: utf-8 -*-
"""
Created on Thu Jul  12, 2016

@author: kurner

LAB:

Create the body of add_element, delete_element
using the input() function to drive a dialog with 
the user
"""

from collections import namedtuple
import json

Element = namedtuple("Atom", "protons abbrev long_name mass")

def load_elements():
    global all_elements  # <--- will be visible to entire module
    f = open("elements_v1.json", "r")
    the_dict = json.load(f)
    f.close()
    all_elements = {}
    for symbol, data in the_dict.items():
        all_elements[symbol] = Element(*data) # "explode" data into 4 inputs
    
def save_elements():
    f = open("elements_v1.json", "w")
    json.dump(all_elements, f)
    f.close()

def add_element():
    """
    add namedtuple object from 
    all_elements dict by key
    """
    global all_elements
    new_key = input("What symbol? > ")
    if new_key in all_elements:
        print("That element is already in the database")
    else:
        protons = int(input("How many protons? > "))
        long = input("Long name? > ")
        the_mass = float(input("Mass? > "))
        all_elements[new_key] = Element(protons, new_key, long, the_mass)
        print("Element {} added".format(new_key))

def delete_element():
    """
    remove namedtuple object from 
    all_elements dict 
    by key
    """
    global all_elements
    the_key = input("What symbol? > ")
    if the_key not in all_elements:
        print("That element is not in the database")
    else:
        del all_elements[the_key]
        print("Element {} removed".format(the_key))

def print_table():
    """
    sort all_elements by number of protons, ordered_elements local only
    """
    ordered_elements = sorted(all_elements.values(), key=lambda e: e.protons)
    
    print("PERIODIC TABLE OF THE ELEMENTS")
    print("----------------------------------------------")
    print("Symbol |Long Name             |Protons |Mass")
    print("----------------------------------------------")
    
    for the_atom in ordered_elements:
        print("{:6} | {:20} | {:6} | {:5.1f}".format(the_atom.abbrev, 
                          the_atom.long_name, 
                          the_atom.protons, 
                          the_atom.mass))

if __name__ == "__main__":
    load_elements()
    print_table()



