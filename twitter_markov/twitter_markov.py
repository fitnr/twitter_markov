import os
import re
import logging
import Levenshtein
from cobe import scoring
from cobe.brain import Brain
from twitter_bot_utils import api, helpers
from wordfilter import Wordfilter
from . import checking

class Twitter_markov(api.API):

    """docstring for Twitter_markov"""

    default_brain = None
    _recently_tweeted = []

    def __init__(self, screen_name, brains, **kwargs):
        super(Twitter_markov, self).__init__(screen_name, **kwargs)

        self.logger = logging.getLogger(screen_name)

        try:
            if isinstance(brains, list):
                brains = [self.config['brains']]
            else:
                brains = self.config['brains']

            self.brains = self.setup_brains(brains)

        except IndexError:
            self.logger.error('Unable to find any brains!')

        self.logger.debug('Brains: {0}'.format(self.brains.keys()))

        self.dry_run = kwargs.get('dry_run', False)

        self.wordfilter = Wordfilter()
        self.wordfilter.add_words(self.config['blacklist'])

        if not kwargs.get('no_learn'):
            self.learn_parent()

    def setup_brains(self, brains):
        self.logger.debug('setting up brains')
        out = dict()

        try:
            for pth in brains:
                brainpath = os.path.expanduser(pth)
                name = os.path.basename(brainpath).replace('.brain', '')

                out[name] = Brain(brainpath)
                out[name].scorer.add_scorer(2.0, scoring.LengthScorer())

        except Exception as e:
            self.logger.error(out)
            raise e

        self.default_brain = os.path.basename(brains[0]).replace('.brain', '')

        return out

    @property
    def recently_tweeted(self):
        if len(self._recently_tweeted) == 0:
            recent_tweets = self.user_timeline(self.screen_name, count=self.config.get('checkback', 20))
            self._recently_tweeted = [x.text for x in recent_tweets]

        return self._recently_tweeted

    def check_tweet(self, text):
        if len(text) == 0:
            self.logger.info("Rejected (empty)")
            return False

        text = text.strip().lower()

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

    def reply_all(self, brain=None):
        mentions = self.mentions_timeline(since_id=self.last_reply)
        self.logger.debug('{0} mentions found'.format(len(mentions)))

        for status in mentions:
            self.reply(status, brain)

    def reply(self, status, brainname=None):
        self.logger.debug('Replying to a mention')

        text = self.compose(status.text, brainname, max_len=138 - len(status.screen_name))

        reply = u'@' + status.user.screen_name + ' ' + text

        if not self.dry_run:
            self.update_status(reply, in_reply_to_status_id=status.id_str)

        self.logger.debug(reply)

    def tweet(self, catalyst='', brainname=None):
        self.logger.debug('tweeting')

        text = self.compose(catalyst, brainname)

        if not self.dry_run:
            self.update_status(text)

        self.logger.debug(text)

    def compose(self, catalyst, brain=None, max_len=140):
        '''Format a tweet with a reply from a brain'''

        max_len = min(140, max_len)

        brainname = brain or self.default_brain
        brain = self.brains[brainname]

        catalyst = helpers.format_status(catalyst)

        reply = brain.reply(catalyst, max_len=max_len)

        self.logger.debug(u'input> ' + catalyst)
        self.logger.debug(u'reply> ' + reply)

        if len(reply) <= 140:
            return reply

        else:
            self.logger.debug('Tweet was too long, trying again')
            return self.compose(catalyst, brainname, max_len)


    def learn_parent(self, brain=None):
        parent = self.config.get('parent')

        if not parent:
            return

        tweet_gate = checking.construct_tweet_checker(
            no_retweets=self.config.get('no_retweets'),
            no_replies=self.config.get('no_replies')
            )

        tweet_filter = checking.construct_tweet_filter(
            no_mentions=self.config.get('no_mentions'),
            no_hashtags=self.config.get('no_hashtags'),
            no_urls=self.config.get('no_urls'),
            no_media=self.config.get('no_media'),
            no_symbols=self.config.get('no_symbols')
            )

        tweets = self.user_timeline(parent, since_id=self.last_tweet)

        brain = brain or self.default_brain

        for status in tweets:
            if not tweet_gate(status):
                continue

            text = tweet_filter(status)

            text = helpers.format_text(text)

            self.brains[brain].learn(text)
