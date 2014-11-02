import os
import logging
import argparse
from .botconfig import read_config
import tweepy
from twitter_bot_utils import setup

def main():
    logger = logging.getLogger('twitter_ebooks')

    parser = argparse.ArgumentParser(description="Post ebooks tweets to twitter.")
    parser.add_argument('-v', '--verbose', action='store_true', help="Output to stdout")
    parser.add_argument('-n', '--dry-run', action='store_true', help="don't post to twitter.")
    parser.add_argument('-t', '--tweet', help="Tweet arbitrary text instead of using the brain.")
    parser.add_argument('-c', '--config', help="Path to yaml config file. Defaults to ./botrc")

    print os.cwd()

    args = parser.parse_args()

    config = read_config(args.config)

    auth = tweepy.OAuthHandler(consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'])
    auth.set_access_token(key=config['token'], secret=config['token_secret'])

    t = tweepy.API(auth)

    if args.tweet:
        t.update_status(args.tweet)
    else:
        tweet = twert_helper.create_tweet()

        logger.log(tweet)

        if not args.dry_run:
            t.update_status(status=tweet)

if __name__ == '__main__':
    main()
