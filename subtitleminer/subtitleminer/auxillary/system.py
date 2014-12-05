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
        Method for generating the specific string used for search
        for subtitles to a movie at submax.com
        Filters out non-ascii chars and joins name and year with "-en"
        before concatenating with base_url

        :param name : name (and year) of movie in one string
        :rtype : object
        :return: concatenated string
        """
        base_url = 'http://subsmax.com/api/10/%s'
        filteredName = self.remove_non_ascii_chars(st=name)
        try:
            url = ('-'.join([str(x) for x in string.split(filteredName.lower(),
                                                          " ")]) + '-en')
            return base_url % self.remove_illegal_search_chars(url)
        except Exception as e:
            self.log.write_to_log(message=e, where="generate-url-from-name")

    def generate_random_alphanumeric_string(self, length=5):
        """
        Function for generating a random string og alphanumeric chars.


        :param length : length of the random string. default 5
        :rtype : object
        :return :
        """
        return ''.join(random.choice('0123456789ABCDEF')
                       for i in range(length))

    def remove_non_ascii_chars(self, st):
        """
        Method for removing non-ascii char that mess up certain
        functions using lambda expression.

        :param string : the string to be cleared
        :rtype : object
        :return : ascii string
        """
        return filter(lambda y: y in string.printable, st)

    def remove_illegal_search_chars(self, txt):
        """
        Method for removing illegal chars for searcing
        like single and double quotes

        :param txt: String to be escaped
        :rtype : object
        :return: escaped string.
        """
        return (re.sub('[!@#$.\'/:\"]', '', txt))
