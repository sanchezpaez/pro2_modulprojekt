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
        assert calculate_levenshtein_distance('help', 'loop') == 4


class TestBKTree:
    words = ["book", "books", "cake", "boo", "boon", "cook", "cake", "cape", "cart"]
    tree = BKTree(words)

    def test_search_word(self):
        assert self.tree.search_word('book', 1) == []

def test_create_triple():
    connections = ('book', {1: ('books', {2: ('boo', {1: ('boon', {}), 2: ('cook', {})})}),
                            4: ('cake', {0: ('cake', {}), 1: ('cape', {}), 2: ('cart', {})})})
    assert bktree.create_triple(connections) == [
        ('book', 'books', 1), ('books', 'boo', 2), ('boo', 'boon', 1), ('boo', 'cook', 2), ('book', 'cake', 4),
        ('cake', 'cake', 0), ('cake', 'cape', 1), ('cake', 'cart', 2)
    ]

def test_visualize_graph():
    test_triples = [
        ('book', 'books', 1), ('books', 'boo', 2), ('boo', 'boon', 1),
        ('boo', 'cook', 2), ('book', 'cake', 4), ('cake', 'cake', 0),
        ('cake', 'cape', 1), ('cake', 'cart', 2)
    ]
    test_tuples = [
        ('book', 'books'), ('books', 'boo'), ('boo', 'boon'), ('boo', 'cook'),
        ('book', 'cake'), ('cake', 'cake'), ('cake', 'cape'), ('cake', 'cart')
    ]
    assert bktree.visualize_graph(test_tuples, test_triples) == 0

def test_get_edge_labels():
    test_triples = [
        ('book', 'books', 1), ('books', 'boo', 2), ('boo', 'boon', 1),
        ('boo', 'cook', 2), ('book', 'cake', 4), ('cake', 'cake', 0),
        ('cake', 'cape', 1), ('cake', 'cart', 2)
    ]
    assert bktree.get_edge_labels(test_triples) == {}
