# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:27:07 2016

@author: kurner

A namedtuple is a subclass of tuple allowing for named
columns and therefore dot notation access, treating 
elements as named attributes.

Bookmark(place='Anaconda.org', url='http://anaconda.org')
"""

from collections import namedtuple

Bmk = namedtuple('Bookmark', 'place url')

# tuple of tuples
tuples = (
    ("Guild Programming Courses @ DropBox", "http://bit.ly/1TrSJFB"),
    ("Anaconda.org", "http://anaconda.org"),
    ("Python.org", "http://python.org"),
    ("Python Docs", "https://docs.python.org/3/"),
    ("'New Math' by Tom Lehrer (animated)","https://youtu.be/UIKGV2cTgqA"),
    ("Spaghetti Code", "http://c2.com/cgi/wiki?SpaghettiCode"),
    ("Structured Programming", "http://c2.com/cgi/wiki?StructuredProgramming"),
    ("Map of Languages", "http://archive.oreilly.com/pub/a/oreilly//news/languageposter_0504.html"),
    ("XKCD", "http://xkcd.com"),
    ("PDX Code Guild", "https://pdxcodeguild.com/"),
    ("Will 'Geeks' Rule? CBS News (world domination meme)","http://www.cbsnews.com/news/will-geeks-rule-the-world/"),
    ("Django","https://docs.djangoproject.com/"),
    ("PythonAnywhere","https://www.pythonanywhere.com/"),
    ("CodeAcademy: Python","https://www.codecademy.com/learn/python"),
    ("Unicode on Youtube", "https://www.youtube.com/watch?v=Z_sl99D2a18"),
    ("In Defense of Ada", "http://www.grunch.net/synergetics/adaessay.html"),
    ("Grace Hopper on Letterman", "https://www.youtube.com/watch?v=1-vcErOPofQ"),
    ("The Mind of a Genius: John von Neumann", "https://www.youtube.com/watch?v=XZ9tt72feL8"),
    ("World Domination meme", "https://www.google.com/search?q=linux+world+domination&safe=off&source=lnms&tbm=isch"),
    ("Warriors of the Net", "https://www.youtube.com/watch?v=PBWhzz_Gn10"),
    ("LAMP stack", "https://www.google.com/search?q=lamp+stack&safe=off&biw=787&bih=535&source=lnms&tbm=isch"),
    ("LAMP stack (Wikipedia)","https://en.wikipedia.org/wiki/LAMP_(software_bundle)"),
    ("In the Beginning was the Command Line", "http://c2.com/cgi/wiki?InTheBeginningWasTheCommandLine"),
    ("First Wiki","http://c2.com/cgi-bin/wiki" ),
    ("'Meme' on Wikipedia", "https://en.wikipedia.org/wiki/Meme"),
    ("Financial Data Visualization","http://finviz.com/map.ashx"),
    ("Human Development Index","http://hdr.undp.org/en/content/human-development-index-hdi"),
    ("Inside The Eye","http://ngm.nationalgeographic.com/2016/02/evolution-of-eyes-text"),
    ("Top 10 Languages to Learn in 2016", "https://youtu.be/Z56GLRXxh88"),
    ("Pretty Good Python Summary by Derek Banas", "https://youtu.be/N4mEzFDjqtA"),
    ("How To Think Like a Computer Scientist - Free Book","http://www.greenteapress.com/thinkpython/thinkCSpy.pdf"),
    ("SQL Syntax", "https://www.google.com/search?q=sql+syntax&safe=off&biw=787&bih=535&source=lnms&tbm=isch"),
    ("Python Cookbook","http://chimera.labs.oreilly.com/books/1230000000393/index.html"),
    ("Learn Python the Hard Way","http://learnpythonthehardway.org/book/"),
    ("What Is Code?","http://www.bloomberg.com/graphics/2015-paul-ford-what-is-code/"),
    ("Become a Better Programmer Through Mundane Programming","http://mundaneprogramming.github.io/slides/#/"),
    )

# lets make these namedtuples instead OK?
# *tup explodes each tuple into two positionals, what Bmk expects
bookmarks = [Bmk(*tup) for tup in tuples] # list comprehension!
    
for bmk in bookmarks:
    # Bookmark(place='Anaconda.org', url='http://anaconda.org')
    print(bmk)   # notice format of output: __repr__
    print("-")

# skeleton of any web page
page = """\
<!DOCTYPE HTML>
{}
"""

html = """\
<HTML>
<HEAD>
<TITLE>Bookmarks for Python</TITLE>
</HEAD>
<BODY>
<H3>Bookmarks</H3>
<BR />
<UL>
{bookmarks}
</UL>
</BODY>
</HTML>
""".lower()

the_links = ""
for bmk in sorted(bookmarks):
    # note the placeholder {0} accepts dot notation too, bmk being a namedtuple
    the_links += "<li><a href='{0.url}'>{0.place}</a></li>\n".format(bmk)

# challenge:  instead of writing to a text file, write to a SQLite DB
# using sqlite3.  Two column table:  e.g. place, url

out = open("links.html", "w")
print(page.format(html.format(bookmarks = the_links)), file=out)
out.close()
