import csv
import sys

from decouple import config
from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor

from preprocessor import cleaner

consumer_key = config('CONSUMER_KEY')
consumer_secret = config('CONSUMER_SECRET')
access_token = config('ACCESS_TOKEN')
access_token_secret = config('ACCESS_TOKEN_SECRET')


def extract_coordinates(coordinate_data, location_data):
    try:
        if coordinate_data is None:
            bounding_box = location_data['bounding_box']['coordinates'][0]
            lon_sum = 0.0
            lat_sum = 0.0
            for coordinates in bounding_box:
                lon_sum += coordinates[0]
                lat_sum += coordinates[1]
            coord = [lon_sum / 4, lat_sum / 4]
        else:
            coord = coordinate_data['coordinates']
    except TypeError:
        coord = [0, 0]
    return coord


def preprocessing(tweet_json):
    id = tweet_json['id']
    text = cleaner(tweet_json["full_text"])
    if text is None:
        return None
    return id, text


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
auth_api = API(auth)

account_list = []
source_list = set()
if (len(sys.argv) > 1):
    account_list = sys.argv[1:]
else:
    print("Please provide a list of usernames at the command line.")
    sys.exit(0)

if len(account_list) > 0:
    for target in account_list:
        print("Getting data for " + target)

        tweet_count = 0
        for status in Cursor(
            auth_api.user_timeline,
            id=target,
            tweet_mode='extended'
        ).items():
            if hasattr(status, 'retweeted_status'):
                source = status.retweeted_status.user
                source_list.add(source.name)
                tweet = preprocessing(status.retweeted_status._json)
            else:
                tweet = preprocessing(status._json)
            if tweet is not None:
                tweet_count += 1
                print(tweet[1])

                with open("tweets_radio_sp.csv", 'a', encoding='utf-8') as csv_file:
                    field_names = ['id', 'text', 'class']
                    writer = csv.DictWriter(
                        csv_file, delimiter=';',
                        lineterminator='\n',
                        fieldnames=field_names
                    )
                    writer.writerow({
                        'id': tweet[0],
                        'text': tweet[1],
                        'class': None
                    })

        print(f'All done. Processed {tweet_count} tweets')
        print(f'Retweeted from {source_list}')
