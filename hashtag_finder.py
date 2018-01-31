from streaming import retrieve_authentication
import re, tweepy, json


HASHTAG_REGEX = re.compile(r'(#\w+fire)', re.IGNORECASE)
extract = lambda x: HASHTAG_REGEX.match(x).group()
matched = lambda x: HASHTAG_REGEX.match(x) is not None

def calfire_hashtags(api):
    statuses = api.user_timeline(screen_name="CALFIRESANDIEGO", count=100)
    return [extract(status.text) for status in statuses if matched(status.text)]

def top_trending(api, woeid):
    response = api.trends_place(woeid)[0]
    trends = response['trends']
    return [extract(trend['name']) for trend in trends if matched(trend['name'])]

if __name__ == "__main__":
    auth = retrieve_authentication()
    api = tweepy.API(auth)

    for hashtag in calfire_hashtags(api):
        print(hashtag)

    with open("woeids.json") as handle:
        woeids = json.load(handle)

    for hashtag in top_trending(api, woeids['san diego']):
        print(hashtag)
