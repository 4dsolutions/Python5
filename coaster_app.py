# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 16:05:10 2017

@author: kurner
"""

from make_coasters_db import DB
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/coasters")
def coasters():
    return all_coasters()

@app.route("/coasters/<coaster>")
def coaster(coaster):
    return one_coaster(coaster)
    
def all_coasters():
    with DB() as db:
        query = ("SELECT name, park, yr_opened FROM Coasters "
                 "ORDER BY name")
        db.get_coasters(query)
        results = []
        for rec in db.cursor.fetchall():
            results.append(rec)
    body =  "<ul>"+ \
            "\n".join(["<li>{}, {}, {}</li>".format(*data) for data in results]) + \
            "</ul>"
    return basic_html("All Coasters", body)

def one_coaster(coaster):
    with DB() as db:
        if coaster:
            query = ("SELECT * FROM Coasters "
                     "WHERE name = '{}'".format(coaster))           
        db.get_coasters(query)
        results = []
        for rec in db.cursor.fetchall():
            results.append(rec)
    fields =("Name:  {} <br /> ",
           "Park:  {} <br /> ",
           "State: {} <br /> ",
           "Country: {} <br /> ",
           "Duration: {} <br /> ", 
           "Speed: {} <br />",
           "Height: {} <br />",
           "VertDrop: {} <br />", 
           "Length: {} <br />",
           "Yr_Opened: {} <br />",
           "Inversions: {} <br />")
    body = ("\n".join(fields))
    body = body.format(*results[0])
    return basic_html(coaster, body)
    
def basic_html(title="Web Page", body="content goes here"):
    page = ("<!doctype html>\n"
            "<html>\n"
            "<head>\n"
            "<title>{}</title>\n"
            "</head>\n"
            "<body>\n"
            "{}\n"
            "</body>\n"
            "</html>").format(title, body)
    return page
        
if __name__ == "__main__":
    app.run()
    