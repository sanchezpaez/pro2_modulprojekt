# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 22.08.2022


import unittest

import networkx as nx
from networkx import DiGraph
from networkx.drawing.nx_pydot import graphviz_layout

from classes.bk_tree import BKTree
from classes.exception import NoWordsMatchedError, NotATextFileError, EmptyTreeError
from classes.file import File
from classes.graph import Graph

words = ["book", "books", "cake", "boo", "boon", "cook", "cape", "cart"]


class TestFile:
    dataset = File('demo_words2.txt')
    dataset2 = File('test_words_whitespace.txt')

    def test_load_vocab(self):
        assert self.dataset.load_vocab() == [
            'help', 'hell', 'hello', 'loop', 'helps', 'troop', 'shell', 'helper'
        ]

    def test_word_each_line(self):
        assert self.dataset2.load_vocab() == ['hello', 'here', 'is', 'an', 'example']

    def test_make_bktree_from_file_type(self):
        assert type(self.dataset.make_bktree_from_file()) == BKTree

    def test_make_bktree_from_file_tree_unloaded(self):
        assert self.dataset.make_bktree_from_file().tree == (
            'help', {1: ('hell', {2: ('helps', {})}),
                     2: ('hello', {2: ('shell', {}),
                                   3: ('helper', {})}), 3: ('loop', {}), 4: ('troop', {})}
        )

    def test_make_bktree_from_file_tree_loaded(self):
        assert self.dataset.make_bktree_from_file().tree \
               == self.dataset.make_bktree_from_file(is_loaded=True).tree


class TestBKTree:
    tree = BKTree(words, 'words')
    built_tree = tree.build_tree()
    tree_2 = BKTree(words, 'words_2')

    def test_build_loaded_tree(self):
        assert self.tree_2.build_tree(is_loaded=True) == (
            'book', {1: ('books', {2: ('boo', {1: ('boon', {}),
                                               2: ('cook', {})})}),
                     4: ('cake', {1: ('cape', {}), 2: ('cart', {})})}
        )
        assert self.tree.tree == self.tree_2.tree

    def test_calculate_height(self):
        assert self.tree.calculate_height(self.tree.tree) == 4

    # Test search_word

    def test_search_word_no_distance(self):
        assert self.tree.search_word('book', 0) == ['book']

    def test_search_word_several_matches(self):
        assert self.tree.search_word('book', 1) == ['book', 'books', 'boo', 'boon', 'cook']

    # Test calculate_levenshtein_distance:
    def test_distance_0(self):
        assert self.tree.calculate_levenshtein_distance('man', 'man') == 0

    def test_distance_empty_string(self):
        assert self.tree.calculate_levenshtein_distance('', 'man') == 3

    def test_different_length_words(self):
        assert self.tree.calculate_levenshtein_distance('help', 'loop') == 3

    def test_transposition(self):
        assert self.tree.calculate_levenshtein_distance('abcdef', 'abcfad') == 3

    # Test calculate_damerau_levenshtein:
    def test_distance_0_dam(self):
        assert self.tree.calculate_damerau_levenshtein('man', 'man') == 0

    def test_distance_empty_string_dam(self):
        assert self.tree.calculate_damerau_levenshtein('', 'man') == 3

    def test_different_length_words_dam(self):
        assert self.tree.calculate_damerau_levenshtein('help', 'loop') == 2

    def test_damerau_levenshtein_transposition(self):
        assert self.tree.calculate_damerau_levenshtein('ab', 'ba') == 1
        assert self.tree.calculate_damerau_levenshtein('abcdef', 'abcfad') == 2


class TestGraph:
    tree = BKTree(words, 'words')
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


class MyTestCase(unittest.TestCase):
    dataset = File('demo_words')
    tree = BKTree(words, 'words')
    built_tree = tree.build_tree()
    empty_list = []
    empty_tree = BKTree(empty_list, 'empty')
    empty_tree.build_tree()

    def test_search_word_no_matches_error(self):
        with self.assertRaises(NoWordsMatchedError):
            self.tree.search_word('hedgehog', 1)

    def test_not_text_file_error(self):
        with self.assertRaises(NotATextFileError):
            self.dataset.load_vocab()

    def test_empty_list_error(self):
        with self.assertRaises(EmptyTreeError):
            self.empty_tree.calculate_height(self.empty_tree.root)
