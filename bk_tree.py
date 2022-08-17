# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022
import sys

import numpy as np
from tqdm import tqdm
from graph import Graph


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

    @staticmethod
    def calculate_levenshtein_dynamic(string_1, string_2) -> int:
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

    def print_levenshtein_distance(self, string_1, string_2):
        lev_dist = self.calculate_levenshtein_dynamic(string_1, string_2)
        print(f"The Levenshtein distance between '{string_1}' and '{string_2}' is {lev_dist}.")

    @staticmethod
    def calculate_damerau_levenshtein(string_1, string_2) -> int:
        """
        Like the Levenstein Distance, computing transpositions
        (swapping of adjacent symbols) as well.
        """
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
                    # If the characters are identical, no edit needs to be made
                    distance_matrix[r][c] = distance_matrix[r - 1][c - 1]
                else:
                    # In all other cases the cost is 1, added to the calculation
                    distance_matrix[r][c] = 1 + min(
                                            distance_matrix[r][c - 1],  # Insertion
                                            distance_matrix[r - 1][c],  # Deletion
                                            distance_matrix[r - 1][c - 1],
                                            distance_matrix[r - 2, c - 2])  # Substitution
        return int(distance_matrix[l1][l2])

    @staticmethod
    def calculate_hamming_distance(string_1, string_2):
        """
        If two strings are of the same length, calculate the
        number of substitutions to turn one string into the
        other.
        :return: int representing number of substitutions.
        """
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

    @staticmethod  # classmethod??
    def print_hamming_distance(string_1, string_2):
        hamming_d = BKTree.calculate_hamming_distance(string_1, string_2)
        print(f"The Hamming distance between '{string_1}' and '{string_2}' is {hamming_d}.")

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

        if search(self.tree):
            print(f"The most similar words to {word} are: {search(self.tree)}")
        else:
            print(f"No words in the list match your query.")
            # todo: raise Exception
        return search(self.tree)  # get rid of empty list

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

    @staticmethod
    def max(number_1, number_2):
        """Return greater value."""
        if number_1 > number_2:
            return number_1
        else:
            return number_2

    def calculate_height(self, node):
        """Calculate the longest path from root to leaf."""
        if self.tree:
            children = node[1]
            height = 0
            for i in children:
                # Search children nodes recursively
                height = self.max(self.calculate_height(children[i]), height)
            return height + 1
        else:
            print('The height is 0.')
            # todo: write Exception

    def get_status(self):
        """
        Return size and height of tree, being size the number
        of leaves, and height the number of nodes on the
        longest path from root to leaf.
        """
        number_of_words = len(self.wordlist)
        print(f"The tree has {number_of_words} leaves (words).")
        # height = self.calculate_height(self.root)
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

    def load_tree(self, filename):
        """Load pre-saved tree structure as self.tree."""
        with open(filename, encoding='utf-8') as file:
            self.tree = file.read()
        return self.tree

    def make_graph_from_tree(self):
        # Build graph from tree
        tree_graph = Graph(self.tree)
        # Plot graph
        tree_graph.visualize_graph()

    def interactive_mode_search_word(self):
        user_input = input('Please enter a word query and the desired edit distance threshold separated by a space .\n')
        if user_input:
            if len(user_input) == 1:
                print('You need to type a word followed by an integer number.')
                # todo: raise Exc
            else:
                search_word = user_input.split()[0]
                number = user_input.split()[1]
                if not search_word.isalpha():
                    print('That is not an actual word.')
                    # todo: exception, isinstance
                if isinstance(int(number), int):
                    d = int(number)
                else:
                    print('That is not a number.')
                self.search_word(search_word, d)
        else:
            # todo: raise Exception
            sys.exit()
