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



class Graph:

    def __init__(self, tree):
        self.tree = tree
        self.tuples = None
        self.triples = None
        self.labels = None



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
        self.ld = self.calculate_levenshtein_dynamic
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
        rows = l1 + 1
        cols = l2 + 1
        distance_matrix = np.zeros((rows, cols))
        for r in range(rows):
            for c in range(cols):
                if r == 0:
                    distance_matrix[r][c] = c
                elif c == 0:
                    distance_matrix[r][c] = r
                elif string_1[r - 1] == string_2[c - 1]:
                    distance_matrix[r][c] = distance_matrix[r - 1][c - 1]
                else:
                    distance_matrix[r][c] = 1 + min(distance_matrix[r][c - 1],  # Insertion
                                                    distance_matrix[r - 1][c],  # Deletion
                                                    distance_matrix[r - 1][c - 1])  # Substitution
        return int(distance_matrix[l1][l2])

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

    def max(self, number_1, number_2):
        """Return greater value."""
        if (number_1 > number_2):
            return number_1
        else:
            return number_2

    def calculate_height(self, node):
        """Calculate the longest path from root to leaf."""
        if self.tree:
            children = node[1]
            height = 0
            for i in children:
                # print(children[i])
                # print(i)
                # Search children nodes recursively
                height = self.max(self.calculate_height(children[i]), height)
            return height + 1
        else:
            print('The height is 0.')
            #todo: write Exception

    def get_status(self):
        """
        Return size and height of tree, being size the number
        of leaves, and height the number of nodes on the
        longest path from root to leaf.
        """
        number_of_words = len(self.wordlist)
        print(f"The tree has {number_of_words} leaves (words).")
        #height = self.calculate_height(self.root)
        height = self.calculate_height(self.tree)
        print(f"The height of the tree is {height}.")
        # tree.tree = ('book', {1: ('books', {2: ('boo', {1: ('boon', {}), 2: ('cook', {})})}),
        #                         4: ('cake', {0: ('cake', {}), 1: ('cape', {}), 2: ('cart', {})})})

    def save_tree(self, filename):
        """
        Save tree structure into file, so it does not
        need to be calculated every time and can be loaded."""
        with open(filename, "w") as file:
            words_string = str(self.tree)
            file.write(words_string)
        return file



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

class File:
    def __init__(self, filename):
        self.filename = filename

    def load_vocab(self):
        with open(self.filename, encoding='utf-8') as file:
            text = file.read()  # Text as string
            words = text.split(',')
        return words

def make_bktree_from_file(filename):
    dataset = File(filename)
    wordlist = dataset.load_vocab()
    bk_tree = BKTree(wordlist)
    bk_tree.tree = bk_tree.build_tree()
    bk_tree.save_tree('bktree.txt')
    bk_tree.get_status()
    return bk_tree


if __name__ == '__main__':
    if len(sys.argv) == 2:
        filename = sys.argv[1]
        demo_tree = make_bktree_from_file(filename)
        print(demo_tree.calculate_levenshtein_distance('help', 'loop'))
        print(demo_tree.calculate_levenshtein_dynamic('help', 'loop'))
        print(demo_tree.calculate_hamming_distance('can', 'man'))
        print(demo_tree.tree)
        demo_tree.save_tree('demo_tree.txt')
        # test_tree.tree = None
        # new_tree = load_tree('tree.txt')
        # print(new_tree)
        # test_tree.tree = new_tree
        # print(test_tree.tree)
        # print(test_tree.search_word('help', 1))
        # print(test_tree.calculate_height(built_tree))

        # Second stage: Visualize bk-tree as graph
        tree_graph = Graph(demo_tree.tree)
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
    else:
        print('Not possible')
        #todo: raise Exception

    # Download and save wordlist
    # wordlist = sorted(list(set(words.words())))
    # save_vocab(wordlist, 'words_nltk.txt')
    # filename = sys.argv[1]

    # words = load_vocab(filename)
    # bk_tree = BKTree(words)
    # print(len(bk_tree.wordlist))
    # print(bk_tree.calculate_levenshtein_distance('help', 'loop'))
    # print(bk_tree.calculate_hamming_distance('can', 'man'))
    # built_bk_tree = bk_tree.build_tree()
    # bk_tree.save_tree('bktree_nltk.txt')
    # print(bk_tree.search_word('help', 1))
    # print(bk_tree.status())

    # First stage: read data from file and build bk tree

