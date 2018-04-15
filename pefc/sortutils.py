# Python Engineering Foundation Class Library (pefc)
# sortutils library
# Copyright(C) 2017 Heng Swee Ngee
#
# The Alphanum Algorithm is an improved sorting algorithm for strings
# containing numbers.  Instead of sorting numbers in ASCII order like
# a standard sort, this algorithm sorts numbers in numeric order.
#
# The Alphanum Algorithm is discussed at http://www.DaveKoelle.com
#
# Python implementation provided by Chris Hulan (chris.hulan@gmail.com)
# Distributed under same license as original
# Copyright(C) 2017 Dave Kolle
#
# Released under the MIT License - https://opensource.org/licenses/MIT
#

import re
from operator import itemgetter


class AlphaNum:
    # Class AlphaNum is based on Dave Kolle's Alphanum's Algorithm
    """ Solves 'The Problem' described by Dave Koelle
    Look at most sorted list of file names, product names, or any other
    text that contains alphanumeric characters - both letters and numbers.
    Traditional sorting algorithms use ASCII comparisons to sort
    these items, which means the end-user sees an unfortunately
    ordered list that does not consider the numeric values
    within the strings.

    For example, in a sorted list of files, "z100.html" is sorted
    before "z2.html". But obviously, 2 comes before 100!
    Sorting algorithms should sort alphanumeric strings in the order
    that users would expect, especially as software becomes increasingly
    used by nontechnical people. Besides, it's the 21st Century;
    software engineers can do better than this.

    Usage:
           string_list.sort(key=AlphaNum) or
           sorted_str_lst = sorted(string_list, key=AlphaNum) """

    re_chunk = re.compile(r"([\D]+|[\d]+)")
    re_letters = re.compile(r"\D+")
    re_numbers = re.compile(r"\d+")

    def __init__(self, obj):
        self.obj = obj

    @classmethod
    def getchunk(cls, item):
        itemchunk = cls.re_chunk.match(item)

        # Subtract the matched portion from the original string
        # if there was a match, otherwise set it to ""
        item = (item[itemchunk.end():] if itemchunk else "")
        # Don't return the match object, just the text
        itemchunk = (itemchunk.group() if itemchunk else "")

        return itemchunk, item

    @classmethod
    def cmp(cls, x, y):
        """
        Replacement for built-in function cmp that was removed in Python 3

        Compare the two objects x and y and return an integer according to
        the outcome. The return value is negative if x < y, zero if x == y
        and strictly positive if x > y.
        """

        return (x > y) - (x < y)

    @classmethod
    def cmp_alphanum(cls, a, b):
        n = 0

        while n == 0:
            # Get a chunk and the original string with the chunk subtracted
            ac, a = cls.getchunk(a)
            bc, b = cls.getchunk(b)

            # Both items contain only letters
            if cls.re_letters.match(ac) and cls.re_letters.match(bc):
                n = cls.cmp(ac, bc)
            else:
                # Both items contain only numbers
                if cls.re_numbers.match(ac) and cls.re_numbers.match(bc):
                    n = cls.cmp(int(ac), int(bc))
                # One item has letters and one item has numbers,
                # or one item is empty
                else:
                    n = cls.cmp(ac, bc)
                    # Prevent deadlocks
                    if n == 0:
                        n = 1

        return n

    def __lt__(self, other):
        return self.cmp_alphanum(self.obj, other.obj) < 0

    def __gt__(self, other):
        return self.cmp_alphanum(self.obj, other.obj) > 0

    def __eq__(self, other):
        return self.cmp_alphanum(self.obj, other.obj) == 0

    def __le__(self, other):
        return self.cmp_alphanum(self.obj, other.obj) <= 0

    def __ge__(self, other):
        return self.cmp_alphanum(self.obj, other.obj) >= 0

    def __ne__(self, other):
        return self.cmp_alphanum(self.obj, other.obj) != 0


def sort_by_month(dates_ls):
    """ Sort list of string_dates by month such as
        ['APR 2017.xls', 'JAN 2017.xls' ...]
    dates_ls: list of sorted string_dates to sort by month without year check
    return: sorted list
    """
    if not isinstance(dates_ls, list):
        print('Error: sort_by_month function process list of strings only')
        return dates_ls

    # cover also Bahasa Melayu but not Bahasa Indonesia
    month_dc = {'JAN': 1, 'JANUARY': 1, 'JANUARI': 1,
                'FEB': 2, 'FEBRUARY': 2, 'FEBRUARI': 2,
                'MAR': 3, 'MAC': 3, 'MARCH': 3, 'APR': 4, 'APRIL': 4,
                'MAY': 5, 'MEI': 5, 'JUN': 6, 'JUNE': 6,
                'JUL': 7, 'JULY': 7, 'JULAI': 7,
                'AUG': 8, 'AUGUST': 8, 'OGO': 8, 'OGOS': 8,
                'SEP': 9, 'SEPTEMBER': 9, 'SEPT': 9, 'OCT': 10, 'OCTOBER': 10,
                'NOV': 11, 'NOVEMBER': 11,
                'DEC': 12, 'DECEMBER': 12, 'DISEMBER': 12, 'DIS': 12}
    # use decorate and undecorate sorting method - Schwartzian transform
    decorate = []
    months = month_dc.keys()
    for date_s in dates_ls:
        date_us = date_s.upper()
        for mth in months:
            if date_us.rfind(mth) != -1:
                i = month_dc.get(mth)
                decorate.append((i, date_s))
                break
        else:
            decorate.append((13, date_s))  # if no such month put last
    decorate.sort(key=itemgetter(0))
    # undecorate and return
    return [date_s[1] for date_s in decorate]
