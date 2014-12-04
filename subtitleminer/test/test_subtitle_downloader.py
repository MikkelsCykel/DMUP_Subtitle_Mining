# -*- coding: utf-8 -*-
from subtitleminer import SubtitleDownloader


def test_subtitle_download_from_url_success():
    srt_name = SubtitleDownloader()\
        .download_subtitle_in_srt_from_movie_name('8 mile 2002')
    assert type(srt_name) is str


def test_subtitle_download_from_url_failure():
    srt_name = SubtitleDownloader()\
        .download_subtitle_in_srt_from_movie_name('the amazing\
                                                   spidermonster 1972')
    assert type(srt_name) is int
