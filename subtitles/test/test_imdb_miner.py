import re
from subtitleminer import ImdbMiner

"""test data Pulp Fiction comes with the package"""
pathname = "data/Pulp_Fiction.en.srt"


def test_imdb_fetching_fromUrl():
    info = ImdbMiner.fetch_imdb_releases(range=1)
    assert len(info.keys()) > 0

#
# def test_that_subtitle_result_is_dictionary_object():
#     x = StampedSrt(path=pathname)
#     assert type(x) is dict
#
#
# def test_that_symbols_can_be_removed():
#     x = StampedSrt(path=pathname, remove_symbols=True)
#     temp = ""
#     for i in x.keys():
#         temp += x[i]
#     temp = re.findall(r'([-\!$%^&*()_+|~=`{}\[\]:";<>\?,.\/])', temp)
#     assert len(temp) == 0
#
#
# def test_that_symbols_can_be_included():
#     x = StampedSrt(path=pathname, remove_symbols=False)
#     temp = ""
#     for i in x.keys():
#         temp += x[i]
#     temp = re.findall(r'([-\!$%^&*()_+|~=`{}\[\]:";<>\?,.\/])', temp)
#     assert len(temp) > 0
#
#
# def test_that_stamped_srt_is_devided_into_a_time_interval_list():
#     x = StampedSrt(path=pathname, remove_symbols=True)
#     interval = 120
#     y = SubtitleInIntervals(stamped_srt=x, interval_sec=interval)
#     z = sorted(x.keys())[-1] / interval
#     assert z == len(y)
