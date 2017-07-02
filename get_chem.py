#!/usr/bin/env python

from urllib.request import urlopen
import json
import sys

if len(sys.argv) > 1:
   get_elem = sys.argv[1]
else:
   get_elem = "C"

url = "http://localhost:8000/cgi-bin/testing.cgi?elem=" + get_elem
response = urlopen(url)
L = json.loads(response.read())

for datum in L:
   print(datum)

