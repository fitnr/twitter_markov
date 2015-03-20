# Copyright 2014-2015 Neil Freeman contact@fakeisthenewreal.org
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

from twitter_bot_utils import helpers
import wordfilter
import re


def reply_checker(tweet):
    try:
        if tweet.in_reply_to_user_id:
            return False

    except AttributeError:
        try:
            if tweet.get('in_reply_to_user_id'):
                return False

        except AttributeError:

            try:
                if "@" == tweet[0]:
                    return False

            except AttributeError:
                pass

    return True


def rt_checker(tweet):
    try:
        if tweet.retweeted:
            return False

    except AttributeError:
        try:
            if tweet.get('retweeted_status'):
                return False

        except AttributeError:

            try:
                if "RT" in tweet[:2]:
                    return False

            except AttributeError:
                pass

    return True


def wf_checker(tweet):
    try:
        if wordfilter.blacklisted(tweet.text):
            return False

    except AttributeError:
        try:
            if wordfilter.blacklisted(tweet['text']):
                return False

        except (KeyError, TypeError):
            pass

    return True

def construct_tweet_checker(no_retweets=False, no_replies=False, no_badwords=True):
    '''Returns a tweet checker'''
    checks = []

    if no_retweets:
        checks.append(rt_checker)

    if no_replies:
        checks.append(reply_checker)

    if no_badwords:
        checks.append(wf_checker)

    def checker(tweet):
        for check in checks:
            if not check(tweet):
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
        # ignore strings
        if isinstance(tweet, str):
            text = tweet

        else:
            text = helpers.remove_entities(tweet, entitytypes)

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
