#usr/bin/python3
import os
import configparser
import json
import logging
import re
from tweepy import Stream, OAuthHandler
from tweepy.streaming import StreamListener
try:
    import meany
except ImportError:
    from . import meany

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'nicebot_conf.ini'))
twitter_auth = config['twitter_auth']
logging.basicConfig(filename='nicelog.log', filemode='w', level=logging.INFO)


class Listener(StreamListener):

    def __init__(self, log=True, just_tweets=False, print_it=True):
        self.log = log
        self.just_tweets = just_tweets
        self.print_it = print_it
        self.tweet_count = 0

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data.get('text')
        if tweet and '@' in tweet and not tweet.startswith('RT '):
            tweet_body = tweet.replace('\n', ' ').strip()
            mean = meany.meany(tweet_body)
            mean.how_mean()
            if mean.mean_lvl and mean.mean_lvl > 6:
                if self.just_tweets:
                    log_msg = re.sub(r'([@|#][\S]{1,})|(http[s|]:\/\/[\S]{1,})', '', tweet_body)
                    logging.info(log_msg)
                    self.tweet_count += 1
                elif self.log and not self.just_tweets:
                    username = all_data['user']['screen_name']
                    log_msg = '{} sent a tweet with meanness level {}:\n\t{}\n'.format(username,  mean.mean_lvl, tweet)
                    logging.info(log_msg)
                    self.tweet_count += 1
                if log_msg and self.print_it:
                    print('##### mean tweet {} #####\n'.format(self.tweet_count))
                    print(log_msg)
                    print('\n')
                return True
        
    def on_error(self, status):
        logging.warning(status)
        
auth = OAuthHandler(twitter_auth['ckey'], twitter_auth['csecret'])
auth.set_access_token(twitter_auth['atkn'], twitter_auth['asecret'])


def enable_stream(**kwargs, which='nice_stuff'):
    if which not in ['nice_stuff', 'mean_stuff']:
        raise ValueError("which param must be either 'nice' or 'mean'")
    twitterStream = Stream(auth, Listener(**kwargs))
    try:
        twitterStream.filter(track=config[which]['words'].split(','))
    except KeyboardInterrupt:
        print('\nnicebot disabled')
        
        
if __name__ == '__main__':
    import time
    print("Let's kill em with kindness!")
    print("- press Ctrl+c to disable at anytime")
    print("- Starting in")
    s = 1
    for sec in ['5','4','3','2','1']:
        print(' '*s + sec)
        s += 1
        time.sleep(1)
    enable_stream(just_tweets=True, print_it=True)