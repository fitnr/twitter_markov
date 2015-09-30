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

from __future__ import unicode_literals, print_function
import os
import re
import logging
import Levenshtein
from cobe import scoring
from cobe.brain import Brain
import twitter_bot_utils as tbu
from wordfilter import Wordfilter
from . import checking


class Twitter_markov(object):

    """Posts markov-generated text to twitter"""

    default_brain = None
    _recently_tweeted = []

    def __init__(self, screen_name, brains=None, **kwargs):

        self.screen_name = screen_name

        self.api = kwargs.get('api', tbu.api.API(screen_name, **kwargs))

        self.config = self.api.config

        self.logger = logging.getLogger(screen_name)

        try:
            if isinstance(brains, str):
                brains = [brains]

            if not brains:
                brains = [self.config.get('brain')] + self.config.get('brains', [])
                brains = [b for b in brains if b is not None]

            self.brains = self._setup_brains(brains)

        except (IOError, IndexError, RuntimeError) as e:
            self.logger.error('Feed me brains: unable to find any brains!')
            raise e

        self.logger.debug('Brains: {0}'.format(list(self.brains.keys())))

        self.dry_run = kwargs.get('dry_run', False)

        self.wordfilter = Wordfilter()
        self.wordfilter.add_words(self.config.get('blacklist', []))

        if kwargs.get('learn', True):
            self.learn_parent()

    def _setup_brains(self, brains):
        self.logger.debug('setting up brains')
        out = dict()

        try:
            for pth in brains:
                brainpath = os.path.expanduser(pth)
                name = os.path.basename(brainpath).replace('.brain', '')

                if not os.path.exists(brainpath):
                    raise IOError("Brain file '{0}' missing".format(brainpath))

                out[name] = Brain(brainpath)
                out[name].scorer.add_scorer(2.0, scoring.LengthScorer())

        except AttributeError as e:
            self.logger.error(e)
            self.logger.error("Probably couldn't find the brain file.")
            raise e

        except IOError as e:
            self.logger.error(e)
            self.logger.error(brains)
            raise e

        self.default_brain = os.path.basename(brains[0]).replace('.brain', '')

        return out

    @property
    def recently_tweeted(self):
        if len(self._recently_tweeted) == 0:
            recent_tweets = self.api.user_timeline(self.screen_name, count=self.config.get('checkback', 20))
            self._recently_tweeted = [x.text for x in recent_tweets]

        return self._recently_tweeted

    def check_tweet(self, text):
        text = text.strip().lower()

        if len(text) == 0:
            self.logger.info("Rejected (empty)")
            return False

        if self.wordfilter.blacklisted(text):
            self.logger.info("Rejected (blacklisted)")
            return False

        for line in self.recently_tweeted:
            if text in line.strip().lower():
                self.logger.info("Rejected (Identical)")
                return False

            if Levenshtein.ratio(re.sub(r'\W+', '', text), re.sub(r'\W+', '', line.lower())) >= 0.70:
                self.logger.info("Rejected (Levenshtein.ratio)")
                return False

        return True

    def reply_all(self, brainname=None):
        mentions = self.api.mentions_timeline(since_id=self.api.last_reply)
        self.logger.debug('{0} mentions found'.format(len(mentions)))

        for status in mentions:
            self.reply(status, brainname)

    def reply(self, status, brainname=None):
        self.logger.debug('Replying to a mention')

        if status.user.screen_name == self.screen_name:
            self.logger.debug('Not replying to self')
            return

        catalyst = tbu.helpers.format_status(status)
        text = self.compose(catalyst, brainname, max_len=138 - len(status.user.screen_name))

        reply = '@' + status.user.screen_name + ' ' + text

        self.logger.info(reply)
        self._update(reply, in_reply=status.id_str)

    def tweet(self, catalyst='', brainname=None):
        self.logger.debug('tweeting')

        text = self.compose(catalyst, brainname)

        self.logger.info(text)
        self._update(text)

    def _update(self, tweet, in_reply=None):
        if not self.dry_run:
            self.api.update_status(status=tweet, in_reply_to_status_id=in_reply)

    def compose(self, catalyst='', brainname=None, max_len=140):
        '''Format a tweet with a reply from brainname'''

        max_len = min(140, max_len)

        brainname = brainname or self.default_brain
        brain = self.brains[brainname]

        reply = brain.reply(catalyst, max_len=max_len)

        self.logger.debug('input> ' + catalyst)
        self.logger.debug('reply> ' + reply)

        if len(reply) <= 140:
            return reply

        else:
            self.logger.debug('Tweet was too long, trying again')
            return self.compose(catalyst, brainname, max_len)

    def learn_parent(self, brainname=None):
        parent = self.config.get('parent')

        last_tweet = self.api.last_tweet

        if not parent or not last_tweet:
            return

        tweet_filter = checking.construct_tweet_filter(
            no_mentions=self.config.get('filter_mentions'),
            no_hashtags=self.config.get('filter_hashtags'),
            no_urls=self.config.get('filter_urls'),
            no_media=self.config.get('filter_media'),
            no_symbols=self.config.get('filter_symbols')
        )

        tweet_checker = checking.construct_tweet_checker(
            no_badwords=self.config.get('filter_parent_badwords', True),
            no_retweets=self.config.get('no_retweets'),
            no_replies=self.config.get('no_replies')
            )

        tweets = self.api.user_timeline(parent, since_id=last_tweet)

        brain = brainname or self.default_brain

        for status in tweets:
            if not tweet_checker(status):
                continue

            text = tweet_filter(status)

            text = tbu.helpers.format_text(text)

            self.brains[brain].learn(text)
