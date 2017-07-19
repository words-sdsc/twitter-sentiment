import sqlite3
def insertTweetInfo( dbName, dataBaseLoc, tweetId, epoch, tweet, sent ):
    # Connect to specified DB
    conn = sqlite3.connect(dataBaseLoc)

    # Insert a row of data
    try:
        conn.execute("INSERT INTO " + dbName + " (ID, EPOCH, TWEET, SENTIMENT) \
            VALUES ( ?, ?, ?, ? )", ( (tweetId, epoch, tweet, sent) ))
        conn.commit()   
    except:
        print("Error inserting into dataBase %s\nID for reference: %s" % dbName, tweetId)
    
    conn.close()
