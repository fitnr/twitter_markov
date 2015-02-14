#!/usr/bin/env python
from setuptools import setup

try:
    from pypandoc import convert

    def read_md(f):
        try:
            return convert(f, 'rst')
        except IOError:
            return ''

except ImportError:
    print("pypandoc module not found, could not convert Markdown to RST")

    def read_md(f):
        try:
            return open(f, 'r').read()
        except IOError:
            return ''


setup(
    name='twitter_markov',

    version='0.2.4',

    description='Create markov chain ("_ebooks") accounts on Twitter',

    long_description=read_md('readme.md'),

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    url='https://github.com/fitnr/twitter_markov',

    packages=['twitter_markov'],

    license='GPL',

    entry_points={
        'console_scripts': [
            'twittermarkov=twitter_markov.tweet:main',
            'twittermarkov_learn=twitter_markov.learn:main',
        ],
    },

    install_requires=[
        'cobe==2.1.1',
        'python-Levenshtein==0.12.0',
        'pyyaml',
        'argparse==1.2.1',
        'tweepy',
        'twitter_bot_utils==0.6.2.1',
        'wordfilter==0.1.8'
    ],

)
