# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 19.08.2022


class NotATextFileError(Exception):
    pass
    # print('This is not a .txt file_name!')


class NoWordsMatchedError(Exception):
    pass
    # print(f"No words in the list match your query.")

class EmptyTreeError(Exception):
    pass
    # print('The height is 0.')

class EmptyListError(Exception):
    pass

class NotAWordError(Exception):
    pass
    # print('That is not an actual word.')