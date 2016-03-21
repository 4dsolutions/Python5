# -*- coding: utf-8 -*-
"""
Created on Thu Feb  6 2016

@author: Kirby Urner

Ideas for facilitating chess on a web page.  

In manual mode (no server), the Game.play_game method alternately prompts 
black and white to move.  Players enter start and end positions in row 
column format (rows and columns numbered 0-7).  Keeps track of captured 
pieces.  Makes no attempt to validate the legality of moves.

In server mode, the board with all pieces in starting positions is 
displayed and clicking in each square checks with the server for 
what it contains.  play_game is not implemented in the server version.
The goal was to get as far as having AJAXy GET lookups of the board
on the server, demonstrating 2-way communication without page reloading.

Could be enhanced to:

* provide a server mode that allows actual moves
* persist moves-per-game in a sqlite3 DB or other database for playback
* prevent illegal moves by computing squares legally within range of any piece
* implement more rules e.g. pawn promotion, castle, en passant

"""

from collections import namedtuple

Piece = namedtuple('Piece', 'type color position unicode')
Move  = namedtuple('Move',  'Piece start end')

# basic skeleton for HTML.  Because setup to use placeholders for 
# str.format(), any literal curly braces need to be doubled.
page_template = ("""\
<!DOCTYPE html>
<html>
<head> 
<style>table, th, td {{border: 1px solid black;}}
td {{font-size: 30px;}}
td.square {{overflow:hidden; width:40px; height:40px;}}
</style>
<title>Chess Game</title> 
</head>
<body onload = "detectServer()">
<div align='center'>Piece selected:<br />
<span id='from_server'>None Selected</span></div>
<br />
<div align='center'>{0}</div>
<br />
<div align="center" id="server_status">{1}</div>

<script type="text/javascript">

this.prevCellId = nil;
this.prevLegalMoves = nil;
 

// runs when the body loads.Server's sig == tip-off running in server mode
this.live_server = false;   // only set to true if Flask left a message.

function detectServer() {{ 
   server_says = document.getElementById("server_status").innerHTML;
   if (server_says.indexOf("Flask") != -1){{
       this.live_server = true;

   }}
}}

// If in server mode, talk with server to find out what if any chess
// piece is in the current location or if selected cell is already green.  
// XMLHttpRequest object used for this.

// if cell not already green, turns a clicked-on cell red while 
// returning the last clicked cell to its original color based 
// on a row-column computation (same used to get original coloring)
// previous greens returned to board coloring.  Says what piece was
// clicked on if any due to a GET ?cell request.

// turns on legal next positions if piece select and not already moving

// if clicking on green square, then moving, so move piece with PUT ?move 
// requiest, and then turn off all red or green coloring, showing no 
// piece is selected, with board updated


function showCell(theCell) {{
    oldcolor = theCell.bgColor;
    moving = false;
    if (oldcolor == "00E800") {{
        moving = true;
    }}
    found = Boolean(this.prevCellId);
    // alert("prev id: " + this.prevCellId + " " + String(found));
    if (found) {{
        oldCell = document.getElementById(this.prevCellId);
        // extract row,column of old cell and set bgcolor to dark or light
        row    = Number(prevCellId.charAt(1));
        column = Number(prevCellId.charAt(3));
        oldCell.bgColor = (row + column)%2==0 ? ('#ffffff') : ('#a9a9a9');   
    }}  
    theCell.bgColor = "E80000";
    this.prevCellId = theCell.id;
    // alert("old cell_id " + this.prevCellId);
    if (this.live_server) {{
        // AJAXy stuff here
       xhttp = new this.XMLHttpRequest();
       xhttp.onreadystatechange = function() {{
           // alert("readyState: " + xhttp.readyState);
           if (xhttp.readyState == 4 && xhttp.status == 200) {{
               data_dict = JSON.parse(xhttp.responseText);
               display_text = data_dict['response_text'];
               legal_moves  = data_dict['legal_moves'];
               piece_symbol = data_dict['unicode'];
               piece_pos = data_dict['position'];
               got_piece = data_dict['has_piece'];
               document.getElementById("from_server").innerHTML = display_text;
               if ((!moving)  && got_piece) {{
                  for (r = 0; r <= 7; ++r) {{
                       for (c = 0; c <= 7; ++c ) {{
                           the_id = "r" + String(r) + "c" + String(c);
                           theCell = document.getElementById(the_id);
                           if (theCell.bgColor == "00E800") {{
                               theCell.bgColor = (r + c)%2==0 ? ('#ffffff') : ('#a9a9a9'); 
                           }}
                       }}
                   }} 
                   for (cell_id of legal_moves) {{
                       the_cell = document.getElementById(cell_id);
                       the_cell.bgColor = "00E800";
                   }}
               }} 
               if ((!moving) && !got_piece){{
                   for (r = 0; r <= 7; ++r) {{
                       for (c = 0; c <= 7; ++c ) {{
                           the_id = "r" + String(r) + "c" + String(c);
                           theCell = document.getElementById(the_id);
                           if (theCell.bgColor == "00E800") {{
                               theCell.bgColor = (r + c)%2==0 ? ('#ffffff') : ('#a9a9a9'); 
                           }}
                       }}
                   }}               
               }}
               if (moving) {{
                   for (r = 0; r <= 7; ++r) {{
                       for (c = 0; c <= 7; ++c ) {{
                           the_id = "r" + String(r) + "c" + String(c);
                           theCell = document.getElementById(the_id);
                           theCell.bgColor = (r + c)%2==0 ? ('#ffffff') : ('#a9a9a9'); 
                       }}     
                   }}
                   the_id = "r" + String(piece_pos[0]) + "c" + String(piece_pos[1]);
                   newCell = document.getElementById(the_id);
                   newCell.innerHTML = piece_symbol;
                   oldCell.innerHTML = '';  
                   this.prevCellId = nil;
               }}
           }}
       }}
       
       if (moving) {{  
           row = theCell.id.charAt(1);
           column = theCell.id.charAt(3);
           putvals = "/move?r=" + row + "&c=" + column;
           // alert("PUT happens: " + putvals);
           xhttp.open("PUT", putvals, true);
           xhttp.send();
       }} else {{
           row = theCell.id.charAt(1);
           column = theCell.id.charAt(3);
           getvals = "/cell?r=" + row + "&c=" + column;
           // alert("GET happens: " + getvals);
           xhttp.open("GET", getvals, true);
           xhttp.send();
       }}
    }}
}}

</script>
</body>
</html>""")
        
class Board:
    
    def __init__(self, **kwargs): # name="a phrase mentioning Flask" if serving
        self.grid = [ ]
        for r in range(8):
            self.grid.append([None, None, None, None, 
                              None, None, None, None])
        self._reset()
        
        # arbitary named arguments become Board object attributes
        # an attribute named 'name' is vital for detecting server mode
        for attrib,val in kwargs.items():
            self.__dict__[attrib]=val
                
    def _reset(self):
        self.grid[7] = [  
                    Piece("Rook"   , "black", [7,0], "&#9820;"),
                    Piece("Knight" , "black", [7,1], "&#9822;"),
                    Piece("Bishop" , "black", [7,2], "&#9821;"),
                    Piece("Queen"  , "black", [7,3], "&#9819;"),
                    Piece("King"   , "black", [7,4], "&#9818;"),
                    Piece("Bishop" , "black", [7,5], "&#9821;"),
                    Piece("Knight" , "black", [7,6], "&#9822;"),
                    Piece("Rook"   , "black", [7,7], "&#9820;") ]
        self.grid[6] = [ ]
        for c in range(8):
            self.grid[6].append(Piece("Pawn", "black", [6,c], "&#9823;"))
            
        self.grid[0] = [  
                    Piece("Rook"   , "white", [0,0], "&#9814;"),
                    Piece("Knight" , "white", [0,1], "&#9816;"),
                    Piece("Bishop" , "white", [0,2], "&#9815;"),
                    Piece("Queen"  , "white", [0,3], "&#9813;"),
                    Piece("King"   , "white", [0,4], "&#9812;"),
                    Piece("Bishop" , "white", [0,5], "&#9815;"),
                    Piece("Knight" , "white", [0,6], "&#9816;"),
                    Piece("Rook"   , "white", [0,7], "&#9814;") ]
        self.grid[1] = [ ]
        for c in range(8):
            self.grid[1].append(Piece("Pawn", "white", [1,c], "&#9817;"))
            
    def __str__(self):
        global page_template
        table = "\n<table name='board' height='400' width='400' cellpadding='15'>\n"
        new_row = ""
        for r, row in enumerate(self.grid):
            new_row = "<tr class='row'>{0}</tr>\n"
            squares = ""
            for c, content in enumerate(row):
                the_id = "r{}c{}".format(r,c)
                symbol = content.unicode if isinstance(content, Piece) else " "
                if (r+c)%2:
                    squares += \
                    "\n<td bgcolor='#a9a9a9' class='square' " + \
                    "onclick='showCell(this)' id='{0}'>{1}</td>"\
                    .format(the_id, symbol)
                else:
                    squares += \
                    "\n<td bgcolor='#ffffff' class='square' " + \
                    "onclick='showCell(this)'" + \
                    " id='{0}'>{1}</td>" \
                    .format(the_id, symbol)                    
            new_row = new_row.format(squares)
            table  += new_row
        table += "\n</table>\n"
        sig = " " # nada
        if hasattr(self, 'name'):
            sig="Brought to you by: " + self.name
        render = page_template.format(table, sig)
        return render

    def _check_for_piece(self, r,c):
        piece = self.grid[r][c]
        if isinstance(piece, Piece):
            return piece
        else:
            return False

class Player:
    
    def __init__(self, color, game):
        self.color = color
        self.game = game
        self.num_moves = 0
        board = self.game.board.grid
        if self.color == "black":
            self.on_board = board[7] + board[6]
        else:
            self.on_board = board[0] + board[1]
        self.captured =  [ ]
        self.lost = [ ]

    def move(self):
        
        while True:  # from here...
            try:
                print("Enter 'status' or 'resign' or...")                
                user = input("Pick up a {0.color} piece at: ".format(self))
                if user == 'status':
                    print(self.game.status())        # <-- check status
                    continue
                elif user == "resign":
                    return self.color + " resigns."  # <-- Resigns!
                r, c = tuple(map(int, user.split()))
            except:
                print("Please enter two ints separated by \
                        a space, status or resign")
                continue
            my_piece = self.game.board._check_for_piece(r,c)
            if not my_piece:
                print("No piece in that place.")
                continue
            elif my_piece.color != self.color:
                print("That piece belongs to the other player!")
                continue
            print("Move a {0.color} {0.type} at {1}".format(my_piece,(r,c)))
            ok = input("Is that right? (y/n) :")
            if ok == "n":
                continue
            break
        
        while True:  # ... to there
            taking = False  # becomes True if target is other player piece
            try:
                newr, newc = \
                    tuple(map(int,(input("Move {0.color} {0.type} to...?: ".
                    format(my_piece)).split())))  # new row, new column                
            except:    
                print("Please enter two ints separated by a space")
                continue                
            other_piece = self.game.board._check_for_piece(newr, newc)
            if not other_piece:
                pass
            elif other_piece.color != self.color:
                taking = True
            elif other_piece.color == self.color:
                print("One of your own pieces is on that square!")
                continue
            print("OK, moving the {0.color} {0.type} to {1}.".
                format(my_piece,(newr, newc)))
            if taking:
                print("Taking a {0.color} {0.type}!".format(other_piece))
                self._lose_piece(other_piece)
            break
        
        my_piece.position[0] = newr
        my_piece.position[1] = newc
        self.game.board.grid[r][c] = None
        self.game.board.grid[newr][newc] = my_piece            
        self.num_moves += 1
        
        return Move(my_piece, (r, c), (newr, newc))

    def _lose_piece(self, piece):
        try:
            self.other.on_board.remove(piece)
        except ValueError:
            print("Error: ")
            print(repr(self.other))
            print("Other player's pieces:", self.other.on_board)
            print("To take: ", piece)
            print("This player's pieces:", self.on_board)
            raise  # piece not found
        r,c = piece.position
        self.game.board.grid[r][c]   = None  # remove piece
        piece.position[0] = None             # no location
        piece.position[1] = None             # no location
        self.other.lost.append(piece)        # lost to opponent
        self.captured.append(piece)          # POWs
        
    def __repr__(self):
        return "Player: {}  Moves: {}".format(self.color, self.num_moves)
    
class Game:
    
    def __init__(self, **kwargs):

        self.server = False  # may override with server = "Flask app...." 
        for attrib,val in kwargs.items():
            self.__dict__[attrib]=val
        
        if self.server:  # server mode if Flask app is in control
            self.board = Board(name=self.server) # passing through
        else:
            self.board = Board()  # manual mode, write html direct to file          
            with open("chessgame.html", "w") as output:
                print(self.board, file = output)

        self.player1 = Player("white", self)
        self.player2 = Player("black", self)
        self.player1.other = self.player2
        self.player2.other = self.player1
        self.the_moves = [ ]  # history of moves
        self.num_turns = 0
        if not self.server:   # not implemented in server version
            self.play_game()  # manual mode event loop
        
    def _save_move(self, the_move):
        self.the_moves.append(the_move)
    
    def play_game(self):     # for manual in-console control
        turn = self.player1  # white goes first
        game_over = False
        while not game_over:
            if turn == self.player1:
                print(" [{}] White's turn...".format(self.player1.num_moves))
                the_move = self.player1.move() 
                if "resigns" in the_move:
                    game_over = True
                self._save_move(the_move)
                turn = self.player2
            else:
                print(" [{}] Black's turn...".format(self.player2.num_moves))
                the_move = self.player2.move()
                if "resigns" in the_move:
                    game_over = True
                self._save_move(the_move)
                turn = self.player1

            print("Printing board...")
            with open("chessgame.html", "w") as output:
                print(self.board, file = output)
            print("=================\n")
            self.num_turns += 1
            if self.num_turns > 5:  # optional max number of turns
                game_over = True
        else:
            print("Lets play again someday")
            # this would be a place to possibly save all the moves
            # in permanent storage e.g. a sqlite3 DB
    
    def reset(self):
        self.board = Board()
        self.player1 = Player("white", self.board)
        self.player2 = Player("black", self.board)

    def status(self):
        output = ("Status Report\n" + \
        "Turn: [{}]".format(self.num_turns) + \
        "Player one (white):\n" + \
        "Lost: {}\n".format(self.player1.lost) + \
        "Captured:  {}\n".format(self.player1.captured))
        output = (output + "\n" + \
        "Player two (black):\n" + \
        "Lost: {}\n".format(self.player2.lost) + \
        "Captured: {}\n".format(self.player2.captured))
        return output

    def legal(self, the_piece):
        moves = []
        if the_piece.type == "Knight":
            for x,y in ((1,2),(-1,2),(1,-2),(-1,-2),
                        (2,1),(2,-1),(-2,1),(-2,-1)):
                candidate = (the_piece.position[0] + x, 
                            the_piece.position[1] + y)
                if (0 <= candidate[0] <= 7) and (0 <= candidate[1] <= 7):
                    p = self.board._check_for_piece(*candidate)                  
                    if (not p) or (p.color != the_piece.color):
                        moves.append("r{}c{}".format(*candidate))
            
        return moves
            
                
if __name__ == "__main__":
    the_game = Game()