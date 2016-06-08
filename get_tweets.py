#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler("EZ5jWl0nSq5NtmEdnZhF5DmJV",  "kGlSXAoCHE5mVdVxu4SrQsbTxdZfXfcxCxhi6KKMOvewk80G7V")
	auth.set_access_token("359884653-a5Ciw6AL9RivBGn0JlSAaEa1Sat6P0Yc63E6mpw7", "tKCO2rC9fWZ4xcpOBEeXTagkzohoFC04eM70dbjWH1sh6")
	api = tweepy.API(auth)
	
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
		print "getting tweets before %s" % (oldest)
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print "...%s tweets downloaded so far" % (len(alltweets))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8"), tweet.retweet_count, tweet.in_reply_to_user_id, tweet.place, tweet.in_reply_to_screen_name, tweet.source] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'wb') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text","retweet_count", "in_reply_to_user_id", "place", "in_reply_to_screen_name", "source"])
		writer.writerows(outtweets)
	
	pass

	#Twitter handle from the top 3 exec at AudienseCo and AudienseCo account ( @javierburon / @aartiles24 / @serrita22)
if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("twitter_handle")
