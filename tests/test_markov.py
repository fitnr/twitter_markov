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
from cobe.brain import Brain
from twitter_markov import twitter_markov

class tweeter_markov_tests(unittest.TestCase):

    def setUp(self):
        self.brainfile = path.join(path.dirname(__file__), 'data', 'test.brain')
        self.configfile = path.join(path.dirname(__file__), '..', 'bots.yaml')

        brain = Brain(self.brainfile)
        del brain

    def testTwitterMarkovAttribs(self):
        tm = twitter_markov.Twitter_markov('example_screen_name', self.brainfile,
                                           config=self.configfile, dry_run=True, learn=False)

        assert type(tm) == twitter_markov.Twitter_markov

        assert hasattr(tm, 'screen_name')
        assert hasattr(tm, 'api')
        assert hasattr(tm, 'config')
        assert hasattr(tm, 'wordfilter')
        assert hasattr(tm, 'brains')
        del tm

    def testTwitterMarkovConfigBrain(self):
        tm = twitter_markov.Twitter_markov('example_screen_name', config=self.configfile,
                                           dry_run=True, learn=False)
        assert type(tm) == twitter_markov.Twitter_markov
        del tm

    def testTwitterMarkovListBrain(self):
        tm = twitter_markov.Twitter_markov('example_screen_name', [self.brainfile], config=self.configfile,
                                           dry_run=True, learn=False)
        assert type(tm) == twitter_markov.Twitter_markov
        del tm

    def testTwitterMarkovErrors(self):
        self.assertRaises(IOError, twitter_markov.Twitter_markov, 'example_screen_name', 'foo.brain')
