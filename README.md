twitter_markov
==============

Create markov chain ("_ebooks") accounts on Twitter

The audience for this library is those with at least basic Python experience. Before you set this up, you'll need:

* A twitter account
* A twitter application (register at [dev.twitter.com](http://dev.twitter.com)) with authentication keys for the account ([read more](https://dev.twitter.com/oauth))
* A corpus for the bot to learn, which can be a text file or a Twitter archive. Several thousand lines are needed to get decent results

## Install

Download or clone the package and run `python setup.py install`. Feel free to use a virtualenv, if you're into that.

## Brain Train

Train the brain with the `twittermarkov_learn` command.

The `twittermarkov_learn` comes with options to ignore replies or retweets, and to filter out mentions, urls, media, and/or hashtags.

When reading an archive, these argument use the tweet's metadate to precisely strip the offending content. This may not work well for tweets posted before 2011 or so. For text files or older tweets, a regular expression search is used.

```bash
# Usage is twittermarkov_learn ARCHIVE BRAIN
$ twittermarkov_learn twitter/archive nameof.brain

# teach the brain from a text file
$ twittermarkov_learn --txt file.txt nameof.brain

$ twittermarkov_learn --no-replies twitter/archive nameof.brain
# Text like this will be ignored:
# @sample I ate a sandwich

# Text like this will be read in:
# I ate a sandwich with @sample
````

If you're using a Twitter archive, the ARCHIVE argument should be the top-level folder of the archive (usually a long name like 16853453_3f21d17c73166ef3c77d7994c880dd93a8159c88). If you have a text file, the argument should be a file name

## Config

See the [bots.yaml](bots.yaml) file for a full list of settings. Plug your settings in and save the file as `bots.yaml` to your home directory  or `~/bots`. You can also use JSON, if that's your thing.

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

## First Tweet

Tweeting is easy. By default, the `twittermarkov` application will learn recent tweets from your parent and send one tweet.

The very first time you tweet, you should use:

````bash
$ twittermarkov --tweet --no-learn example_screen_name
````

After that, use:

````bash
$ twittermarkov --tweet example_screen_name
````

To have your bot reply to mentions, use:

````bash
$ twittermarkov --reply example_screen_name
````

## Automating

On a *nix system, set up a cron job like so:

````
0 10-20 * * * twittermarkov --tweet example_screen_name
15,45 10-20 * * * twittermarkov --reply example_screen_name
````
