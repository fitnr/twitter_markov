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

from cobe.brain import Brain
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
