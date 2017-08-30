# -*- coding: utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import
"""

Contains main classes used in game

"""

import logging

import game.default_settings

__author__ = 'tom.gabriele'
logger = logging.getLogger(__name__)


class Element:
    """
    Generic class which define either element of the map
    """

    def __init__(self, symbol=" ", element_name="default", walkable=True, can_be_picked_up=False,
                 randomly_placed=False, is_start=False, is_exit=False):
        self.symbol = symbol
        self.element_name = element_name
        self.walkable = walkable
        self.can_be_picked_up = can_be_picked_up
        self.randomly_placed = randomly_placed
        self.is_start = is_start
        self.is_exit = is_exit


class Conditions:
    """
    define conditions to say if player win or loose the game.
    """
    pass


class Labyrinth:
    """
    Represent a Labyrinth as an entity composed of:
    - A map : map name, path of map files, elements composing the map.
    - A set of success conditions,
    - A player : player name and it's abilities: move, pick_up objects , dying, attack the guard...
    """
    ELEMENTS_OF_MAPS = {
        """
        How to use this dict:
        'map_name':[list_of_the_map_elements]
        """
    }

    def __init__(self, ):
        pass

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
