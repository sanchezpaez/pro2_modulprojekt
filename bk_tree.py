# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 19.08.2022

import pickle
import sys

import numpy as np
from tqdm import tqdm

from graph import Graph


class BKTree:
    """
    Class that instantiates a BKTree from a list of words, which can
    also be visualised when transformed into an instance of Graph.
    The static methods calculate the relevant string metrics.
    Other main methods are build_tree(), search_word and make_graph_from_tree.
    """
    def __init__(self, wordlist, name):
        self.wordlist = wordlist
        self.name = name  # It is needed to generate posterior files
        self.ld = self.calculate_levenshtein_distance
        self.root = wordlist[0]
        self.tree = (self.root, {})

    @staticmethod
    def calculate_levenshtein_distance(string_1, string_2) -> int:
        """
        The Levenshtein distance is a string metric that measures the difference
        between two sequences. If two strings are similar, the distance should
        be small. If they are very different, the distance should be large.
        :rtype: int representing the minimum number of single-character edits
        (insert, delete or replace) necessary to transform one word (string)
        into another.
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
                    # If the characters are the same, we don't increase the edits
                    distance_matrix[r][c] = distance_matrix[r - 1][c - 1]
                else:
                    # Else we do by 1
                    # Compute the minimal number of edits (insert, delete, or replace)
                    distance_matrix[r][c] = 1 + min(distance_matrix[r][c - 1],  # Insertion
                                                    distance_matrix[r - 1][c],  # Deletion
                                                    distance_matrix[r - 1][c - 1])  # Substitution
        return int(distance_matrix[l1][l2])

    def print_levenshtein_distance(self, string_1, string_2):
        lev_dist = self.calculate_levenshtein_distance(string_1, string_2)
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
                        distance_matrix[r - 1][c - 1],  # Substitution
                        distance_matrix[r - 2, c - 2])  # Transposition
        return int(distance_matrix[l1][l2])

    def print_damerau_levenshtein(self, string_1, string_2):
        dam_lev_dist = self.calculate_damerau_levenshtein(string_1, string_2)
        print(f"The Damerau Levenshtein distance between '{string_1}' and '{string_2}' is {dam_lev_dist}.")

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

    @staticmethod
    def print_hamming_distance(string_1, string_2):
        hamming_d = BKTree.calculate_hamming_distance(string_1, string_2)
        print(f"The Hamming distance between '{string_1}' and '{string_2}' is {hamming_d}.")

    def build_tree(self, is_loaded=False) -> tuple:
        """
        Build BK Tree from list of strings.
        :param is_loaded: if True, a pre-saved self.tree is loaded, else
        a new self.tree structure is built
        :rtype tuple
        """
        if is_loaded:
            self.tree = self.load_tree(str(self.name) + '.pkl')
        else:
            for word in tqdm(self.wordlist[1:]):
                self.tree = self.insert_word(self.tree, word)
                # Use self.name to generate .pkl file name
                self.save_tree(str(self.name) + '.pkl')
        return self.tree

    def insert_word(self, node, word) -> tuple:
        """
        Insert a new word in the tree by using levenshtein distance.
        :param node: tuple, the tree to which the leaf will be added.
        :parameter word: str, the leaf which will be added to the tree.
        :rtype tuple, the new node resulting of adding one word.
        """
        d = self.ld(word, node[0])
        distances = node[1]
        if d in distances:
            self.insert_word(distances[d], word)
        else:
            distances[d] = (word, {})
        return node

    def search_word(self, word, d) -> list:
        """
        Return all words within the specified edit distance (d)
        from the search word.
        :param word: str
        :param d: int with the desired threshold
        :rtype list with all the matching words (strings)
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
        height = self.calculate_height(self.tree)
        print(f"The height of the tree is {height}.")

    def save_tree(self, filename):
        """
        Save tree structure into file_name (.pkl file), so it does not
        need to be calculated every time and can be loaded."""
        with open(filename, "wb") as file:
            pickle.dump(self.tree, file)

    def load_tree(self, filename) -> tuple:
        """Load pre-saved tree structure as self.tree."""
        with open(filename, "rb") as file:
            output = pickle.load(file)
            self.tree = output
            return self.tree

    def make_graph_from_tree(self):
        """Instantiate Graph from BKTree and plot graphic."""
        # Build graph from tree
        tree_graph = Graph(self.tree)
        # Plot graph
        tree_graph.visualize_graph()

    def interactive_mode_search_word(self):
        """
        use self.search_word() in interactive mode by
        asking for a user's input. The user will see the matching
        words on the screen.
        Handle typing errors and exit program if user does not type
        anything.
        """
        user_input = input('Please enter a word query and the'
                           ' desired edit distance threshold separated by a space .\n')
        if user_input:
            try:
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
            except IndexError:
                print('You need to type a word followed by an integer number.')
        else:
            # todo: raise Exception
            sys.exit()
