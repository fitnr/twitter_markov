#!/usr/bin/env python
from setuptools import setup
from twitter_markov import __version__

readme = 'readme.rst'

setup(
    name='twitter_markov',

    version=__version__,

    description='Create markov chain ("_ebooks") accounts on Twitter',

    long_description=open(readme, 'r').read(),

    author='Neil Freeman',

    author_email='contact@fakeisthenewreal.org',

    url='https://github.com/fitnr/twitter_markov',

    packages=['twitter_markov'],

    license='GPLv3',

    entry_points={
        'console_scripts': [
            'twittermarkov=twitter_markov.cli:main',
        ],
    },

    install_requires=[
        'cobe>=2.1.1, <2.2',
        'python-Levenshtein>=0.12.0, <0.13',
        'pyyaml',
        'argparse>=1.2.1, <1.3',
        'tweepy',
        'twitter_bot_utils>=0.8, <0.9',
        'wordfilter>=0.1.8, <0.2.0'
    ],

    test_suite='tests',
    tests_require=[
        'mock==1.1.2'
    ],
)
