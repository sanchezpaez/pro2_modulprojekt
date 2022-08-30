# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 22.08.2022


import sys

from classes.exception import NotATextFileError
from classes.file import File
from vocabulary import save_vocab


def main(file_name, dam_lev, presaved, visualise_tree):
    """
    Build tree from file based on a string metric,
    implement search_word()
    and give information about tree. If the wordlist upon
    which the tree is built is of manageable size,
    visualize tree too.
    :param file_name: str with name of file which contains vocabulary.
    :param dam_lev: bool. If True builds tree with
    calculate_levenshtein_distance().
    :param presaved: bool. If True loads a pre_saved tree instead of
    building it.
    :param visualise_tree: bool. If True draws graphic to represent tree.
    :return: make_bktree_from_file(), make_graph_from_tree()
    if visualise_tree=True
    and interactive_mode_search_word().
    """
    # First stage: read data from file_name and build bk tree
    try:
        dataset = File(file_name)
    except NotATextFileError():
        print('This is not a .txt file_name!')
        sys.exit()
    if file_name == 'words_nltk.txt':
        save_vocab()
    if presaved:
        demo_tree = dataset.make_bktree_from_file(is_loaded=True)
    else:
        if dam_lev:
            print('Building a BK Tree'
                  ' based on Damerau Levenshtein distance...')
            demo_tree = dataset.make_bktree_from_file(dam_lev=True)
            demo_tree.print_example_of_damerau_levenshtein('loop', 'pool')
        else:
            print('Building a BK Tree based on the'
                  ' default metric: Levenshtein distance...')
            demo_tree = dataset.make_bktree_from_file()
            demo_tree.print_example_of_levenshtein_distance('help', 'loop')
    if visualise_tree:
        # Second stage: Visualize bk-tree as graph
        tree_graph = demo_tree.make_graph_from_tree()
        print('Close the window with the tree graph in order to'
              ' continue with the program.')
        tree_graph.visualize_graph()

    # Third stage: interactive mode (word query)
    while True:
        demo_tree.interactive_mode_search_word()


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
    except IndexError:
        print('You need a minimum of two arguments (name of .py file_name'
              ' and name of .txt file_name) and a maximum of 4 (flags '
              'to calculate Damerau-Levenshtein and to load '
              'pre-saved tree).')
        sys.exit()
    visualise = '-v' in sys.argv
    load_tree = '-t' in sys.argv
    compute_dam_lev = '-dl' in sys.argv
    if load_tree and compute_dam_lev:
        raise RuntimeError("You must have run the program with '-dl'"
                           " before calling the '-t' option")
    main(filename, compute_dam_lev, load_tree, visualise)
