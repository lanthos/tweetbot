import tweepy
import json
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from settings import consumer_secret, consumer_key, access_secret, access_token

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth)


class MyListener(StreamListener):
    def on_data(self, data):
        try:
            with open('pokemon.json', 'a') as f:
                f.write(data)
                return True
        except BaseException as e:
                print "Error on_data: {}".format(e)
        return True
    def on_error(self, status):
        print status
        return True
twitter_stream = Stream(auth, MyListener())
twitter_stream.filter(track=["#pokemongo"])

with open('pokemon.json', 'r') as f:
    line = f.readline()
    tweet = json.loads(line)
    print json.dumps(tweet, indent=4)
