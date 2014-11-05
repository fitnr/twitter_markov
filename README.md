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

# teach the brain, ignoring mentions
$ twittermarkov_learn --no-mentions twitter/archive nameof.brain
# Text like this will be edited to remove the mention:
# I ate a sandwich with @sample

$ twittermarkov_learn --no-replies twitter/archive nameof.brain
# Text like this will be ignored:
# @sample I ate a sandwich

# Text like this will be read in:
# I ate a sandwich with @sample
````

If you're using a Twitter archive, the ARCHIVE argument should be the top-level folder of the archive (usually a long name like 16853453_3f21d17c73166ef3c77d7994c880dd93a8159c88). If you have a text file, the argument should be a file name
