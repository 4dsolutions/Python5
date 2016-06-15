# -*- coding: utf-8 -*-
"""
Created on Wed Jun 15 12:19:05 2016

@author: Kirby Urner, 4D Solutions
(c) MIT License, 2016

Create tables to store 26 "points of interest"
A-Z as quadray coordinates [1], already converted 
to XYZ as well, in the Coords table.  

Define polyhedrons in Polys with one-to-many
relationship to Faces, which get distilled 
into edges e.g. EFG -> EF FG GE.

Assign volumes from the Concentric Hierarchy in 
Synergetics:
http://grunch.net/synergetics/volumes.html
http://grunch.net/synergetics/volumes2.html

[1]  https://en.wikipedia.org/wiki/Quadray_coordinates
"""

import sqlite3 as sql

import sys
sys.path.append("/Users/kurner/Documents/Python5")

from string import ascii_uppercase as AtoZ
from qrays import Qvector
import time, os

# four spokes of a caltrop
A = Qvector((1,0,0,0))
B = Qvector((0,1,0,0))
C = Qvector((0,0,1,0))
D = Qvector((0,0,0,1))
E, F, G, H       = B+C+D, A+C+D, A+B+D, A+B+C   # inverse tet
I, J, K, L, M, N = A+B, A+C, A+D, B+C, B+D, C+D # octahedron
O, P, Q, R, S, T = I+J, I+K, I+L, I+M, N+J, N+K # cuboctahedron
U, V, W, X, Y, Z = N+L, N+M, J+L, L+M, M+K, K+J # ...

class DB:
    backend  = 'sqlite3'  # default
    timezone = int(time.strftime("%z", time.localtime()))
    target_path = os.getcwd()  # current directory
    db_name = ":file:"
    db_name = os.path.join(target_path, 'shapes_lib.db')

    @classmethod
    def connect(cls):
        if cls.backend == 'sqlite3':
            DB.conn = sql.connect(DB.db_name)
            DB.c = DB.conn.cursor()
        elif cls.backend == 'postgres':
            DB.conn = sql.connect(host='localhost',
                                  user='root', port='8889')
            DB.c = DB.conn.cursor()

    @classmethod
    def disconnect(cls):
        DB.conn.close()
            
def make_tables():

    # https://www.sqlite.org/lang_droptable.html
    DB.c.execute("""DROP TABLE IF EXISTS Polys""")
    DB.c.execute("""CREATE TABLE Polys 
        (poly_nick text PRIMARY KEY,
         poly_long text,
         poly_V int,
         poly_F int,
         poly_E int,
         poly_volume float,
         poly_color text,
         updated_by text)""")

    DB.c.execute("""DROP TABLE IF EXISTS Faces""")
    DB.c.execute("""CREATE TABLE Faces 
        (poly_face_id text PRIMARY KEY,
         poly_nick text,
         vertex_labels text,
         updated_by text)""")

    DB.c.execute("""DROP TABLE IF EXISTS Coords""")
    DB.c.execute("""CREATE TABLE Coords 
        (poly_face_id text PRIMARY KEY,
         vertex_label text,
         coord_a float,
         coord_b float,
         coord_c float,
         coord_d float,
         coord_x float,
         coord_y float,
         coord_z float,
         updated_by text)""")       

def save_polys(): 
    
    sql_command = ("""INSERT INTO Polys 
    (poly_nick, poly_long, poly_V, poly_F, poly_E, poly_volume, poly_color) 
    VALUES ('TETRA', 'Tetrahedron', 6, 4, 6, 1, 'Orange')""")  
    DB.c.execute(sql_command)
    
    sql_command = ("""INSERT INTO Polys 
    (poly_nick, poly_long, poly_V, poly_F, poly_E, poly_volume, poly_color) 
    VALUES ('INVTET', 'Inverse Tetrahedron', 6, 4, 6, 1, 'Black')""")
    DB.c.execute(sql_command)

    sql_command = ("""INSERT INTO Polys 
    (poly_nick, poly_long, poly_V, poly_F, poly_E, poly_volume, poly_color) 
    VALUES ('CUBE', 'Cube', 8, 6, 12, 3, 'Green')""")
    DB.c.execute(sql_command)

    sql_command = ("""INSERT INTO Polys 
    (poly_nick, poly_long, poly_V, poly_F, poly_E, poly_volume, poly_color) 
    VALUES ('OCTA', 'Octahedron', 6, 8, 12, 4, 'Red')""")
    DB.c.execute(sql_command)

    sql_command = ("""INSERT INTO Polys 
    (poly_nick, poly_long, poly_V, poly_F, poly_E, poly_volume, poly_color) 
    VALUES ('RD', 'Rhombic Dodecahedron', 14, 12, 24, 6, 'Blue')""")
    DB.c.execute(sql_command)

    sql_command = ("""INSERT INTO Polys 
    (poly_nick, poly_long, poly_V, poly_F, poly_E, poly_volume, poly_color) 
    VALUES ('VE', 'Cuboctahedron', 12, 14, 24, 20, 'Yellow' )""")
    DB.c.execute(sql_command)
    
    DB.conn.commit()  

def save_faces():
    sql_command = ("""INSERT INTO Faces 
    (poly_face_id, poly_nick, vertex_labels) 
    VALUES (1, 'TETRA', '("A", "B", "C")""")
    sql_command = ("""INSERT INTO Faces 
    (poly_face_id, poly_nick, vertex_labels) 
    VALUES (2, 'TETRA', '("A", "C", "D")' """)
    sql_command = ("""INSERT INTO Faces 
    (poly_face_id, poly_nick, vertex_labels) 
    VALUES (3, 'TETRA', '("A", "D", "C")' """)
    sql_command = ("""INSERT INTO Faces 
    (poly_face_id, poly_nick, vertex_labels) 
    VALUES (4, 'TETRA', '("B", "C", "D")' """)    
    DB.c.execute(sql_command)

def save_coords():  
    # we don't mind having globals and we do take 
    # advantage of the simplicity A-Z labels affords us
    for letter in AtoZ:
        the_data = dict() # empty
        vector = globals()[letter]
        the_data['label'] = letter
        the_data['a'] = vector.a
        the_data['b'] = vector.b
        the_data['c'] = vector.c
        the_data['d'] = vector.d
        xyz_vector    = vector.xyz()
        the_data['x'] = xyz_vector.x
        the_data['y'] = xyz_vector.y
        the_data['z'] = xyz_vector.z
        sql_insert = ("""INSERT INTO Coords 
        (vertex_label, coord_a, coord_b, coord_c, coord_d, 
        coord_x, coord_y, coord_z) 
        VALUES ('{label}', {a}, {b}, {c}, {d}, {x}, {y}, {z})""")
        sql_command = sql_insert.format(**the_data)
        # print(query)
        DB.c.execute(sql_command)
        DB.conn.commit()  

DB.connect()
make_tables()
save_coords()
#save_faces()
save_polys()
DB.disconnect()