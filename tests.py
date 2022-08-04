# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


from bktree import calculate_levenshtein_distance, BKTree
import bktree


class TestLevenshtein:

    def test_distance_0(self):
        assert calculate_levenshtein_distance('man', 'man') == 0

    def test_distance_empty_string(self):
        assert calculate_levenshtein_distance('', 'man') == 3

    def test_different_length_words(self):
        assert calculate_levenshtein_distance('cream', 'corn') == 4


class TestBKTree:
    words = ["book", "books", "cake", "boo", "boon", "cook", "cake", "cape", "cart"]
    tree = BKTree(words)

    def test_search_word(self):
        assert self.tree.search_word('book', 1) == []

def test_create_triple():
    connections = ('book', {1: ('books', {2: ('boo', {1: ('boon', {}), 2: ('cook', {})})}),
                            4: ('cake', {0: ('cake', {}), 1: ('cape', {}), 2: ('cart', {})})})
    assert bktree.create_triple(connections) == []
