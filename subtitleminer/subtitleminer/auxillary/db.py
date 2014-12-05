# -*- coding: utf-8 -*-
import sqlite3
import os
from subtitleminer.auxillary import Log


class DB:
    #
    # Create and connect to Database
    def __init__(self, db_file="data/imdb.db"):
        """
        Initiation function of the database object.
        Takes a path to a db file, and if it does not exist,
        create it and initialize database default data.

        :param db_file: path to the database file.
        :rtype : object
        """
        database_already_exists = os.path.exists(db_file)
        self.db = sqlite3.connect(db_file)
        self.log = Log()
        if not database_already_exists:
            self.setupDefaultData()

    def select(self, sql):
        """
        Method for selecting from the database.

        :param sql: SQL query as string
        :return: data from db as list
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            records = cursor.fetchall()
            cursor.close()
            return records
        except Exception as e:
            self.log.write_to_log(message=e, where="DB -> SELECT  " + sql)
            return 0

    def insert(self, sql):
        """
        Method for inserting into the sqlite db

        :param sql: SQL query as string
        :return: nothing
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
            self.log.write_to_log(message=e, where=("DB -> INSERT : " + sql))
            return e

    def execute(self, sql):
        """
        Method for executing custom scripts in the sqlite db

        :param sql: SQL query as string
        :return: nothing
        """
        try:
            cursor = self.db.cursor()
            cursor.execute(sql)
            self.db.commit()
            cursor.close()
        except Exception as e:
            self.log.write_to_log(message=e, where="DB -> EXECUTE : " + sql)
            return e

    def executescript(self, sql):
        """
        Method for executing script in the sqlite db.
        Supports multiple scripts in one.

        :param sql: SQL query as string
        :return: nothing
        """
        try:
            cursor = self.db.cursor()
            cursor.executescript(sql)
            self.db.commit()
            cursor.close()
        except Exception as e:
            self.log.write_to_log(message=e,
                                  where="DB -> EXECUTESCRIPT : " + sql)
            return e

    def setupDefaultData(self):

        """
        Method for initializing the database upon creation
        Creates movie table

        :rtype : object
        """
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
