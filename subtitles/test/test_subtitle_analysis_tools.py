# -*- coding: utf-8 -*-
from subtitleminer import StampedSrt, SubtitleInIntervals,\
    ValenceArouselDominance
from pytest import raises

"""test data Pulp Fiction comes with the package"""

pathname = "data/Pulp_Fiction.en.srt"
interval = 120


def test_that_valence_arousel_dominance_is_calculated():
    x = StampedSrt(path=pathname, remove_symbols=True)
    y = SubtitleInIntervals(stamped_srt=x, interval_sec=interval,
                            remove_stop_words=True)
    vac = ValenceArouselDominance().compute_vad_intervals(text_intervals=y)
    assert vac[0][0][:3] == (3.73, 3.85, 3.91)


def test_that_lemmatizer_fallback_is_used():
    x1 = StampedSrt(path=pathname, remove_symbols=True)
    y1 = SubtitleInIntervals(stamped_srt=x1, interval_sec=interval,
                             remove_stop_words=True)
    vac1 = ValenceArouselDominance()\
        .compute_vad_intervals(text_intervals=y1, lmtzr_fall_back=True)
    assert vac1[0][0][:3] == (3.73, 3.85, 3.91)


def test_ability_to_mean_data_in_each_interval():
    x = StampedSrt(path=pathname, remove_symbols=True)
    y = SubtitleInIntervals(stamped_srt=x, interval_sec=interval,
                            remove_stop_words=True)
    vad = ValenceArouselDominance()
    VAD = vad.compute_vad_intervals(text_intervals=y)
    m_data = vad.mean_data(VAD)
    t_mean = (sum(VAD[0][0]) / len(VAD[0][0]))
    assert m_data[0][0] == t_mean


def test_invalid_input_argument_text_intervals():
    vad = ValenceArouselDominance()
    with raises(TypeError):
        vad.compute_vad_intervals(text_intervals=True)
