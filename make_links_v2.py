# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:27:07 2016

@author: kurner

A namedtuple is a subclass of tuple allowing for named
columns and therefore dot notation access, treating 
elements as named attributes.
"""
from collections import namedtuple

Bmk = namedtuple('Bookmark', 'place url')

# tuple of tuples
bookmarks = (
    Bmk("Intro to Programming @ DropBox", "http://bit.ly/1TrSJFB"),
    Bmk("Anaconda.org", "http://anaconda.org"),
    Bmk("Python.org", "http://python.org"),
    Bmk("Python Docs", "https://docs.python.org/3/"),
    Bmk("Spaghetti Code", "http://c2.com/cgi/wiki?SpaghettiCode"),
    Bmk("Structured Programming", "http://c2.com/cgi/wiki?StructuredProgramming"),
    Bmk("Map of Languages", "http://archive.oreilly.com/pub/a/oreilly//news/languageposter_0504.html"),
    Bmk("XKCD", "http://xkcd.com"),
    Bmk("Django","https://docs.djangoproject.com/"),
    Bmk("PythonAnywhere","https://www.pythonanywhere.com/"),
    Bmk("CodeAcademy: Python","https://www.codecademy.com/learn/python"),
    Bmk("Unicode on Youtube", "https://www.youtube.com/watch?v=Z_sl99D2a18"),
    Bmk("In Defense of Ada", "http://www.grunch.net/synergetics/adaessay.html"),
    Bmk("Grace Hopper on Letterman", "https://www.youtube.com/watch?v=1-vcErOPofQ"),
    Bmk("The Mind of a Genius: John von Neumann", "https://www.youtube.com/watch?v=XZ9tt72feL8"),
    Bmk("World Domination meme", "https://www.google.com/search?q=linux+world+domination&safe=off&source=lnms&tbm=isch"),
    Bmk("Warriors of the Net", "https://www.youtube.com/watch?v=PBWhzz_Gn10"),
    Bmk("LAMP stack", "https://www.google.com/search?q=lamp+stack&safe=off&biw=787&bih=535&source=lnms&tbm=isch"),
    Bmk("LAMP stack (Wikipedia)","https://en.wikipedia.org/wiki/LAMP_(software_bundle)"),
    Bmk("In the Beginning was the Command Line", "http://c2.com/cgi/wiki?InTheBeginningWasTheCommandLine"),
    Bmk("First Wiki","http://c2.com/cgi-bin/wiki" ),
    Bmk("Financial Data Visualization","http://finviz.com/map.ashx"),
    Bmk("Human Development Index","http://hdr.undp.org/en/content/human-development-index-hdi"),
    Bmk("Inside The Eye","http://ngm.nationalgeographic.com/2016/02/evolution-of-eyes-text"),
    Bmk("Top 10 Languages to Learn in 2016", "https://youtu.be/Z56GLRXxh88"),
    Bmk("Pretty Good Python Summary by Derek Banas", "https://youtu.be/N4mEzFDjqtA"),
    Bmk("How To Think Like a Computer Scientist - Free Book","http://www.greenteapress.com/thinkpython/thinkCSpy.pdf"),
    Bmk("SQL Syntax", "https://www.google.com/search?q=sql+syntax&safe=off&biw=787&bih=535&source=lnms&tbm=isch")
    )
    
for bmk in bookmarks:
    print(bmk.place, bmk.url, sep="\n") # using dot notation to get elements
    print("-")

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
{}
</UL>
</BODY>
</HTML>
""".lower()

the_body = ""
for bmk in sorted(bookmarks):
    # note the placeholder {0} accepts dot notation too, bmk being a namedtuple
    the_body += "<li><a href='{0.url}'>{0.place}</a></li>\n".format(bmk)

out = open("links.html", "w")
print(page.format(html.format(the_body)), file=out)
out.close()
