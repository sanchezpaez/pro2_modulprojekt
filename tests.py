# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


from bktree import BKTree, create_triple, get_edge_labels
from bktree import calculate_levenshtein_distance, calculate_hamming_distance


class TestLevenshtein:

    def test_distance_0(self):
        assert calculate_levenshtein_distance('man', 'man') == 0

    def test_distance_empty_string(self):
        assert calculate_levenshtein_distance('', 'man') == 3

    def test_different_length_words(self):
        assert calculate_levenshtein_distance('help', 'loop') == 3


class TestHamming:

    def test_different_length(self):
        assert True == calculate_hamming_distance('book', 'books')

    def test_same_length_one(self):
        assert calculate_hamming_distance('can', 'man') == 1

    def test_same_legth_many(self):
        assert calculate_hamming_distance('miracle', 'milagro') == 4


class TestBKTree:
    words = ["book", "books", "cake", "boo", "boon", "cook", "cake", "cape", "cart"]
    tree = BKTree(words)
    tree.build_tree()

    def test_search_word(self):
        assert self.tree.search_word('book', 1) == ['book', 'books', 'boo', 'boon', 'cook']


def test_create_triple():
    connections = ('book', {1: ('books', {2: ('boo', {1: ('boon', {}), 2: ('cook', {})})}),
                            4: ('cake', {0: ('cake', {}), 1: ('cape', {}), 2: ('cart', {})})})
    assert create_triple(connections) == [
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
    assert visualize_graph(test_tuples, test_triples) == 0


def test_get_edge_labels():
    test_triples = [
        ('book', 'books', 1), ('books', 'boo', 2), ('boo', 'boon', 1),
        ('boo', 'cook', 2), ('book', 'cake', 4), ('cake', 'cake', 0),
        ('cake', 'cape', 1), ('cake', 'cart', 2)
    ]
    assert get_edge_labels(test_triples) == {
        ('book', 'books'): 1, ('books', 'boo'): 2, ('boo', 'boon'): 1,
        ('boo', 'cook'): 2, ('book', 'cake'): 4, ('cake', 'cake'): 0,
        ('cake', 'cape'): 1, ('cake', 'cart'): 2
    }
