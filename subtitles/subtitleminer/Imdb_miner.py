# -*- coding: utf-8 -*-
import urllib2
import re
import json
from BeautifulSoup import BeautifulSoup
from subtitleminer.auxillary import DB, Log, System


class ImdbMiner:
    def __init__(self):
        self.log = Log()
        self.db = DB()
        self.system = System()

    def fetchAllNewImdbReleases(self):
        """

        :rtype : object
        """
        response = urllib2.urlopen('http://www.imdb.com/list/ls056315119/')
        html = response.read()
        soup = BeautifulSoup(html)
        listItems = soup.findAll('div', {'class': re.compile(r'\binfo\b')})
        info = []
        for x in listItems:
            try:
                info.append(x.find('b').getText())
            except Exception:
                continue

        print info

    def fetch_imdb_releases(self, range=100):

        """
        Run over all movies. List contains 10000 films,
        displaying 100 at a time, so we will make use of i*100
        range to collect all.

        Static sites from IMDB to mine from, due to anti-mining methods
        this list contains all movies from 1974-2014
        Since there are 10000 films, presented 100 at a time,
        this loop will fetch all.

        :param range: range to pick movies. Takes 100 movies for each range.
        :rtype : object
        """
        info = []

        for i in xrange(0, range):
            url = 'http://www.imdb.com/list/ls057823854/?start=\
                   %i&view=detail&sort=listorian:asc' % (i * 100)
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html)
            listItems = soup.findAll('div',
                                     {'class':
                                      re.compile(r'\bhover-over-image\b')})
            for x in listItems:
                try:
                    info.append(x.get('data-const'))
                except Exception:
                    continue

        return self.system.generateUniqueSetFromList(info)

    def fetch_imdb_info(self, id="", title=""):

        """

        :rtype : object
        """
        URL = 'http://www.omdbapi.com/?'

        if id != "":
            URL += 'i=%s' % id
        else:
            if (title != ""):
                URL += 't=%s' % title
            else:
                return 0

        response = urllib2.urlopen(URL)
        html = response.read()
        soup = BeautifulSoup(html)
        new_dictionary = json.loads(str(soup))
        # API throws error if string does not match a title or ID
        if (new_dictionary.get('Error')):
            return 0
        else:
            return new_dictionary

    def insert_imdb_info_into_db(self, info=[]):
        """

        :rtype : object
        """
        sql = """
        INSERT INTO movies (
            imdb_movie_id,
            title,
            runtime,
            year,
            genre,
            plot,
            imdb_rating,
            imdb_votes,
            meta_score,
            poster
        ) VALUES (
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s",
            "%s"
        )""" % (info['imdbID'], info['Title'].replace('"', "'"),
                info['Runtime'], info['Year'], info['Genre']
                .replace('"', "'"), info['Plot'].replace('"', "'"),
                info['imdbRating'], info['imdbVotes'],
                info['Metascore'], info['Poster'])
        self.db.insert(sql=sql)

    def select_imdb_info_from_db(self, onlySubtitle=False,
                                 onlyWithoutSubtitle=False, offset=0):
        """

        :rtype : object
        """
        if (onlySubtitle):
            sql = 'SELECT * FROM movies\
                   WHERE subtitle_name is not null\
                   LIMIT 10000 OFFSET %s ' % offset
        elif (onlyWithoutSubtitle):
            sql = "SELECT * FROM movies\
                   where subtitle_name is null\
                   or subtitle_name = '' "
        else:
            sql = 'SELECT * FROM movies LIMIT 10000 OFFSET %s ' % offset

        return self.db.select(sql=sql)

    def assign_subtitle_name_to_movie(self, subtitle_name, imdb_id):
        """

        :rtype : object
        """
        sql = """
        UPDATE movies SET subtitle_name = '%s'
        WHERE imdb_movie_id = '%s'
        """ % (subtitle_name, imdb_id)
        self.db.execute(sql=sql)
