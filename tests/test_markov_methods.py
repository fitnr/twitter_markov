# twitter_markov - Create markov chain ("_ebooks") accounts on Twitter
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
from __future__ import unicode_literals
import unittest
import os
from os import path
import mock
import tweepy
import markovify.text
from twitter_markov import TwitterMarkov

try:
    basestring
except NameError:
    basestring = str

TIMELINE = [
    {
        "id": 1235,
        "id_str": "1235",
        "in_reply_to_user_id": None,
        "retweeted": False,
        "entities": {},
        "user": {"screen_name": "Random"},
        "text": "Lorem ipsum dolor sit amet"
    },
    {
        "id": 1234,
        "id_str": "1234",
        "in_reply_to_user_id": 1,
        "retweeted": False,
        "entities": {},
        "user": {"screen_name": "Random"},
        "text": "Quas doloremque velit deleniti unde commodi voluptatum incidunt."
    },
    {
        "id": 1233,
        "id_str": "1233",
        "retweeted": True,
        "in_reply_to_user_id": None,
        "entities": {},
        "user": {"screen_name": "Random"},
        "text": "Sunt, culpa blanditiis, nostrum doloremque illum excepturi quam."
    },
]


def fake_timeline():
    return [tweepy.Status.parse(tweepy.api, t) for t in TIMELINE]


class tweeter_markov_tests(unittest.TestCase):

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def setUp(self, _):
        self.corpus = path.join(path.dirname(__file__), 'data', 'tweets.txt')
        self.configfile = path.join(path.dirname(__file__), '..', 'bots.yaml')

        self.tm = TwitterMarkov('example_screen_name', [self.corpus], config=self.configfile,
                                dry_run=True, learn=False)

        self.tm.log.setLevel(100)

    def testCheckModels(self):
        for m in self.tm.models.values():
            self.assertIsInstance(m, markovify.text.NewlineText)

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def testTwitterMarkovCompose(self, *_):
        response = self.tm.compose(tries=150, max_overlap_ratio=2, max_overlap_total=100)

        assert isinstance(response, basestring)
        assert len(response) < 140

    @mock.patch.object(tweepy.API, 'mentions_timeline', return_value=fake_timeline())
    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def testTwitterMarkovReply(self, *_):
        r = self.tm.reply_all(tries=75, max_overlap_ratio=2, max_overlap_total=100)

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def testTwitterMarkovRecentlyTweeted(self, _):
        recents = self.tm.recently_tweeted
        assert recents[0] == TIMELINE[0]['text']

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def testTwitterMarkovCheckTweet(self, _):
        assert self.tm.check_tweet('') is False
        assert self.tm.check_tweet('badword') is False
        assert self.tm.check_tweet('Lorem ipsum dolor sit amet') is False
        assert self.tm.check_tweet('Lorem ipsum dolor sit amet!') is False
        assert self.tm.check_tweet('Lorem ipsum dolor set namet') is False
        assert self.tm.check_tweet('Random Text that should work totally') is True
        assert self.tm.check_tweet('@reply Random Text') is True

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def testTwitterMarkovLearn(self, _):
        tmp = path.join(path.dirname(__file__), 'data', 'tmp.txt')
        self.tm.learn_parent(corpus=tmp)

        try:
            with open(tmp) as f:
                result = f.read()

                assert TIMELINE[0]['text'] in result
                assert TIMELINE[1]['text'] in result
                assert TIMELINE[2]['text'] in result

        finally:
            os.remove(tmp)
