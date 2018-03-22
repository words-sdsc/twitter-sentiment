import sqlite3

def addTable( dbName, tableName ):
    conn = sqlite3.connect(dbName)

    conn = conn.cursor()

    try:
        # Create table
        conn.execute('''CREATE TABLE %s
                 (ID            INT PRIMARY KEY UNIQUE  NOT NULL,
                 DATE           INT                     NOT NULL,
                 TWEET          CHAR(250)               NOT NULL,
                 SENTIMENT      REAL);''' % tableName)

    except:
        print("Table: %s already exists in Database: %s." % tableName, dbName ) 

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()

def createDB( dbName ):
    try:
        conn = sqlite3.connect(dbName)
    except:
        print("Error creating %s\n" % dbName)

addTable( "TweetInfo.db", "Test_run" )
