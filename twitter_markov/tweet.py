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
import twitter_bot_utils.args as tbu
from .learn import learn
from .twitter_markov import Twitter_markov
from . import __version__


def main():
    parser = argparse.ArgumentParser('Tweet with a markov bot, or teach it from a twitter archive.')

    parser.add_argument('-V', '--version', action='version', version="%(prog)s " + __version__)

    subparsers = parser.add_subparsers()
    tweet = subparsers.add_parser(
        'tweet', parents=[tbu.parent()],
        description='Post markov chain ("ebooks") tweets to Twitter', usage='%(prog)s [options] SCREEN_NAME')

    tweet.add_argument('-r', '--reply', action='store_const', const='reply', dest='action', help='tweet responses to recent mentions')
    tweet.add_argument('--brain', dest='brains', metavar='BRAIN', type=str, help='cobe .brain file')
    tweet.add_argument('--no-learn', dest='learn', action='store_false', help='skip learning')
    tweet.add_argument('screen_name', type=str, metavar='SCREEN_NAME', help='User who will be tweeting')
    tweet.set_defaults(prog='tweet', action='tweet')

    learnparser = subparsers.add_parser(
        'learn', description='Teach a Cobe brain the contents of a Twitter archive',
        usage="%(prog)s [options] ARCHIVEPATH NEWBRAIN")

    add_learn_subparser_arguments(learnparser)

    args = parser.parse_args()
    argdict = vars(args)

    # Tweet
    if args.prog == 'tweet':
        tbu.add_logger(args.screen_name, args.verbose)
        logger = logging.getLogger(args.screen_name)

        tm = Twitter_markov(**argdict)

        if args.tweet:
            logger.debug('tweeting...')
            tm.tweet()

        if args.reply:
            logger.debug('replying to all')
            tm.reply_all()

    # Learn
    elif args.prog == 'learn':
        if not args.quiet:
            print("Reading from " + args.archive, file=sys.stderr)
            print("Teaching " + args.brain, file=sys.stderr)

        if args.brain[-6:] == '.brain':
            brainpath = args.brain
        else:
            brainpath = args.brain + '.brain'

        count = learn(args.archive, brainpath, **argdict)

        if not args.quiet:
            print("Taught {0} tweets".format(count))


def add_learn_subparser_arguments(parser):
    parser.add_argument('--no-replies', action='store_true', help='skip replies')
    parser.add_argument('--no-retweets', action='store_true', help='skip retweets')
    parser.add_argument('--no-urls', action='store_true', help='Filter out urls')
    parser.add_argument('--no-media', action='store_true', help='filter out media')
    parser.add_argument('--no-hashtags', action='store_true', help='filter out hashtags')
    parser.add_argument(
        '--language', type=str, default='english', help='language. Defaults to English')
    parser.add_argument(
        '--txt', action='store_true', help='Read from a text file, one tweet per line')
    parser.add_argument('-q', '--quiet', action='store_true', help='run quietly')
    parser.add_argument('archive', type=str, metavar='ARCHIVEPATH',
                        default=os.getcwd(), help='top-level folder of twitter archive')
    parser.add_argument('brain', type=str, metavar='NEWBRAIN', help='brain file to create')
    parser.set_defaults(prog='learn')


if __name__ == '__main__':
    main()
