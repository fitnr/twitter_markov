#!/usr/bin/env python
from setuptools import setup

try:
    from pypandoc import convert
    read_md = lambda f: convert(f, 'rst')
except ImportError:
    print("pypandoc module not found, could not convert Markdown to RST")
    read_md = lambda f: open(f, 'r').read()

setup(
    name='twitter_markov',

    version='0.1.1',

    description='Create markov chain ("_ebooks") accounts on Twitter',

    long_description=read_md('README.md'),

    author='fitnr',

    url='https://github.com/fitnr/twitter_markov',

    packages=['twitter_markov'],

    license=open('LICENSE').read(),

    entry_points={
        'console_scripts': [
            'twittermarkov=twitter_markov.tweet:main',
            'twittermarkov_learn=twitter_markov.learn:main',
        ],
    },

    dependency_links=[
        'https://github.com/fitnr/twitter_bot_utils/archive/0.4.2.tar.gz#egg=twitter_bot_utils-0.4.2',
        'https://github.com/fitnr/wordfilter/archive/master.zip#egg=wordfilter-0.1.7'
        ],

    install_requires=[
        'cobe>=2.1.1',
        'python-Levenshtein>=0.10.2',
        'pyyaml',
        'argparse==1.2.1',
        'tweepy>=1.10.0',
        'twitter_bot_utils>=0.4.2',
        'wordfilter'
    ],
)
