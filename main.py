# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import sys

from bk_tree import BKTree
from file import File


def main(file, dam_lev=False, hamming=False, visualise_tree=False):
    """
    Shows the tree visualization and all relevant metric distances.
    :param file:
    :param dam_lev:
    :param hamming:
    :return:
    """
    # First stage: read data from file and build bk tree
    dataset = File(file)
    demo_tree = dataset.make_bktree_from_file()
    demo_tree.print_levenshtein_distance('help', 'loop')
    if dam_lev:
        demo_tree.print_damerau_levenshtein('cab', 'abc')
    if hamming:
        demo_tree.print_hamming_distance('can', 'man')

    if visualise_tree:
    # Second stage: Visualize bk-tree as graph
        demo_tree.make_graph_from_tree()

    # Third stage: interactive mode (word query)
    demo_tree.interactive_mode_search_word()

def demo_with_loaded_tree(file):
    """
    Loads built tree to speed up process and is more effective to find similar words.
    Skip visualization for it is too large to display.
    :param file:
    :param dam_lev:
    :param hamming:
    :return:
    """
    # First stage: read data from file and build bk tree
    dataset = File(file)
    wordlist = dataset.load_vocab()
    bk_tree = BKTree(wordlist)
    bk_tree.ld = bk_tree.calculate_levenshtein_dynamic
    bk_tree.root = wordlist[0]
    bk_tree.tree = bk_tree.load_tree('demo_tree.pkl')
    print(bk_tree.tree)
    print(type(bk_tree.tree))
    bk_tree.calculate_height(bk_tree.tree)

    # Third stage: interactive mode (word query)
    bk_tree.interactive_mode_search_word()


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print('You need a minimum of two arguments (name of .py file and name of .txt file) and a maximum of 4 (flags '
              'to calculate Damerau-Levenshtein and Hamming distance).')
        # todo: raise Exception
    else:
        filename = sys.argv[1]
        visualise = True
        if filename == 'words_nltk.txt':
            visualise = False
        try:
            damerau_levenshtein_flag = sys.argv[2]
            compute_dam_lev = damerau_levenshtein_flag == '-dl'
        except IndexError:
            compute_dam_lev = False
        try:
            hamming_flag = sys.argv[3]
            compute_hamming = hamming_flag == '-h'
        except IndexError:
            compute_hamming = False
        main(filename, compute_dam_lev, compute_hamming, visualise)
        #demo_with_loaded_tree()

