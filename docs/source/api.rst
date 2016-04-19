API
===

Twitter Markov
--------------

For commands that generate text, the first corpus in the found corpora (or in the config file) will be the default. When using the class with more than corpus, you can specify a corpus with the `model` keyword argument using the basename of the given file, e.g. "special.txt" for the corpus stored at "dir/special.txt".

.. autoclass:: twitter_markov.TwitterMarkov
    :members:

Checking
--------

.. automodule:: twitter_markov.checking
   :members:
   :undoc-members:
