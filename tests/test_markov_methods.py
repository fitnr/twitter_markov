# twitter_markov - Create markov chain ("_ebooks") accounts on Twitter
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

import unittest
from os import path
import mock
import tweepy
from cobe.brain import Brain
from twitter_markov import twitter_markov

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
        self.brainfile = path.join(path.dirname(__file__), 'data', 'test.brain')
        self.configfile = path.join(path.dirname(__file__), '..', 'bots.yaml')

        brain = Brain(self.brainfile)
        del brain

        self.tm = twitter_markov.Twitter_markov('example_screen_name', [self.brainfile], config=self.configfile,
                                                dry_run=True)

    def testTwitterMarkovCompose(self):
        response = self.tm.compose()

        self.assertEqual(type(response), unicode)
        assert len(response) < 140

        tweeted = self.tm.tweet()
        assert tweeted == None

    @mock.patch.object(tweepy.API, 'mentions_timeline', return_value=fake_timeline())
    def testTwitterMarkovReply(self, _):
        r = self.tm.reply_all()
        assert r == None

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def testTwitterMarkovRecentlyTweeted(self, _):
        recents = self.tm.recently_tweeted
        assert recents[0] == TIMELINE[0]['text']

    @mock.patch.object(tweepy.API, 'user_timeline', return_value=fake_timeline())
    def testTwitterMarkovCheckTweet(self, _):
        assert self.tm.check_tweet('') == False
        assert self.tm.check_tweet('badword') == False
        assert self.tm.check_tweet('Lorem ipsum dolor sit amet') == False
        assert self.tm.check_tweet('Lorem ipsum dolor sit amet!') == False
        assert self.tm.check_tweet('Lorem ipsum dolor set namet') == False
        assert self.tm.check_tweet('Random Text that should work totally') == True
        assert self.tm.check_tweet('@reply Random Text') == True
