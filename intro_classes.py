# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 18:28:39 2016

@author: Kirby Urner

Intro to classes
with thanks to PDX Code Guild, Instructor:  Tiffany
"""

from random import choice

class Smell:
    pass

class Mammal:
    
    def __init__(self):
        self.stomach = [ ]
        
    def eat(self, food):
        self.stomach.append(food)
        
class Dog(Mammal):
    
    def __init__(self, name, breed):
        super().__init__()
        self.name = name
        self.breed = breed
        
    def bark(self, how_many):  # expect int
        return "Bark! " * how_many
        
    def sniff(self, the_smell):
        if the_smell.food_smell:
            return "Whine!"
        
class Die:  # as in dice
    """model a die of n sides"""
    
    def __init__(self, sides = None):
        if not sides:
            self.sides = list(map(str, range(1,7)))
        else:
            self.sides = sides
        self.current_value = self.sides[0]
        
    def roll(self):
        """pick a side, any side..."""
        self.current_value = choice(self.sides)
        return self.current_value
        
    def __repr__(self):
        return "Die with value {}".format(self.current_value)

if __name__ == "__main__":    
    
    # Dog section
    puppy = Dog("Snoopy", "Beagle")
    print(puppy.bark(3))
    puppy.eat("steak!")
    print("Inside puppy:", puppy.stomach)
    yummy = Smell()
    yummy.food_smell = True
    print(puppy.sniff(yummy))
    
    # Die section
    it, it1, it2, it3 = Die(), Die(), Die(), Die()
    print((it2.roll(), it3.roll()))
    print(it.roll())
    print(it.roll())
    print(it.roll())
    print(it.roll())
    print(it)
    print("it:", it.__dict__)
    print("it2:", it2.__dict__)

