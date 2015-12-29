0.4.1
-----

* Small update for changed twitter bot utils API

0.4
---

* Replace `cobe` with `markovify`. This simplifies learning, since it's just adding to a text file corpus.
* Also changes `Twitter_markov` API, removing catalyst argument and replacing 'brain' keyword arguments with 'corpus' or 'model'.
* Replace `twittermarkov learn` with `twittermarkov corpus`
* Add checking.generator function
* Restore similarity/blacklist checker for generated text
* rename class from Twitter_markov to TwitterMarkov
* Rework cli tools, renaming twittermarkov learn -> twittermarkov corpus

0.3
---

* Combine two command line tools into one command with subcommands.
* Handle errors in learning more cleanly.

0.2.4
-----

* `Twitter_markov` class no longer extends Tweepy.API, so an existing API object can be passed in
* Cleaned up code around brain naming.
* Expanded readme.
