#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
    SentimentAnalysis. SentimentAnalysis for social networks.
    Copyright (C) 2013  Christian Ladr¨®n, Carlos M¨¦ndez, Wulfrano Moreno.

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

import json
from tweepy.streaming import StreamListener
from words.tokenizer import vector
import tweepy


class Conector(object):
    def __init__(self, id):
        self.id = id
        self.key = "" # Particular twitter application data.
        self.secret = "" # Particular twitter application data.
        self.token = "" # Particular twitter application data.
        self.tSecret = "" # Particular twitter application data.


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

    def setStream(self, listener):
        self.stream = tweepy.Stream(self.auth, listener)


class Stream(StreamListener):

    def __init__(self):
        self.arch = ""
        self.keys = ""
        self.queue = None

    def on_data(self, data):
        self.liveStream(data, self.keys, self.queue)
        return True

    def on_error(self, status):
        print status

    def liveStream(self, obj, keys, queue):
        tweet = json.loads(obj)
        queue[0].sink(vector(tweet['text'], queue[0].path, keys))
        queue[1].sink(tweet['user']['lang'])
        print tweet['text'].encode('utf-8')
