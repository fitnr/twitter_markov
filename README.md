twitter markov
==============

Create markov chain ("_ebooks") accounts on Twitter.

The audience for this library is those with at least basic Python experience. Before you set this up, you'll need:

* A twitter account
* A twitter application (register at [dev.twitter.com](http://dev.twitter.com)) with authentication keys for the account ([read more](https://dev.twitter.com/oauth))
* A corpus for the bot to learn, which can be a text file or a Twitter archive. Several thousand lines are needed to get decent results, with fewer than 100 or so it won't work at all.

## Install

Run `pip install twitter_markov`, or download/clone the package and run `python setup.py install`. Feel free to use a virtualenv, if you're into that.

## Corpus Pocus

"Corpus" is just a fancy-schmancy word for "a bunch of text". `twittermarkov` expects a corpus that's a text file with one tweet per line.

You can turn anything as a corpus. If you're looking for free material, try [Project Gutenberg](http://www.gutenberg.org) and the [Internet Archive](https://archive.org/details/texts).

### Transforming a Twitter archive into a corpus

[Check the docs for a complete guide](http://pythonhosted.org/twitter_markov/corpus.html).

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

Once a corpus is set up, the `twittermarkov tweet` command will send tweets out. If a `parent` is specified, this command will send one tweet and trigger adding recent tweets to the corpus file.

The learning also won't happen if twittermarkov can't find it's previous tweets, which might happen if there are problems with the Twitter API, or your _ebooks account has never tweeted.

Since learning depends on the `_ebooks` account having an existing tweet, send a first tweet with the `--no-learn` flag.
````bash
twittermarkov tweet --no-learn example_screen_name
````

To have your bot reply to mentions, use:
````bash
twittermarkov tweet --reply example_screen_name
````

## Automating

On a Unix-based system, set up a cron job like so:

````
0 10-20 * * * twittermarkov tweet example_screen_name
15,45 10-20 * * * twittermarkov tweet --reply example_screen_name
````

## API

[See the docs](http://pythonhosted.org/twitter_markov/api.html).

### Example

This assumes a corpus file (`corpus.txt`) and config file (`config.yaml`). 

````python
from twitter_markov import TwitterMarkov

tm = TwitterMarkov('example_screen_name', 'corpus.txt', config_file='config.yaml')
tweet = tm.compose()

# do something more with tweet, or use the Tweepy API in a different way
tm.api.update_status(tweet)
````
