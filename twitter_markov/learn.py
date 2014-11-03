import os
import re
import json
from cobe.brain import Brain
import glob
import argparse
from twitter_bot_utils import helpers, add_logger

DATA_FILES = 'data/js/tweets/*.js'

def archive_gen(directory):
    '''Scrape a twitter archive file. Inspiration from https://github.com/mshea/Parse-Twitter-Archive'''
    files = os.path.join(directory, DATA_FILES)
    files = glob.glob(files)

    for fname in files:
        with open(fname) as f:
            # Twitter's JSON first line is bogus
            data = f.readlines()[1:]
            data = "".join(data)
            tweetlist = json.loads(data)
            for tweet in tweetlist:
                yield tweet


def construct_tweet_checker(no_retweets=False, no_replies=False):
    '''Returns a tweet checker'''
    def checker(tweet):
        if no_retweets and tweet.get('retweeted_status'):
            return False

        if no_replies and tweet.get('in_reply_to_user_id'):
            return False

        return True

    return checker


def construct_tweet_filter(no_mentions=False, no_urls=False, no_media=False, no_hashtags=False):
    '''returns a filter for tweet text'''

    entitytypes = []

    if no_mentions:
        entitytypes.append('user_mentions')

    if no_hashtags:
        entitytypes.append('hashtags')

    if no_urls:
        entitytypes.append('urls')

    if no_media:
        entitytypes.append('media')

    def filterer(tweet):
        text = helpers.remove_entities(tweet, entitytypes)

        # Older tweets don't have entities
        if no_urls and text.find('http') > -1:
            # regex stolen from http://stackoverflow.com/questions/6883049/regex-to-find-urls-in-string-in-python
            text = re.sub(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", '', text)

        if no_mentions and text.find('@') > -1:
            text = re.sub(r'@\w+', '', text)

        if no_hashtags and text.find('#') > -1:
            text = re.sub(r'#\w+', '', text)

        return text

    return filterer


def main():
    parser = argparse.ArgumentParser(description='Teach a Cobe brain the contents of a Twitter archive')

    parser.add_argument('--no-replies', action='store_true', help='skip replies')
    parser.add_argument('--no-retweets', action='store_true', help='skip retweets')
    parser.add_argument('--no-mentions', action='store_true', help='filter out mentions')
    parser.add_argument('--no-urls', action='store_true', help='Filter out urls')
    parser.add_argument('--no-media', action='store_true', help='filter out media')
    parser.add_argument('--no-hashtags', action='store_true', help='filter out hashtags')

    parser.add_argument('-q', '--quiet', action='store_true', help='be quiet')

    parser.add_argument('archive', type=str, metavar='ARCHIVEPATH', default=os.getcwd(), help='archive')
    parser.add_argument('brain', type=str, metavar='NEWBRAIN', help='brain file to create')

    args = parser.parse_args()

    logger = add_logger('learner', '.')

    if not args.quiet:
        print "Reading from " + args.archive
        print "Teaching " + args.brain

    if args.brain[-6:] == '.brain':
        brainpath = args.brain
    else:
        brainpath = args.brain + '.brain'

    # start brain. Batch saves us from lots of I/O
    brain = Brain(brainpath)
    brain.start_batch_learning()

    tweet_generator = archive_gen(args.archive)

    cool_tweet = construct_tweet_checker(args.no_retweets, args.no_replies)
    tweet_filter = construct_tweet_filter(args.no_mentions, args.no_urls, args.no_media, args.no_hashtags)

    skip, count = 0, 0
    for status in tweet_generator:

        if not cool_tweet(status):
            skip += 1
            continue

        text = tweet_filter(status)

        brain.learn(text)
        logger.info(text)

        count += 1

    brain.stop_batch_learning()

    if not args.quiet:
        print "Skipped {0} tweets".format(skip)
        print "Learned {0} tweets".format(count)

if __name__ == '__main__':
    main()
