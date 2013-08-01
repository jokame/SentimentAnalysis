'''
    SentimentAnalysis. SentimentAnalysis for social networks.
    Copyright (C) 2013  Christian Ladrón, Carlos Méndez, Wulfrano Moreno.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import tweepy
import json
from tokenizer import vector
from tweepy.streaming import StreamListener


class Monitor():
    def __init__(self, conector):
        self.id = conector.id
        self.key = conector.key
        self.secret = conector.secret
        self.token = conector.token
        self.tSecret = conector.tSecret
        self.auth = tweepy.OAuthHandler(self.key, self.secret)
        self.auth.set_access_token(self.token, self.tSecret)
        self.api = tweepy.API(self.auth)
        self.keys = ""
        self.simqueue = None

    def setStream(self, listener):
        self.stream = tweepy.Stream(self.auth, listener)

    def simulate(self, json_file):
        tweets = [json.loads(line) for line in open(json_file)]
        path = "../words.txt"

        for tw in tweets:
            self.liveSim(tw, self.keys, path, self.simqueue)

    def liveSim(self, obj, keys, path, queue):
        tweet = obj
        queue.sink(vector(tweet['text'], path, keys))
        print tweet['text'].encode('utf-8')


class Stream(StreamListener):

    def __init__(self):
        self.arch = ""
        self.keys = ""
        self.queue = None

    def on_data(self, data):
        path = "../words.txt"
        self.live(data, self.keys, path, self.queue)
        return True

    def on_error(self, status):
        print status

    def live(self, obj, keys, path, queue):
        tweet = json.loads(obj)
        queue.sink(vector(tweet['text'], path, keys))
        print tweet['text'].encode('utf-8')
