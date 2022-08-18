# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import sys

from file import File


def main(file, dam_lev=False, hamming=False, visualise_tree=False, loaded_tree=False):
    """
    Shows the tree visualization and all relevant metric distances.
    :param loaded_tree:
    :param visualise_tree:
    :param file:
    :param dam_lev:
    :param hamming:
    :return:
    """
    # First stage: read data from file and build bk tree
    dataset = File(file)
    if loaded_tree:
        demo_tree = dataset.make_bktree_from_file(is_loaded=True)
    else:
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


if __name__ == '__main__':
    if len(sys.argv) < 2 or len(sys.argv) > 4:
        print('You need a minimum of two arguments (name of .py file'
              ' and name of .txt file) and a maximum of 4 (flags '
              'to calculate Damerau-Levenshtein and Hamming distance).')
        # todo: raise Exception
    else:
        filename = sys.argv[1]
        visualise = True
        with open (filename, encoding='utf-8') as file:
            text = file.read()
            words = text.split(',')
        # If the list contains too many words (>25) the tree will be too big for visualisation)
        if len(words) > 25:
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
        main(filename, compute_dam_lev, compute_hamming, visualise, loaded_tree=True)
