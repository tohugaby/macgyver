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
        print(condition)

    def test_create_condition_with_unrecognized_conditions(self):
        """
        test with recognized and unrecognized conditions in dict passed to __init__ method.
        :return:
        """
        condition = gc.Conditions(**self.condition_dict2)
        assert hasattr(condition, "to_pick_up_objects")
        assert not hasattr(condition, "to_walk_on_zone")
        print(condition)

    def test_create_empty_condition(self):
        """
        test with unrecognized condition in dict passed to __init__ method.
        :return:
        """
        condition = gc.Conditions(**self.condition_dict3)
        assert not hasattr(condition, "to_pick_up_objects")
        self.assertEqual(condition.__dict__, {})
        print(condition)


class TestElement(unittest.TestCase):
    """
    tests for game.core module Element class.
    """

    def setUp(self):
        """
        define all test's data.
        :return:
        """
        pass

    def test_create_element(self):
        pass

    def test_create_element_from_settings(self):
        for element_type in gc.Element.get_elements_types_list():
            element = gc.Element.create_from_default_settings(element_type)
            for attr in element.__dict__.keys():
                self.assertEqual(getattr(element, attr), ds.ELEMENTS_TYPE[element_type][attr])


class TestLabyrinth(unittest.TestCase):
    def setUp(self):
        """
        define all test's data.
        :return:
        """
        pass

    def test_create_labyrinth(self):
        conditions = gc.Conditions()
        lab = gc.Labyrinth('example_map', conditions, 'tom')
        print(lab.positions)

    def test_create_labyrinth_with_bad_map_name(self):
        conditions = gc.Conditions()
        with self.assertRaises(FileNotFoundError):
            gc.Labyrinth('doesnotexist_map', conditions, 'tom')
