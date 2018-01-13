import tweepy, json

from SentimentAnalysis.sentimentAnalysis import *
from flask_socketio import SocketIO, emit

import settings


def retrieve_authentication():
    manager = CredentialsManager(settings.CREDENTIALS_PATH)
    cred = manager.read()

    auth = tweepy.OAuthHandler(cred['twitter_api_key'], cred['twitter_api_secret'])
    auth.set_access_token(cred['access_token'], cred['access_token_secret'])

    return auth


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

        retweeted = True if 'RT @' in json_data['text'] else False
        text = json_data['text'].replace('RT @', '')
        sentiment = getSentiment(text)

        self.socketio.emit("response",
                {   "text": text,
                    "created_at": json_data["created_at"],
                    "sentiment": sentiment,
                    "retweeted": retweeted },
                    namespace="/streaming")


    def on_error(self, status_code):
        print('ERROR', status_code)
        if status_code == 420:
            return False




class UndefinedChildClass(Exception):
    pass


class DataFlow():


    def __init__(self):
        self.auth = retrieve_authentication()


    @staticmethod
    def factory(child):
        if child == 'historical':
            return HistoricalFlow()
        if child == 'live':
            return LiveFlow()

        err = 'The provided child argument (' + child + ') is not supported'
        raise UndefinedChildClass(err)


class HistoricalFlow(DataFlow):


    def __init__(self):
        super().__init__()
        self.api = tweepy.API(self.auth)


    def start(self, message, socketio):
        counter = 0
        last_id = -1
        hashtag = message['hashtag']

        max_tweets = 1000

        while counter < max_tweets:
            max_id = str(last_id - 1)

            try:
                tweets = self.api.search(q=hashtag, count=100, max_id=max_id, lang=['en'])
                counter += len(tweets)

                if not tweets:
                    break

                last_id = tweets[-1].id

                for tweet in tweets:

                    retweeted = True if 'RT @' in tweet.text else False
                    text      = tweet.text.replace('RT @', '')
                    sentiment = getSentiment(text)
                    creation  = tweet.created_at.strftime('%Y-%m-%d %H:%M:%S')

                    socketio.emit("response",
                            { "text": text,
                              "created_at": creation,
                              "sentiment": sentiment,
                              "retweeted": retweeted },
                            namespace="/streaming")

            except tweepy.TweepError as err:
                break


    def stop(self):
        print('stop')


class LiveFlow(DataFlow):


    def __init__(self):
        super().__init__()
        self.stream = None


    def start(self, message, socketio):
        hashtag = message["hashtag"]

        if 'bounding box' in message:
            listener = StreamListener(socketio, hashtag)
            self.stream = tweepy.Stream(self.auth, listener)

            bbox = message["bounding box"]
            self.stream.filter(locations=bbox, languages=["en"])
        else:
            listener = StreamListener(socketio)
            self.stream = tweepy.Stream(self.auth, listener)

            self.stream.filter(track=[hashtag], languages=["en"])


    def stop(self):
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
