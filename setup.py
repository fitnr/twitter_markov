#!/usr/bin/env python
from setuptools import setup


setup(
    name='twitter_markov',

    version="0.3.2",

    description='Create markov chain ("_ebooks") accounts on Twitter',

    long_description=open('readme.rst', 'r').read(),

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

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2.7',
        'Operating System :: OS Independent',
    ],

    install_requires=[
        'cobe>=2.1.2, <2.2',
        'python-Levenshtein>=0.12.0, <0.13',
        'pyyaml',
        'tweepy',
        'argparse==1.2.1',
        'twitter_bot_utils>=0.9, <0.10',
        'wordfilter>=0.1.8, <0.2.0'
    ],

    test_suite='tests',
    tests_require=[
        'setuptools>=17.1',
        'pbr>=0.11,<1.0',
        'mock',
    ],
)
