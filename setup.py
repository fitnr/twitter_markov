#!/usr/bin/env python
from setuptools import setup

readme = 'readme.rst'

setup(
    name='twitter_markov',

    version='0.2.5',

    description='Create markov chain ("_ebooks") accounts on Twitter',

    long_description=open(readme, 'r').read(),

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
        'twitter_bot_utils>=0.6.7',
        'wordfilter==0.1.8'
    ],

)
