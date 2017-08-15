from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from keys import *
import time
import json

import sqlite3


#Get input in the form of string
key_word = input('Enter the search keyword: ')
print ("Streaming results of %s" % key_word)

#class listener inherting from StreamListener
class listener(StreamListener):
    def on_data(self, data):
        try:
            # Loads for a stirng, load for an object file
            json_obj = json.loads(data)  
            info = ""

            # Selects value of name of lsit user of obj jsonObj
            info +=  json_obj['user']['name']
            info += " tweeted: \n"
            info += json_obj['text']
            info += "\n on " + json_obj['created_at'] + "\n"
            print (info)
            return True

        except e:
            print( 'failed ondata' , str(e) )
            return False

def on_error(self, status):
    print (status)

#START OF MAIN, AUTHORIZING OUR DEV POWERS
#Initialize our tokens for access
auth = OAuthHandler(consumer_key(), consumer_secret())
auth.set_access_token(access_token(), access_token_secret())

#Sets up our twitter streaming using our class
twitterStream = Stream(auth, listener())
twitterStream.filter(track=[key_word])
