# -*- coding: utf-8 -*-
"""
Created on Tue Feb  9 09:41:11 2016

@author: Kirby Urner

Minimalist Flask application to record mouse
clicks on a chess board.  Asks server what's
in a cell using GET requests.  No capability
to move a piece using POST yet implemented.

The game board is sensitized to mouse clicks
in each square (JavaScript showCell function)
and, when in server mode, chessgame.html turns 
a click into a GET request asking the server 
what piece is there.  

Client-side JavaScript has no independent 
record of the board and piece positions in 
this version.

"""

import flask as f
from flask import Flask, current_app, redirect, request
from chessgame import Game

app = Flask(__name__)

@app.route("/")
def index():
    global game
    game = Game(server=current_app.name + ", a Flask application")
    board = game.board
    print("Sending Board")
    return str(board)

@app.route("/cell", methods=['GET'])
def get_cell():
    if request.method == "GET":
        r = int(request.args.get('r'))
        c = int(request.args.get('c'))
        the_piece = game.board._check_for_piece(r, c)
        if the_piece == False:
            the_color = "no piece"
            the_type = "in that location."
        else:
            the_color = the_piece.color
            the_type = the_piece.type
    return "{} {}".format(the_color, the_type)
    
@app.route("/deepblue")
def some_handler():
    return redirect('http://www-03.ibm.com/ibm/history/ibm100/us/en/icons/deepblue/')

@app.route("/theturk")
def other_handler():
    return redirect('http://www.slate.com/blogs/atlas_obscura/2015/08/20/the_turk_an_supposed_chess_playing_robot_was_a_hoax_that_started_an_early.html')

if __name__ == '__main__':
    app.run(debug=True)
    