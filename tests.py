# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022


from bktree import calculate_levenshtein_distance


class TestLevenshtein:

    def test_distance_0(self):
        assert calculate_levenshtein_distance('man', 'man') == 0

    def test_distance_empty_string(self):
        assert calculate_levenshtein_distance('', 'man') == 3

    def test_different_length_words(self):
        assert calculate_levenshtein_distance('cream', 'corn') == 4
