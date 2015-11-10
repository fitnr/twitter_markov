#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
import sys
import logging
import argparse
import twitter_bot_utils as tbu
from . import TwitterMarkov
from . import checking
from . import __version__ as version


def main():
    parser = argparse.ArgumentParser('twittermarkov', description='Tweet with a markov bot, or teach it from a twitter archive.')

    parser.add_argument('-V', '--version', action='version', version="%(prog)s " + version)

    subparsers = parser.add_subparsers()
    tweeter = subparsers.add_parser('tweet',
                                    parents=[tbu.args.parent()],
                                    description='Post markov chain ("ebooks") tweets to Twitter', usage='%(prog)s [options] SCREEN_NAME')

    tweeter.add_argument('-r', '--reply', action='store_const', const='reply', dest='action', help='tweet responses to recent mentions')
    tweeter.add_argument('--corpus', dest='corpus', metavar='corpus', type=str, help='text file, one sentence per line')
    tweeter.add_argument('--no-learn', dest='learn', action='store_false', help='skip learning (by default, recent tweets are added to corpus)')
    tweeter.set_defaults(func=tweet_func, action='tweet')

    learner = subparsers.add_parser('corpus',
                                    description='Turn a twitter archive into a twitter_markov-ready text file',
                                    usage="%(prog)s [options] archive corpus")

    learner.add_argument('--no-replies', action='store_true', help='skip replies')
    learner.add_argument('--no-retweets', action='store_true', help='skip retweets')
    learner.add_argument('--no-mentions', action='store_true', help='filter out mentions')
    learner.add_argument('--no-urls', action='store_true', help='filter out urls')
    learner.add_argument('--no-media', action='store_true', help='filter out media')
    learner.add_argument('--no-hashtags', action='store_true', help='filter out hashtags')
    learner.add_argument('-q', '--quiet', action='store_true', help='run quietly')
    learner.add_argument('archive', type=str, metavar='archive',
                         default=os.getcwd(), help='archive csv file (e.g. tweets.csv found in Twitter archive)')
    learner.add_argument('corpus', type=str, nargs='?', metavar='corpus',
                         help='text file to create (defaults to stdout)', default='/dev/stdout')

    learner.set_defaults(func=learn_func)

    args = parser.parse_args()
    func = args.func

    argdict = vars(args)
    del argdict['func']

    func(argdict)


def tweet_func(args):
    tbu.args.add_logger(args['screen_name'], args['verbose'])
    logger = logging.getLogger(args['screen_name'])

    tm = TwitterMarkov(**args)

    if args['action'] == 'tweet':
        logger.debug('tweeting...')
        tm.tweet()

    if args['action'] == 'reply':
        logger.debug('replying to all')
        tm.reply_all()


def learn_func(args):
    if not args['quiet']:
        print("Reading " + args['archive'], file=sys.stderr)

    generator = checking.generator(tbu.archive.read_csv(args.get('archive')), **args)

    if args['corpus'] in ('-', '/dev/stdout'):
        for tweet in generator:
            print(tweet.get('text'), file=sys.stdout)

    else:
        if not args['quiet']:
            print("Teaching " + args['corpus'], file=sys.stderr)

        with open(args.get('corpus'), 'w') as f:
            f.writelines([(tweet + '\n').encode('utf-8') for tweet in generator])

if __name__ == '__main__':
    main()
