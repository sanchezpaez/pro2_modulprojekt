# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import sys

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


class StringMetric:

    def __init__(self, string_1, string_2):
        self.string_1 = string_1
        self.string_2 = string_2


def read_data_from_filename(filename):
    with open(filename) as file:
        content = file.read().lower().split()
        return content


def create_triple(nested_tuple):
    """
    Take in a nested tuple with a bk-tree structure and adapt it to
    a tuple of 3 format, where node_1, node_2 and their edit distance is
    represented. The resulting list of tuples will be then used by networkx
    to draw a graph visualization of the bk-tree structure.
    :param nested_tuple: str, str, int
    :return: list of labels
    """
    triples = []
    node_1 = nested_tuple[0]
    nested_element = nested_tuple[1]
    for distance in nested_element:
        node_2 = nested_element[distance][0]
        triple = node_1, node_2, distance
        triples.append(triple)
        new_tuple = nested_element[distance]
        if new_tuple[1]:
            triples = triples + create_triple(new_tuple)

    return triples


def create_tuple(nested_tuple):
    tuples = []
    node_1 = nested_tuple[0]
    nested_element = nested_tuple[1]
    for distance in nested_element:
        node_2 = nested_element[distance][0]
        tuple = node_1, node_2
        tuples.append(tuple)
        new_tuple = nested_element[distance]
        if new_tuple[1]:
            tuples = tuples + create_tuple(new_tuple)

    return tuples


def visualize_graph(tuples, triples):
    G = nx.DiGraph()
    G.add_edges_from(tuples)
    pos = graphviz_layout(G, prog='dot')
    # G.add_weighted_edges_from(triples)
    nx.draw_networkx(G, pos=pos, node_size=1500, arrows=True)
    edge_labels = get_edge_labels(triples)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=edge_labels)
    plt.savefig("bktree.png")
    plt.show()


def get_edge_labels(triples):
    labels = {}
    for triple in triples:
        node_1 = triple[0]
        node_2 = triple[1]
        label = triple[2]
        if (node_1, node_2) not in labels:
            labels[node_1, node_2] = label

    return labels


class BKTree:
    def __init__(self, wordlist):
        self.wordlist = wordlist
        self.ld = self.calculate_levenshtein_distance
        self.root = wordlist[0]
        self.tree = (self.root, {})

    def calculate_levenshtein_distance(self, string_1, string_2) -> int:
        """
        The Levenshtein distance is a string metric that measures the difference
        between two sequences. If two strings are similar, the distance should
        be small. If they are very different, the distance should be large.
        :rtype: int representing the minimum number of single-character edits
        (insert, delete or replace) necessary to transform one word (string)
        into another.
        """
        if string_1 == string_2:
            edits = 0
        elif not string_1:
            edits = len(string_2)
        elif not string_2:
            edits = len(string_1)
        else:
            # Compute the minimal number of edits (insert, delete, or replace)
            edits = min(self.calculate_levenshtein_distance(string_1, string_2[1:]) + 1,
                        self.calculate_levenshtein_distance(string_1[1:], string_2) + 1,
                        # If the characters are the same, we don't increase the edits, else we do by 1
                        self.calculate_levenshtein_distance(string_1[1:], string_2[1:]) + (string_1[0] != string_2[0]))
        return edits

    def calculate_hamming_distance(self, string_1, string_2):
        """
        If two strings are of the same length, calculate the
        number of substitutions to turn one string into the
        other.
        :return: int representing number of substitutions.
        """
        is_not_measurable = False
        if len(string_1) != len(string_2):
            is_not_measurable = True
            print(f"'{string_1}' and '{string_2}' cannot be compared,"
                  f" for they are of different length.")
            return is_not_measurable
        else:
            edits = 0
            for i, ch in enumerate(string_1):
                if string_2[i] != string_1[i]:
                    edits += 1
        return edits

    def build_tree(self):
        """Build BK Tree from list of strings."""
        for word in self.wordlist[1:]:
            self.tree = self.insert_word(self.tree, word)
        print(self.tree)
        return self.tree

    def insert_word(self, node, word):
        """Insert a new word in the tree."""
        d = self.ld(word, node[0])
        if d in node[1]:
            self.insert_word(node[1][d], word)
        else:
            node[1][d] = (word, {})
        return node

    def search_word(self, word, d):
        """
        Find words within the specified edit distance (d)
        from the search word.
        """

        def search(node):
            distance_to_root = self.ld(word, node[0])
            matching_words = []
            if distance_to_root <= d:
                matching_words.append(node[0])
            for i in range(distance_to_root - d, distance_to_root + d + 1):
                children = node[1]
                if i in children:
                    matching_words.extend(search(node[1][i]))
            return matching_words

        root = self.tree
        return search(root)

    def status(self):
        number_of_words = len(self.wordlist)


if __name__ == '__main__':
    # First stage: read data from file and build bk tree
    filename = sys.argv[1]
    words = read_data_from_filename(filename)
    terminal_tree = BKTree(words)
    test_words = ["help", "hell", "hello", "loop", "helps", "troop", "shell", "helper"]
    test_tree = BKTree(test_words)
    print(test_tree.calculate_levenshtein_distance('help', 'loop'))
    print(test_tree.calculate_hamming_distance('can', 'man'))
    built_tree = test_tree.build_tree()
    print(test_tree.search_word('help', 1))

    # Second stage: Visualize bk-tree as graph
    # Reformat data
    test_triples = create_triple(built_tree)
    print(test_triples)
    tests_tuples = create_tuple(built_tree)
    print(tests_tuples)
    graph = visualize_graph(tests_tuples, test_triples)

    # Third stage: interactive mode (word query)
    user_input = input('Please enter a word query and the desired edit distance\n')
    search_word = user_input.split()[0]
    d = user_input.split()[1]
