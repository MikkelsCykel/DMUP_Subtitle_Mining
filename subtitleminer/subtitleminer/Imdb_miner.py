# -*- coding: utf-8 -*-
import urllib2
import re
import json
from BeautifulSoup import BeautifulSoup
from subtitleminer.auxillary import DB, Log, System
from subtitleminer import subtitle_downloader.SubtitleDownloader

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
        :rtype : object returns unique set containing movie UID's
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

        return self.system.generate_unique_set_from_list(info)

    def fetch_imdb_info(self, id="", title=""):

        """
        Method for fetching movie info either IMDB UID or movie title.

        Favours UID if set.
        returns 0 if API error if thrown

        :param id: IMDB UID of movie as string
        :param title: Title of movie as string urlencoded
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

    def insert_imdb_info_into_db(self, info):
        """
        Method for inserting the IMDB info into the database.

        :param info: list containing all imdb info fetched from previous method
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
        Method for fetching data from imdb using predefined queries.
        Used for mining over multiple runs

        :param onlySubtitle: Boolean value specifying whether to fetch
        only rows that has subtitle downloaded
        :param onlyWithoutSubtitle: Boolean value specifying whether to fetch
        only rows has no subtitle downloaded
        :param offset: offset in database rows
        :rtype : object passes on the database function select.
        """
        if (onlySubtitle):
            sql = 'SELECT * FROM movies\
                   WHERE subtitle_name is not null\
                   LIMIT 10000 OFFSET %s ' % offset
        elif (onlyWithoutSubtitle):
            sql = "SELECT * FROM movies\
                   where subtitle_name is null\
                   or subtitle_name = ''\
                  LIMIT 10000 OFFSET %s " % offset
        else:
            sql = 'SELECT * FROM movies LIMIT 10000 OFFSET %s ' % offset

        return self.db.select(sql=sql)

    def assign_subtitle_name_to_movie(self, subtitle_name, imdb_id):
        """
        Method for assigning the subtitle file name to a UID in the db after
        download

        :param subtitle_name: name of the downloaded subtitle file
        :param imdb_id: UID of movie from IMDB
        :rtype : object
        """
        sql = """
        UPDATE movies SET subtitle_name = '%s'
        WHERE imdb_movie_id = '%s'
        """ % (subtitle_name, imdb_id)
        self.db.execute(sql=sql)

   def get_subtitle_name_from_title(self, id=""):
        subtitleDownloader = SubtitleDownloader()

        sql = "SELECT subtitle_name FROM movies WHERE imdb_movie_id = '{0:s}' LIMIT 1 ".format(id)

        result = self.db.select(sql=sql)

        if (result == 0):
            info = self.fetchImdbInfo(id=id)
            name = self.system.remove_non_ascii_chars(name="Jurassic Park 1993")
            subtitle_name = subtitleDownloader.download_subtitle_in_srt_from_movie_name(name=name)

            if (subtitle_name == 0):
                return 0


        for movie in result:
            subtitle_name = movie[0]

        print subtitle_name


