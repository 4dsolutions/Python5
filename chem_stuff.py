# -*- coding: utf-8 -*-
"""
Created on Tue Jul  19, 2016

@author: kurner

LAB:

"""
import json

series_types = ["Don't Know", "Other nonmetal", "Alkali metal", 
                "Alkaline earth metal", "Nobel gas", "Metalloid", 
                "Halogen", "Transition metal", "Post-transition metal", 
                "Lanthanoid", "Actinoid"]
                
class Element:
    fields = ["protons", "symbol ", "long_name", "mass", "series"]
    repstr = ("Atom(protons={protons}, symbol='{symbol}', "
    "long_name='{long_name}', "
    "mass={mass}, series='{series}')")
   
    def __init__(self, protons: int, symbol: str,
                 long_name: str, mass: float, series: str):

        # build self.__dict__       
        self.protons = protons
        self.symbol = symbol
        self.long_name = long_name
        self.__dict__['mass'] = mass # same idea
        self.series = series
    
    def __getitem__(self, idx):  # simulates collection.namedtuple behavior
        return self.__dict__[self.fields[idx]]
       
    def __repr__(self):
        return self.repstr.format(**self.__dict__)

Atom = Element # synonyms

class ElementEncoder(json.JSONEncoder):
    """
    See:  https://docs.python.org/3.5/library/json.html
    """
    def default(self, obj):
        if isinstance(obj, Element):  # how to encode an Element
            return [obj.protons, obj.symbol, obj.long_name, obj.mass, obj.series]
        return json.JSONEncoder.default(self, obj) # just do your usual
            
def load_elements(the_file):
    global all_elements  # <--- visible to entire module
    try:
        f = open(the_file, "r") # <--- open the_file instead
    except IOError:
        print("Sorry, no such file!")
    else:
        the_dict = json.load(f)
        f.close()
        all_elements = {}
        for symbol, data in the_dict.items():
            all_elements[symbol] = Atom(*data) # "explode" data into 5 inputs
        print("File:", the_file, 'loaded.')
 
def print_periodic_table(sortby=1):
    """
    sort all_elements by number of protons, ordered_elements local only
    What about series?
    Sort Order:
    1. protons
    2. symbol
    3. series
    """
    print("Selected:", sortby)
    
    if sortby == 1:
        ordered_elements = sorted(all_elements.values(), key = lambda k: k.protons)
    elif sortby == 2:
        ordered_elements = sorted(all_elements.values(), key = lambda k: k.symbol)        
    elif sortby == 3:
        ordered_elements = sorted(all_elements.values(), key = lambda k: k.series)
        
    print("PERIODIC TABLE OF THE ELEMENTS")
    print("-" * 70)
    print("Symbol |Long Name             |Protons |Mass   |Series  " )
    print("-" * 70)
   
    for the_atom in ordered_elements:
        print("{:6} | {:20} | {:6} | {:5.2f} | {:15}".format(the_atom.symbol,
                          the_atom.long_name,
                          the_atom.protons,
                          the_atom.mass,
                          the_atom.series))

if __name__ == "__main__":
    load_elements("periodic_table.json")  # actually do it
    print_periodic_table(3)  # do it for real