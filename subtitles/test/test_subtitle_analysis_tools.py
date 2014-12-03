from subtitleminer import StampedSrt, SubtitleInIntervals,\
    ValenceArouselDominance

"""test data Pulp Fiction comes with the package"""
pathname = "data/Pulp_Fiction.en.srt"


def test_that_valence_arousel_dominance_is_calculated():
    x = StampedSrt(path=pathname, remove_symbols=True)
    interval = 120
    y = SubtitleInIntervals(stamped_srt=x, interval_sec=interval,
                            remove_stop_words=True)
    vac = ValenceArouselDominance().compute_vad_intervals(text_intervals=y)
    assert vac[0][:3] == ('3.73', '4.43', '3.5')
