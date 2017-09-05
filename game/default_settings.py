# -*- coding: utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import
"""

contains default settings used when labyrinth map files do not provide specifics ones

"""

import logging
import os
import string

__author__ = 'tom.gabriele'
logger = logging.getLogger(__name__)

# ELEMENTS_TYPE must contains the name of the element as key and a dict of element 's
# specifications according to Element class attributes
ELEMENTS_TYPE = {
    'player': {
        "symbol": "X",
        "element_name": "player",
        'walkable': False,
        'can_be_picked_up': False,
        'randomly_placed': False,
        'is_start': False,
        'is_exit': False,
        'is_player': True
    },

    'start': {
        "symbol": "s",
        "element_name": "start",
        'walkable': True,
        'can_be_picked_up': False,
        'randomly_placed': False,
        'is_start': True,
        'is_exit': False,
        'is_player': False
    },

    'ground': {
        "symbol": ".",
        "element_name": "ground",
        'walkable': True,
        'can_be_picked_up': False,
        'randomly_placed': False,
        'is_start': False,
        'is_exit': False,
        'is_player': False
    },
    'wall': {
        "symbol": "#",
        "element_name": "wall",
        'walkable': False,
        'can_be_picked_up': False,
        'randomly_placed': False,
        'is_start': False,
        'is_exit': False,
        'is_player': False
    },
    'inventory': {
        "symbol": "i",
        "element_name": "inventory_object",
        'walkable': True,
        'can_be_picked_up': True,
        'randomly_placed': True,
        'is_start': False,
        'is_exit': False,
        'is_player': False
    },
    'exit': {
        "symbol": "g",
        "element_name": "guard",
        'walkable': True,
        'can_be_picked_up': False,
        'randomly_placed': False,
        'is_start': False,
        'is_exit': True,
        'is_player': False
    }
}
DEFAULT_ELEMENT_TYPE = 'ground'
PLAYER_TYPE = 'player'
PLAYER_SYMBOLS = list(set(['X', '@', '0', '&'] + list(string.punctuation)))

# a list of all path containing maps (makes game possibilities scalable and makes unit tests easier)
MAP_FOLDER_PATH_LIST = [
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'maps'),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'game', 'maps'),
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'game', 'maps', 'example'),
]
