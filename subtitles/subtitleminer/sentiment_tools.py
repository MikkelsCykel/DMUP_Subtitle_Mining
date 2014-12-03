from subtitleminer import WarrinerRatings
from nltk.stem.wordnet import WordNetLemmatizer
from auxillary import Log


class ValenceArouselDominance(object):
    """
    This class contains methods for computing valence arousal and dominance
    """
    def __init__(self, arg):
        super(ValenceArouselDominance, self).__init__()
        self.wariner_ratings = WarrinerRatings()

    def compute_vad_intervals(self, text_intervals):
        x = self.wariner_ratings
        Log()
        lmtzr = WordNetLemmatizer()
        result = zip(*[(x[w][0], x[w][3], x[w][6])
                       for t in text_intervals
                       for w in t
                       if w or lmtzr.lemmatize(w) in x])
        return result
