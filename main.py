# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 22.08.2022


import sys

from file import File


def main(file_name, dam_lev=False, presaved=False, visualise_tree=False):
    """
    Build tree from file, compute relevant string metrics, implement search_word()
    and give information about tree. If the wordlist upon which the tree is
    built is of manageable size, visualize tree too.
    :param file_name: str with name of file which contains vocabulary.
    :param dam_lev: bool. If True prints an example of calculate_levenshtein_distance().
    :param presaved: bool. If True loads a pre_saved tree.
    :param visualise_tree: bool. If True draws graphic to represent tree.
    :param loaded_tree: bool. If True loads pre-saved tree instead of building it.
    :return: make_bktree_from_file(), make_graph_from_tree() if visualise_tree=True
    and interactive_mode_search_word().
    """
    # First stage: read data from file_name and build bk tree
    dataset = File(file_name)
    if presaved:
        demo_tree = dataset.make_bktree_from_file(is_loaded=True)
    else:
        if dam_lev:
            print('Building a BK Tree based on Damerau Levenshtein distance...')
            demo_tree = dataset.make_bktree_from_file(dam_lev=True)
        else:
            demo_tree = dataset.make_bktree_from_file()
    # The program always shows an example of Levenshtein distance.
    # The other metrics are optional
    demo_tree.print_levenshtein_distance('help', 'loop')
    if visualise_tree:
        # Second stage: Visualize bk-tree as graph
        demo_tree.make_graph_from_tree()
    # Third stage: interactive mode (word query)
    demo_tree.interactive_mode_search_word()


if __name__ == '__main__':
    try:
        filename = sys.argv[1]
        visualise = True
        try:
            with open(filename, encoding='utf-8') as file:
                text = file.read()
                words = text.split(',')
            # If the list is too long the tree will be too big for visualisation
            if len(words) > 25:
                visualise = False
            try:
                loaded_tree_flag = sys.argv[2]
                load_tree = loaded_tree_flag == '-t'
            except IndexError:
                load_tree = False
            try:
                damerau_levenshtein_flag = sys.argv[3]
                compute_dam_lev = damerau_levenshtein_flag == '-dl'
            except IndexError:
                compute_dam_lev = False
            main(filename, compute_dam_lev, load_tree, visualise)
        except FileNotFoundError:
            print(f"File '{filename}' does not exist.")
    except IndexError:
        print('You need a minimum of two arguments (name of .py file_name'
              ' and name of .txt file_name) and a maximum of 4 (flags '
              'to calculate Damerau-Levenshtein and to load '
              'pre-saved tree).')
