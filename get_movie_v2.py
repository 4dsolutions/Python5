# -*- coding: utf-8 -*-
"""
Created on Mon Jul 14 2016

@author: Kirby Urner

Uses API documented at http://www.omdbapi.com/ to query
IMDB movie database.

Uses pickle to store Movie instance
https://docs.python.org/3.5/library/pickle.html

LAB 3:  __str__ has full access to self.content, a dict.
Why not make it even cooler?

If you don't have requests, there's a picked movie instance
to play with.
"""

import requests
# from collections import namedtuple
import json
import pickle

# Movie = namedtuple("Movie", "status_code content")

class Movie:
    
    def __init__(self, status_code, json_data):
        self.status = status_code
        self.content = json.loads(str(json_data, encoding="UTF-8"))
        
    def __str__(self):
        """
        Good place to practice string formatting by adding 
        more data to the output
        """
        obj = self.content  # decoded json, a dict
        the_title = "Title:\n {:^40}\n{:^40}\n".format(obj["Title"], obj["Released"])
        the_actors = "Actors: \n"
        for actor in obj["Actors"].split(","):
            the_actors += ".....{:>30}\n".format(actor) 
        the_story = ("Story: \n")
        the_story += obj["Plot"]+"\n"
        the_awards = "Awards: \n"
        the_awards += obj["Awards"]+"\n"
        return the_title + the_actors + the_story + the_awards
        
    def __repr__(self):
        return "Movie(Title={}, Released={})".format(self.content["Title"], 
                                                self.content["Released"])
        
def get_movie(url):
    r = requests.get(url)
    return Movie(r.status_code, r.content)
    
def test_request_1(imdb_title):
    the_url = "http://www.omdbapi.com/?i={}&plot=full&r=json".format(imdb_title) # GET
    result = get_movie(the_url)  # Movie object
    return result

def test_request_2(name, year):    
    print("-----------")
    the_url = "http://www.omdbapi.com/?t={}&y={}&plot=full&r=json".format(name, year)
    result = get_movie(the_url) # Movie object
    return result

def pickle_it(the_movie):
    with open('movie.pickle', 'wb') as f:  # context manager style 
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(the_movie, f, pickle.HIGHEST_PROTOCOL)
    
def unpickle_it():
    with open('movie.pickle', 'rb') as f:
        # The protocol version used is detected automatically, so we do not
        # have to specify it.
        the_movie = pickle.load(f)
    return the_movie

if __name__ == "__main__":  # means just importing will not trigger this block
    # movie = test_request_2("Titanic", "1997")
    movie = test_request_1("tt0120338")
    print(movie)
    # titanic =  unpickle_it()
    