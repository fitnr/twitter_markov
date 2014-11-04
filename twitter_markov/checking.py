import tweepy
from twitter_bot_utils import helpers
import re


def construct_tweet_checker(no_retweets=False, no_replies=False):
    '''Returns a tweet checker'''
    def checker(tweet):
        if isinstance(tweet, tweepy.Status):
            try:
                if no_retweets and tweet.retweeted:
                    return False
            except AttributeError:
                pass

            try:
                if no_replies and tweet.in_reply_to_user_id:
                    return False
            except AttributeError:
                pass

        else:
            if no_retweets and tweet.get('retweeted_status'):
                return False

            if no_replies and tweet.get('in_reply_to_user_id'):
                return False

        return True

    return checker


def construct_tweet_filter(no_mentions=False, no_urls=False, no_media=False, no_hashtags=False, no_symbols=False):
    '''returns a filter for tweet text'''

    entitytypes = []

    if no_mentions:
        entitytypes.append('user_mentions')

    if no_hashtags:
        entitytypes.append('hashtags')

    if no_urls:
        entitytypes.append('urls')

    if no_media:
        entitytypes.append('media')

    if no_symbols:
        entitytypes.append('symbols')

    def filterer(tweet):
        text = helpers.remove_entities(tweet, entitytypes)

        # Older tweets don't have entities
        if no_urls and text.find('http') > -1:
            # regex stolen from http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
            text = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", '', text)

        if no_mentions and text.find('@') > -1:
            text = re.sub(r'@\w+', '', text)

        if no_hashtags and text.find('#') > -1:
            text = re.sub(r'#\w+', '', text)

        return text

    return filterer
