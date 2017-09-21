# -*- coding: utf-8 -*-
# for python 2.7 only
# from __future__ import print_function, unicode_literals, absolute_import
"""
Module that execute the program
"""
import game.core as gc


def main():
    """
    Function that execute the program
    :return:
    """

    CHOICES = [
        ('Mode Graphique', gc.GraphicalLabyrinth),
        ('Mode Console', gc.CommandLineLabyrinth),
    ]

    conditions = gc.Conditions(**{
        "to_pick_up_objects": {
            "needle": 1,
            "tube": 1,
            "ether": 1
        }
    })

    mod_question = "Salut fan de MacGyver! \nChoisis un mode de jeux: \n{}:{}\n" \
                   "{}:{}\n".format(0, CHOICES[0][0], 1, CHOICES[1][0])
    choice = str()
    while choice not in [str(i) for i in range(len(CHOICES))]:
        choice = input(mod_question)

    game_mod = CHOICES[int(choice)][1]
    labyrinth = game_mod(map_name='example_map', success_conditions=conditions, player_name='tom')
    labyrinth.play_game()


if __name__ == '__main__':
    main()
