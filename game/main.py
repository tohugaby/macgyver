# -*- coding: utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import

import game.core as gc


def main():
    conditions = gc.Conditions()
    labyrinth = gc.Labyrinth(map_name='example_map', success_conditions=conditions, player_name='tom')
    labyrinth.print_map()
    labyrinth.start_game()


if __name__ == '__main__':
    main()
