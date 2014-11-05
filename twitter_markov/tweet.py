import logging
import twitter_bot_utils
from twitter_markov import Twitter_markov

def main():
    parser = twitter_bot_utils.setup_args(description='Post markov/ebooks tweets to Twitter', usage='%(prog)s [options] SCREEN_NAME')

    parser.add_argument('-r', '--reply', action='store_true', help='tweet responses to recent mentions')
    parser.add_argument('-t', '--tweet', action='store_true', help='tweet')
    parser.add_argument('--brain', dest='brains', metavar='BRAIN', type=str, help='cobe .brain file')
    parser.add_argument('--no-learn', dest='learn', action='store_false', help='skip learning')
    parser.add_argument('screen_name', type=str, metavar='SCREEN_NAME', help='User who will be tweeting')

    args = parser.parse_args()

    twitter_bot_utils.defaults(args.screen_name, args)
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
