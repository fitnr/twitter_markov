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
import sys
from os import path, remove
import subprocess
from twitter_markov import cli
from twitter_bot_utils import archive


class TestMarkovCLI(unittest.TestCase):

    csvpath = path.join(path.dirname(__file__), 'data/tweets.csv')

    def setUp(self):
        self.argv = ['twittermarkov', 'corpus', self.csvpath]

    def testcli(self):
        target = path.join(path.dirname(self.csvpath), 'tmp.txt')

        sys.argv = self.argv + ['-o', target]

        cli.main()

        result = list(t['text'] for t in archive.read_csv(self.csvpath))

        try:
            with open(target) as f:
                self.assertEqual(result[0], f.readline().strip())
                self.assertEqual(result[1], f.readline().strip())

        finally:
            remove(target)

    def testcliStdout(self):
        p = subprocess.Popen(self.argv, stdout=subprocess.PIPE)
        out, err = p.communicate()

        self.assertIsNone(err, 'err is None')
        self.assertIsNotNone(out, 'out is not None')

        sample = 'He could speak a little Spanish, and also a language which nobody understood'

        try:
            self.assertIn(sample, out)

        except (TypeError, AssertionError):
            self.assertIn(sample, out.decode())


if __name__ == '__main__':
    unittest.main()
