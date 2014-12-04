# -*- coding: utf-8 -*-
import string
import random
import re


class System:

    def generate_unique_set_from_list(self, list=[]):
        """
        fast method for creating a unique set.
        This is done to prevent duplicates

        :param list : list to sort
        :rtype : object
        :return: returns unique list of items
        """
        seen = set()
        seen_add = seen.add
        return [x for x in list if not (x in seen or seen_add(x))]

    def generate_subtitle_url_from_movie_name(self, name):
        """

        :rtype : object
        """
        base_url = 'http://subsmax.com/api/10/%s'
        # filter away non-ascii chars
        filteredName = self.remove_non_ascii_chars(name=name)
        try:
            # join name plus year into string for search.
            # Append -en to make english
            url = ('-'.join([str(x) for x in string.split(filteredName.lower(),
                                                          " ")]) + '-en')
            # Substitute illegal characters
            return base_url % self.remove_illegal_search_chars(url)
        except Exception as e:
            self.log.write_to_log(message=e, where="generate-url-from-name")

    def generate_random_alphanumeric_string(self, length=5):
        return ''.join(random.choice('0123456789ABCDEF')
                       for i in range(length))

    def remove_non_ascii_chars(self, name):
        return filter(lambda y: y in string.printable, name)

    def remove_illegal_search_chars(self, txt):
        return (re.sub('[!@#$.\'/:\"]', '', txt))
