# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import sys

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from networkx.drawing.nx_pydot import graphviz_layout
from nltk.corpus import words
from tqdm import tqdm


# nltk.download('reuters')

# big_vocab = set(words.words())  # 235892
# print(len(big_vocab))
# vocab = brown.words()
# print(len(vocab)) # 56057
# vocab_reuters = reuters.words()
# print(len(vocab_reuters)) # 41600
# all_words = set(vocab + vocab_reuters)
# print(len(all_words))  # 82092


# class StringMetric:
#
#     def __init__(self, string_1, string_2):
#         self.string_1 = string_1
#         self.string_2 = string_2


class Graph:

    def __init__(self, tree):
        self.tree = tree
        self.tuples = None
        self.triples = None
        self.labels = None

    # def __getitem__(self, index: int):
    #     return self[index]

    def create_triples(self):
        """
        Take in a nested tuple with a bk-tree structure and adapt it to
        a tuple of 3 format, where node_1, node_2 and their edit distance is
        represented. The resulting list of tuples will be then used by networkx
        to draw a graph visualization of the bk-tree structure.
        :return: list of labels
        """
        self.triples = []
        node_1 = self.tree[0]
        nested_element = self.tree[1]
        for distance in nested_element:
            node_2 = nested_element[distance][0]
            triple = node_1, node_2, distance
            self.triples.append(triple)
            new_tuple = nested_element[distance]
            if new_tuple[1]:
                graph_tuple = Graph(new_tuple)
                self.triples = self.triples + graph_tuple.create_triples()

        return self.triples

    def create_tuples(self):
        self.tuples = []
        node_1 = self.tree[0]
        nested_element = self.tree[1]
        for distance in nested_element:
            node_2 = nested_element[distance][0]
            _tuple = node_1, node_2
            self.tuples.append(_tuple)
            new_tuple = nested_element[distance]
            if new_tuple[1]:
                graph_tuple = Graph(new_tuple)
                self.tuples = self.tuples + graph_tuple.create_tuples()

        return self.tuples

    def get_edge_labels(self):
        self.labels = {}
        for triple in self.triples:
            node_1 = triple[0]
            node_2 = triple[1]
            label = triple[2]
            if (node_1, node_2) not in self.labels:
                self.labels[node_1, node_2] = label

        return self.labels

    def visualize_graph(self):
        tree_graph = nx.DiGraph()
        tree_graph.add_edges_from(self.tuples)
        positions = graphviz_layout(tree_graph, prog='dot')
        nx.draw_networkx(tree_graph, pos=positions, node_size=1500, arrows=True)
        edge_labels = self.get_edge_labels()
        nx.draw_networkx_edge_labels(tree_graph, pos=positions, edge_labels=edge_labels)
        plt.savefig("bktree.png")
        plt.show()


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

    def calculate_levenshtein_dynamic(self, string_1, string_2) -> int:
        l1 = len(string_1)
        l2 = len(string_2)
        # Generate a matrix to store results
        distance_matrix = np.zeros((l1 + 1, l2 + 1))
        for i in range(l1 + 1):
            for j in range(l2 + 1):
                if i == 0:
                    distance_matrix[i][j] = j
                elif j == 0:
                    distance_matrix[i][j] = i
                elif string_1[i - 1] == string_2[j - 1]:
                    distance_matrix[i][j] = distance_matrix[i - 1][j - 1]
                else:
                    distance_matrix[i][j] = 1 + min(distance_matrix[i][j - 1], distance_matrix[i - 1][j], distance_matrix[i - 1][j - 1])
        return distance_matrix[l1][l2]

    @staticmethod
    def calculate_hamming_distance(string_1, string_2):
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
        for word in tqdm(self.wordlist[1:]):
            self.tree = self.insert_word(self.tree, word)
        # print(self.tree)
        return self.tree

    def insert_word(self, node, word):
        """Insert a new word in the tree."""
        d = self.ld(word, node[0])
        distances = node[1]
        if d in distances:
            self.insert_word(distances[d], word)
        else:
            distances[d] = (word, {})
        return node

    def search_word(self, word, d):
        """
        Return all words within the specified edit distance (d)
        from the search word.
        """

        def search(node):
            distance = self.ld(word, node[0])
            matching_words = []
            if distance <= d:
                matching_words.append(node[0])
            # Recursively query every child node numbered between d-n and d+n (inclusive)
            for i in range(distance - d, distance + d + 1):
                children = node[1]
                if i in children:
                    matching_words.extend(search(node[1][i]))
            return matching_words

        return search(self.tree)

        # Version 2
        # matching_words = []
        # distance = self.ld(self.tree[0], word)
        # if distance <= d:
        #     matching_words.append(self.tree[0])
        # for i in range(distance - d, distance + d + 1):
        #     children = self.tree[1]
        #     if str(i) in children:
        #         matching_words.extend(self.search_word(str(i), d))
        # return matching_words

    def status(self):
        number_of_words = len(self.wordlist)
        print(f"The tree has {number_of_words} leaves (words).")
        # height = length to the farthest leaf
        # return number_of_words + height
        # todo: calculate height and finish method

    def save_tree(self, filename):
        """
        Save tree structure into file, so it does not
        need to be calculated every time and can be loaded."""
        with open(filename, "w") as file:
            words_string = str(self.tree)
            file.write(words_string)
        return file

def load_vocab(filename):
    with open(filename, encoding='utf-8') as file:
        text = file.read()  # Text as string
        words = text.split(',')
    return words

def load_tree(filename):
    with open(filename, encoding='utf-8') as file:
        tree = file.read()  # Text as string
    return tree


def save_vocab(wordset, filename):
    """Save tokens into file, separated by comma."""
    with open(filename, "w") as file:
        words_string = ",".join(wordset)
        file.write(words_string)
    return file


if __name__ == '__main__':
    # First stage: read data from file and build bk tree
    # Download and save wordlist
    wordlist = list(set(words.words()))
    save_vocab(wordlist, 'words_nltk.txt')
    filename = sys.argv[1]
    words = load_vocab(filename)
    bk_tree = BKTree(words)
    print(len(bk_tree.wordlist))
    print(bk_tree.calculate_levenshtein_distance('help', 'loop'))
    print(bk_tree.calculate_hamming_distance('can', 'man'))
    # built_bk_tree = bk_tree.build_tree()
    # print(bk_tree.search_word('help', 1))
    # print(bk_tree.status())

    test_words = ["help", "hell", "hello", "loop", "helps", "troop", "shell", "helper"]
    test_tree = BKTree(test_words)
    print(test_tree.calculate_levenshtein_distance('help', 'loop'))
    print(test_tree.calculate_levenshtein_dynamic('help', 'loop'))
    print(test_tree.calculate_hamming_distance('can', 'man'))
    built_tree = test_tree.build_tree()
    print(built_tree)
    test_tree.save_tree('tree.txt')
    # test_tree.tree = None
    # new_tree = load_tree('tree.txt')
    # print(new_tree)
    # test_tree.tree = new_tree
    # print(test_tree.tree)
    print(test_tree.search_word('help', 1))
    print(test_tree.status())

    # Second stage: Visualize bk-tree as graph
    tree_graph = Graph(built_tree)
    # Reformat data
    test_triples = tree_graph.create_triples()
    print(test_triples)
    tests_tuples = tree_graph.create_tuples()
    print(tests_tuples)
    graph = tree_graph.visualize_graph()

    # Third stage: interactive mode (word query)
    user_input = input('Please enter a word query and the desired edit distance threshold.\n')
    search_word = user_input.split()[0]
    d = int(user_input.split()[1])
    print(test_tree.search_word(search_word, d))
    # import nltk
    # nltk.download('brown')
