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
>>> print x[0][:5]
['forget', 'it.', "it's", 'risky.', "i'm"]
"""


class StampedSrt(dict):
    """Timestamped Subtitle"""

    def __new__(cls, path, remove_symbols=False):
        """
        Constructs a new dictionary containing lines spoken,
        keyed by timestamp in seconds

        Params
        ------
        path           : path to subtitle
        remove_symbols : should symbols be removed, default False
        """
        if type(remove_symbols) != bool:
            print ("remove_symbols is %s, expected bool. defaulting to False"
                   % type(remove_symbols))
            remove_symbols = False

        subtitle_result = cls.__load_subtitle(path=path)
        formatted_dict = cls.__format_subtitle_result(subtitle_result,
                                                      remove_symbols)
        return formatted_dict

    @classmethod
    def __load_subtitle(cls, path):
        """Loads the subtitle from specified path"""
        subtitle = ''
        try:
            with open(path) as subtitlefile:
                for r in subtitlefile:
                    subtitle += r
            return subtitle
        except IOError:
            raise IOError('The subtitle file was not found in %s' % path)

    @classmethod
    def __format_subtitle_result(cls, srt, remove_symbols):
        """This method formats the subtitle into a nice looking dictionary"""
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
        """
        A subtitle has a timestamp of the following form:
        00:01:17,911 --> 00:01:19,980
        We want to convert this into a integer timestamp in seconds for this
        example it would become 77

        """
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
    """Subtitle divided into time intervals"""
    def __new__(cls, stamped_srt, interval_sec, remove_stop_words=False):
        """
        Constructs a new list of lists.
        A list i generated for each interval in the subtitle, consisting of the
        words spoken whitin the given time interval.

        Params
        ------
        stamped_srt      : a StampedSrt dictionary
        interval_sec     : a timeinterval in seconds
        remove_stop_words: should stopwords be removed? default False
        """

        try:
            assert type(stamped_srt) == dict
        except AssertionError:
            raise TypeError('stamped_srt is of %s, expected dict. \
                values should be strings' % type(StampedSrt))

        try:
            assert type(interval_sec) == int
        except AssertionError:
            raise TypeError('interval_sec is of %s, expected int. \
                value is a timeinterval in int' % type(StampedSrt))

        if type(remove_stop_words) != bool:
            print 'invalid %s for remove_stop_words defaulting to False'\
                  % type(remove_stop_words)
            remove_stop_words = False

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
