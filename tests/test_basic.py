import os
import sys
# print(sys.path)
# print(__file__)
# print(os.path.dirname(__file__))
# print(os.path.join(os.path.dirname(__file__), '..'))
# print(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest

import game.core as gc

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


# print(sys.path)


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

    def create_element(self):
        pass

