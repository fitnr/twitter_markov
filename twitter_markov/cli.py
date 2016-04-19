#!/usr/bin/env python
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
import sys
from signal import signal, SIGPIPE, SIG_DFL
import argparse
import twitter_bot_utils as tbu
from . import TwitterMarkov
from . import checking
from . import __version__ as version


TWEETER_DESC = 'Post markov chain ("ebooks") tweets to Twitter'
LEARNER_DESC = 'Turn a twitter archive into a twitter_markov-ready text file'


def main():
    parser = argparse.ArgumentParser(
        'twittermarkov', description='Tweet with a markov bot, or teach it from a twitter archive.')

    parser.add_argument('-V', '--version', action='version', version="%(prog)s " + version)

    subparsers = parser.add_subparsers()

    tweeter = subparsers.add_parser('tweet', description=TWEETER_DESC,
                                    parents=[tbu.args.parent()], usage='%(prog)s [options] SCREEN_NAME')
    tweeter.add_argument('-r', '--reply', action='store_const', const='reply',
                         dest='action', help='tweet responses to recent mentions')
    tweeter.add_argument('--corpus', dest='corpus', metavar='corpus', type=str,
                         help='text file, one sentence per line')
    tweeter.add_argument('--no-learn', dest='learn', action='store_false',
                         help='skip learning (by default, recent tweets are added to corpus)')
    tweeter.set_defaults(func=tweet_func, action='tweet')

    learner = subparsers.add_parser('corpus', description=LEARNER_DESC, usage="%(prog)s [options] archive corpus")
    learner.add_argument('-o', type=str, dest='output', metavar='corpus',
                         help='output text file (defaults to stdout)', default='/dev/stdout')
    learner.add_argument('--no-retweets', action='store_true', help='skip retweets')
    learner.add_argument('--no-replies', action='store_true', help='filter out replies')
    learner.add_argument('--no-mentions', action='store_true', help='filter out mentions')
    learner.add_argument('--no-urls', action='store_true', help='filter out urls')
    learner.add_argument('--no-media', action='store_true', help='filter out media')
    learner.add_argument('--no-hashtags', action='store_true', help='filter out hashtags')
    learner.add_argument('-q', '--quiet', action='store_true', help='run quietly')
    learner.add_argument('archive', type=str, metavar='archive',
                         default=os.getcwd(), help='archive csv file (e.g. tweets.csv found in Twitter archive)')

    learner.set_defaults(func=learn_func)

    args = parser.parse_args()
    func = args.func
    argdict = vars(args)
    del argdict['func']
    func(argdict)


def tweet_func(args):
    tm = TwitterMarkov(**args)

    if args['action'] == 'tweet':
        tm.tweet()

    elif args['action'] == 'reply':
        tm.reply_all()


def learn_func(args):
    if not args['quiet']:
        print("Reading " + args['archive'], file=sys.stderr)

    archive = tbu.archive.read_csv(args.get('archive'))
    gen = checking.generator(archive, **args)
    tweets = (tweet.replace(u'\n', u' ') + '\n' for tweet in gen)

    if args['output'] in ('-', '/dev/stdout'):
        signal(SIGPIPE, SIG_DFL)
        sys.stdout.writelines(tweets)

    else:
        if not args['quiet']:
            print("Writing " + args['output'], file=sys.stderr)

        with open(args.get('output'), 'w') as f:
            f.writelines(tweets)

if __name__ == '__main__':
    main()
