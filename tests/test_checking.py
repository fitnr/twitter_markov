import unittest
from os import path
from twitter_markov import learn
from twitter_markov import checking

import tweepy

TWEET = {
    "source": "\u003Ca href=\"http:\/\/twitter.com\/download\/iphone\" rel=\"nofollow\"\u003ETwitter for iPhone\u003C\/a\u003E",
    "entities": {
        "user_mentions": [{
            "name": "John Doe",
            "screen_name": "twitter",
            "indices": [0, 8],
            "id_str": "1",
            "id": 1
        }],
        "media": [],
        "hashtags": [],
        "urls": []
    },
    "in_reply_to_status_id_str": "318563540590010368",
    "id_str": "318565861172600832",
    "in_reply_to_user_id": 14155645,
    "text": "@twitter example tweet example tweet example tweet",
    "id": 318565861172600832,
    "in_reply_to_status_id": 318563540590010368,
    "in_reply_to_screen_name": "twitter",
    "in_reply_to_user_id_str": "14155645",
    "retweeted": None,
    "user": {
        "name": "Neil Freeman",
        "screen_name": "fitnr",
        "protected": False,
        "id_str": "6853512",
        "profile_image_url_https": "https:\/\/pbs.twimg.com\/profile_images\/431817496350314496\/VGgzYAE7_normal.jpeg",
        "id": 6853512,
        "verified": False
    }
}


class tweeter_markov_tests(unittest.TestCase):

    def setUp(self):
        api = tweepy.API()
        self.status = tweepy.Status.parse(api, TWEET)

        self.txtfile = path.join(path.dirname(__file__), 'data/tweets.txt')

        self.archive = path.dirname(__file__)

    def test_mention_filter(self):
        mention_filter = checking.construct_tweet_filter(no_mentions=True)
        assert mention_filter(self.status) == u' example tweet example tweet example tweet'

    def test_rt_filter(self):
        retweet_filter = checking.construct_tweet_checker(no_retweets=True)
        assert retweet_filter(self.status)

    def test_reply_filter(self):
        reply_filter = checking.construct_tweet_checker(no_replies=True)
        assert reply_filter(self.status) is False

    def test_reply_filtering_txtfile(self):
        generator = learn.tweet_generator(self.txtfile, txt=1, no_replies=1)
        assert len(list(generator)) == 3

    def test_reply_filtering_archive(self):
        generator = learn.tweet_generator(self.archive, no_replies=1)
        assert len(list(generator)) == 2

    def test_rt_filtering(self):
        generator = learn.tweet_generator(self.txtfile, txt=1, no_retweets=1)
        assert len(list(generator)) == 3

    def test_rt_filtering_archive(self):
        generator = learn.tweet_generator(self.archive, no_retweets=1)
        assert len(list(generator)) == 2

if __name__ == '__main__':
    unittest.main()
