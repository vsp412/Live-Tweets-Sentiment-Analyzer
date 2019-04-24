from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import json
from textblob import TextBlob
import matplotlib.pyplot as plt
import re


positive=0
negative=0
compound=0

#Instead of having to close down the whole window everytime in order to stop the stream of tweets, you can 
#set a count variable stating how many tweets you want to display, and then when count reaches that value, 
#you just return false and it will stop
count=0
plt.ion()

#You can put your keys here
ckey = 'dYxKfXE9ROdrnfuXpM4NdPY3S'
csecret = 'taWLHDEwzdPepTvRMQdx4LjtCt0e4GxXbKWSuk6ezCxWQUzriC'
atoken = '1111731702378881024-b14M2YvweE2gexuxEUG2Wa2hvfIKOm'
asecret = 'Nb0e9IEW4d1EwZntwzFX3KY7Ae8PU85HAFryAdfdFeIxP'

class listener(StreamListener):
    
    def on_data(self,data):
        
        all_data=json.loads(data)
        tweet=all_data["text"]
        #Cleaning each tweet
        tweet=" ".join(re.findall("[a-zA-Z]+", tweet))
        blob=TextBlob(tweet.strip())

        global positive
        global negative     
        global compound  
        global count
        
        count=count+1
        #'Sentiment' function used from textblob. It has 2 more functions polarity and subjectivity. 
        #A way to make this model better would be to also get the sentiment.subjectivity scores for each
        #tweet, and only plot those tweets who have very low subjectivity, in order to reduce the effect of 
        # things like one's subjective views in writing a tweet, sarcasm. The subjectivity value is also betwee
        # 0 and 1, and we can set a minimum threshold. Any tweets above this value won't be considered.
        senti=0
        for sen in blob.sentences:
        #if sen.sentiment.subjectivity < 0.3 
            senti=senti+sen.sentiment.polarity
            if sen.sentiment.polarity >= 0:
                positive=positive+sen.sentiment.polarity 
                #print(sen.sentiment.subjectivity)
            else:
                negative=negative+sen.sentiment.polarity  
        compound=compound+senti        
    
        print(tweet.strip())
        
        print(str(positive) + ' ' + str(negative) + ' ' + str(compound)) 
        
    #Plotting.
    #Go to Settings (For my Mac, I have to go to Preferences), IPython Console, and then on the 
    #Graphics tab. Set the 'Backend' to Automatic. Default is inline
        plt.ion()
        plt.axis([ 0, 700, -20,20])
        plt.xlabel('Time')
        plt.ylabel('Sentiment')
        plt.plot([positive],'go',[negative],'ro',[compound],'bo')
        plt.show()
        
        plt.pause(0.0001)
        
        
    def on_error(self,status):
        print(status)


auth=OAuthHandler(ckey,csecret)
auth.set_access_token(atoken,asecret)

twitterStream=  Stream(auth, listener(count))
twitterStream.filter(track=["Ethereum"])