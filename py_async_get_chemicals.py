# -*- coding: utf-8 -*-
"""
Created on Mon June 12 2017
@author: Kirby Urner

Hits against thekirbster.pythonanywhere.com to get json
strings for chemical elements.  Demonstrates using asyncio
"""

import aiohttp
import asyncio

from collections import namedtuple
import json

Element = namedtuple("Element", "title url")
Atom = namedtuple("Atom", "protons symbol name mass category edited initials")

elements = []
elements.append(
	Element("Hydrogen", 
			"http://thekirbster.pythonanywhere.com/api/elements?elem=H")
	)

elements.append(
	Element("Oxygen", 
			"http://thekirbster.pythonanywhere.com/api/elements?elem=O")
	)

elements.append(
	Element("Oxygen", 
			"http://thekirbster.pythonanywhere.com/api/elements?elem=Au")
	)

elements.append(
	Element("Oxygen", 
			"http://thekirbster.pythonanywhere.com/api/elements?elem=S")
	)

elements.append(
	Element("Oxygen", 
			"http://thekirbster.pythonanywhere.com/api/elements?elem=Pb")
	)

elements.append(
	Element("Oxygen", 
			"http://thekirbster.pythonanywhere.com/api/elements?elem=Hg")
	)

elements.append(
	Element("Oxygen", 
			"http://thekirbster.pythonanywhere.com/api/elements?elem=O")
	)
async def get_element(elem):
	print(elem.url)
	response = await aiohttp.request('GET', url=elem.url)
	print("Waiting")
	return (await response.text())

ioloop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(get_element(elem), loop=ioloop)
			for elem in elements]

the_work = asyncio.gather(*tasks, loop=ioloop)
ioloop.run_until_complete(the_work)

print("Done!")

results = the_work.result()
atoms = []
for result in results:
	data = json.loads(result)
	atoms.append(Atom(*data))

for atom in atoms:
	print(atom)
