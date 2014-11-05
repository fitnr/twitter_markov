import os
import json
from cobe.brain import Brain
import glob
import argparse
from . import checking
from twitter_bot_utils import helpers


def archive_gen(directory, date_files='data/js/tweets/*.js'):
    '''Scrape a twitter archive file. Inspiration from https://github.com/mshea/Parse-Twitter-Archive'''
    files = os.path.join(directory, date_files)
    files = glob.glob(files)

    for fname in files:
        with open(fname, 'r') as f:
            # Twitter's JSON first line is bogus
            data = f.readlines()[1:]
            data = "".join(data)
            tweetlist = json.loads(data)

        for tweet in tweetlist:
            yield tweet


def txt_gen(data_file):
    with open(data_file, 'r') as f:
        data = f.readlines()

    for tweet in data:
        yield tweet.rstrip()


def learn(archive, brain, **kwargs):
    # start brain. Batch saves us from lots of I/O
    brain = Brain(brain)
    brain.set_stemmer(kwargs.get('language', 'english'))

    brain.start_batch_learning()

    if kwargs.get('txt'):
        tweet_generator = txt_gen(archive)
    else:
        tweet_generator = archive_gen(archive)

    cool_tweet = checking.construct_tweet_checker(kwargs.get('no_retweets', False), kwargs.get('no_replies', False))

    tweet_filter = checking.construct_tweet_filter(
        no_mentions=kwargs.get('no_mentions', False),
        no_urls=kwargs.get('no_urls', False),
        no_media=kwargs.get('no_media', False),
        no_hashtags=kwargs.get('no_hashtags', False),
        no_symbols=kwargs.get('no_symbols', False)
    )

    skip, count = 0, 0
    for status in tweet_generator:

        if not cool_tweet(status):
            skip += 1
            continue

        text = tweet_filter(status)
        text = helpers.format_text(text)
        brain.learn(text)
        count += 1

    brain.stop_batch_learning()

    return count, skip


def main():
    parser = argparse.ArgumentParser(description='Teach a Cobe brain the contents of a Twitter archive', usage="%(prog)s [options] ARCHIVEPATH NEWBRAIN")

    parser.add_argument('--no-replies', action='store_true', help='skip replies')
    parser.add_argument('--no-retweets', action='store_true', help='skip retweets')
    parser.add_argument('--no-urls', action='store_true', help='Filter out urls')
    parser.add_argument('--no-media', action='store_true', help='filter out media')
    parser.add_argument('--no-hashtags', action='store_true', help='filter out hashtags')

    parser.add_argument('--language', type=str, default='english', help='language. Defaults to English')

    parser.add_argument('--txt', action='store_true', help='Read from a text file, one tweet per line')

    parser.add_argument('-q', '--quiet', action='store_true', help='run quietly')

    parser.add_argument('archive', type=str, metavar='ARCHIVEPATH', default=os.getcwd(), help='top-level folder of twitter archive')
    parser.add_argument('brain', type=str, metavar='NEWBRAIN', help='brain file to create')

    args = parser.parse_args()

    if not args.quiet:
        print "Reading from " + args.archive
        print "Teaching " + args.brain

    if args.brain[-6:] == '.brain':
        brainpath = args.brain
    else:
        brainpath = args.brain + '.brain'

    argdict = vars(args)
    kwargs = dict((x, argdict[x]) for x in ['language', 'no_replies', 'no_hashtags', 'no_retweets', 'no_urls', 'no_media', 'txt'])

    count, skip = learn(args.archive, brainpath, **kwargs)

    if not args.quiet:
        print "Skipped {0} tweets".format(skip)
        print "Learned {0} tweets".format(count)

if __name__ == '__main__':
    main()
