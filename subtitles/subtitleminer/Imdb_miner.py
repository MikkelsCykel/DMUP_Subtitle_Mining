import urllib2
import re
import json

from BeautifulSoup import BeautifulSoup

from auxillary import db, log, system


class ImdbMiner:
    def __init__(self):
       self.log = log.Log()
       self.db = db.DB()
       self.system = system.System()

    def fetchAllNewImdbReleases(self):
        response = urllib2.urlopen('http://www.imdb.com/list/ls056315119/')
        html = response.read()
        soup = BeautifulSoup(html)
        listItems = soup.findAll('div', {'class': re.compile(r'\binfo\b')})
        info = []
        for x in listItems:
            try:
                info.append(x.find('b').getText())
            except Exception as e:
                continue

        print info


    def fetchImdbReleases(self):

        info = []
        # Run over all movies. List contains 10000 films, displaying 100 at a time, so we will make use of i*100 range to collect all.
        for i in xrange(0, 100):
            # Static sites from IMDB to mine from, due to anti-mining methods this list contains all movies from 1974-2014
            url = 'http://www.imdb.com/list/ls057823854/?start=%i&view=detail&sort=listorian:asc' % (i*100)
            response = urllib2.urlopen(url)
            html = response.read()
            soup = BeautifulSoup(html)
            listItems = soup.findAll('div', {'class': re.compile(r'\bhover-over-image\b')})
            for x in listItems:
                try:
                    info.append(x.get('data-const'))
                except Exception as e:
                    continue

        return self.system.generateUniqueSetFromList(info)


    def fetchImdbInfo(self, id="", title=""):

        URL = 'http://www.omdbapi.com/?'

        if id != "" :
            URL += 'i=%s' % id
        else:
            if (title != ""):
                URL += 't=%s' % title
            else:
                return 0

        response = urllib2.urlopen(URL)
        html = response.read()
        soup = BeautifulSoup(html)
        new_dictionary=json.loads(str(soup))
        # API throws error if string does not match a title or ID
        if (new_dictionary.get('Error')) :
            return 0
        else :
            return new_dictionary



    def insertImdbInfoIntoDB(self, info=[]):
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
        )""" % (info['imdbID'], info['Title'].replace('"', "'"), info['Runtime'], info['Year'], info['Genre'].replace('"', "'"), info['Plot'].replace('"', "'"), info['imdbRating'], info['imdbVotes'], info['Metascore'], info['Poster'])
        self.db.insert(sql=sql)


    def selectImdbInfoFromDB(self, onlySubtitle = False, onlyWithoutSubtitle=False, offset=0):
        if (onlySubtitle):
            sql = 'SELECT * FROM movies WHERE subtitle_name is not null LIMIT 10000 OFFSET %s ' % offset
        elif (onlyWithoutSubtitle):
            sql = "SELECT * FROM movies where subtitle_name is null or subtitle_name = '' "
        else:
            sql = 'SELECT * FROM movies LIMIT 10000 OFFSET %s ' % offset

        return self.db.select(sql=sql)


    def assign_subtitle_name_to_movie(self, subtitle_name, imdb_id):
        sql = """
        UPDATE movies SET subtitle_name = '%s'
        WHERE imdb_movie_id = '%s'
        """ % (subtitle_name, imdb_id)
        self.db.execute(sql=sql)