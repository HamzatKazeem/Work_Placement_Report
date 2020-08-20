# tweetlistener.py
"""TweetListener downloads tweets and stores them in MongoDB."""
import json
import tweepy

class TweetListener(tweepy.StreamListener):
    
    """Handles incoming Tweet stream."""

    def __init__(self, api, database, limit=10):
            """Create instance variables for tracking number of tweets."""
            self.dbase = database
            self.tweet_count = 0
            self.TWEET_LIMIT = limit  # 10,000 by default
            super().__init__(api)  # call superclass's init

    def on_connect(self):
        """Called when your connection attempt is successful, enabling 
       you to perform appropriate application tasks at that point.
       """
    print('Successfully connected to Twitter\n')

    def on_data(self, data):
        """Called when Twitter pushes a new tweet to you."""
        self.tweet_count += 1  # track number of tweets processed
        json_data = json.loads(data)  # convert string to JSON
        self.dbase.tweets.insert_one(json_data)  # store in tweets collection
        print(f'    Screen name: {json_data["user"]["name"]}') 
        print(f'     Created at: {json_data["created_at"]}') 
        print(f'Tweets received: {self.tweet_count}')  

       # if TWEET_LIMIT is reached, return False to terminate streaming
        return self.tweet_count != self.TWEET_LIMIT
    def on_error(self, status):
        print(status)
        return True
