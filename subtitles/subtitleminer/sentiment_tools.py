from subtitleminer import WarrinerRatings
from nltk.stem.wordnet import WordNetLemmatizer


class ValenceArouselDominance(object):
    """
    This class contains methods for computing valence arousal and dominance
    """
    def __init__(self):
        super(ValenceArouselDominance, self).__init__()
        self.warriner_ratings = WarrinerRatings()
        self.lmtzr_fall_back = False

    def compute_vad_intervals(self, text_intervals, lmtzr_fall_back=False):
        x = self.warriner_ratings
        self.lmtzr_fall_back = lmtzr_fall_back
        result = [zip(*[(
            '{0:.3g}'.format(float
                        (x[self.word_in_warriner_rankings(w)][0])),
            '{0:.3g}'.format(float
                            (x[self.word_in_warriner_rankings(w)][3])),
            '{0:.3g}'.format(float
                            (x[self.word_in_warriner_rankings(w)][6])))
                        for w in t if self.word_in_warriner_rankings(w)])
                  for t in text_intervals]
        return result

    def word_in_warriner_rankings(self, word):
        lmtzr = WordNetLemmatizer()
        if word in self.warriner_ratings.keys():
            return word
        if self.lmtzr_fall_back:
            word = lmtzr.lemmatize(word)
            if lmtzr.lemmatize(word) in self.warriner_ratings.keys():
                return word
        return False

    def mean_data(self, vad):
        return [sum(t) / len(t) for i in vad for t in i]
