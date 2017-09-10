# -*- coding: utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import
"""

Contains main classes used in game.

"""
import json
import operator
import os
import logging
import random
import re
import pygame

from pygame.locals import *

import game.default_settings as def_settings

__author__ = 'tom.gabriele'
logger = logging.getLogger(__name__)


# logging.basicConfig(level=logging.DEBUG)


class MissingElementException(Exception):
    """Exception to raise when an mandatory element miss on a map"""

    def __init__(self, labyrinth, key, message="A mandatory element is missing"):
        """

        :param labyrinth:
        :param key:
        :param message:
        """
        super(MissingElementException, self).__init__(labyrinth, key, message)
        self.labyrinth = labyrinth
        self.key = key


class Element:
    """
    Generic class which define either element of the map
    """

    def __init__(self, symbol=" ", element_name="default", walkable=True, can_be_picked_up=False,
                 randomly_placed=False, is_start=False, is_exit=False, is_player=False,
                 picture=None):
        self.symbol = symbol
        self.element_name = element_name
        self.walkable = walkable
        self.can_be_picked_up = can_be_picked_up
        self.randomly_placed = randomly_placed
        self.is_start = is_start
        self.is_exit = is_exit
        self.is_player = is_player
        # if no image is provided we take default image
        # TODO: provide a default image for each type of element in default settings
        # if picture is None:
        #     self.picture = def_settings.ELEMENTS_TYPE[def_settings.DEFAULT_ELEMENT_TYPE]['picture']
        # else:
        self.picture = picture

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

    @staticmethod
    def __get_method_attached_to_attribute_name(attribute_name):
        """
        determine method attached to valid attribute
        :return:
        """
        return "check_" + attribute_name

    @staticmethod
    def __get_attribute_attached_to_method(method_name):
        """
        dertimine attribute attached to check method
        :return:
        """
        reg = r"^check_(.*)$"
        expression = re.search(reg, method_name)
        return expression.group(1)

    @staticmethod
    def check_conditions(labyrinth):
        """
        browse check conditions method
        :param labyrinth:
        :return:
        """

        for check_method in labyrinth.success_conditions.get_list_of_active_checks():
            if getattr(labyrinth.success_conditions, check_method)(labyrinth) is False:
                print("{}: constraint not satisfied".format(check_method))
                return False
        return True

    def get_list_of_active_checks(self):
        """
        determine the list of active method according to instance attributes
        :return: the list of check method needed relative to Condition instance attributes
        """

        return [self.__get_method_attached_to_attribute_name(key) for key in self.__dict__.keys()]

    def check_to_pick_up_objects(self, labyrinth):
        """
        compare inventory with instance attribute 'to_pick_up_objects'
        :return:
        """
        attribute_name = self.__get_attribute_attached_to_method(self.check_to_pick_up_objects.__name__)

        inventory = {}
        for key, value in labyrinth.player['inventory'].items():
            new_key = key
            inventory[new_key] = value['nb']
        logger.info("objects to pick up: {} ".format(getattr(self, attribute_name)))
        logger.info("inventory : {}".format(inventory))
        return getattr(self, attribute_name) == inventory


class Labyrinth:
    """
    Represent a Labyrinth as an entity composed of:
    - A map : map name, path of map files, elements composing the map.
    - A set of success conditions,
    - A player : player name and it's abilities: move, pick_up objects , dying, attack the guard...
    """

    used_char = set()

    def __init__(self, map_name: str, success_conditions: Conditions, player_name: str):

        self.map = map_name
        self.success_conditions = success_conditions
        self.positions = self.__get_elements_positions()
        # self player is a dict containing
        # 'element': Element instance, 'is_alive' status , 'position' and 'inventory' dict
        self.player = self.__create_player_element(player_name)
        self.quit = False

    def __repr__(self):
        return "{}".format(self.map, self.print_map())

    # GAME METHODS
    def print_map(self):
        """
        print a CLI representation of the map acccording to self.positions and player_position attribute
        :return:
        """
        map_str = ''

        for r in range(self.max_row_index + 1):
            for c in range(self.max_column_index + 1):
                try:
                    if isinstance(self.positions[r, c], Element):
                        if (r, c) == self.player['position']:
                            map_str += self.player['element'].symbol
                        else:
                            map_str += self.positions[r, c].symbol
                    else:
                        map_str += str(self.positions[r, c])
                except KeyError as e:
                    if r == self.max_row_index and c == self.max_column_index:
                        return map_str
                    else:
                        raise e
        return map_str

    def draw_background(self):
        """

        :return:
        """
        background_path = os.path.join(def_settings.ROOT_PATH, 'media', 'background.jpg')
        background = pygame.image.load(background_path).convert()
        return background

    def draw_element(self, element):
        """
        draw elements in graphical mod
        :param element:
        :return:
        """
        pict = element.picture
        picture_path = os.path.join(def_settings.ROOT_PATH, 'media', pict)
        sprite = pygame.image.load(picture_path).convert_alpha()
        return sprite

    def draw_player(self):
        """
        draw player in graphical mod
        :return:
        """
        player = self.player['element'].picture
        player_picture_path = os.path.join(def_settings.ROOT_PATH, 'media', player)
        player_sprite = pygame.image.load(player_picture_path).convert_alpha()
        return player_sprite

    def start_game(self):
        """
        execution of the game
        :return:
        """
        logger.info("\nGetting initial position of player %s\n" % self.player['element'].element_name)
        print("\nGetting initial position of player %s \n" % self.player['element'].element_name)
        continue_game = True
        self.__get_player_initial_position()
        pygame.init()

        window = pygame.display.set_mode((600, 720))
        player_sprite = self.draw_player()
        player_position = player_sprite.get_rect()
        player_position.top, player_position.left = tuple([40 * i for i in self.player['position']])
        player_position.top += 120
        while continue_game:
            for event in pygame.event.get():
                if event.type == QUIT:
                    continue_game = False
                if event.type == KEYDOWN:
                    line_move, column_move = self.move_player(event.key)
                    player_position = player_position.move(column_move * 40, line_move * 40)
                    continue_game = not self.game_finished()

            window.blit(self.draw_background(), (0, 120))
            for key, element in self.positions.items():
                if not isinstance(element, str):
                    row, col = key
                    if element.picture is not None:
                        window.blit(self.draw_element(element), (col * 40, row * 40 + 120))
            window.blit(player_sprite, player_position)

            myfont = pygame.font.SysFont("monospace", 15)

            row, column = 1, 1
            for key, obj in self.player['inventory'].items():
                r, c = row * 40, column * 40

                pict = obj['picture']
                picture_path = os.path.join(def_settings.ROOT_PATH, 'media', pict)
                inv = pygame.image.load(picture_path).convert_alpha()
                label = myfont.render(str(obj['nb']), 1, (255, 255, 0))
                window.blit(inv, (c, r))
                window.blit(label, (c + 40, r))
                column += 1
            # render text


            pygame.display.flip()

        # check if conditions are satisfied
        if self.checked_conditions():
            print("You win !")
        else:
            print("You loose...")

    def move_player(self, key):
        """
        change player position on map according to button pressed
        and attributes of targetted position (Element) on the map
        :return:
        """

        keyboard_commands = {
            K_UP: (-1, 0),
            K_RIGHT: (0, 1),
            K_DOWN: (1, 0),
            K_LEFT: (0, -1)
        }

        next_position = tuple(map(operator.add, self.player['position'], keyboard_commands[key]))

        # check if new coordonates exist
        if self.__is_position_on_map(next_position):
            # check if it's walkable
            if self.__is_position_walkable(next_position):
                # change player position
                self.player['position'] = next_position
                # check if it is pickable
                if self.__is_position_pickable(next_position):
                    # pick up object and add to inventory
                    gift = self.positions[next_position]
                    self.player['inventory'][gift.element_name]['nb'] += 1
                    print(self.player['inventory'])
                    self.positions[next_position] = Element.create_from_default_settings(
                        def_settings.DEFAULT_ELEMENT_TYPE)
                return keyboard_commands[key]
        return 0, 0

    # GAME AND CONDITIONS CHEKING METHODS
    def game_finished(self):
        """
        is player on exit
        :return:
        """
        if self.player['position'] in self.exit_positions:
            return True
        else:
            return self.quit

    def checked_conditions(self):
        """
        are success condition satisfied
        :return:
        """
        return Conditions.check_conditions(self)

    @staticmethod
    def __ask_direction():
        """
        wait for user input
        :return:
        """
        direction = ""
        while direction not in ('Z', 'S', 'W', 'Q'):
            direction = input("Choisir une direction Z,S,W,Q : ").upper()
        return direction

    # POSITIONS CHECKING METHODS
    def __is_position_on_map(self, position: tuple):
        """
        check if coordinates of position are on map
        :param position:
        :return: True if position is in map
        """
        row_is_ok = position[0] in range(0, self.max_row_index + 1)
        # player can not be placed on carriage return
        column_is_ok = position[1] in range(0, self.max_column_index)
        return row_is_ok and column_is_ok

    def __is_position_walkable(self, position: tuple):
        """

        :param position:
        :return: True if position is walkable.
        """
        return self.positions[position].walkable

    def __is_position_pickable(self, position: tuple):
        """
        return True if position is pickable.
        :param position:
        :return:
        """
        return self.positions[position].can_be_picked_up

    def __is_position_exit(self, position: tuple):
        """
        return True if position is the exit
        :param position:
        :return:
        """
        return self.positions[position].is_exit

    # CREATE LABYRINTH ELEMENTS AND STRUCTURE METHODS
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

    def __map_to_str(self):
        """
        translate txt map file to str
        :return:
        """
        pass

    def __map_json_to_dict(self):
        """
        translate json description file to dict.
        :return: name and type of element of the map
        :type:dict
        """
        dict_path = self.__get_map_files_path()[1]
        with open(dict_path) as file:
            json_dict = json.load(file)
        return json_dict

    def __create_element_from_map_files(self, char):
        """
        allow to create all Element instances according to map file and map dict.
        if not dict is provided with map DEFAULT_MAP_DICT is used. If no correspondences exists
        between characters in map dict and ELEMENTS_TYPE default behavior is applied:
        unknow character get a DEFAULT_ELEMENT_TYPE.
        :param char:
        :param dict_path:
        :return:
        """
        if char == '\n':
            return char

        json_dict = self.__map_json_to_dict()
        # TODO: Write unit test :with the case their is nothing provided in json file or their is a missing type
        try:
            element = Element.create_from_default_settings(json_dict[char]['type'])
            element.element_name = json_dict[char]['name']
            element.symbol = char
            if 'picture' in json_dict[char].keys():
                element.picture = json_dict[char]['picture']

        except KeyError as e:
            logger.warning("%s :\n Element type of char %s not defined in %s. "
                           "Default type %s will be applied" % (e,
                                                                char,
                                                                json_dict,
                                                                def_settings.DEFAULT_ELEMENT_TYPE))
            element = Element.create_from_default_settings(def_settings.DEFAULT_ELEMENT_TYPE)
            element.symbol = char
        except Exception:
            raise
            # we add the symbol to used symbol
        self.used_char = set(list(self.used_char) + [char])

        return element

    @staticmethod
    def __get_walkable_elements_coordonates(structure):
        """
        list coordonates of walkable element of the map
        :param structure:
        :return:
        """
        elements_coordinates = [key for key, value in structure.items() if isinstance(value, Element)]
        walkable_coordinates = [key for key in elements_coordinates if
                                structure[key].walkable and not (structure[key].is_start or structure[key].is_exit)]
        print(walkable_coordinates)
        return walkable_coordinates

    def __get_randomly_placed_elements(self):
        """
        extract randomly placed elements from description json file
        :return:
        """
        objects_to_place = {}
        json_dict = self.__map_json_to_dict()
        for key, value in json_dict.items():
            element_type = value['type']
            if def_settings.ELEMENTS_TYPE[element_type]['randomly_placed']:
                objects_to_place[key] = value
        return objects_to_place

    def __randomly_place_inventory_objects_on_map(self, structure: dict):
        """

        :param structure:
        :return:
        """
        available_coordonates = self.__get_walkable_elements_coordonates(structure)
        for key, element in self.__get_randomly_placed_elements().items():
            i = random.randrange(len(available_coordonates))
            structure[available_coordonates[i]] = self.__create_element_from_map_files(key)

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
                row = r
                c = 0
                for char in line:
                    column = c
                    structure[row, column] = self.__create_element_from_map_files(char)
                    c += 1
                r += 1

        self.__randomly_place_inventory_objects_on_map(structure)

        return structure

    def __get_elements_positions(self):
        """
        return a dictionary containing coordinates (tuple) of as keys and elements instances as values.
        :return:
        """
        return self.__get_map_file_structure()

    # CREATE AND PLACE PLAYER METHODS
    def __create_player_element(self, player_name: str):
        """
        create player attribute values: element instance and initial position, and state
        :return:
        """
        # TODO: Write unit test
        authorized_symbol = list(set(def_settings.PLAYER_SYMBOLS).difference(self.used_char))
        element = Element.create_from_default_settings(element_type=def_settings.PLAYER_TYPE)
        element.element_name = player_name

        if element.symbol in self.used_char:
            element.symbol = authorized_symbol[0]

        inventory = dict()
        for key, obj in self.pickable_elements_position.items():
            inventory[obj.element_name] = {'picture': obj.picture,
                                           'nb': 0}

        return dict(element=element, is_alive=True, position=tuple(), inventory=inventory)

    def __get_player_initial_position(self):
        """

        :return: initial player position
        """
        self.player['position'] = self.start_position

    @property
    def pickable_elements_position(self):
        """
        extract all objects that can be picked up
        :return:
        """

        pickable_objects = {}
        for key, element in self.positions.items():
            if not isinstance(element, str):
                if element.can_be_picked_up:
                    pickable_objects[key] = element
        return pickable_objects

    @property
    def max_row_index(self):
        """

        :return: max row index
        """
        if self.positions != {}:
            return sorted([key[0] for key in self.positions.keys()])[-1]
        return 0

    @property
    def max_column_index(self):
        """

        :return: max row index
        """
        if self.positions != {}:
            return sorted([key[1] for key in self.positions.keys()])[-1]
        return 0

    @property
    def start_position(self):
        """

        :return: start coordonates
        """
        for key, element in self.positions.items():
            if not isinstance(element, str):
                if element.is_start:
                    return key
        raise MissingElementException(self,
                                      'is_start',
                                      "There is no start point in this map. Please modify txt and json map file")

    @property
    def exit_positions(self):
        """

        :return: a list of exit coordonates
        """
        exit_list = []
        for key, element in self.positions.items():
            if not isinstance(element, str):
                if element.is_exit:
                    exit_list.append(key)
        if exit_list:
            return exit_list
        else:
            raise MissingElementException(self,
                                          'is_exit',
                                          "There is no exit point in this map. Please modify txt and json map file")
