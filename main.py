import tweepy
import random, math
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier, DecisionTreeClassifier, MaxEntClassifier
from twitter_sentiment import tweet_from_user, classify_tweets

#nycklar/tokens för twitteråtkmst
consumer_key = "kv2G5lkydpHSsFs9sZlgXfcZf"
consumer_secret = "A7qt38K3hls0ZuwF0IQi0zPyyvym4Qbej3cjpxeNeAHQqdGA9z"

access_token = "945432997653893120-o1uqI136rvjijmf2g05oGU8xvRQsUB9"
access_token_secret= "LjyX5U3ufzVkFDhr7XVUls9CGWt0NJKqJOfM7qp9hyXcn"

authenticator = tweepy.OAuthHandler(consumer_key, consumer_secret)

authenticator.set_access_token(access_token, access_token_secret)

my_api = tweepy.API(authenticator)

#hämta riksbankens tweets samt försök till klassificering av dem
tweetlst=tweet_from_user("riksbanken", my_api)
samplelst=classify_tweets(tweetlst)
test_set_riksbank=samplelst[0]+samplelst[1]


#läser in dataset som redan är klassificerat
with open("text_pos.txt", "r") as lines:
	pos_sample = []
	for line in lines:
		line = line.replace('\"', '')
		pos_sample.append((line.rstrip(), "pos"))

with open("text_neg.txt", "r") as lines:
	neg_sample = []
	for line in lines:
		line = line.replace('\"', '')
		neg_sample.append((line.rstrip(), "neg"))

#slumpa ordningen av datan och skapa träningsdata(80%) och testdata(20%)
total_sample = pos_sample+neg_sample
random.shuffle(total_sample)

training_set = total_sample[0:math.floor(0.9*len(total_sample))]
test_set = total_sample[math.floor(0.9*len(total_sample)):]

#tränar klassificeraren och evaluerar på två olika testset
classifier_bayes = NaiveBayesClassifier(training_set)
print("Accuracy Naive Bayes: " + str(classifier_bayes.accuracy(test_set)))
print("Accuracy Naive Bayes Riksbank: " +str(classifier_bayes.accuracy(test_set_riksbank)))
