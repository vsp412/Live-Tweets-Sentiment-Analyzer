
import nltk
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import json
import t1 as tt

#You can change these accordingly
ckey = 'dYxKfXE9ROdrnfuXpM4NdPY3S'
csecret = 'taWLHDEwzdPepTvRMQdx4LjtCt0e4GxXbKWSuk6ezCxWQUzriC'
atoken = '1111731702378881024-kqOUbnUM37uHF20k9EAQEVHf1XuDy4'
asecret = 'pQyzQAXtxyPlxPbk1xPEnNVUPG8HsnWZvj3IltVLbnifX'

class listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        
        #The Naives Bayes classification is happening here now. 
        tweet = all_data["text"]
        sentiment_value = tt.classifier.classify(tt.bag_of_words(tweet))
        print(sentiment_value)
        

        #A sentiment value 'pos' or 'neg', is being written here
        output = open("any_file.txt", "a")
        output.write(sentiment_value)
        output.write('\n')
        output.close()
        #The file, plot2.py, reads the above file, and plots a line graph, indicating the sentiment of each of the tweets
        return True

    def on_error(self, status):
        print(status)

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

twitterStream = Stream(auth, listener())
twitterStream.filter(track=["India"])  
