#!/usr/bin/env python
# twitter_markov - Create markov chain ("_ebooks") accounts on Twitter
# Copyright 2014-2016 Neil Freeman contact@fakeisthenewreal.org

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup

try:
    readme = open('README.rst', 'r').read()
except IOError:
    readme = ''

with open('twitter_markov/__init__.py') as i:
    version = next(r for r in i.readlines() if '__version__' in r).split('=')[1].strip('"\' \n')

setup(
    name='twitter_markov',

    version=version,

    description='Create markov chain ("_ebooks") accounts on Twitter',

    long_description=readme,

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
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
    ],

    use_2to3=True,

    zip_safe=True,

    install_requires=[
        'twitter_bot_utils>=0.11.2,<0.12',
        'markovify>=0.2.4,<0.4',
        'python-Levenshtein>=0.12.0, <0.13',
        'wordfilter>=0.1.8, <0.2.0'
        'pyyaml',
        'tweepy',
    ],

    test_suite='tests',
    tests_require=[
        'setuptools>=17.1',
        'pbr>=0.11,<1.0',
        'mock',
    ],
)
