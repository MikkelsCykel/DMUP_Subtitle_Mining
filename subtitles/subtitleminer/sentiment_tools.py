import WarrinerRatings
from nltk.stem.wordnet import WordNetLemmatizer


class ValenceArouselDominance(object):
    """
    This class contains methods for computing valence arousal and dominance
    """
    def __init__(self, arg):
        super(ValenceArouselDominance, self).__init__()
        self.wariner_ratings = WarrinerRatings()

    def compute_vad_intervals(self, text_intervals):
        V = []
        A = []
        D = []
        x = self.wariner_ratings
        lmtzr = WordNetLemmatizer()

        V = zip([[(x[w][0], x[w][3], x[w][6])
             for w in i if w or lmtzr.lemmatize(w) in x]
             for i in text_intervals]
        # for i in text_intervals:
        #     tempV = 0
        #     tempA = 0
        #     tempD = 0
        #     count = 0.0
        #     for word in i:
        #         if word in self.wariner_ratings:
        #             count += 1
        #             tempV += float(self.wariner_ratings[word][0])
        #             tempA += float(self.wariner_ratings[word][3])
        #             tempD += float(self.wariner_ratings[word][6])
        #             continue
        #         z = lmtzr.lemmatize(word)
        #         if z in self.wariner_ratings:
        #             count += 1
        #             tempV += float(self.wariner_ratings[z][0])
        #             tempA += float(self.wariner_ratings[z][3])
        #             tempD += float(self.wariner_ratings[z][6])
        #     if count != 0.0:
        #         V.append(tempV / count)
        #         A.append(tempA / count)
        #         D.append(tempD / count)
        #     else:
        #         V.append(V[-1])
        #         A.append(A[-1])
        #         D.append(D[-1])
        # return V, A, D
