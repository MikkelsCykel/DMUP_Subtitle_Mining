import csv

"""
This class is providing the Warriner Rankings of almost 14.000 english words.
for further information please check, the authors documentation available at:
http://crr.ugent.be/papers/Warriner_et_al_affective_ratings.pdf

Exampels:
---------
>>> w = WarrinerRatings()
>>> w['attribute_names'][0:3]
['V.Mean.Sum','V.SD.Sum','V.Rat.Sum','A.Mean.Sum']

>>> w['awesome'][0:3]
['7.86','1.85','21','6.05']

"""


class WarrinerRatings(dict):
    """Warriner Ratings"""

    def __new__(cls):
        """Constructs a new dictionary containing words and their ratings"""

        x = {}
        with open('data/Ratings_Warriner_et_al.csv') as file:
            data = csv.reader(file, delimiter=',')
            x['attribute_names'] = data.next()[2:]
            for r in data:
                x[r[1]] = r[2:]
        return x
