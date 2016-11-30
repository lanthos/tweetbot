import tweepy
import string
import time
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from settings import consumer_secret, consumer_key, access_secret, access_token


def get_twitter_auth():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth


def get_twitter_client():
    auth = get_twitter_auth()
    client = tweepy.API(auth)
    return client


class MyListener(StreamListener):

    def __init__(self, fname):
        safe_fname = format_filename(fname)
        self.outfile = "stream_{}.jsonl".format(safe_fname)
        self.start = time.monotonic()
        self.timeout = 900

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                if time.monotonic() - self.start > self.timeout:
                    print("It's been 15 minutes so quiting!")
                    return False
                return True
        except BaseException as e:
            print("Error on_data: {}\n".format(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        if status == 420:
            print("Rate limit exceeded\n")
            return False
        else:
            print("Error {}\n".format(status))
            return True


def format_filename(fname):
    """Convert fname into a safe string for a file name.

    Return: string
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if "invalid".

    Return: string
    """
    valid_chars = "-_.{}{}".format(string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'

if __name__ == '__main__':
    query = ['trump', 'president']
    query_fname = '-'.join(query)
    auth = get_twitter_auth()
    twitter_stream = Stream(auth, MyListener(query_fname))
    twitter_stream.filter(track=query, async=True)
