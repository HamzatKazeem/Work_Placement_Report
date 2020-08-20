# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 23:11:46 2020

@author: Kazeem Hamzat
"""

# sentimentlisener.py
"""Script that searches for tweets that match a search string
and tallies the number of positive, neutral and negative tweets."""

from tweetutilities import Utilities
from tweetlistener import TweetListener
import tweepy
class SentimentListener :
       
    def __init__(self):
        
        self.pointer = Utilities()
        self.search_key=''
                
    def main(self):
        #global web
        #linker= web.Utilities()
        api = self.pointer.get_API()
        self.search_key=['askhighfield']
        cursor=tweepy.Cursor(api.search,self.search_key,count=200,tweet_mode='extended')
    
        # Get the Query to search Tweets
        tweets =self.pointer.get_tweet_content(cursor)
    
        # Obtain the sentiments of Tweets
        self.pointer.get_tweet_sentiment(tweets)
        
        # Obtain the GPS coordinates of Twitter User
        # self.pointer.get_geocodes(tweets)
        
        # Method to fit the Tweets on map to show Twitter locations
        #self.pointer.ukMap(tweets)
        
        # Method to show topical words discussed about Highfield
        #self.pointer.show_WordCloud(tweets)
        
        # Method to show topical words discussed about Highfield
        print(self.pointer.twoplus2(10,5))


# call main if this file is executed as a script
if __name__ == '__main__':
    mainSentimentListener=SentimentListener()
    mainSentimentListener.main()