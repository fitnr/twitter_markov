Tweeting
========

First Tweet
-----------

Once a corpus is set up, the ``twittermarkov tweet`` command will send
tweets out. If a ``parent`` is specified, this command will send one
tweet and trigger adding recent tweets to the corpus file.

The learning also won't happen if twittermarkov can't find it's previous
tweets, which might happen if there are problems with the Twitter API,
or your \_ebooks account has never tweeted.

Since learning depends on the ``_ebooks`` account having an existing
tweet, send a first tweet with the ``--no-learn`` flag.

.. code:: bash

    twittermarkov tweet --no-learn example_screen_name

To have your bot reply to mentions, use:

.. code:: bash

    twittermarkov tweet --reply example_screen_name

Automating
----------

On a Unix-based system, set up a cron job like so:

::

    0 10-20 * * * twittermarkov tweet example_screen_name
    15,45 10-20 * * * twittermarkov tweet --reply example_screen_name
