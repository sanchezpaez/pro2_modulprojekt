# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


import sys

from file import File


def main():
    filename = sys.argv[1]
    # First stage: read data from file and build bk tree
    dataset = File(filename)
    demo_tree = dataset.make_bktree_from_file()
    demo_tree.print_levenshtein_distance('help', 'loop')
    demo_tree.print_hamming_distance('can', 'man')

    # Second stage: Visualize bk-tree as graph
    demo_tree.make_graph_from_tree()

    # Third stage: interactive mode (word query)
    demo_tree.interactive_mode_search_word()


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Two arguments are needed: name of .py file and name of .txt file.')
        # todo: raise Exception
    else:
        main()

        # test_tree.tree = None
        # new_tree = load_tree('tree.txt')
        # print(new_tree)
        # test_tree.tree = new_tree
        # print(test_tree.tree)
        # print(test_tree.search_word('help', 1))
        # print(test_tree.calculate_height(built_tree))
