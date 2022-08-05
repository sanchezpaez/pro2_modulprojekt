# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import sys

import matplotlib.pyplot as plt
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout


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

    # And another one
    # T = nx.balanced_tree(2, 5)
    #
    # pos = graphviz_layout(T, prog="twopi")
    # nx.draw(T, pos)
    # plt.show()

    # g = nx.DiGraph()
    # g.add_weighted_edges_from(test_triples)
    # p = nx.drawing.nx_pydot.to_pydot(g)
    # p.write_png('example.png')


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
        self.ld = calculate_levenshtein_distance
        self.root = wordlist[0]
        self.tree = (self.root, {})

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
    #test_words = ["book", "books", "cake", "boo", "boon", "cook", "cake", "cape", "cart"]
    test_words = ["help", "hell", "hello", "loop", "helps", "troop", "shell", "helper"]
    test_tree = BKTree(test_words)
    print(calculate_levenshtein_distance('help', 'loop'))
    built_tree = test_tree.build_tree()
    print(test_tree.search_word('help', 1))
    test_triples = create_triple(built_tree)
    print(test_triples)
    tests_tuples = create_tuple(built_tree)
    print(tests_tuples)

    # Second stage: Visualize bk-tree as graph
    graph = visualize_graph(tests_tuples, test_triples)

    # Third stage: interactive mode (word query)
    user_input = input('Please enter a word query and the desired edit distance\n')
    search_word = user_input.split()[0]
    d = user_input.split()[1]
