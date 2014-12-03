from subtitleminer import WarrinerRatings
# from nltk.stem.wordnet import WordNetLemmatizer


class ValenceArouselDominance(object):
    """
    This class contains methods for computing valence arousal and dominance
    """
    def __init__(self):
        super(ValenceArouselDominance, self).__init__()
        self.wariner_ratings = WarrinerRatings()

    def compute_vad_intervals(self, text_intervals):
        x = self.wariner_ratings
        result = [(x[w][0], x[w][3], x[w][6], w)
                  for t in text_intervals for w in t
                  if w in x.keys()]
        return result

    # def __is_word_in_warriner_rankings(self, wr, word):
    #     lmtzr = WordNetLemmatizer()
    #     if w in wr.keys():
    #         return w
    #     lmtzr.lemmatize(word)
    #     if lmtzr.lemmatize(word) in wr.keys():
    #         return
