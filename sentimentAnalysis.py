from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')


def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i)<128)

filename = "Words.txt"
myString = ""
with open(filename, 'r') as f:
    for line in f:
        myString += line

myString = remove_non_ascii_1(myString)
#print(myString) 
res = nlp.annotate(myString,
                   properties={
                       'annotators': 'sentiment',
                       'outputFormat': 'json',
                       'timeout': 1000,
                   })

for s in res["sentences"]:
    # Prints( "Index: Words : Tokens : Sentiment value result : Sentiment (Pos/Neg/Neutral)" )
    print "%d: '%s': %s %s" % ( s["index"],
        " ".join([t["word"] for t in s["tokens"]]),
        s["sentimentValue"], s["sentiment"])

