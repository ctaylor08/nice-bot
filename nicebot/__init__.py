#usr/bin/python3
import os
import configparser
import json
import time
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'nicebot_conf.ini'))
twitter_auth = config['twitter_auth']

class Listener(StreamListener):

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data.get('text')
        if tweet and not tweet.startswith('RT '):
            username = all_data['user']['screen_name']
            print('{} tweeted:\n\t{}\n'.format(username, tweet))
            return True
        
    def on_error(self, status):
        print(status)
        
auth = OAuthHandler(twitter_auth['ckey'], twitter_auth['csecret'])
auth.set_access_token(twitter_auth['atkn'], twitter_auth['asecret'])

twitterStream = Stream(auth, Listener())
def enable():
    try:
        twitterStream.filter(track=['cunt', 'nigger', 'spic', 'kike', 'felch'])
    except KeyboardInterrupt:
        print('\nnicebot disabled')
        
if __name__ == '__main__':
    print("Let's kill em with kindness!")
    print("- press Ctrl+c to disable at anytime")
    print("- Starting in")
    s = 1
    for sec in ['5','4','3','2','1']:
        print(' '*s + sec)
        s += 1
        time.sleep(1)
    enable()