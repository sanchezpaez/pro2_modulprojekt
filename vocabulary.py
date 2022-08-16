# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022

from nltk.corpus import words


def save_vocab(word_set, filename):
    """Save tokens into file, separated by comma."""
    with open(filename, "w") as file:
        words_string = ",".join(word_set)
        file.write(words_string)
    return file


# Download and save wordlist
wordlist = sorted(list(set(words.words())))
save_vocab(wordlist, 'words_nltk.txt')
