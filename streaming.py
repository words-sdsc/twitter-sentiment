import tweepy, json

from SentimentAnalysis.sentimentAnalysis import *
from flask_socketio import SocketIO, emit

import settings


class StreamListener(tweepy.StreamListener):

    def __init__(self, socketio):
        super().__init__()
        self.socketio = socketio

    def on_connect(self):
        print("Successfully connected to the Twitter Streaming API")

    def on_data(self, data):
        json_data = json.loads(data)

        tweet_id = json_data['id']
        text = json_data['text']
        sentiment = getSentiment(text)

        retweeted = True if "RT @" in text else False
        if retweeted: 
            text = text.replace("RT @", "")

        self.socketio.emit("response",
                           { "text": text,
                             "sentiment": sentiment,
                             "tweet_id": tweet_id,
                             "retweeted": retweeted },
                           namespace="/streaming")

    def on_error(self, status_code):
        print('ERROR', status_code)
        if status_code == 420:
            return False


class TwitterStream():

    def __init__(self, socketio):
        manager = CredentialsManager(settings.CREDENTIALS_PATH)
        cred = manager.read()

        auth = tweepy.OAuthHandler(cred['twitter_api_key'] ,
                                   cred['twitter_api_secret'])

        auth.set_access_token(cred['access_token'],
                              cred['access_token_secret'])
        self.stream = tweepy.Stream(auth, StreamListener(socketio))

    def flow(self, hashtag):
        self.stream.filter(track=[hashtag])


class CredentialsManager():

    def __init__(self, path):
        self._path = path

    def read(self):
        c = Credentials()

        with self._path.open() as f:
            for line in f:
                k, v = line.strip().split('=')
                c[k] = v

        return c

    def write(self, credentials):
        with self._path.open('w') as f:
            for k, v in credentials.items():
                f.write(k + '=' + v + '\n')


class Credentials(dict):

    def __init__(self):
        super(Credentials, self).__init__(
            { 'twitter_api_key': 'None', 'twitter_api_secret': 'None',
              'access_token': 'None', 'access_token_secret': 'None' }
        )
