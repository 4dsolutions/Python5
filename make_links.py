# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 21:27:07 2016

@author: kurner
"""


# tuple of tuples
bookmarks = (
    ("Intro to Programming @ Google Drive", "http://bit.ly/1QzO5CF"),
    ("Intro to Programming @ DropBox", "http://bit.ly/1TrSJFB"),
    ("Anaconda.org", "http://anaconda.org"),
    ("Python.org", "http://python.org"),
    ("Python Docs", "https://docs.python.org/3/"),
    ("Spaghetti Code", "http://c2.com/cgi/wiki?SpaghettiCode"),
    ("Structured Programming", "http://c2.com/cgi/wiki?StructuredProgramming"),
    ("Map of Languages", "http://archive.oreilly.com/pub/a/oreilly//news/languageposter_0504.html"),
    ("XKCD", "http://xkcd.com"),
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
    ("Financial Data Visualization","http://finviz.com/map.ashx"),
    ("Human Development Index","http://hdr.undp.org/en/content/human-development-index-hdi"),
    ("Inside The Eye","http://ngm.nationalgeographic.com/2016/02/evolution-of-eyes-text"),
    ("Top 10 Languages to Learn in 2016", "https://youtu.be/Z56GLRXxh88"),
    ("Pretty Good Python Summary by Derek Banas", "https://youtu.be/N4mEzFDjqtA"),
    ("How To Think Like a Computer Scientist - Free Book","http://www.greenteapress.com/thinkpython/thinkCSpy.pdf"),
    ("SQL Syntax", "https://www.google.com/search?q=sql+syntax&safe=off&biw=787&bih=535&source=lnms&tbm=isch")
    )

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
for place, url in sorted(bookmarks):
    the_body += "<li><a href='{}'>{}</a></li>\n".format(url, place)

out = open("links.html", "w")
print(page.format(html.format(the_body)), file=out)
out.close()
