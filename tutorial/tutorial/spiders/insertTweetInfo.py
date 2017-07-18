import sqlite3

def insertTweetInfo( dbName, dataBaseLoc, tweetId, date, epoch, tweet, sent ):
    # Connect to specified DB
    conn = sqlite3.connect(dataBaseLoc)

    # Insert a row of data
    try:
        conn.execute("INSERT INTO " + dbName + " (ID, DATE, EPOCH, TWEET, SENTIMENT) \
           VALUES ( ?, ?, ?, ?, ? )", ( (tweetId, date, epoch, tweet, sent) ))
    except:
        print( "ERROR INSERTING INTO DB" )
    
    conn.commit()   
    conn.close()
