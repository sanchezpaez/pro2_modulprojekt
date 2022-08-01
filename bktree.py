# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022

class BKTree:
    def __init__(self, wordlist):
        self.wordlist = wordlist


def calculate_levenshtein_distance(str_1, str_2) -> int:
    """
    The Levenshtein distance is a string metric that measures the difference
    between two sequences. If two strings are similar, the distance should
    be small. If they are very different, the distance should be large.
    :rtype: int representing the minimum number of single-character edits
    (insert, delete or replace) necessary to transform one word (string)
    into another.
    """
    if str_1 == str_2:
        edits = 0
    elif not str_1:
        edits = len(str_2)
    elif not str_2:
        edits = len(str_1)
    else:
        # Compute the minimal number of edits (insert, delete, or replace)
        edits = min(calculate_levenshtein_distance(str_1, str_2[1:]) + 1,
                    calculate_levenshtein_distance(str_1[1:], str_2) + 1,
                    calculate_levenshtein_distance(str_1[1:], str_2[1:]) + (str_1[0] != str_2[0]))
    return edits


if __name__ == '__main__':
    test_wordlist = BKTree(["cat", "cut", "hat", "man", "hit"])
    print(calculate_levenshtein_distance('cat', 'chello'))
