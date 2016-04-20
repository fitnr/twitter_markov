# Copyright 2014-2016 Neil Freeman contact@fakeisthenewreal.org
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import re
from twitter_bot_utils import helpers
import wordfilter


def generator(tweets, return_status=None, **kwargs):
    '''
    Returns a generator that returned a filtered input iterable of tweets or
    tweet-like objects (tweepy.Status objects or dictionaries).

    Args:
        tweets (iterable):
        return_status (boolean): If true, returns entire status with modified test
        no_retweets (boolean): Exclude retweets (e.g. strings beginning RT) (default False)
        no_replies (boolean): Exclude replies (e.g. strings beginning @screen_name) (default False)
        no_mentions (boolean): Filter out mentions (e.g. strings containing @screen_name) (default False)
        no_badwords (boolean): Exclude derogatory terms for people (default True)
        no_urls (boolean): filter out exclude urls (default False)
        no_hashtags (boolean): filter out hashtags (default False)
        no_media (boolean): filter out media (twitter objects only) (default False)
        no_symbols (boolean): filter out symbols (twitter objects only) (default False)
    '''

    tweet_checker = construct_tweet_checker(
        no_retweets=kwargs.get('no_retweets', False),
        no_replies=kwargs.get('no_replies', False),
        no_badwords=kwargs.get('no_replies', True)
    )

    tweet_filter = construct_tweet_filter(
        no_mentions=kwargs.get('no_mentions', False),
        no_urls=kwargs.get('no_urls', False),
        no_media=kwargs.get('no_media', False),
        no_hashtags=kwargs.get('no_hashtags', False),
        no_symbols=kwargs.get('no_symbols', False)
    )

    for status in tweets:
        if not tweet_checker(status):
            continue

        text = helpers.format_text(tweet_filter(status))

        if return_status:
            try:
                status.text = text
            except AttributeError:
                status['text'] = text

            yield status

        yield text


def isreply(tweet):
    try:
        return bool(tweet.in_reply_to_user_id)

    except AttributeError:
        try:
            return bool(tweet.get('in_reply_to_user_id') or tweet.get('in_reply_to_status_id'))

        except AttributeError:
            try:
                return tweet[0] == "@"

            except AttributeError:
                pass

    return False


def isretweet(tweet):

    try:
        return bool(tweet.retweeted)

    except AttributeError:
        try:
            return bool(tweet.get('retweeted_status') or tweet.get('retweeted_status_id'))

        except AttributeError:
            try:
                return tweet[:3].upper() == 'RT '

            except AttributeError:
                pass

    return False


def isblacklisted(tweet):
    try:
        return wordfilter.blacklisted(tweet.text)

    except AttributeError:
        try:
            return wordfilter.blacklisted(tweet['text'])

        except (KeyError, TypeError):
            return wordfilter.blacklisted(tweet)

    return False


def construct_tweet_checker(no_retweets=False, no_replies=False, no_badwords=True):
    '''Returns a tweet checker'''
    checks = []

    if no_retweets:
        checks.append(isretweet)

    if no_replies:
        checks.append(isreply)

    if no_badwords:
        checks.append(isblacklisted)

    def checker(tweet):
        return not any(isbad(tweet) for isbad in checks)

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
        # ignore strings
        try:
            text = helpers.remove_entities(tweet, entitytypes)
        except AttributeError:
            text = tweet

        # Older tweets don't have entities
        if no_urls:
            # regex stolen from http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
            text = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", '', text)

        if no_mentions:
            text = re.sub(r'@\w+', '', text)

        if no_hashtags:
            text = re.sub(r'#\w+', '', text)

        if no_symbols:
            text = re.sub(r'\$[a-zA-Z]+', '', text)

        return text

    return filterer
