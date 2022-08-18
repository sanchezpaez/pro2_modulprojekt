# -*- coding: utf-8 -*-
# Authorin: Sandra Sánchez
# Project: Modulprojekt PRO II
# Datum: 31.07.2022

import logging

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class NotATextFileError(Exception):
    pass
    #logger.warning('This is not a .txt file!')



