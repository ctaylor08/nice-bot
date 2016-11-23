#usr/bin/python3
import os
import configparser
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'nicebot_conf.ini'))
twitter_auth = config['twitter_auth']

class Listener(StreamListener):

    def on_data(self, data):
        print(data)
        return True
        
    def on_error(self, status):
        print(status)
        
auth = OAuthHandler(twitter_auth['ckey'], twitter_auth['csecret'])
auth.set_access_token(twitter_auth['atkn'], twitter_auth['asecret'])

twitterStream = Stream(auth, Listener())
twitterStream.filter(track=['car'])