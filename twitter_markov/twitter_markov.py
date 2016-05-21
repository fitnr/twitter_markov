# -*- coding: utf-8 -*-
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
from __future__ import unicode_literals, print_function
import os
import re
import logging
from random import choice
from collections import Iterable
import Levenshtein
import markovify.text
import twitter_bot_utils as tbu
from wordfilter import Wordfilter
from . import checking

LEVENSHTEIN_LIMIT = 0.70


class TwitterMarkov(object):
    """
    Posts markov-generated text to twitter

    Args:
        screen_name (str): Twitter user account
        corpus (str): Text file to read to generate text.
        api (:ref:`tweepy.API <tweepy:tweepy.api>`): API to use to post tweets.
        dry_run (boolean): If set, TwitterMarkov won't actually post tweets.
        blacklist (Sequence): A list of words to avoid generating.
    """

    default_model = None
    _recently_tweeted = []

    def __init__(self, screen_name, corpus=None, **kwargs):
        if 'api' in kwargs:
            self.api = kwargs.pop('api')
        else:
            self.api = tbu.API(screen_name=screen_name, **kwargs)

        try:
            self.log = self.api.logger
        except AttributeError:
            self.log = logging.getLogger(screen_name)

        self.screen_name = screen_name
        self.config = self.api.config
        self.dry_run = kwargs.pop('dry_run', False)

        self.log.debug('screen name: %s', screen_name)
        self.log.debug("dry run: %s", self.dry_run)

        try:
            corpus = corpus or self.config.get('corpus')

            if isinstance(corpus, basestring):
                corpora = [corpus]

            elif isinstance(corpus, Iterable):
                corpora = corpus

            else:
                raise RuntimeError('Unable to find any corpora!')

            self.corpora = [b for b in corpora if b is not None]

            state_size = kwargs.get('state_size', self.config.get('state_size'))

            self.models = self._setup_models(self.corpora, state_size)

        except RuntimeError as e:
            self.log.error(e)
            raise e

        self.log.debug('models: %s', list(self.models.keys()))

        blacklist = kwargs.get('blacklist') or self.config.get('blacklist', [])
        self.wordfilter = Wordfilter()
        self.wordfilter.add_words(blacklist)

        self.log.debug('blacklist: %s terms', len(self.wordfilter.blacklist))

        if kwargs.get('learn', True):
            self.log.debug('learning...')
            self.learn_parent()

    def _setup_models(self, corpora, state_size):
        """
        Given a list of paths to corpus text files, set up markovify models for each.
        These models are returned in a dict, (with the basename as key).
        """
        self.log.debug('setting up models (state_size=%s)', state_size)
        out = dict()

        state_size = state_size or 2

        try:
            for pth in corpora:
                corpus_path = os.path.expanduser(pth)
                name = os.path.basename(corpus_path)

                with open(corpus_path) as m:
                    out[name] = markovify.text.NewlineText(m.read(), state_size=state_size)

        except AttributeError as e:
            self.log.error(e)
            self.log.error("Probably couldn't find the model file.")
            raise e

        except IOError as e:
            self.log.error(e)
            self.log.error('Error reading %s', corpus_path)
            raise e

        self.default_model = os.path.basename(corpora[0])

        return out

    @property
    def recently_tweeted(self):
        '''Returns recent tweets from ``self.screen_name``.'''
        if len(self._recently_tweeted) == 0:
            recent_tweets = self.api.user_timeline(self.screen_name, count=self.config.get('checkback', 20))
            self._recently_tweeted = [x.text for x in recent_tweets]

        return self._recently_tweeted

    def check_tweet(self, text):
        '''Check if a string contains blacklisted words or is similar to a recent tweet.'''
        text = text.strip().lower()

        if len(text) == 0:
            self.log.info("Rejected (empty)")
            return False

        if self.wordfilter.blacklisted(text):
            self.log.info("Rejected (blacklisted)")
            return False

        for line in self.recently_tweeted:
            if text in line.strip().lower():
                self.log.info("Rejected (Identical)")
                return False

            if Levenshtein.ratio(re.sub(r'\W+', '', text), re.sub(r'\W+', '', line.lower())) >= LEVENSHTEIN_LIMIT:
                self.log.info("Rejected (Levenshtein.ratio)")
                return False

        return True

    def reply_all(self, model=None, **kwargs):
        '''Reply to all mentions since the last time ``self.screen_name`` sent a reply tweet.'''
        mentions = self.api.mentions_timeline(since_id=self.api.last_reply)
        self.log.info('replying to all...')
        self.log.debug('mentions found: %d', len(mentions))

        if not self.dry_run:
            for status in mentions:
                self.reply(status, model, **kwargs)

    def reply(self, status, model=None, max_len=140, **kwargs):
        '''
        Compose a reply to the given ``tweepy.Status``.

        Args:
            status (tweepy.Status): status to reply to.
            model (str): name of model.
            max_len (int): maximum length of tweet (default: 140)
        '''
        self.log.debug('Replying to a mention')

        if status.user.screen_name == self.screen_name:
            self.log.debug('Not replying to self')
            return

        if self.wordfilter.blacklisted(status.text):
            self.log.debug('Not replying to tweet with a blacklisted word (%d)', status.id)
            return

        text = self.compose(model, max_len=max_len - 2 - len(status.user.screen_name), **kwargs)
        reply = '@{} {}'.format(status.user.screen_name, text)

        self.log.info(reply)
        self._update(reply, in_reply=status.id_str)

    def tweet(self, model=None, **kwargs):
        '''
        Post a tweet composed by "model" (or the default model).
        Most of these arguments are passed on to Markovify.

        Args:
            model (str): one of self.models
            max_len (int): maximum length of the output (default: 140).
            init_state (tuple): tuple of words to seed the model
            tries (int): (default: 10)
            max_overlap_ratio (float): Used for testing output (default: 0.7).
            max_overlap_total (int): Used for testing output (default: 15)
        '''
        model = self.models[model or self.default_model]
        text = self.compose(model, **kwargs)
        if text:
            self.log.info(text)
            self._update(text)

    def _update(self, tweet, in_reply=None):
        if not self.dry_run:
            self.api.update_status(status=tweet, in_reply_to_status_id=in_reply)

    def compose(self, model=None, max_len=140, **kwargs):
        '''
        Returns a string generated from "model" (or the default model).
        Most of these arguments are passed on to Markovify.

        Args:
            model (str): one of self.models
            max_len (int): maximum length of the output (max: 140, default: 140).
            init_state (tuple): tuple of words to seed the model
            tries (int): (default: 10)
            max_overlap_ratio (float): Used for testing output (default: 0.7).
            max_overlap_total (int): Used for testing output (default: 15)

        Returns:
            str
        '''
        model = model or self.models[self.default_model]
        max_len = min(140, max_len)
        self.log.debug('making sentence, max_len=%s, %s', max_len, kwargs)
        text = model.make_short_sentence(max_len, **kwargs)

        if text is None:
            self.log.error('model failed to generate a sentence')
            return

        # convert to unicode in Python 2
        if hasattr(text, 'decode'):
            text = text.decode('utf8')

        else:
            # Check tweet against blacklist and recent tweets
            if not self.check_tweet(text):
                # checked out: break and return
                text = self.compose(model=model, max_len=max_len, **kwargs)

        self.log.debug('TwitterMarkov: %s', text)

        return text

    def learn_parent(self, corpus=None, parent=None):
        '''
        Add recent tweets from the parent account (since the last time ``self.screen_name`` tweeted)
        to the corpus. This is subject to the filters described in ``bots.yaml``.
        '''
        parent = parent or self.config.get('parent')
        corpus = corpus or self.corpora[0]

        if not parent or not self.api.last_tweet:
            self.log.debug('Cannot teach: missing parent or tweets')
            return

        tweets = self.api.user_timeline(parent, since_id=self.api.last_tweet)

        try:
            gen = checking.generator(tweets,
                                     no_mentions=self.config.get('filter_mentions'),
                                     no_hashtags=self.config.get('filter_hashtags'),
                                     no_urls=self.config.get('filter_urls'),
                                     no_media=self.config.get('filter_media'),
                                     no_symbols=self.config.get('filter_symbols'),
                                     no_badwords=self.config.get('filter_parent_badwords', True),
                                     no_retweets=self.config.get('no_retweets'),
                                     no_replies=self.config.get('no_replies')
                                    )

            self.log.debug('%s is learning', corpus)

            with open(corpus, 'a') as f:
                f.writelines(tweet + '\n' for tweet in gen)

        except IOError as e:
            self.log.error('Learning failed for %s', corpus)
            self.log.error(e)
