#!/usr/bin/python
# -*- coding: utf-8 -*-

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

import sma.conector as app
import sma.words.streaming as ws
import sma.lang.streaming as ls
import sma.queue.db as db
import sys
import getopt
import locale


def main(argv):

    c = app.Conector("example")
    language, output_encoding = locale.getdefaultlocale()

    try:
        opts, args = getopt.getopt(argv, "", ["sim=", "file=", "stream="])

    except getopt.GetoptError:
        print "Option not recognized"
        sys.exit(2)

    for opt, arg in opts:
        if opt == "--sim" and arg == "words":
            db_words = db.DB("words", "../words.txt")

            m = ws.Monitor(c)
            m.keys = [opts[1][1]]

            m.simqueue = db_words
            db_words.flushDB(0.3)

            m.simulate("../"+opts[1][1]+".json")

        if opt == "--sim" and arg == "lang":
            db_lang = db.DB("lang", "../lang.txt")

            l = ls.Monitor(c)
            l.keys = [opts[1][1]]

            l.simqueue = db_lang
            db_lang.flushDB(0.3)

            l.simulate("../"+opts[1][1]+".json")

        if opt == "--stream":
            t = 0.4
            db_words = db.DB("words", "../words.txt")
            db_words.flushDB(t)

            db_lang = db.DB("lang", "../lang.txt")
            db_lang.flushDB(t)

            keyWords = arg.decode(output_encoding).encode('utf-8').split(",")

            mon = app.Monitor(c)
            mon.keys = keyWords

            listener = app.Stream()
            listener.keys = keyWords
            listener.queue = [db_words, db_lang]

            mon.setStream(listener)
            mon.stream.filter(track=mon.keys)


if __name__ == '__main__':
    main(sys.argv[1:])
