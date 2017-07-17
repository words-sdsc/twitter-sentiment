import sqlite3

def okay():
    for i in range(1, 10):
        print( "WORKED\n" )

def insertTweetInfo( dbName, dataBaseLoc, tweetId, date, epoch, tweet, sent ):
    # Conenct to the database
    conn = sqlite3.connect(dataBaseLoc)

    # Insert a row of data
    conn.execute("INSERT INTO " + dbName + " (ID, DATE, EPOCH, TWEET, SENTIMENT) \
       VALUES ( ?, ?, ?, ?, ? )", ( (tweetId, date, epoch, tweet, sent) ))


    # Commit the changes made
    conn.commit()

    # close the connection
    conn.close()


