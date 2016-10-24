import json
import tweepy
from tweepy import StreamListener
from elasticsearch import Elasticsearch
import certifi
import optparse
from dateutil import parser
#Variables that contains the user credentials to access Twitter API
access_token = 
access_token_secret = 
consumer_key = 
consumer_secret = 
endpoint = 

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(tweepy.StreamListener):
    def __init__(self, es, f):
        super(StdOutListener, self).__init__()
        self.es = es
        self.f = f

    def on_data(self, data):
        tweet = json.loads(data)
        try: 
            if tweet['coordinates']:
                print tweet["coordinates"]
                print tweet
                coordinates = tweet['coordinates']['coordinates']
                timestamp = parser.parse(tweet['created_at'])
                timestamp = timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')
                twitter = {"text" : tweet["text"], 
                            "user": tweet['user']["screen_name"],
                            "geo": {
                                "lat" : coordinates[1],
                                "lon" : coordinates[0]
                            }
                            "time" : timestamp}
                es.index(index = 'twittmap', doc_type='tweets',id = tweet['id'], body=twitter)
                f.write(twitter)

        except Exception as e:
            print e

    def on_error(self, status):
        print status

    
if __name__ == '__main__':
    with open('tweetstream.log', 'a') as f:
        es = Elasticsearch(hosts = [endpoint], port = 443, use_ssl = True, verify_certs = True, ca_certs = certifi.where())
    #This handles Twitter authetification and the connection to Twitter Streaming API
        l = StdOutListener(es, f)

        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        stream = tweepy.Stream(auth, l)
     
        #This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=['Kobe', 'James', 'NBA', 'Lakers', 'Boston', 'New York', 'Curry', 'Cartoon', 'News', 'Car'])

    



















