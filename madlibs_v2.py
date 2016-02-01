#!/usr/env python3.4
"""
Madlibs provide exercise in 'string substitution' wherein
we have a Template text (something with blanks in it, like
a Form to fill out), and then the information to complete
it.  There is not just one way to do it.

Real use case:  generate scene description language
for povray (povray.org) by filling in various templates
with computed values.  Good for rendering perspective
stills called "ray tracings" (see povray.org gallery
for examples).

Demonstrate one of those ways:  use str.format( )

"""

# Example using .format()

# (pretending to be a limerick or haiku or something)

silly_story = """There once was a boy from {any_town} who
loved to eat lots of {junk_food}.  He ate so many
{junk_food} that one day (the people of {any_town}
claim) he actually turned into a {something}."""  # note repeating keys

# now lets get user input:
the_data = {} # empty dict (curly braces -- not a set)
print("I need to ask you for three things...")

for key in ["junk_food", "any_town", "something"]:  # strings we need
    usr = input("Please give me a value for [" + key + "]: ")
    # usr input could have issues so 'guard code' might go here
    # lets just hope it all makes sense for now...
    the_data[key] = usr  # store answer as value to the key

print("Thank you for your time") # be polite

# pass in keyward / named arguments
filled_in = silly_story.format( any_town  = the_data["any_town"],
                                junk_food = the_data["junk_food"],
                                something = the_data['something'])

print("OK, here is your silly story of the day: \n") # <-- add a newline
print("{:^20}".format("silly story".title()))  # center within 20 spaces
print(filled_in)

# However there's an easier way to get all those keyed arguments
# from the_data:  explode it with **the_data

# pass in keyward / named arguments
# dict keys need to match the place holder names in this pattern
# you'll get a KeyError if any place holder name goes unmatched.

filled_in = silly_story.format(**the_data)    # turns dict into named args

# in general, dicts may be exploded into keyword arguments (useful!)

print("\n\n... and here it is a second time: \n") # <-- adding newlines
print("{:^20}".format("silly story".title())) # center within 20 spaces
print(filled_in)

# Now please try something similar, where you solicit input from
# the user in a loop and use that input to fill in some template
# or form.  It might be a passport application or formal document.
