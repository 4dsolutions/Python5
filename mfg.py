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

from flask import Flask, current_app, redirect, request
from chessgame import Game
import json

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
    global game
    if request.method == "GET":
        r = int(request.args.get('r'))
        c = int(request.args.get('c'))
        the_piece = game.board._check_for_piece(r, c)
        if not the_piece:
            the_color = "no piece"
            the_type = "in that location."
            game.selected = None
            data_dict = dict(response_text="{} {}".format(the_color, the_type), 
                         legal_moves = ['r3c2','r3c3'], has_piece=False,
                         unicode = "")
        else:
            the_color = the_piece.color
            the_type = the_piece.type
            game.selected = the_piece
            print("Selected:", game.selected)
            the_symbol = the_piece.unicode
            the_pos = the_piece.position
            data_dict = dict(response_text="{} {}".format(the_color, the_type), 
                         legal_moves = game.legal(the_piece), unicode=the_symbol,
                         has_piece=True, position = the_pos)
    return json.dumps(data_dict)

@app.route("/move", methods=['PUT'])
def move_piece():
    global game
    r = int(request.args.get('r'))
    c = int(request.args.get('c'))
    new_position = [r,c]
    the_piece = game.selected
    old_position = the_piece.position.copy()    
    game.board.grid[old_position[0]][old_position[1]] = None  
    the_color = the_piece.color
    the_type = the_piece.type
    the_symbol = the_piece.unicode
    the_piece.position[0] = r
    the_piece.position[1] = c
    game.board.grid[r][c] = the_piece 
    data_dict = dict(response_text="Moved: {} {} from {} to {}".format(
                     the_color, the_type, old_position, new_position), 
                     legal_moves = [], has_piece=False, unicode=the_symbol,
                     position = new_position)
    return json.dumps(data_dict)
    
@app.route("/deepblue")
def some_handler():
    return redirect('http://www-03.ibm.com/ibm/history/ibm100/us/en/icons/deepblue/')

@app.route("/theturk")
def other_handler():
    return redirect('http://www.slate.com/blogs/atlas_obscura/2015/08/20/the_turk_an_supposed_chess_playing_robot_was_a_hoax_that_started_an_early.html')

if __name__ == '__main__':
    app.run(debug=True)
    