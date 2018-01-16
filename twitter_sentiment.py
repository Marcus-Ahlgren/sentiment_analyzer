import tweepy
import random, math
from textblob import TextBlob
from textblob.classifiers import NaiveBayesClassifier

#hämta tweets från användare
def tweet_from_user(user, api):
	tweetlst = []
	#läser in 200 första tweets(maxantal)
	tweets = api.user_timeline(screen_name = user, count = 200, include_rts = True)

	tweetlst.extend(tweets)
	#sparar senaste tweetid
	last_tweet_id = tweets[-1].id - 1
	number_of_tweets = len(tweets)
	#fortsätter läsa in tweets och lägger till i lista tils flödet är slut
	while len(tweets) > 0:
		tweets = api.user_timeline(screen_name = user, count=200, max_id=last_tweet_id)

		if tweets is None or len(tweets) == 0:
		    continue
		last_tweet_id = tweets[-1].id - 1
		number_of_tweets += len(tweets)

		tweetlst.extend(tweets)
	return tweetlst

#försök till klassificering av riksbankens tweets med generiska ord som kan förknippas med positiva/negativa besked
def classify_tweets(mylst):
	pos_words = ["bättre", "sänkt", "positiv", "stark", "tillväxt", "snabb", "nära"]
	neg_words = ["dålig", "sämre", "höjd", "orolig", "långsam", "svag", "inte"]

	pos_sample = []
	neg_sample = []

	#om tweets innehåller ovvannämnda ord läggs de in i lista som samlar positiva/negativa tweets. Dessa set kan senare användas för modellevaluering. 
	for status in mylst:
		if any(word in status.text for word in pos_words):
			pos_sample.append((TextBlob(status.text).translate(from_lang="sv", to="en"), "pos"))
			continue
		if any(word in status.text for word in neg_words):
				neg_sample.append((TextBlob(status.text).translate(from_lang="sv", to="swe"), "neg"))
	return [pos_sample, neg_sample]

