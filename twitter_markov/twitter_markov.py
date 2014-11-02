import Levenshtein
import os
import re
import db_manager
from HTMLParser import HTMLParser
from botconfig import read_config
from cobe.brain import Brain
import datetime
from twitter_bot_utils import api

# load blacklist
blacklist = read_config()['blacklist']
# get all our tweets
lines = db_manager.get_tweets()

today_is_friday = datetime.date.today().weekday() == 4

# check tweet vs text files and reject if >70% the same as a tweet up in there or if it contains a blacklisted word
# also reject any blank tweets (this condition can happen when filtering urls)

class Twitter_markov(api.API):
    """docstring for Twitter_markov"""
    def __init__(self, screen_name, **kwargs):
        super(Twitter_markov, self).__init__(screen_name, **kwargs)

        

def check_tweet(content):
    for k in config['blacklist']:
        # makes the blacklist case insensitive
        if k.lower() in content.lower():
            print "[debug] Rejected (blacklist): " + content
            return False
    for line in lines:
        if Levenshtein.ratio(re.sub(r'\W+', '', content.lower()), re.sub(r'\W+', '', line.lower())) >= 0.70:
            print "[debug] Rejected (Levenshtein.ratio): " + content
            return False
        if content.strip(' \t\n\r').lower() in line.strip(' \t\n\r').lower():
            print "[debug] Rejected (Identical): " + content
            return False
    if "#ff" in content and not today_is_friday:
        print "[debug] Rejected (#ff)"
        return False
    if len(content) == 0:
        print "[debug] Rejected (empty)"
        return False
    return True

# filter out url from tweet and then remove whitespace around the edges


def smart_truncate(content, length=140):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]


def create_tweet(catalyst=''):
    b = Brain(os.path.join(os.path.dirname(__file__), 'cobe.brain'))

    # get a reply from brain, encode as UTF-8
    i = 0

    while True:
        tweet = b.reply(catalyst).encode('utf-8', 'replace')
        if(config['filter_urls']):
            tweet = remove_url(tweet)
        tweet = smart_truncate(tweet)
        # make sure we're not tweeting something close to something else in the txt files
        # or we can just give up after 100 tries
        if check_tweet(tweet) or i >= 100:
            break
        i += 1

    tweet = HTMLParser().unescape(tweet)

    # put the tweet in the db
    db_manager.insert_tweet(tweet)

    return tweet
