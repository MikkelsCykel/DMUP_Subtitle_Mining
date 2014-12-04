# -*- coding: utf-8 -*-
from subtitleminer import WarrinerRatings


def test_that_warriner_ratings_is_generated():
    w = WarrinerRatings()
    assert len(w.keys()) > 0


def test_that_warriner_ratings_attribute_headers_is_generated():
    w = WarrinerRatings()
    assert len(w['attribute_names']) > 0


def test_that_warriner_ratings_is_a_dictionary_object():
    w = WarrinerRatings()
    assert type(w) is dict
