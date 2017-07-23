from textblob import TextBlob

for row in cursor:
    blob = TextBlob(text)

    for sentence in blob.sentences:
        print(sentence.sentiment.polarity)
