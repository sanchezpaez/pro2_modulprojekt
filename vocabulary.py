# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 22.08.2022

from nltk.corpus import words


def save_vocab(word_set=None, filename='words_nltk.txt'):
    """Save wordlist into file_name, separated by comma."""
    if not word_set:
        # Download and save list of unique 235892 words from nltk.words()
        word_set = sorted(list(set(words.words())))
    with open(filename, "w") as file:
        words_string = ",".join(word_set)
        file.write(words_string)
    return file
