# -*- coding: utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import
"""

Contains main classes used in game

"""

import logging

__author__ = '$USER'
logger = logging.getLogger(__name__)

# ELEMENTS_TYPE must contains the name of the element as key and a dict of element 's
# specifications according to Element class attributes


ELEMENTS_TYPE = {
    'ground': {},
    'wall': {},
    'inventory': {},
    'guard': {}
}

DEFAULT_ELEMENT_TYPE = ELEMENTS_TYPE['ground']
MAP_FILE_PATH_LIST = []  # a list of all path containing maps (makes game possibilities scalable


# and makes unit tests easier)


class Element:
    """
    Generic class which define either element of the map
    """
    ELEMENTS_OF_MAP = {
        """
        How to use this dict:
        'map_name':[list_of_the_map_elements]
        """
    }

    def __init__(self, symbol=" ", element_name="default", walkable=True, can_be_picked_up=False,
                 randomly_placed=False, is_exit=False):
        self.symbol = symbol
        self.element_name = element_name
        self.walkable = walkable
        self.can_be_picked_up = can_be_picked_up
        self.randomly_placed = randomly_placed
        self.is_exit = is_exit

    @classmethod
    def create_elements_from_map_files(cls, map_name):
        """
        allow to create all Element instances according to map file and map dict.
        if not dict is provided with map DEFAULT_MAP_DICT is used. If no correspondences exists
        between characters in map dict and ELEMENTS_TYPE default behavior is applied:
        unknow character get a DEFAULT_ELEMENT_TYPE. Each instance created is registered
        ELEMENTS_OF_MAP
        get
        :param map_name:name of the map used to get the relative map files
        :return:
        """
        pass


class Player:
    """
    define the player name and it's abilities: move, pick_up, dying, attack
    """
    pass


class Conditions:
    """
    define conditions to say if player win or loose the game.
    """
    pass


class Labyrinth:
    """

    """
    pass
