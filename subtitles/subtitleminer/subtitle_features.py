# -*- coding: utf-8 -*-
import re
from nltk.corpus import stopwords


"""
This collection is providing various features for data extraction of subtitles

Exampels:
---------
>>> s = StampedSrt('data/Pulp_Fiction.en.srt')
>>> print s[8950]
And I will strike down upon thee with great vengeance and furious anger...

>>> x = SubtitleInIntervals(stamped_srt = s,
                            interval_sec = 180,
                            remove_stop_words=True)
>>> s
"""


class StampedSrt(dict):
    """Timestamped Subtitle"""

    def __new__(cls, path, remove_symbols=False):
        """
        Constructs a new dictionary containing lines spoken,
        keyed by timestamp in seconds
        """
        subtitle_result = cls.__load_subtitle(path=path)
        formatted_dict = cls.__format_subtitle_result(subtitle_result,
                                                      remove_symbols)
        return formatted_dict

    @classmethod
    def __load_subtitle(cls, path):
        subtitle = ''
        with open(path) as subtitlefile:
            for r in subtitlefile:
                subtitle += r
        return subtitle

    @classmethod
    def __format_subtitle_result(cls, srt, remove_symbols):
        srt = srt.replace('\r', '').split('\n')
        result = {}
        d = 0
        mc = 1
        sc = 1
        for s in srt:
            if s in '' or s.isdigit() or 'Downloaded From www.' in s:
                continue
            if '-->' in s:
                st, mc, sc, d = cls.__gen_stamp_from_srt_notation(s, mc, sc, d)
                if d > st:
                    break
                st = st - d
                continue
            if remove_symbols:
                s = re.sub(r'[^\w]', ' ', s)
            if st in result:
                result[st] += ' ' + s
                continue
            result[st] = s
        return result

    @classmethod
    def __gen_stamp_from_srt_notation(cls, stamp, minutes_count,
                                      seconds_count, difference):

        regex = re.findall('([0-9]+):([0-9]+):([0-9]+)', stamp)
        out_stamp = int(regex[0][0] + regex[0][1] + regex[0][2])

        temp = out_stamp / 10000
        if temp > minutes_count:
            minutes_count = temp
        if temp == minutes_count:
            difference += 4000
            minutes_count += 1

        temp = out_stamp / 100
        if temp > seconds_count:
            seconds_count = temp
        if temp == seconds_count:
            difference += 40
            seconds_count += 1
        return out_stamp, minutes_count, seconds_count, difference


class SubtitleInIntervals(list):
    """Provides a list of text from provided timeinterval in seconds"""
    def __new__(cls, stamped_srt, interval_sec, remove_stop_words=False):
        result = []
        swords = []
        if remove_stop_words:
            swords = stopwords.words('english')
        threshold = interval_sec
        temp = []
        for k in sorted(stamped_srt.keys()):
            if k < threshold:
                temp += [w.lower() for w in stamped_srt[k].split()
                         if w.lower() not in swords]
            else:
                result.append(temp)
                temp = []
                threshold += interval_sec
        return result
