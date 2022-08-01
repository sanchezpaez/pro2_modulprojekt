# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import sys


class BKTree:
    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.ld = calculate_levenshtein_distance
        self.root = wordlist[0]
        self.tree = (self.root, {})

    def build_tree(self):
        """Build BK Tree from list of strings."""
        for word in self.wordlist[1:]:
            self.tree = self.insert_word(self.tree, word)
            print(self.tree)

    def insert_word(self, node, word):
        d = self.ld(word, node[0])
        if d not in node[1]:
            node[1][d] = (word, {})
        else:
            self.insert_word(node[1][d], word)
        return node


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


# todo: add another string metric: string metrics like Damerau-Levenshtein,
# Hamming distance, Jaro-Winkler and Strike a match.

def read_data_from_filename(filename):
    with open(filename) as file:
        content = file.read().lower().split()
        return content


if __name__ == '__main__':
    # filename = sys.argv[1]
    # words = read_data_from_filename(filename)
    # terminal_tree = BKTree(words)
    test_words = ["book", "books", "cake", "boo", "boon", "cook", "cake", "cape", "cart"]
    test_tree = BKTree(test_words)
    print(calculate_levenshtein_distance('book', 'cake'))
    print(test_tree.build_tree())


# Added txt file as example and started building tree from wordlist