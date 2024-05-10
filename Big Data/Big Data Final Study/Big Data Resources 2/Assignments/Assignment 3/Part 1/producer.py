from kafka import KafkaProducer
import tweepy
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
from transformers import pipeline
import json
import configparser


#Twiiter API Credentials
consumer_key = "CBEZnjZeKI3zNwJY8tCxqYmli"
consumer_secret = "WBL3QFTnXWQiRWmiTCcqOKkXiVuRw5G8Znj7RCnM7fBCJySy3y"
access_token = "773777586606473216-RZrvGB4w1iQ41lof4BSzVq5x6OzjkVL"
access_secret = "xjBz8bA0wgmaNVDTSIWd7EqmKTSVznvavEqbjzdsKNpnC"


def perform_analysis(tweet):
	t_sentiment = classifier(json.loads(tweet)["text"])
	sentiment = t_sentiment[0]["label"]
	return sentiment


class KafkaPushListener(StreamListener):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

    def on_data(self, data):
        sentiment = perform_analysis(data)
        self.producer.send(config['arguments']['topic'], sentiment.encode('utf-8'))
        return True

    def on_error(self, status):
        print("status error - ",status)
        return True



if __name__ == "__main__":
	auth = OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api = tweepy.API(auth)
	config = configparser.ConfigParser()
	config.read('config.ini')

	classifier = pipeline('assignment3part1')
	listener = KafkaPushListener()
	twitter_stream = Stream(auth, listener)

	twitter_stream.filter(track=[config["arguments"]["search"]])
