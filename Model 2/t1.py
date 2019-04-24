import string
import re
import nltk
#Data cleaning and all the text processing done here
nltk.download('stopwords')
from nltk.corpus import stopwords 
stopwords_english = stopwords.words('english')
 
from nltk.stem import PorterStemmer
stemmer = PorterStemmer()
 
from nltk.tokenize import TweetTokenizer
 

emoticons_happy = set([
    ':-)', ':)', ';)', ':o)', ':]', ':3', ':c)', ':>', '=]', '8)', '=)', ':}',
    ':^)', ':-D', ':D', '8-D', '8D', 'x-D', 'xD', 'X-D', 'XD', '=-D', '=D',
    '=-3', '=3', ':-))', ":'-)", ":')", ':*', ':^*', '>:P', ':-P', ':P', 'X-P',
    'x-p', 'xp', 'XP', ':-p', ':p', '=p', ':-b', ':b', '>:)', '>;)', '>:-)',
    '<3'
    ])
 
emoticons_sad = set([
    ':L', ':-/', '>:/', ':S', '>:[', ':@', ':-(', ':[', ':-||', '=L', ':<',
    ':-[', ':-<', '=\\', '=/', '>:(', ':(', '>.<', ":'-(", ":'(", ':\\', ':-c',
    ':c', ':{', '>:\\', ';('
    ])
 
emoticons = emoticons_happy.union(emoticons_sad)
 
 # This function does all the cleaning of the tweet passed to it
def clean_tweets(tweet):
   
    tweet = re.sub(r'\$\w*', '', tweet)
 
    
    tweet = re.sub(r'^RT[\s]+', '', tweet)
 
    
    tweet = re.sub(r'https?:\/\/.*[\r\n]*', '', tweet)
    
    tweet = re.sub(r'#', '', tweet)
 
    
    tokenizer = TweetTokenizer(preserve_case=False, strip_handles=True, reduce_len=True)
    tweet_tokens = tokenizer.tokenize(tweet)
 
    tweets_clean = []    
    for word in tweet_tokens:
        if (word not in stopwords_english and 
              word not in emoticons and 
                word not in string.punctuation): 
            
            stem_word = stemmer.stem(word)
            tweets_clean.append(stem_word)
 
    return tweets_clean
 

def bag_of_words(tweet):
    words = clean_tweets(tweet)
    words_dictionary = dict([word, True] for word in words)    
    return words_dictionary
 
#imported assigned tweets from NLTK. A training and testing set of 1000 tweets each will be created from this
#This will be used to create a Naives Bayes tweet classifier. Its accuracy, and other readings can be obtained by printing the 'accuracy', 
#and 'show most informative features'

# This classifier is used to classify tweets in real time, in the next file, t2.py

from nltk.corpus import twitter_samples

 
pos_tweets = twitter_samples.strings('positive_tweets.json')

 
neg_tweets = twitter_samples.strings('negative_tweets.json')

 
all_tweets = twitter_samples.strings('tweets.20150430-223406.json')

pos_tweets_set = []
for tweet in pos_tweets:
    pos_tweets_set.append((bag_of_words(tweet), 'pos'))    
 

neg_tweets_set = []
for tweet in neg_tweets:
    neg_tweets_set.append((bag_of_words(tweet), 'neg'))


import random
from random import shuffle 
shuffle(pos_tweets_set)
shuffle(neg_tweets_set)
 
test_set = pos_tweets_set[:1000] + neg_tweets_set[:1000]
train_set = pos_tweets_set[1000:] + neg_tweets_set[1000:]


from nltk import classify
from nltk import NaiveBayesClassifier
 
classifier = NaiveBayesClassifier.train(train_set)
 
accuracy = classify.accuracy(classifier, test_set)
print(accuracy) 
 
print (classifier.show_most_informative_features(10)) 



