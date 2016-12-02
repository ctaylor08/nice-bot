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

from nltk.corpus import stopwords
config['random_stuff']['words'] = ','.join(list(set(stopwords.words('english'))))

class Listener(StreamListener):

    def __init__(self, log=True):
        self.log = log

    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data.get('text')
        if tweet and '@' in tweet and not tweet.startswith('RT '):
            tweet_body = tweet.replace('\n', ' ').strip()
            tweet_text = re.sub(r'([@|#][\S]{1,})|(http[s|]:\/\/[\S]{1,})', '', tweet_body)
            mean = meany.meany(tweet_text)
            mean.is_mean()
            if mean.mean:
                print('### MEAN ###\n')
                print(tweet_body)
                print('')
            elif not mean.mean:
                print('### NOT MEAN ###\n')
                print(tweet_body)
                print('')
            if self.log:
                logging.info(str(mean.mean) + ' <<< ' + tweet_body + ' >>>')
            return True
        
    def on_error(self, status):
        logging.warning(status)
        
auth = OAuthHandler(twitter_auth['ckey'], twitter_auth['csecret'])
auth.set_access_token(twitter_auth['atkn'], twitter_auth['asecret'])


def enable_stream(which='nice_stuff', **kwargs):
    if which not in ['nice_stuff', 'mean_stuff', 'random_stuff']:
        raise ValueError("which param must be either 'nice_stuff', 'mean_stuff', or 'random_stuff'")
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
    enable_stream(which='random_stuff')