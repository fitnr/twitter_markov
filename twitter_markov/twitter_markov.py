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
from collections import Iterable
import logging
import Levenshtein
import markovify.text
import twitter_bot_utils as tbu
from wordfilter import Wordfilter
from . import checking

LEVENSHTEIN_LIMIT = 0.70

class Twitter_markov(object):

    """Posts markov-generated text to twitter"""

    default_model = None
    _recently_tweeted = []

    def __init__(self, screen_name, corpus=None, **kwargs):

        self.screen_name = screen_name

        self.api = kwargs.get('api', tbu.api.API(screen_name, **kwargs))

        self.config = self.api.config

        self.logger = logging.getLogger(screen_name)

        self.logger.debug('{}, {}, {}'.format(screen_name, corpus, kwargs))

        try:
            corpus = corpus or self.config.get('corpus')

            if isinstance(corpus, basestring):
                corpora = [corpus]

            elif isinstance(corpus, Iterable):
                corpora = corpus

            else:
                raise RuntimeError('Unable to find any corpora!')

            self.corpora = [b for b in corpora if b is not None]
            self.logger.debug('corpora: {}'.format(self.corpora))

            self.models = self._setup_models(self.corpora)

        except RuntimeError as e:
            self.logger.error(e)
            raise e

        self.logger.debug('models: {0}'.format(list(self.models.keys())))

        self.dry_run = kwargs.get('dry_run', False)

        self.wordfilter = Wordfilter()
        self.wordfilter.add_words(self.config.get('blacklist', []))

        if kwargs.get('learn', True):
            self.learn_parent()

    def _setup_models(self, corpora):
        """
        Given a list of paths to corpus text files, set up markovify models for each.
        These models are returned in a dict, (with the basename as key).
        """
        self.logger.debug('setting up models')
        out = dict()

        try:
            for pth in corpora:
                corpus_path = os.path.expanduser(pth)
                name = os.path.basename(corpus_path)

                with open(corpus_path) as m:
                    out[name] = markovify.text.NewlineText(m.read(), state_size=3)

        except AttributeError as e:
            self.logger.error(e)
            self.logger.error("Probably couldn't find the model file.")
            raise e

        except IOError as e:
            self.logger.error(e)
            self.logger.error('Error reading {}'.format(corpus_path))
            raise e

        self.default_model = os.path.basename(corpora[0])

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

            if Levenshtein.ratio(re.sub(r'\W+', '', text), re.sub(r'\W+', '', line.lower())) >= LEVENSHTEIN_LIMIT:
                self.logger.info("Rejected (Levenshtein.ratio)")
                return False

        return True

    def reply_all(self, model=None, **kwargs):
        mentions = self.api.mentions_timeline(since_id=self.api.last_reply)
        self.logger.debug('{0} mentions found'.format(len(mentions)))

        for status in mentions:
            self.reply(status, model, **kwargs)

    def reply(self, status, model=None, **kwargs):
        self.logger.debug('Replying to a mention')

        if status.user.screen_name == self.screen_name:
            self.logger.debug('Not replying to self')
            return

        text = self.compose(model, max_len=138 - len(status.user.screen_name), **kwargs)

        reply = '@' + status.user.screen_name + ' ' + text

        self.logger.info(reply)
        self._update(reply, in_reply=status.id_str)

    def tweet(self, model=None, **kwargs):
        self.logger.debug('tweeting')

        text = self.compose(model, **kwargs)

        self.logger.info(text)
        self._update(text)

    def _update(self, tweet, in_reply=None):
        if not self.dry_run:
            self.api.update_status(status=tweet, in_reply_to_status_id=in_reply)

    def compose(self, model=None, max_len=140, **kwargs):
        '''Format a tweet with a reply.'''

        max_len = min(140, max_len)

        model = self.models[model or self.default_model]

        text = ''

        while True:
            sentence = model.make_sentence(**kwargs)

            if not sentence:
                continue

            if len(text + sentence) < max_len - 1:
                text = text + ' ' + sentence

            else:
                break

        self.logger.debug('text> ' + text)

        return text

    def learn_parent(self, corpus=None, parent=None):
        '''Add recent tweets from @parent to corpus'''
        parent = parent or self.config.get('parent')
        corpus = corpus or self.corpora[0]

        if not parent or not self.api.last_tweet:
            self.logger.debug('Cannot teach: missing parent or tweets')
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

            self.logger.debug('{} is learning'.format(corpus))

            with open(corpus, 'a') as f:
                f.writelines(tweet + '\n' for tweet in gen)

        except IOError as e:
            self.logger.error('Learning failed for {}'.format(corpus))
            self.logger.error(e)

