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

    tbu.args.add_default_args(parser, version, ())

    subparsers = parser.add_subparsers()

    tweeter = subparsers.add_parser('tweet', description=TWEETER_DESC, usage='%(prog)s [options]')
    tbu.args.add_default_args(tweeter, include=('user', 'config', 'dry-run', 'verbose', 'quiet'))
    tweeter.add_argument('-r', '--reply', action='store_const', const='reply',
                         dest='action', help='tweet responses to recent mentions')
    tweeter.add_argument('--corpus', dest='corpus', metavar='corpus', type=str,
                         help='text file, one sentence per line')
    tweeter.add_argument('--max-len', type=int, default=140, help='maximum output length. default: 140')
    tweeter.add_argument('--state-size', type=int, help='model state size. default: 2')
    tweeter.add_argument('--no-learn', dest='learn', action='store_false',
                         help='skip learning (by default, recent tweets from the "parent" account are added to corpus)')
    tweeter.set_defaults(subparser='tweet', func=tweet_func, action='tweet')

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

    learner.set_defaults(subparser='learn', func=learn_func, action='learn')

    args = parser.parse_args()
    func = args.func
    argdict = vars(args)
    del argdict['func']

    if args.subparser == 'tweet':
        func(**argdict)

    elif args.subparser == 'learn':
        func(**argdict)


def tweet_func(action, max_len=None, **kwargs):
    tm = TwitterMarkov(**kwargs)

    if action == 'tweet':
        tm.log.debug('tweeting')
        tm.tweet(max_len=max_len)

    elif action == 'reply':
        tm.log.debug('replying')
        tm.reply_all(max_len=max_len)


def learn_func(**kwargs):
    if not kwargs['quiet']:
        print("Reading " + kwargs['archive'], file=sys.stderr)

    archive = tbu.archive.read_csv(kwargs.get('archive'))
    gen = checking.generator(archive, **kwargs)
    tweets = (tweet.replace(u'\n', u' ') + '\n' for tweet in gen)

    if kwargs['output'] in ('-', '/dev/stdout'):
        signal(SIGPIPE, SIG_DFL)
        sys.stdout.writelines(tweets)

    else:
        if not kwargs['quiet']:
            print("Writing " + kwargs['output'], file=sys.stderr)

        with open(kwargs.get('output'), 'w') as f:
            f.writelines(tweets)

if __name__ == '__main__':
    main()
