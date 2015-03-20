twitter_markov
==============

Create markov chain ("_ebooks") accounts on Twitter

The audience for this library is those with at least basic Python experience. Before you set this up, you'll need:

* A twitter account
* A twitter application (register at [dev.twitter.com](http://dev.twitter.com)) with authentication keys for the account ([read more](https://dev.twitter.com/oauth))
* A corpus for the bot to learn, which can be a text file or a Twitter archive. Several thousand lines are needed to get decent results

## Install

Run `pip install twitter_markov`, or download/clone the package and run `python setup.py install`. Feel free to use a virtualenv, if you're into that.

## Brain Train

Train the brain with the `twittermarkov_learn` command.

The `twittermarkov_learn` comes with options to ignore replies or retweets, and to filter out mentions, urls, media, and/or hashtags.

When reading an archive, these arguments use the tweet's metadata to precisely strip the offending content. This may not work well for tweets posted before 2011 or so. For text files or older tweets, a regular expression search is used.

```bash
# Usage is twittermarkov_learn ARCHIVE BRAIN
$ twittermarkov learn twitter/archive/path archive.brain

# teach the brain from a text file
$ twittermarkov learn --txt file.txt txt.brain

$ twittermarkov_learn --no-replies twitter/archive/path archive-no-replies.brain
# Text like this will be ignored:
# @sample I ate a sandwich

# Text like this will be read in:
# I ate a sandwich with @sample
````

If you're using a Twitter archive, the ARCHIVE argument should be the top-level folder of the archive (usually a long name like 16853453_3f21d17c73166ef3c77d7994c880dd93a8159c88). If you have a text file, the argument should be a file name

## Config

See the [bots.yaml](https://github.com/fitnr/twitter_markov/blob/master/bots.yaml) file for a full list of settings. Plug your settings in and save the file as `bots.yaml` to your home directory  or `~/bots`. You can also use JSON, if that's your thing.

At a minimum, your config file will need to look like this:
````yaml
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
````

Read up on [dev.twitter.com](https://dev.twitter.com/oauth/overview) on obtaining authentication tokens.

## First Tweet

Tweeting is easy. By default, the `twittermarkov` command line application will learn recent tweets from your parent and send one tweet.

After that, use:
````bash
$ twittermarkov tweet --no-learn example_screen_name
````

To have your bot reply to mentions, use:
````bash
$ twittermarkov tweet --reply example_screen_name
````

To have your bot reply to mentions, use:

````bash
$ twittermarkov tweet --reply example_screen_name
````

If you don't want to bot to learn from the parent account, use
````bash
$ twittermarkov tweet --no-learn example_screen_name
````

The learning also won't happen if twittermarkov can't find it's previous tweets, which might happen if there are problems with the Twitter API, or your _ebooks account has never tweeted.

## Automating

On a *nix system, set up a cron job like so:

````
0 10-20 * * * twittermarkov tweet example_screen_name
15,45 10-20 * * * twittermarkov tweet --reply example_screen_name
````

## API

If you want to write a script to expand on twitter_markov, you'll find a fairly simple set of tools.

_class twitter_markov.Twitter_markov(screen_name, brains=None, config=None, api=None)_

* screen_name - Twitter user account
* brains - Path to a brain file, or a list of paths. If omitted, Twitter_markov looks in its config for a `brains` entry.
* config - A dictionary of configuration settings. But default, twitter_markov will try to read this from the bots.yaml file (see above)/
* api - A tweepy-like API object. In the twitter_markov class, this is a `twitter_bot_utils.API` object.

The first brain in brains (or in the config file) will be the default brain.

Properties:
* recently_tweeted - A list of the 20 (or `config['checkback']`) most recent tweets from `self.screen_name`.

Methods:

* `check_tweet(text)`: Check if a string contains blacklisted words or is similar to a recent tweet.
* `reply(status, brainname=None): Compose a reply to the given `tweepy.Status`. Brainname could refer to the filename of a given brain (for instance, "special" for the brain stored at "dir/special.brain").
* `reply_all(brainname=None)`: Reply to all mentions since the last time `self.screen_name` sent a reply tweet.
* `compose(catalyst='', brainname=None, max_len=140)`: Returns a string generated "brainname" (or the default brain).
* `tweet(catylyst='', brainname=None)`: Post a tweet composed by giving "catalyst" to "brainname" (or the default brain).
* `learn_parent(brainname=None)`: Learn recent tweets (since the last time `self.screen_name` tweeted) by the parent account. This is subject to the filters described in `bots.yaml`.

