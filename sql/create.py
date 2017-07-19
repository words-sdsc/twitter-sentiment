import sqlite3

conn = sqlite3.connect('TweetInfo.db')

conn = conn.cursor()

# Create table

conn.execute('''CREATE TABLE TWEET_INFO_LOL
         (ID            INT PRIMARY KEY UNIQUE  NOT NULL,
         DATE           TEXT                    NOT NULL,
         EPOCH          INT                     NOT NULL,
         TWEET          CHAR(250)               NOT NULL,
         SENTIMENT      INT);''')


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
