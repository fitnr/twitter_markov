Config files
============

See the
`bots.yaml <https://github.com/fitnr/twitter_markov/blob/master/bots.yaml>`__
file for a full list of settings. Plug your settings in and save the
file as ``bots.yaml`` to your home directory or ``~/bots``. You can also
use JSON, if that's your thing.

At a minimum, your config file will need to look like this:

.. code:: yaml

    apps:
        example_app_name:
            consumer_key: ...
            consumer_secret: ...

    users:
        example_screen_name:

            key: ...
            secret: ...

            app: example_app_name

            # If you want your bot to continue to learn, include this
            parent: your_screen_name

Read up on `dev.twitter.com <https://dev.twitter.com/oauth/overview>`__
on obtaining authentication tokens.
