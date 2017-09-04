# -*- coding: utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import
"""

Contains main classes used in game.

"""
import json
import os
import logging

import game.default_settings as def_settings
from game.default_settings import PLAYER_TYPE

__author__ = 'tom.gabriele'
logger = logging.getLogger(__name__)


# logging.basicConfig(level=logging.DEBUG)


class MissingElementException(Exception):
    """Exception to raise when an mandatory element miss on a map"""

    def __init__(self, labyrinth, key, message="A mandatory element is missing"):
        """

        :param error_arguments:
        """
        super(MissingElementException, self).__init__(labyrinth, key, message)
        self.labyrinth = labyrinth
        self.key = key


class Element:
    """
    Generic class which define either element of the map
    """

    def __init__(self, symbol=" ", element_name="default", walkable=True, can_be_picked_up=False,
                 randomly_placed=False, is_start=False, is_exit=False, is_player=False):
        self.symbol = symbol
        self.element_name = element_name
        self.walkable = walkable
        self.can_be_picked_up = can_be_picked_up
        self.randomly_placed = randomly_placed
        self.is_start = is_start
        self.is_exit = is_exit
        self.is_player = is_player

    def __repr__(self):
        return "'{}' {}".format(self.symbol, self.element_name)

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
            return cls(**element_dict)


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
    used_char = set()

    def __init__(self, map_name: str, success_conditions: Conditions, player_name: str):

        self.map = map_name
        self.success_conditions = success_conditions
        self.row_max_index = 0
        self.column_max_index = 0
        self.positions = self.__get_elements_positions()
        # self player is a dict containing
        # 'element' containing Element instance, 'is_alive' status , 'position' and 'inventory' dict
        self.player = self.__create_player_element(player_name)

    def __repr__(self):
        return self.map

    def print_map(self):
        """
        print a CLI representation of the map acccording to self.positions and player_position attribute
        :return:
        """
        map_str = ''

        for r in range(self.row_max_index + 1):
            for c in range(self.column_max_index + 1):
                try:
                    if isinstance(self.positions[r, c], Element):
                        if (r, c) == self.player['position']:
                            map_str += self.player['element'].symbol
                        else:
                            map_str += self.positions[r, c].symbol
                    else:
                        map_str += str(self.positions[r, c])
                except KeyError as e:
                    if r == self.row_max_index and c == self.column_max_index:
                        return map_str
                    else:
                        raise e
        return map_str

    def __get_elements_positions(self):
        """
        return a dictionary containing coordinates (tuple) of as keys and elements instances as values.
        :return:
        """
        return self.__get_map_file_structure()

    def start_game(self):
        """

        :return:
        """
        for key, element in self.positions.items():
            if not isinstance(element, str):
                if element.is_start:
                    return key
        raise MissingElementException(self,
                                      'is_start',
                                      "There is no start point in this map. Please modify txt and json map file")

    def __ask_direction(self):
        """
        :return:
        """

        return input("Choisir une direction : ")

    def move_player(self):
        """
        change player position on map according to button pressed
        and attributes of targetted position (Element) on the map
        :param keyboard_button: pressed button on keyboard
        :return:
        """
        next_direction = self.__ask_direction()

    def __is_next_position_walkable(self, next_position: tuple):
        """
        return True if next position is walkable.
        :param next_position:
        :return:
        """
        return self.positions[next_position].walkable

    def __is_next_position_pickable(self, next_position: tuple):
        """
        return True if position is pickable.
        :param next_position:
        :return:
        """
        return self.positions[next_position].can_be_picked_up

    def __is_next_position_exit(self, next_position: tuple):
        """
        return True if position is the exit
        :param next_position:
        :return:
        """
        return self.positions[next_position].is_exit

    def __create_player_element(self, player_name: str):
        """
        create player attribute values: element instance and initial position, and state
        :return:
        """
        # TODO: Write unit test
        authorized_symbol = list(set(def_settings.PLAYER_SYMBOLS).difference(self.used_char))
        element = Element.create_from_default_settings(element_type=PLAYER_TYPE)
        element.element_name = player_name

        if element.symbol in self.used_char:
            element.symbol = authorized_symbol[0]

        return dict(element=element, is_alive=True, position=tuple(), inventory=dict())

    def __create_element_from_map_files(self, char, dict_path):
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
        if char == '\n':
            return char

        with open(dict_path) as file:
            json_dict = json.load(file)
        # TODO: Write unit test :with the case their is nothing provided in json file or their is a missing type
        try:
            element = Element.create_from_default_settings(json_dict[char]['type'])
            element.element_name = json_dict[char]['name']
            element.symbol = char
        except KeyError as e:
            logger.warning("Element type of char %s not defined in %s. Default type %s will be applied" % (
                char, json_dict, def_settings.DEFAULT_ELEMENT_TYPE))
            element = Element.create_from_default_settings(def_settings.DEFAULT_ELEMENT_TYPE)
            element.symbol = char
        except Exception:
            raise
            # we add the symbol to used symbol
        self.used_char = set(list(self.used_char) + [char])

        return element

    def __get_map_file_structure(self):
        """

        :return:
        """
        map_path, dict_path = self.__get_map_files_path()
        structure = {}
        with open(map_path, 'r') as file:
            lines = file.readlines()
            r = 0
            for line in lines:
                self.row_max_index = row = r
                c = 0
                for char in line:
                    column = c
                    if c > self.column_max_index:  # Last line has maybe no carriage return and could be shorter
                        #     # we don't want to take it into account.
                        self.column_max_index = c  # we take into account carriage return to print correctly map
                    structure[row, column] = self.__create_element_from_map_files(char, dict_path)
                    c += 1
                r += 1
        return structure

    def __get_map_files_path(self):
        """

        :return:
        """
        map_file_name = self.map + '.txt'
        map_dict_file_name = self.map + '.json'
        map_files_path = None

        def search_file_in_folder(folder):
            for root, dirs, files in os.walk(folder):
                logger.info("Searching map...")
                if map_file_name in files and map_dict_file_name in files:
                    logger.info("Map found !")
                    return os.path.join(root, map_file_name), os.path.join(root, map_dict_file_name)

        for maps_folder in def_settings.MAP_FOLDER_PATH_LIST:
            map_files_path = search_file_in_folder(maps_folder)
            if map_files_path:
                break

        if not map_files_path:
            raise FileNotFoundError(
                "Files %s or %s do not exist in maps folders : %s" % (map_file_name, map_dict_file_name,
                                                                      def_settings.MAP_FOLDER_PATH_LIST))
        return map_files_path
