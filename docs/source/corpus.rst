Create a corpus
===============

The ``twittermarkov corpus`` command will create such a file from a Twitter archive, with options to ignore replies or retweets, and to filter out mentions, urls, media, and/or hashtags.

"Corpus" is just a fancy-schmancy word for "a bunch of text". `twittermarkov` expects a corpus that's a text file with one tweet per line. Several thousand lines are needed to get decent results, with fewer than 100 or so it won't work at all

You can turn anything as a corpus. If you're looking for free material, try `Project Gutenberg <http://www.gutenberg.org>`__ and the `Internet Archive <https://archive.org/details/texts>`__.

When reading an archive, these arguments use the tweet's metadata to precisely strip the offending content. This may not work well for tweets posted before 2011 or so. For text files or older tweets, a regular expression search is used.

.. code::bash

    # Usage is twittermarkov corpus archive output
    # This creates the file corpus.txt
    twittermarkov corpus twitter/archive/path corpus.txt

    twittermarkov corpus --no-retweets --no-replies twitter/archive/path corpus-no-replies.txt
    # Teweets like this will be ignored:
    # RT @sample I ate a sandwich

    # Tweets like this will be read in without the @ name:
    # @example Was it tasty?


All the filtering options:

* ``--no-retweets`` - skip retweets
* ``--no-replies`` - filter out replies (keeps the tweet, just removes the starting username)
* ``--no-mentions`` - filter out mentions
* ``--no-urls`` - filter out urls
* ``--no-media`` - filter out media
* ``--no-hashtags`` - filter out hashtags

If you're using a Twitter archive, the archive argument should be the tweet.csv file found in the archive folder (which usually has a long name like ``16853453_3f21d17c73166ef3c77d7994c880dd93a8159c88``).

