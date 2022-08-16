# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022
from bk_tree import BKTree


class File:
    def __init__(self, filename):
        self.filename = filename

    def load_vocab(self):
        with open(self.filename, encoding='utf-8') as file:
            text = file.read()  # Text as string
            words = text.split(',')
        return words

    def make_bktree_from_file(self):
        wordlist = self.load_vocab()
        bk_tree = BKTree(wordlist)
        bk_tree.tree = bk_tree.build_tree()
        bk_tree.save_tree('bktree.txt')
        bk_tree.get_status()
        return bk_tree