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

import sys
import time
import redis
import csv
import locale
import ast


def writeVec(path, vec):
    language, output_encoding = locale.getdefaultlocale()
    with open(path, 'w') as f:
        if vec != []:
            write = csv.writer(f, delimiter='|')
            write.writerow([w.encode(output_encoding) for w in vec])
    f.close()


def writeSingle(path, vec):
    language, output_encoding = locale.getdefaultlocale()
    with open(path, 'w') as f:
        if vec != "":
            f.write(vec.encode(output_encoding))
    f.close()


def flush(t, db, path):
    r = redis.StrictRedis('localhost')

    while True:
        if r.lindex(db, 0) is not None:
            w = r.lpop(db)

            try:
                w = ast.literal_eval(w)
                writeVec(path, w)
            except Exception:
                writeSingle(path, w)

            print w
        else:
            time.sleep(0.1)
            f = open(path, 'w')
            f.write("")
            f.close()

        time.sleep(float(t))


if __name__ == '__main__':
    flush(sys.argv[1], sys.argv[2], sys.argv[3])
