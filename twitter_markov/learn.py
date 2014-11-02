import os
from botconfig import config
from json import loads, dumps
from cobe.brain import Brain
import db_manager

from twitter import *

b = Brain(os.path.join(os.path.dirname(__file__), 'cobe.brain'))

try:
    state = loads(open(os.path.join(os.path.dirname(__file__), '.state'), 'r').read())
except:
    state = {}

if 'accounts' not in state:
    state['accounts'] = {}


api = Twitter(auth=OAuth(**config['api']))

b.start_batch_learning()

tweets = 0


def smart_truncate(content, length=140):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]

for account in config['dump_accounts']:
    print "Grabbing tweets for %s" % account

    params = {'screen_name': account, 'count': 200, 'exclude_replies': True, 'include_rts': False}

    if account in state['accounts']:
        last_tweet = long(state['accounts'][account])
        params['since_id'] = last_tweet
    else:
        last_tweet = 0

    timeline = api.statuses.user_timeline(**params)

    for tweet in timeline:
        b.learn(tweet['text'])
        # add it to the db
        db_manager.insert_tweet(tweet['text'].encode('utf-8', 'replace'), False)
        last_tweet = max(tweet['id'], last_tweet)
        tweets += 1

    print "%d found..." % tweets
    state['accounts'][account] = str(last_tweet)

print "Learning %d tweets" % tweets
b.stop_batch_learning()
# close the learned txt
open(os.path.join(os.path.dirname(__file__), '.state'), 'w').write(dumps(state))
