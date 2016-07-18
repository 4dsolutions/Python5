# -*- coding: utf-8 -*-
"""
Created on Mon Jul 11 2016

@author: Kirby Urner

Uses API documented at http://www.omdbapi.com/ to query
IMDB movie database.
"""

import requests
# from collections import namedtuple
import json

# Movie = namedtuple("Movie", "status_code content")

class Movie:
    
    def __init__(self, status_code, json_data):
        self.status = status_code
        self.content = json.loads(str(json_data, encoding="UTF-8"))
        
    def __str__(self):
        obj = self.content  # decoded json, a dict
        the_title = "Title: {:^40}\n".format(obj["Title"])
        the_actors = "Actors: \n"
        for actor in obj["Actors"].split(","):
            the_actors += ".....{:>30}\n".format(actor) 
        the_story = ("Story: \n")
        the_story += obj["Plot"]
        return the_title + the_actors + the_story
        
    def __repr__(self):
        return "Movie(Title={}, Released={})".format(self.content["Title"], 
                                                self.content["Released"])
        
def get_movie(url):
    r = requests.get(url)
    return Movie(r.status_code, r.content)
    
# test
    
the_url = "http://www.omdbapi.com/?i=tt0120338&plot=full&r=json" # GET
result = get_movie(the_url)
print(result.content)

print("-----------")
the_url = "http://www.omdbapi.com/?t=Titanic&y=1997&plot=full&r=json"
result = get_movie(the_url)
print(result)

