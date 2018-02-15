from streaming import retrieve_authentication
import re, tweepy, json


EVENT = r'(fire|flooding|winds)'
HASHTAG_PATTERN = re.compile('(#\w+' + EVENT + ')', re.IGNORECASE)

extract = lambda x: HASHTAG_PATTERN.search(x).group()
match = lambda x: HASHTAG_PATTERN.search(x) is not None


def most_common(xs, n):
    from collections import Counter
    c = Counter()
    for x in xs:
        c[x] += 1
    return [word for word, count in c.most_common(n)]

def parse(xs):
    for x in xs:
        if match(x): yield extract(x)

def calfire_hashtags(calfire_twitter_name):
    auth = retrieve_authentication()
    api = tweepy.API(auth)
    response = api.user_timeline(screen_name=calfire_twitter_name, count=100)
    statuses = [obj.text for obj in response]
    return most_common(parse(statuses), 3)

def top_trending(api, woeid):
    auth = retrieve_authentication()
    api = tweepy.API(auth)
    response = api.trends_place(woeid)[0]
    trends = [trend['name'] for trend in response['trends']]
    return trends

if __name__ == "__main__":

    for hashtag in calfire_hashtags("CAL_FIRE"):
        print(hashtag)

    '''
    with open("woeids.json") as handle:
        woeids = json.load(handle)

    for hashtag in top_trending(api, woeids['los angeles']):
        print(hashtag)
    '''
