#usr/bin/python3
import os
import configparser
import json
import logging
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

    def on_data(self, data, log=True, print_it=True):
        all_data = json.loads(data)
        tweet = all_data.get('text')
        if tweet and not tweet.startswith('RT '):
            mean = meany.meany(tweet)
            mean.how_mean()
            if mean.mean_lvl and mean.mean_lvl > 6:
                username = all_data['user']['screen_name']
                log_msg = '{} sent a tweet with meanness level {}:\n\t{}\n'.format(username,  mean.mean_lvl, tweet)
                if log:
                    logging.info(log_msg)
                if print_it:
                    print(log_msg)
                return True
        
    def on_error(self, status):
        logging.warning(status)
        
auth = OAuthHandler(twitter_auth['ckey'], twitter_auth['csecret'])
auth.set_access_token(twitter_auth['atkn'], twitter_auth['asecret'])

twitterStream = Stream(auth, Listener())
def enable():
    try:
        twitterStream.filter(track=config['mean_stuff']['words'].split(','))
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
    enable()