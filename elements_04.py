# -*- coding: utf-8 -*-
"""
Created on Thu Jul  12, 2016

@author: kurner

LAB:

"""

# from collections import namedtuple <--- using Element instead
import json

class Element:
    
    def __init__(self, protons, abbrev, long_name, mass, series=''):
        """
        An Element is born!
        """
        self.protons = protons
        self.abbrev = abbrev
        self.long_name = long_name
        self.mass = mass
        self.series = series
        
    def __getitem__(self, idx):
        """
        Allow subscripting just like a namedtuple would
        """
        if idx == 0:
            return self.protons
        elif idx == 1:
            return self.abbrev
        elif idx == 2:
            return self.long_name
        elif idx == 3:
            return self.mass
        elif idx == 4:
            return self.series
        else:
            raise IndexError

    def __repr__(self):
        fmt = "Atom(protons={protons}, abbrev={abbrev}, " + \
        "long_name={long_name}, mass={mass}, series={series})"
        return fmt.format(**self.__dict__)

Atom = Element  # create a synonym (to names for same thing)

class ElementEncoder(json.JSONEncoder):
    """
    See:  https://docs.python.org/3.5/library/json.html
    """
    def default(self, obj):
        if isinstance(obj, Element):  # how to encode an Element
            return [obj.protons, obj.abbrev, obj.long_name, obj.mass, obj.series]
        return json.JSONEncoder.default(self, obj) # just do your usual
            
# Element = namedtuple("Atom", "protons abbrev long_name mass")

def load_elements():
    global all_elements  # <--- will be visible to entire module
    f = open("elements_v2.json", "r")
    the_dict = json.load(f)
    f.close()
    all_elements = {}
    for symbol, data in the_dict.items():
        all_elements[symbol] = Atom(*data) # "explode" data into 4 inputs
    
def save_elements():
    f = open("elements_v2.json", "w")
    json.dump(all_elements, f, cls=ElementEncoder) # extended encoder
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
        the_series = input("Series? > ")
        all_elements[new_key] = Element(protons, new_key, long, the_mass, the_series)
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
    sort all_elements by number of protons, 
    ordered_elements local only series?
    """
    ordered_elements = sorted(all_elements.values(), key = lambda k: k.protons)
    
    print("PERIODIC TABLE OF THE ELEMENTS")
    print("--------------------------------------------------------")
    print("Symbol |Long Name             |Protons |Mass   |Series")
    print("--------------------------------------------------------")
    
    for the_atom in ordered_elements:
        print("{:6} | {:20} | {:6} | {:5.1f} | {:20}".format(the_atom.abbrev, 
                          the_atom.long_name, 
                          the_atom.protons, 
                          the_atom.mass,
                          the_atom.series))

if __name__ == "__main__":
    load_elements()
    print_table()
