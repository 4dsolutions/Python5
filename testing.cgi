#!/usr/bin/env python
import cgitb

import cgi
import sqlite3 as sql
import json

fs = cgi.FieldStorage()

print("Content-type:text/plain\n")

conn = sql.connect("./cgi-bin/periodic_table.db")

if not conn:
    print("<h1>No connection established</h1>")
else:          
    curs = conn.cursor()
    element = fs.getvalue("elem")
    curs.execute("select * from elements where elem_symbol = ?", (element,))
    result = curs.fetchone()
    print(json.dumps(result))
    conn.close()
