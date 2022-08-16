# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


from bk_tree import BKTree
from graph import Graph


class TestBKTree:
    words = ["book", "books", "cake", "boo", "boon", "cook", "cape", "cart"]
    tree = BKTree(words)
    built_tree = tree.build_tree()

    def test_search_word(self):
        assert self.tree.search_word('book', 1) == ['book', 'books', 'boo', 'boon', 'cook']

    # class TestLevenshtein:
    def test_distance_0(self):
        assert self.tree.calculate_levenshtein_dynamic('man', 'man') == 0

    def test_distance_empty_string(self):
        assert self.tree.calculate_levenshtein_dynamic('', 'man') == 3

    def test_different_length_words(self):
        assert self.tree.calculate_levenshtein_dynamic('help', 'loop') == 3

    # class TestHamming:

    def test_different_length(self):
        assert True == self.tree.calculate_hamming_distance('book', 'books')

    def test_same_length_one(self):
        assert self.tree.calculate_hamming_distance('can', 'man') == 1

    def test_same_length_many(self):
        assert self.tree.calculate_hamming_distance('miracle', 'milagro') == 4

    def test_calculate_height(self):
        assert self.tree.calculate_height(self.built_tree) == 4


class TestGraph:
    words = ["book", "books", "cake", "boo", "boon", "cook", "cape", "cart"]
    tree = BKTree(words)
    tree.tree = tree.build_tree()
    graph = Graph(tree.tree)
    graph.get_edge_labels()

    def test_create_triples(self):
        assert self.graph.triples == [
            ('book', 'books', 1), ('books', 'boo', 2), ('boo', 'boon', 1),
            ('boo', 'cook', 2), ('book', 'cake', 4), ('cake', 'cape', 1),
            ('cake', 'cart', 2)
        ]

    def test_create_tuples(self):
        assert self.graph.tuples == [
            ('book', 'books'), ('books', 'boo'), ('boo', 'boon'),
            ('boo', 'cook'), ('book', 'cake'), ('cake', 'cape'),
            ('cake', 'cart')
        ]

    def test_visualize_graph(self):
        test_triples = [
            ('book', 'books', 1), ('books', 'boo', 2), ('boo', 'boon', 1),
            ('boo', 'cook', 2), ('book', 'cake', 4), ('cake', 'cake', 0),
            ('cake', 'cape', 1), ('cake', 'cart', 2)
        ]
        test_tuples = [
            ('book', 'books'), ('books', 'boo'), ('boo', 'boon'), ('boo', 'cook'),
            ('book', 'cake'), ('cake', 'cake'), ('cake', 'cape'), ('cake', 'cart')
        ]
        assert self.graph.visualize_graph() == 0

    def test_get_edge_labels(self):
        assert self.graph.get_edge_labels() == {
            ('book', 'books'): 1, ('books', 'boo'): 2, ('boo', 'boon'): 1,
            ('boo', 'cook'): 2, ('book', 'cake'): 4,
            ('cake', 'cape'): 1, ('cake', 'cart'): 2
        }
