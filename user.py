from datetime import datetime

from decouple import config
import tweepy


class TweetMiner:

    data = []
    api = False

    twitter_keys = {
        'consumer_key': config('CONSUMER_KEY'),
        'consumer_secret': config('CONSUMER_SECRET'),
        'access_token_key': config('ACCESS_TOKEN'),
        'access_token_secret': config('ACCESS_TOKEN_SECRET')
    }

    def __init__(self, keys_dict=twitter_keys, api=api):
        self.twitter_keys = keys_dict

        auth = tweepy.OAuthHandler(keys_dict['consumer_key'], keys_dict['consumer_secret'])
        auth.set_access_token(keys_dict['access_token_key'], keys_dict['access_token_secret'])

        self.api = tweepy.API(auth)
        self.twitter_keys = keys_dict

    def mine_user_tweets(self, user, mine_rewteets=False):
        data = []

        statuses = self.api.user_timeline(
            screen_name=user,
            tweet_mode='extended',
            count=4000,
            include_retweets=True
        )

        item_count = 0

        for item in statuses:
            item_count += 1
            mined = {
                'tweet_id': item.id,
                'name': item.user.name,
                'screen_name': item.user.screen_name,
                'retweet_count': item.retweet_count,
                'text': item.full_text,
                'mined_at': datetime.now(),
                'created_at': item.created_at,
                'favourite_count': item.favorite_count,
                'hashtags': item.entities['hashtags'],
                'status_count': item.user.statuses_count,
                'location': item.place,
                'source_device': item.source
            }

            try:
                mined['retweet_text'] = item.retweeted_status.full_text
            except:
                mined['retweet_text'] = 'None'

            try:
                mined['quote_text'] = item.quoted_status.full_text
                mined['quote_screen_name'] = item.quoted_status.user.screen_name
            except:
                mined['quote_text'] = 'None'
                mined['quote_screen_name'] = 'None'

            print(f'Mined {item_count} tweets')
            data.append(mined)
        return data


USER = 'OperacoesRio'
miner = TweetMiner()
mined_tweets = miner.mine_user_tweets(user=USER)

print(type(mined_tweets))
