# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import sys
import networkx as nx
import matplotlib.pyplot as plt


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
    :return: list of triples
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
    filename = sys.argv[1]
    words = read_data_from_filename(filename)
    terminal_tree = BKTree(words)
    test_words = ["book", "books", "cake", "boo", "boon", "cook", "cake", "cape", "cart"]
    test_tree = BKTree(test_words)
    print(calculate_levenshtein_distance('book', 'cake'))
    test_tree.build_tree()
    print(test_tree.search_word('book', 1))


    connections = ('book', {1: ('books', {2: ('boo', {1: ('boon', {}), 2: ('cook', {})})}),
                            4: ('cake', {0: ('cake', {}), 1: ('cape', {}), 2: ('cart', {})})}
                   )
    test_triples = create_triple(connections)
    print(test_triples)

    G = nx.Graph()
    G.add_weighted_edges_from(test_triples)
    pos = {'book': (20, 30), 'books': (40, 30), 'boo': (30, 10), 'boon': (0, 40), 'cook': (10, 30),
           'cake': (40, 10), 'cape': (10, 20), 'cart': (0, 20)}
    nx.draw_networkx(G, pos=pos, node_size=1500)
    nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=G.edges)
    plt.show()

    # G.add_edges_from([('book', 'boo'), ('boo', 'boom'), ('book', 'boom'), ('book', 'boop')])
    # pos = {'book': (20, 30), 'boo': (40, 30), 'boom': (30, 10), 'boop': (0, 40)}
    # labels = {('book', 'boo'): 1, ('boo', 'boom'): 1, ('book', 'boom'): 1, ('book', 'boop'): 1}
    # nx.draw_networkx(G, pos=pos, node_size=1500)
    # nx.draw_networkx_edge_labels(G, pos=pos, edge_labels=labels)
    plt.savefig("bktree.png")
    plt.show()

    # dod = {0: {1: {"weight": 1}}}  # single edge (0,1)
    # G = nx.from_dict_of_dicts(dod)
    # G = nx.from_nested_tuple(test_tree.tree)
    # pos = {0: (20, 30), 1: (40, 30)}
    # nx.draw_networkx(G, node_size=1500)
    # plt.show()


    user_input = input('Please enter a word query and the desired edit distance\n')
    search_word = user_input.split()[0]
    d = user_input.split()[1]
