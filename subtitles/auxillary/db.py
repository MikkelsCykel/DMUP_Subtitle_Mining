import sqlite3
import os

from auxillary import log


class DB:
    #
    # Create and connect to Database
    def __init__(self, db_file="../data/imdb.db"):
        database_already_exists = os.path.exists(db_file)
        self.db = sqlite3.connect(db_file)
        self.log = log.Log()
        if not database_already_exists:
            self.setupDefaultData()

    def select(self, sql):
        """

        :param sql:
        :return:
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()
            return records
        except Exception as e:
            self.log.writeToLog(message=e, where="DB -> SELECT  " + sql)
            return e

    def insert(self, sql):
        """

        :param sql:
        :return:
        """
        try:
            last_insert_id = 0
            cursor = self.db.cursor()
            cursor.execute(sql)
            last_insert_id = cursor.lastrowid
            self.db.commit()
            cursor.close()
            return last_insert_id
        except Exception as e:
            self.log.writeToLog(message=e, where=("DB -> INSERT : " + sql))
            return e

    def execute(self, sql):
        """

        :param sql:
        :return:
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            cursor.close()
        except Exception as e:
            self.log.writeToLog(message=e, where="DB -> EXECUTE : " + sql)
            return e

    def executescript(self, sql):
        """

        :param sql:
        :return:
        """
        try:
            cursor = self.db.cursor()
            cursor.executescript(sql)
            self.db.commit()
            cursor.close()
        except Exception as e:
            self.log.writeToLog(message=e,
                                where="DB -> EXECUTESCRIPT : " + sql)
            return e

    #
    # Initial setup of the database.
    # Only to be performed at start or after database wipe.
    #
    def setupDefaultData(self):

        # CREATE database tables on startup
        sql = '''
            CREATE TABLE IF NOT EXISTS movies(
                imdb_movie_id TEXT PRIMARY KEY,
                title TEXT,
                runtime TEXT,
                year TEXT,
                genre TEXT,
                plot TEXT,
                imdb_rating TEXT,
                imdb_votes TEXT,
                meta_score TEXT,
                poster TEXT,
                subtitle_link TEXT

            )

        '''
        self.executescript(sql)
