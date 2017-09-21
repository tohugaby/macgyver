# -*- coding:utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import

"""
Module to make basic unit tests
"""
import os
import sys
import unittest

import game.core as gc
import game.default_settings as ds

# add this file root path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestConditions(unittest.TestCase):
    """
    tests for game.core module Condition class.
    """

    def setUp(self):
        """
        define all test's data.
        :return:
        """
        self.condition_dict = {
            "to_pick_up_objects": {
                "needle": 1,
                "small_tube": 1,
                "ether": 1
            }
        }

        self.condition_dict2 = {
            "to_pick_up_objects": {
                "needle": 1,
                "small_tube": 1,
                "ether": 1
            },
            "to_walk_on_zone": {
                "ground_button": 1
            }
        }

        self.condition_dict3 = {}

    def test_create_condition(self):
        """
        test with recognized conditions in dict passed to __init__ method.
        :return:
        """
        condition = gc.Conditions(**self.condition_dict)
        assert hasattr(condition, "to_pick_up_objects")
        self.assertEqual(condition.__repr__(),
                         "to_pick_up_objects : {'needle': 1, 'small_tube': 1, 'ether': 1}")

    def test_create_condition_with_unrecognized_conditions(self):
        """
        test with recognized and unrecognized conditions in dict passed to __init__ method.
        :return:
        """
        condition = gc.Conditions(**self.condition_dict2)
        assert hasattr(condition, "to_pick_up_objects")
        assert not hasattr(condition, "to_walk_on_zone")
        self.assertEqual(condition.__repr__(),
                         "to_pick_up_objects : {'needle': 1, 'small_tube': 1, 'ether': 1}")

    def test_create_empty_condition(self):
        """
        test with unrecognized condition in dict passed to __init__ method.
        :return:
        """
        condition = gc.Conditions(**self.condition_dict3)
        assert not hasattr(condition, "to_pick_up_objects")
        self.assertEqual(condition.__dict__, {})
        self.assertEqual(condition.__repr__(), "")


class TestElement(unittest.TestCase):
    """
    tests for game.core module Element class.
    """

    def setUp(self):
        """
        define all test's data.
        :return:
        """
        self.element_dict = {
            "symbol": "i",
            "element_name": "inventory_object",
            'walkable': True,
            'can_be_picked_up': True,
            'randomly_placed': True,
            'is_start': False,
            'is_exit': False
        }

    def test_create_element(self):
        """
        simple test of Element's class constructor
        :return:
        """
        new_element = gc.Element(**self.element_dict)
        self.assertIsInstance(new_element, gc.Element)
        self.assertFalse(new_element.is_start)
        self.assertTrue(new_element.walkable)
        self.assertTrue(new_element.can_be_picked_up)
        self.assertTrue(new_element.randomly_placed)
        self.assertFalse(new_element.is_exit)
        self.assertEqual(new_element.__repr__(), "'i' inventory_object")

    def test_create_element_from_settings(self):
        """
        Tests element creation of Element's instances from settings.
        :return:
        """
        for element_type in gc.Element.get_elements_types_list():
            element = gc.Element.create_from_default_settings(element_type)
            for attr in element.__dict__.keys():
                self.assertEqual(getattr(element, attr), ds.ELEMENTS_TYPE[element_type][attr])


class TestLabyrinth(unittest.TestCase):
    """
    Test class for CommandLineLabyrinth.
    """
    def setUp(self):
        """
        Define all test's data.
        :return:
        """
        self.labyrinth = {
            'map': 'example_map',
            'conditions': gc.Conditions(),
            'player_name': 'tom'
        }

        self.labyrinth_unavailable_map = {
            'map': 'doesnotexist_map',
            'conditions': gc.Conditions(),
            'player_name': 'tom'
        }

        self.map_str = "#s#############\n" \
                       "#..############\n" \
                       "#..........####\n" \
                       "##########....#\n" \
                       "##########.##.#\n" \
                       "####.......##.#\n" \
                       "#....######.#t#\n" \
                       "####.........##\n" \
                       "#e.#......###n#\n" \
                       "##.##......#..#\n" \
                       "#..##.#######.#\n" \
                       "#.#.#.........#\n" \
                       "#.#.#####..####\n" \
                       "#.............#\n" \
                       "##g############"

        self.used_char = set([char for char in self.map_str if char != '\n'])

        self.map_str_with_player = "#X#############\n" \
                                   "#..############\n" \
                                   "#..........####\n" \
                                   "##########....#\n" \
                                   "##########.##.#\n" \
                                   "####.......##.#\n" \
                                   "#....######.#t#\n" \
                                   "####.........##\n" \
                                   "#e.#......###n#\n" \
                                   "##.##......#..#\n" \
                                   "#..##.#######.#\n" \
                                   "#.#.#.........#\n" \
                                   "#.#.#####..####\n" \
                                   "#.............#\n" \
                                   "##g############"

    def test_create_labyrinth(self):
        """
        test
        CommandLineLabyrinth
        instance
        creation
        :return:
        """
        lab = gc.CommandLineLabyrinth(self.labyrinth['map'], self.labyrinth['conditions'],
                                    self.labyrinth['player_name'])
        self.assertEqual(lab.map, self.labyrinth['map'])
        self.assertEqual(lab.__repr__(), self.labyrinth['map'])
        self.assertEqual(lab.player['element'].element_name, self.labyrinth['player_name'])
        self.assertEqual(lab.max_row_index, 14)
        self.assertEqual(lab.max_column_index, 15)

        # test one of positions
        start = lab.positions[0, 1]
        self.assertIsInstance(start, gc.Element)
        self.assertTrue(start.is_start)
        self.assertTrue(start.walkable)
        self.assertFalse(start.can_be_picked_up)
        self.assertFalse(start.randomly_placed)
        self.assertFalse(start.is_exit)

        # Test print map metho
        self.assertEqual(lab.print_map(), self.map_str)

        # test used_char
        self.assertEqual(lab.used_char, self.used_char)

    def test_print_map_when_player_is_in(self):
        """

        :return:
        """
        lab = gc.CommandLineLabyrinth(self.labyrinth['map'], self.labyrinth['conditions'],
                                    self.labyrinth['player_name'])
        lab.player['position'] = (0, 1)
        # Test print map metho
        self.assertEqual(lab.print_map(), self.map_str_with_player)

    def test_create_labyrinth_with_bad_map_name(self):
        """
        test
        CommandLineLabyrinth
        instance
        creation
        with an unavailable map file
        :return:
        """
        with self.assertRaises(FileNotFoundError):
            gc.CommandLineLabyrinth(self.labyrinth_unavailable_map['map'],
                                  self.labyrinth_unavailable_map['conditions'],
                                  self.labyrinth_unavailable_map['player_name'])
