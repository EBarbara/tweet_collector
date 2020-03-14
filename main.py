import csv
import html
import json
from datetime import datetime

import tweepy
from decouple import config

from preprocessor import cleaner

consumer_key = config('CONSUMER_KEY')
consumer_secret = config('CONSUMER_SECRET')
access_token = config('ACCESS_TOKEN')
access_token_secret = config('ACCESS_TOKEN_SECRET')

# Around Manhattan
REGION_BOUNDS = [
    config('LIMIT_WEST', cast=float),
    config('LIMIT_SOUTH', cast=float),
    config('LIMIT_EAST', cast=float),
    config('LIMIT_NORTH', cast=float)
]


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
    # time = datetime.strptime(
    #     tweet_json['created_at'],
    #     '%a %b %d %H:%M:%S +0000 %Y'
    # )
    # coordinates = extract_coordinates(
    #     tweet_json["coordinates"],
    #     tweet_json["place"]
    # )
    # longitude = coordinates[0]
    # latitude = coordinates[1]
    # text = tweet_json["text"].replace('\n', ' ')
    # return id, time, latitude, longitude, text
    if 'extended_tweet' in tweet_json:
        text = cleaner(tweet_json['extended_tweet']['full_text'])
    else:
        text = cleaner(tweet_json["text"])
    if text is None:
        return None
    return id, text


class StdOutListener(tweepy.StreamListener):

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        tweet_json = json.loads(html.unescape(data))
        tweet = preprocessing(tweet_json)
        if tweet:
            # print(tweet[1])

            with open("tweets_base.csv", 'a', encoding='utf-8') as csv_file:
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

    def on_error(self, status_code):
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False

        # returning non-False reconnects the stream, with backoff.


if __name__ == '__main__':
    listener = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    start_time = str(datetime.now().time())
    print("START STREAMING ON " + start_time)
    stream = tweepy.Stream(auth, listener)
    stream.filter(
        languages=['pt'],
        locations=REGION_BOUNDS
    )
