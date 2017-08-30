# -*- coding: utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import
"""

Contains main classes used in game.

"""

import logging

import game.default_settings as def_settings

__author__ = 'tom.gabriele'
logger = logging.getLogger(__name__)


# logging.basicConfig(level=logging.DEBUG)


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

    def __repr__(self):
        return "{} : {}".format(self.symbol, self.element_name)

    @classmethod
    def _get_default_settings_elements_types(cls):
        """
        protected classmethod that allow getting default elements types from settings.
        :return: dict of elements types
        """
        return def_settings.ELEMENTS_TYPE

    @classmethod
    def get_elements_types_list(cls):
        """
        Parse the dict of elements type to return only the keys. This method is a helper for
        contributors who want to use create_from_default_settings method.
        :return: a list of elements type
        """
        return [key for key in cls._get_default_settings_elements_types().keys()]

    @classmethod
    def create_from_default_settings(cls, element_type: str):
        """
        this method is only used in unittests
        :return:
        """
        if element_type in cls.get_elements_types_list():
            element_dict = cls._get_default_settings_elements_types()[element_type]
            return cls.__init__(**element_dict)


class Conditions:
    """
    define conditions to say if player win or loose the game.
    """

    valid_conditions = ['to_pick_up_objects', ]

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if key in self.valid_conditions:
                setattr(self, key, value)
            else:
                logger.warning(
                    "'%s' is not a valid condition. It means this condition will "
                    "not be added to %s instance and not checked "
                    "because related functionality is not yet implemented." % (key, self.__class__))

    def __repr__(self):
        conditions_repr = ""
        for condition in self.valid_conditions:
            if condition in self.__dict__.keys():
                conditions_repr += "{} : {}".format(condition, getattr(self, condition))
        return conditions_repr


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

    def __repr__(self):
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
