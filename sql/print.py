# -*- coding: utf-8 -*-

import sqlite3
import sys

conn = sqlite3.connect('TweetInfo.db')

print( "Opened database successfully" )

cursor = conn.execute("SELECT * from CORGIS")

for row in cursor:
    print( "Tweet Id: \t%s" % row[0] )
    print( "Date: \t\t%s" % row[1] )
    print( "Tweet Text: \t%s" % row[2] )
    print( "Sentiment: \t%s" % row[3] )
    print()

print( "Operation done successfully" )
conn.close()
