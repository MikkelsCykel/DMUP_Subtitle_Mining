# -*- coding: utf-8 -*-
from subtitleminer import WarrinerRatings
from nltk.stem.wordnet import WordNetLemmatizer
"""
This collection provides features for extracting sentiment related features
from the provided text.

Example
-------

>>> from subtitleminer import StampedSrt, SubtitleInIntervals
>>> s = StampedSrt('data/Pulp_Fiction.en.srt')
>>> t = SubtitleInIntervals(s,180)
>>> vad = ValenceArouselDominance()
>>> VAD = vad.compute_vad_intervals(t)
>>> print VAD[0][0][:5]
(3.73, 5.91, 5.55, 6.82, 7.32)

>>> m_data = vad.mean_data(VAD)
print mean_data[0]
[5.537391304347825, 4.271739130434786, 5.247934782608694]
"""


class ValenceArouselDominance(object):
    """
    This class contains methods for computing valence arousal and dominance
    """
    def __init__(self):
        """Initializes the ValenceArouselDominance object"""
        super(ValenceArouselDominance, self).__init__()
        self.warriner_ratings = WarrinerRatings()
        self.known_words = self.warriner_ratings.keys()
        self.lmtzr_fall_back = False
        self.lmtzr = WordNetLemmatizer()

    def compute_vad_intervals(self, text_intervals, lmtzr_fall_back=False):
        """
        This method computes the Valence, Arousel and Dominance for a
        SubtitleInIntervals list, it returns a list of lists corresponding to
        the intervals. The interval list contains a tuple comtaining the
        score in each dimension, Eg:
        [['interval0word0','interval0word1'],['interval1word0']] =
        [[(V,A,D)(V,A,D)],[(V,A,D)]]

        Params
        ------
        text_intervals : SubtitleInIntervals
        lmtzr_fall_back: Should the analysis fall back to the words stemmed
                         from if it were not found in it given form,
                         default False
        """

        try:
            assert type(text_intervals) == list
        except AssertionError:
            raise TypeError('text_intervals is of %s, expected list. \
                A list of intervals containing text' % type(text_intervals))

        x = self.warriner_ratings
        self.lmtzr_fall_back = lmtzr_fall_back
        result = [zip(*[(float(x[self.word_in_warriner_rankings(w)][0]),
                         float(x[self.word_in_warriner_rankings(w)][3]),
                         float(x[self.word_in_warriner_rankings(w)][6]))
                        for w in t if self.word_in_warriner_rankings(w)])
                  for t in text_intervals]
        return result

    def word_in_warriner_rankings(self, word):
        """
        Check if a word is in our Warriner Ratings dict and return the word in
        its found form. Ie. if lmtzr_fall_back is True it will return the words
        stemmed version. Returns False otherwise.
        """
        if word in self.known_words:
            return word
        if self.lmtzr_fall_back:
            word = self.lmtzr.lemmatize(word)
            if self.lmtzr.lemmatize(word) in self.known_words:
                return word
        return False

    def mean_data(self, vad):
        """
        This method takes a VAD list and computes the mean value score
        for each dimention in each interval
        """
        return [[sum(t) / len(t) for t in i] for i in vad]
