# -*- coding: utf-8 -*-
from subtitleminer import ImdbMiner

"""test data Pulp Fiction comes with the package"""
pathname = "data/Pulp_Fiction.en.srt"


def test_imdb_fetching_from_url_is_list():
    info = ImdbMiner().fetch_imdb_releases(range=1)
    assert type(info) is list


def test_imdb_fetching_from_url_length_of_list():
    info = ImdbMiner().fetch_imdb_releases(range=1)
    assert len(info) > 0


def test_imdb_fetching_title_is_string():
    info = ImdbMiner().fetch_imdb_releases(range=1)
    assert type(info[0][1]) is unicode


def test_imdb_fetching_imdbId_is_present():
    info = ImdbMiner().fetch_imdb_releases(range=1)
    assert type(info[0][0]) is not None
