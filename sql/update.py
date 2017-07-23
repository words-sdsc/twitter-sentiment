import sqlite3
from random import randint



#conn = sqlite3.connect('TweetInfo.db')

str_ = "Test_run"

# update a row of data
conn.execute("UPDATE " + str_ + " set SENTIMENT = ? where ID = ?")

# Save (commit) the changes
conn.commit()


# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
#conn.close()
