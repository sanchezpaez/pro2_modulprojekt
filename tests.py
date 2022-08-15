# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


from bktree import BKTree, Graph


class TestBKTree:
    words = ["book", "books", "cake", "boo", "boon", "cook", "cake", "cape", "cart"]
    tree = BKTree(words)
    built_tree = tree.build_tree()

    def test_search_word(self):
        assert self.tree.search_word('book', 1) == ['book', 'books', 'boo', 'boon', 'cook']

    # class TestLevenshtein:
    def test_distance_0(self):
        assert self.tree.calculate_levenshtein_distance('man', 'man') == 0

    def test_distance_empty_string(self):
        assert self.tree.calculate_levenshtein_distance('', 'man') == 3

    def test_different_length_words(self):
        assert self.tree.calculate_levenshtein_distance('help', 'loop') == 3

    def test_calculate_dynamic(self):
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
    words = ["book", "books", "cake", "boo", "boon", "cook", "cake", "cape", "cart"]
    tree = BKTree(words)
    tree.tree = tree.build_tree()
    print(tree)
    graph = Graph(tree.tree)
    graph.create_triples()
    graph.create_tuples()

    def test_create_triple(self):
        # tree.tree = ('book', {1: ('books', {2: ('boo', {1: ('boon', {}), 2: ('cook', {})})}),
        #                         4: ('cake', {0: ('cake', {}), 1: ('cape', {}), 2: ('cart', {})})})
        assert self.graph.create_triples() == [
            ('book', 'books', 1), ('books', 'boo', 2), ('boo', 'boon', 1), ('boo', 'cook', 2), ('book', 'cake', 4),
            ('cake', 'cake', 0), ('cake', 'cape', 1), ('cake', 'cart', 2)
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
        test_triples = [
            ('book', 'books', 1), ('books', 'boo', 2), ('boo', 'boon', 1),
            ('boo', 'cook', 2), ('book', 'cake', 4), ('cake', 'cake', 0),
            ('cake', 'cape', 1), ('cake', 'cart', 2)
        ]
        assert self.graph.get_edge_labels() == {
            ('book', 'books'): 1, ('books', 'boo'): 2, ('boo', 'boon'): 1,
            ('boo', 'cook'): 2, ('book', 'cake'): 4, ('cake', 'cake'): 0,
            ('cake', 'cape'): 1, ('cake', 'cart'): 2
        }
