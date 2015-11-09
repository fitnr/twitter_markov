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

from __future__ import unicode_literals
import unittest
from os import path
import markovify.text
from twitter_markov import twitter_markov

class tweeter_markov_tests(unittest.TestCase):

    def setUp(self):
        self.corpus = path.join(path.dirname(__file__), 'data', 'tweets.txt')
        self.configfile = path.join(path.dirname(__file__), '..', 'bots.yaml')


    def testTwitterMarkovAttribs(self):
        tm = twitter_markov.Twitter_markov('example_screen_name', self.corpus,
                                           config=self.configfile, dry_run=True, learn=False)

        assert type(tm) == twitter_markov.Twitter_markov

        assert hasattr(tm, 'screen_name')
        assert hasattr(tm, 'api')
        assert hasattr(tm, 'config')
        assert hasattr(tm, 'wordfilter')
        del tm

    def testTwitterMarkovConfigCorpus(self):
        tm = twitter_markov.Twitter_markov('example_screen_name', config=self.configfile,
                                           dry_run=True, learn=False)
        assert type(tm) == twitter_markov.Twitter_markov
        del tm

    def testTwitterMarkovListCorpus(self):
        tm = twitter_markov.Twitter_markov('example_screen_name', [self.corpus], config=self.configfile,
                                           dry_run=True, learn=False)
        assert type(tm) == twitter_markov.Twitter_markov
        del tm

    def testTwitterMarkovErrors(self):
        self.assertRaises(IOError, twitter_markov.Twitter_markov, 'example_screen_name', 'foo')

    def testTwitterMarkovModel(self):
        tm = twitter_markov.Twitter_markov('example_screen_name', self.corpus,
                                           config=self.configfile, dry_run=True, learn=False)

        assert isinstance(tm.models['tweets.txt'], markovify.text.Text)

        string = tm.compose(tries=50, max_overlap_ratio=2, max_overlap_total=100)
        assert isinstance(string, basestring)
        assert len(string) > 0


if __name__ == '__main__':
    unittest.main()
