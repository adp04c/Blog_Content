#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

# Twitter keys for use in twitter API
consumer_key = 'nuBcUpz7hG8hdVPgwcciLOaia'
consumer_secret = 'Mbw6ynD1AWUOB6rCG3Sb7KukpUSJ11WvRIXyMSIHXQ6haVb3yX'
access_token = '2841909646-2h7XY0uG2L3uJLysvNHHS59mIIw8Xfxexsj3CWh'
access_secret = 'Z6kB9xjGjIfCStd6RjkMt1MxZLCh1uyE7656pynfsrFep'


def get_all_tweets(screen_name, sex):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify=True)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		# print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		# print "...%s tweets downloaded so far" % (len(alltweets))

	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [] # Initializing a master list to store all the tweet information
	
	'''
	Looping through tweets to extract desired info, multiple try-excepts are needed to deal with
	the fact that some of the desired varialbes are stored in nested dictionaries, but when
	they are not present in a tweet they cause an IndexError
	'''
	for tweet in alltweets: 
	    try:
	        outtweets.append([screen_name, sex, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), 
	        tweet.favorite_count, tweet.retweet_count, tweet.entities["hashtags"][0]["text"], 
	        tweet.entities["user_mentions"][0]["screen_name"]])
	    except (IndexError):
	        try:
	        	outtweets.append([screen_name, sex, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), 
	            tweet.favorite_count, tweet.retweet_count, tweet.entities["hashtags"][0]["text"], 
	            None])
	        except (IndexError):
	            try:
	                outtweets.append([screen_name, sex, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), 
	                tweet.favorite_count, tweet.retweet_count, None, 
	                tweet.entities["user_mentions"][0]["screen_name"]])
	            except (IndexError):
	                outtweets.append([screen_name, sex, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), 
	                tweet.favorite_count, tweet.retweet_count, None, None])
	#outtweets = map(lambda x: x.encode('utf-8'), outtweets)
	#[x.encode('utf-8') for x in outtweets]
	                       	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["Twitter_Handle", "Sex", "Tweet_id","Created_at","Text",
		    "Favorite_count", "Retweet_count", "Hashtags", "User_mentions"])
		try:
		    writer.writerows(outtweets)
		except:
		    print type(outtweets)
	
	pass


#if __name__ == '__main__':
	#pass in the username of the account you want to download