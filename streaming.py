import tweepy, json

from SentimentAnalysis.sentimentAnalysis import *
from flask_socketio import SocketIO, emit

import settings


class StreamListener(tweepy.StreamListener):

    def __init__(self, socketio, hashtag=""):
        """
        Fields:
            socketio (SocketIO): Used for emitting the tweet data to the client

            hashtag (string): When filtering the stream with a bounding
                              box, an extra filter needs to be performed
                              to emit only the tweets with the desired
                              hashtag

        """

        super().__init__()
        self.socketio = socketio
        self.hashtag  = hashtag.replace("#", "").lower()


    def on_connect(self):
        print("Successfully connected to the Twitter stream")

    def on_data(self, data):
        json_data = json.loads(data)

        # skip this tweet if it doesn't have the basic attributes
        if not all([key in json_data for key in ["text", "created_at"]]):
            return

        if self.hashtag:
            if not ('entities' in json_data and json_data['entities']['hashtags']):
                return

            entities = json_data['entities']
            hashtags = map(lambda x: x['text'].lower(), entities['hashtags'])

            if not self.hashtag in hashtags:
                return

        text = json_data['text']
        sentiment = getSentiment(text)

        retweeted = True if "RT @" in text else False
        if retweeted: 
            text = text.replace("RT @", "")

        self.socketio.emit("response",
                { "text": text,
                    "created_at": json_data["created_at"],
                    "sentiment": sentiment,
                    "retweeted": retweeted },
                namespace="/streaming")


    def on_error(self, status_code):
        print('ERROR', status_code)
        if status_code == 420:
            return False


def retrieve_authentication():
    manager = CredentialsManager(settings.CREDENTIALS_PATH)
    cred = manager.read()

    auth = tweepy.OAuthHandler(cred['twitter_api_key'], cred['twitter_api_secret'])
    auth.set_access_token(cred['access_token'], cred['access_token_secret'])

    return auth


class TwitterStream():

    def __init__(self):
        self.stream = None


    def flow(self, message, socketio):
        auth = retrieve_authentication()
        hashtag = message["hashtag"]

        if 'bounding box' in message:
            listener = StreamListener(socketio, hashtag)
            self.stream = tweepy.Stream(auth, listener)

            bbox = message["bounding box"]
            self.stream.filter(locations=bbox, languages=["en"])
        else:
            listener = StreamListener(socketio)
            self.stream = tweepy.Stream(auth, listener)

            self.stream.filter(track=[hashtag], languages=["en"])


    def end_flow(self):
        self.stream.disconnect()


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
