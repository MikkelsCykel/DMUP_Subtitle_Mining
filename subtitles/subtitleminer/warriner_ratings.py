import csv


class WarrinerRatings(dict):
    """Warriner Ratings provided as a dictionary with words as keys"""

    def __new__(cls):
        x = {}
        with open('data/Ratings_Warriner_et_al.csv') as file:
            data = csv.reader(file, delimiter=',')
            x['attribute_names'] = data.next()[2:]
            for r in data:
                x[r[1]] = r[2:]
            return x
