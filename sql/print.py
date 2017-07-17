# -*- coding: utf-8 -*-

import sqlite3
import sys

conn = sqlite3.connect('TweetInfo.db')

print( "Opened database successfully" )

cursor = conn.execute("SELECT * from TWEET_INFO")

for row in cursor:
    print( row[0])
    print( row[1])
    print( row[2])
    print( row[3])
    print( row[4])
    print()
    print()
    print()

print( "Operation done successfully" )
conn.close()
