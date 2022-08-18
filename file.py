# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


from bk_tree import BKTree
from exception import NotATextFileError


class File:
    def __init__(self, filename):
        self.filename = filename

    def load_vocab(self):
        if str(self.filename).endswith('.txt'):
            with open(self.filename, encoding='utf-8') as file:
                text = file.read()
                words = text.split(',')
            return words
        else:
            raise NotATextFileError()

    def make_bktree_from_file(self, is_loaded=False):
        try:
            wordlist = self.load_vocab()
            bk_tree = BKTree(wordlist)
            if is_loaded:
                bk_tree.build_tree(is_loaded=True)
            else:
                bk_tree.tree = bk_tree.build_tree()
            bk_tree.get_status()
            return bk_tree
        except NotATextFileError:
            pass

