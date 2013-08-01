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

import re
from nltk.corpus import stopwords
import locale


def vector(txt, path, keys):
    language, output_encoding = locale.getdefaultlocale()

    txt = txt.lower()
    bag = re.findall(u"[\w'áéíóúñ]+", txt, flags=re.UNICODE | re.LOCALE)
    e = [word for word in bag if
         word.encode('utf-8') not in stopwords.words('spanish') and
         word.encode('utf-8') not in stopwords.words('english') and
         word.encode('utf-8') not in stopwords.words('twitter') and
         word.encode('utf-8') not in keys]

    return e
