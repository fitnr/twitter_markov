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
