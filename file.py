# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 22.08.2022

from bk_tree import BKTree
from exception import NotATextFileError


class File:
    """This class reads a .txt file and makes an instance of BKTree."""

    def __init__(self, filename: str):
        self.filename = filename

    def load_vocab(self) -> list:
        """Read .txt file and return list of words."""
        if str(self.filename).endswith('.txt'):
            with open(self.filename, encoding='utf-8') as file:
                text = file.read()
                words = text.split(',')
            return words
        else:
            raise NotATextFileError()

    def make_bktree_from_file(self, is_loaded=False, dam_lev=False):
        """
        Use wordlist to instantiate and build BKTree.
        :param is_loaded: if True, skip the build_tree step
        and load pre-saved BKTree.tree.
        :return: BKTree
        """
        try:
            wordlist = self.load_vocab()
            name = self.filename
            bk_tree = BKTree(wordlist, name)
            if is_loaded:
                bk_tree.build_tree(is_loaded=True)
            else:
                if dam_lev:
                    bk_tree.build_tree(dam_lev=True)
                else:
                    bk_tree.tree = bk_tree.build_tree()
            bk_tree.get_status()
            return bk_tree
        except NotATextFileError:
            pass
