.. Twitter Markov documentation index file

Twitter Markov
==================

Twitter Markov is a Python library for creating markov chain ("_ebooks") accounts on Twitter.

The audience for this library is those with at least basic Python experience. Before you set this up, you'll need:

* A twitter account
* A twitter application (register at `dev.twitter.com <http://dev.twitter.com>`__) with authentication keys for the account (`read more <https://dev.twitter.com/oauth>`__)
* A corpus for the bot to learn, which can be a text file or a Twitter archive. Several thousand lines are needed to get decent results, with fewer than 100 or so it won't work at all.

Install
-------

Run ``pip install twitter_markov``. Feel free to use a virtualenv, if you're into that.

Table of contents
-----------------

.. toctree::
   :maxdepth: 2

   corpus
   config
   tweet
   api

Index
======

* :ref:`genindex`
* :ref:`modindex`
