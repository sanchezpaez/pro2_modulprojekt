# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import networkx as nx
from networkx import DiGraph
from networkx.drawing.nx_pydot import graphviz_layout

from bk_tree import BKTree
from graph import Graph

words = ["book", "books", "cake", "boo", "boon", "cook", "cape", "cart"]


class TestBKTree:
    tree = BKTree(words)
    built_tree = tree.build_tree()

    def test_search_word(self):
        assert self.tree.search_word('book', 1) == ['book', 'books', 'boo', 'boon', 'cook']

    # TestLevenshtein:
    def test_distance_0(self):
        assert self.tree.calculate_levenshtein_dynamic('man', 'man') == 0

    def test_distance_empty_string(self):
        assert self.tree.calculate_levenshtein_dynamic('', 'man') == 3

    def test_different_length_words(self):
        assert self.tree.calculate_levenshtein_dynamic('help', 'loop') == 3

    # TestDamerau:
    def test_damerau_levenshtein(self):
        assert self.tree.calculate_damerau_levenshtein('ab', 'ba') == 1
        assert self.tree.calculate_damerau_levenshtein('abcdef', 'abcfad') == 2

    # TestHamming:
    def test_different_length(self):
        assert True == self.tree.calculate_hamming_distance('book', 'books')

    def test_same_length_one(self):
        assert self.tree.calculate_hamming_distance('can', 'man') == 1

    def test_same_length_many(self):
        assert self.tree.calculate_hamming_distance('miracle', 'milagro') == 4

    def test_calculate_height(self):
        assert self.tree.calculate_height(self.built_tree) == 4


class TestGraph:
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

    def test_get_edge_labels(self):
        assert self.graph.get_edge_labels() == {
            ('book', 'books'): 1, ('books', 'boo'): 2, ('boo', 'boon'): 1,
            ('boo', 'cook'): 2, ('book', 'cake'): 4,
            ('cake', 'cape'): 1, ('cake', 'cart'): 2
        }

    def test_visualize_graph(self):
        tree_graph = nx.DiGraph()
        tree_graph.add_edges_from(self.graph.tuples)
        # This layout draws the directed graph in a hierarchical way
        positions = graphviz_layout(tree_graph, prog='dot')
        assert isinstance(nx.DiGraph(), DiGraph)
        assert graphviz_layout(tree_graph, prog='dot') == {
            'book': (103.6, 234.0), 'books': (65.597, 162.0), 'boo': (65.597, 90.0),
            'boon': (28.597, 18.0), 'cook': (103.6, 18.0), 'cake': (142.6, 162.0),
            'cape': (139.6, 90.0), 'cart': (211.6, 90.0)
        }
