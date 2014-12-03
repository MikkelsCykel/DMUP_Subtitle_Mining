
# Class containing general usability axillary functions
from auxillary import log
import string
import random
import re


class System:
    def __init__(self):
        self.log = log.Log()

    def generateUniqueSetFromList(self, list=[]):
        # fast method for creating a unique set. This is done to prevent duplicates
        seen = set()
        seen_add = seen.add
        return [ x for x in list if not (x in seen or seen_add(x))]

    def generate_subtitle_url_from_movie_name(self, name):
        base_url = 'http://subsmax.com/api/10/%s'
        # filter away non-ascii chars
        filteredName = self.remove_non_ascii_chars(name=name)
        try:
            # join name plus year into string for search. Append -en to make english
            url = ('-'.join([str(x) for x in string.split(filteredName.lower(), " ")]) + '-en')
            # Substitute illegal characters
            return base_url % self.remove_illegal_search_chars(url)
        except Exception as e:
            self.log.writeToLog(message=name, where="generate-url-from-name")


    def generateRandomAlphanumericString(self, length=5):
        return ''.join(random.choice('0123456789ABCDEF') for i in range(length))

    def remove_non_ascii_chars(self, name):
        return filter(lambda y: y in string.printable, name)

    def remove_illegal_search_chars(self, txt):
        return (re.sub('[!@#$.\'/:\"]', '', txt))