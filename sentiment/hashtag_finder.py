from streaming import retrieve_authentication
import re, tweepy, json


EVENTS = '(fire|flooding|wind|earthquake)'

def most_common(xs, n):
    from collections import Counter
    c = Counter()
    for x in xs:
        c[x] += 1
    return [word for word, count in c.most_common(n)]

def parse(xs):
    r = re.compile(r'(#\w+' + EVENTS + ")", re.IGNORECASE)
    for x in xs:
        m = r.match(x)
        if m:
            yield m.group()

def calfire_hashtags(calfire_twitter_name):
    auth = retrieve_authentication()
    api = tweepy.API(auth)
    response = api.user_timeline(screen_name=calfire_twitter_name, count=100)
    statuses = [obj.text for obj in response]
    return most_common(parse(statuses), 3)

def event_hashtags(woeid):
    auth = retrieve_authentication()
    api = tweepy.API(auth)
    response = api.trends_place(woeid)[0]
    trends = [trend['name'] for trend in response['trends'] if trend['name'].startswith("#")]
    return parse(trends)

if __name__ == "__main__":

    for hashtag in calfire_hashtags("CAL_FIRE"):
        print(hashtag)

    with open("woeids.json") as handle:
        woeids = json.load(handle)

    for hashtag in event_hashtags(woeids['san diego']):
        print(hashtag)
