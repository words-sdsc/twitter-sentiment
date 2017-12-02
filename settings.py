from pathlib import Path


CREDENTIALS_PATH = Path.cwd() / '.credentials'


def init():
    global url
    url = ""
    global tableName
    tableName = ""
    global searchQuery
    searchQuery = ""

    global tweetListBuffer
    tweetListBuffer = []
