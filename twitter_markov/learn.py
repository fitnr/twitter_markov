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

import os
from cobe.brain import Brain
import argparse
from . import checking
from twitter_bot_utils import helpers, archive


def tweet_generator(archivepath, **kwargs):
    if kwargs.get('txt'):
        generator = archive.read_text(archivepath)
    else:
        generator = archive.read_json(archivepath)

    cool_tweet = checking.construct_tweet_checker(
        kwargs.get('no_retweets', False), kwargs.get('no_replies', False))

    tweet_filter = checking.construct_tweet_filter(
        no_mentions=kwargs.get('no_mentions', False),
        no_urls=kwargs.get('no_urls', False),
        no_media=kwargs.get('no_media', False),
        no_hashtags=kwargs.get('no_hashtags', False),
        no_symbols=kwargs.get('no_symbols', False)
    )

    for status in generator:
        if not cool_tweet(status):
            continue

        text = tweet_filter(status)
        text = helpers.format_text(text)
        yield text


def learn(archivepath, brain, **kwargs):
    # start brain. Batch saves us from lots of I/O
    brain = Brain(brain)
    brain.set_stemmer(kwargs.get('language', 'english'))

    brain.start_batch_learning()

    tweets = tweet_generator(archivepath, **kwargs)
    count = 0

    for text in tweets:
        count = count + 1
        brain.learn(text)

    brain.stop_batch_learning()

    return count


def main():
    parser = argparse.ArgumentParser(
        description='Teach a Cobe brain the contents of a Twitter archive', usage="%(prog)s [options] ARCHIVEPATH NEWBRAIN")

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

    args = parser.parse_args()

    if not args.quiet:
        print("Reading from " + args.archive)
        print("Teaching " + args.brain)

    if args.brain[-6:] == '.brain':
        brainpath = args.brain
    else:
        brainpath = args.brain + '.brain'

    argdict = vars(args)
    kwargs = dict((x, argdict[x]) for x in [
                  'language', 'no_replies', 'no_hashtags', 'no_retweets', 'no_urls', 'no_media', 'txt'])

    count = learn(args.archive, brainpath, **kwargs)

    if not args.quiet:
        print("Taught {0} tweets".format(count))

if __name__ == '__main__':
    main()
