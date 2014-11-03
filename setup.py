#!/usr/bin/env python

from setuptools import setup

setup(
    name='twitter_markov',

    version='0.0.1',

    description='Create markov chain ("_ebooks") accounts on Twitter',

    author='fitnr',

    url='https://github.com/fitnr/twitter_markov',

    packages=['twitter_markov'],

    entry_points={
        'console_scripts': [
            'twittermarkov=twitter_markov.tweet:main',
            'twittermarkov_learn=twitter_markov.learn:main',
        ],
    },

    dependency_links=[
        'https://github.com/fitnr/twitter_bot_utils/archive/0.3.0.tar.gz#egg=twitter_bot_utils-0.3.0'
        ],

    install_requires=[
        'cobe>=2.1.1',
        'python-Levenshtein>=0.10.2',
        'pyyaml',
        'argparse>=1.2.1',
        'tweepy>=1.10.0',
        'twitter_bot_utils>=0.1.0'
    ],
)
