# -*- coding: utf-8 -*-
import re
from subtitleminer import StampedSrt, SubtitleInIntervals
from pytest import raises

"""test data Pulp Fiction comes with the package"""
pathname = "data/Pulp_Fiction.en.srt"


def test_that_subtitle_data_is_loaded_from_path_name():
    x = StampedSrt(path=pathname)
    assert len(x.keys()) > 0


def test_that_subtitle_result_is_dictionary_object():
    x = StampedSrt(path=pathname)
    assert type(x) is dict


def test_that_symbols_can_be_removed():
    x = StampedSrt(path=pathname, remove_symbols=True)
    temp = ""
    for i in x.keys()[:10]:
        temp += x[i]
    temp = re.findall(r'([-\!$%^&*()_+|~=`{}\[\]:";<>\?,.\/])', temp)
    assert len(temp) == 0


def test_that_symbols_can_be_included():
    x = StampedSrt(path=pathname, remove_symbols=False)
    temp = ""
    for i in x.keys()[:10]:
        temp += x[i]
    temp = re.findall(r'([-\!$%^&*()_+|~=`{}\[\]:";<>\?,.\/])', temp)
    assert len(temp) > 0


def test_that_stamped_srt_fails_with_invalid_args():
    invalid_path = 'data/invalid_video.srt'
    with raises(IOError):
        StampedSrt(path=invalid_path, remove_symbols=True)


def test_invalid_remove_symbols_args():
    invalid_param = "String"
    x = StampedSrt(path=pathname, remove_symbols=invalid_param)
    temp = ""
    for i in x.keys()[:10]:
        temp += x[i]
    temp = re.findall(r'([-\!$%^&*()_+|~=`{}\[\]:";<>\?,.\/])', temp)
    assert len(temp) > 0


def test_that_stamped_srt_is_devided_into_a_time_interval_list():
    x = StampedSrt(path=pathname, remove_symbols=True)
    interval = 120
    y = SubtitleInIntervals(stamped_srt=x, interval_sec=interval)
    z = sorted(x.keys())[-1] / interval
    assert z == len(y)


def test_that_stop_words_can_be_removed():
    x = StampedSrt(path=pathname, remove_symbols=True)
    interval = 120
    y = SubtitleInIntervals(stamped_srt=x, interval_sec=interval,
                            remove_stop_words=True)
    z = ' '.join([a for b in y for a in b])
    assert ' i ' not in z


def test_that_stop_words_can_be_left_in_text():
    x = StampedSrt(path=pathname, remove_symbols=True)
    interval = 120
    y = SubtitleInIntervals(stamped_srt=x, interval_sec=interval,
                            remove_stop_words=False)
    z = ' '.join([a for b in y for a in b])
    assert ' i ' in z


def test_that_subtitle_in_intervals_fails_with_invalid_stamped_srt():
    with raises(TypeError):
        SubtitleInIntervals(stamped_srt=['a', 'b', 'c'], interval_sec=120)


def test_that_subtitle_in_intervals_fails_with_invalid_time_interval():
    x = StampedSrt(path=pathname, remove_symbols=True)
    with raises(TypeError):
        SubtitleInIntervals(stamped_srt=x, interval_sec='wrong')


def test_that_subtitle_in_intervals_wrong_remove_sw_type_defaults_false():
    x = StampedSrt(path=pathname, remove_symbols=True)
    y = SubtitleInIntervals(stamped_srt=x, interval_sec=120,
                            remove_stop_words=23)
    z = ' '.join([a for b in y for a in b])
    assert ' i ' in z
