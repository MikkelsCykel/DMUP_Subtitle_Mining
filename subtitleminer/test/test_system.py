# -*- coding: utf-8 -*-
from subtitleminer import system


def test_system():
    srt_name = System().
    assert type(srt_name) is str


def test_subtitle_download_from_url_failure():
    srt_name = SubtitleDownloader()\
        .download_subtitle_in_srt_from_movie_name('the amazing spidermonster 1972')
    assert type(srt_name) is int
