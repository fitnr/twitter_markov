# Copyright 2014 Neil Freeman contact@fakeisthenewreal.org
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

import logging
import argparse
import twitter_bot_utils.args as tbu
from .twitter_markov import Twitter_markov


def main():
    parser = argparse.ArgumentParser(
        description='Post markov chain ("ebooks") tweets to Twitter', usage='%(prog)s [options] SCREEN_NAME',
        parents=[tbu.parent()])

    parser.add_argument('-r', '--reply', action='store_true', help='tweet responses to recent mentions')
    parser.add_argument('-t', '--tweet', action='store_true', help='tweet')
    parser.add_argument('--brain', dest='brains', metavar='BRAIN', type=str, help='cobe .brain file')
    parser.add_argument('--no-learn', dest='learn', action='store_false', help='skip learning')
    parser.add_argument('screen_name', type=str, metavar='SCREEN_NAME', help='User who will be tweeting')

    args = parser.parse_args()

    tbu.add_logger(args.screen_name, args.verbose)
    logger = logging.getLogger(args.screen_name)

    tm = Twitter_markov(**vars(args))

    if args.tweet:
        logger.debug('tweeting...')
        tm.tweet()

    if args.reply:
        logger.debug('replying to all')
        tm.reply_all()

if __name__ == '__main__':
    main()
