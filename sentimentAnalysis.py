from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')

from time import sleep

def remove_non_ascii_1(text):
    return ''.join(i for i in text if ord(i)<128)

filename = "Tweets.txt"
myString = ""
stringArr = []
count = 0

# Form list of string in buckets of 4
with open(filename, 'r') as f:
    for line in f:
        count += 1
        myString += line
        
        # Buckets of strings in array
        if count == 4:
            #myString = myString.replace(".","")
            #myString = myString.replace("?","")
            #myString = myString.replace("!","")
            myString += "."
            stringArr.append(myString)
            count = 0
            myString = ""
            
if myString != "":
    #myString = myString.replace(".","")
    #myString = myString.replace("?","")
    #myString = myString.replace("!","")
    myString += "."
    stringArr.append(myString)

myString = remove_non_ascii_1(myString)
#print(myString) 
print( stringArr )
index = 0

# Annotate the string using coreNLP
for string in stringArr:
    res = nlp.annotate(string,
                   properties={
                   'annotators': 'sentiment',
                   'outputFormat': 'json',
                   'timeout': 1000,
               })
    sleep( 4 )

    # Print out the results!
    for s in res["sentences"]:
    # Prints( "Index: Words : Tokens : Sentiment value result : Sentiment (Pos/Neg/Neutral)" )
        print ( "%d: '%s': %s %s" % ( index, " ".join([t["word"] for t in s["tokens"]]), s["sentimentValue"], s["sentiment"]) )
        index += 1
