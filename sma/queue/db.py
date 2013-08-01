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

import redis
import subprocess


class DB(object):
    def __init__(self, id, path):
        self.id = id
        self.r = redis.StrictRedis(host='localhost')
        self.path = path

    def sink(self, val):
        self.r.rpush(self.id, val)

    def flushDB(self, t):
        subprocess.Popen(["python",
                         "../sma_conector/sma/queue/flush.py",
                         str(t), self.id, self.path],
                         #shell=True)
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
