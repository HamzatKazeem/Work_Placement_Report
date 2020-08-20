# -*- coding: utf-8 -*-
"""
Created on Sun Aug 16 15:09:02 2020

@author: Kazeem Hamzat
"""

# tweetutilities.py
"""Utility functions for interacting with Tweepy objects."""
import tweepy,re
import keys
import time
from geopy import OpenMapQuest
import numpy as np
import pandas as pd
import folium
import preprocessor as p
import nltk
#nltk.download('stopwords')
import imageio
from wordcloud import WordCloud  
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
from textblob import TextBlob
import matplotlib.pyplot as plt
from pymongo import MongoClient

class Utilities():
    
    
    def __init__(self):
        
        pass
    
   
        
    
    def get_API(self, wait=True, notify=True):
        
    
                                
        """Authenticate with Twitter and return API object."""
        # configure the OAuthHandler
        auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
        auth.set_access_token(keys.access_token, keys.access_token_secret)

        # get the API object
        return tweepy.API(auth, wait_on_rate_limit=wait, 
                  wait_on_rate_limit_notify=notify)


        # Method for used Retrieving Tweets using Twitter API Search Method
    def get_tweet_content(self,cursor):
            
        """Return list with data from tweet (API Search Method)."""
        highfield_tm=[]
    
        try:
            for tweet in cursor.items():
                
                             
                fields = {}    
                fields['Name'] = tweet.user.name
                fields['Twitter_handle'] = tweet.user.screen_name

        # get the tweet's text
                try:
                    fields['text'] = tweet.full_text
                    fields['location'] = tweet.user.location
            
                except: 
                    fields['text'] = tweet.text
                    fields['location'] = tweet.user.location
            
        # ignore retweets 
                if fields['text'].startswith('RT') or len(fields['text']) < 1:
                    pass              
            
                else:
                    highfield_tm.append(fields)
             
                return highfield_tm
        except tweepy.TweepError as e: 
            # print error (if any) 
            print("Error : " + str(e))
                
                
        # Method used to clean Tweets combining regular expression and pre-processor        
    def cleanTwits(self,tweets):
        
            p.set_options(p.OPT.URL,p.OPT.RESERVED,p.OPT.MENTION,p.OPT.NUMBER)

            for tweet in tweets:
                tweet['text']=p.clean(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", 
                                                                 tweet['text']).split()))
            return tweets    
        
        
        # Method used to find sentiment contained in the Tweet message
    def get_tweet_sentiment(self, tweets): 
        
        ''' 
        Utility function to classify sentiment of tweets
        using textblob's sentiment method 
        '''
        
        # create TextBlob object of tweet_list text 
        for item in tweets:
            item['sentiment']=' '
            blob = TextBlob(item['text'])
        # set sentiment 
            if blob.sentiment.polarity > 0:
                item['sentiment']= 'Positive'
            elif blob.sentiment.polarity == 0: 
                item['sentiment']= 'Neutral'
            else: 
                item['sentiment']= 'Negative'
        return tweets

        # Method for finding GPS Cordinates of Twitter User
    def get_geocodes(self,tweets):
        """Get the latitude and longitude for each tweet's location.
        Returns the number of tweets with invalid location data."""
        
        print('Getting coordinates for tweet locations...')
        geo = OpenMapQuest(api_key=keys.mapquest_key)  # geocoder
        bad_locations = 0  
    
        for tweet in tweets:
            processed = False
            delay = .1  # used if OpenMapQuest times out to delay next call
            while not processed:
                try:  # get coordinates for tweet['location']
                    geo_location = geo.geocode(tweet['location'])
                    processed = True
                except:  # timed out, so wait before trying again
                    print('OpenMapQuest service timed out. Waiting.')
                    time.sleep(delay)
                    delay += .1
    
            if geo_location:  
                tweet['latitude'] = geo_location.latitude
                tweet['longitude'] = geo_location.longitude
            else:  
                bad_locations += 1  # tweet['location'] was invalid
        
        print('Done geocoding')
        #return bad_locations
            
            
    def ukMap(self,tweets):
            
        df = pd.DataFrame(tweets)
        df=df.dropna()
        ukmap = folium.Map(location=[53.381100, -1.470100],
        tiles='Stamen Terrain',
        zoom_start=5, detect_retina=True)
        
        for t in df.itertuples():
            text = ': '.join([t.name, t.text])
            popup = folium.Popup(text, parse_html=True)
            marker = folium.Marker((t.latitude, t.longitude),
            popup=popup)
            marker.add_to(ukmap)
            ukmap.save('tweet_map.html')
            
    # def show_WordCloud1(self,tweets):
    #     df = pd.DataFrame(tweets)
    #     df=df.dropna()
    #     mask_image = imageio.imread('mask_oval.png')
    #     wordcloud = WordCloud(colormap='prism', mask=mask_image,background_color='white')
    #     wordcloud = wordcloud.generate(str(df['text']))
    #     wordcloud = wordcloud.to_file('high1.png')
    #     fig = plt.figure(1, figsize=(12, 12))
    #     plt.axis('off')
    #     if title: 
    #         fig.suptitle(title, fontsize=20)
    #         fig.subplots_adjust(top=2.3)
    #     plt.imshow(wordcloud)
    #     plt.show()
        
    def show_WordCloud(self,tweets):
        df = pd.DataFrame(tweets)
        df=df.dropna()
        mask_image = imageio.imread('mask_oval.png')
        wordcloud = WordCloud(colormap='prism', mask=mask_image,background_color='white')
        wordcloud = wordcloud.generate(str(df.text))
        wordcloud = wordcloud.to_file('high1.png')
        fig = plt.figure(1, figsize=(12, 12))
        plt.axis('off')
        if title: 
            fig.suptitle(title, fontsize=20)
            fig.subplots_adjust(top=2.3)
        plt.imshow(wordcloud)
        plt.show()
            