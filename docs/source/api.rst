API
===

Example
+++++++

This assumes a corpus file (``corpus.txt``) and config file (``config.yaml``). 

.. code:: python

    from twitter_markov import TwitterMarkov

    tm = TwitterMarkov('example_screen_name', 'corpus.txt', config_file='config.yaml')
    tweet = tm.compose()

    # do something more with tweet, or use the Tweepy API in a different way

    tm.api.update_status(tweet)

TwitterMarkov
+++++++++++++

For commands that generate text, the first corpus in the found corpora (or in the config file) will be the default. When using the class with more than corpus, you can specify a corpus with the `model` keyword argument using the basename of the given file, e.g. "special.txt" for the corpus stored at "dir/special.txt".

.. autoclass:: twitter_markov.TwitterMarkov
    :members:

Checking
--------

.. automodule:: twitter_markov.checking
   :members:
   :undoc-members:
