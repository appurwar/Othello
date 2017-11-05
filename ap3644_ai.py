#!/usr/bin/env python3
# -*- coding: utf-8 -*

"""
COMS W4701 Artificial Intelligence - Programming Homework 2

An AI player for Othello. This is the template file that you need to
complete and submit.

@author: Apoorv Purwar (ap3644)
"""

import random
import sys
import time

# You can use the functions in othello_shared to write your AI
from othello_shared import find_lines, get_possible_moves, get_score, play_move

move_dictionary = dict()

# Method to compute utility value of board
def compute_utility(board, color):
     disk_count = get_score(board)
     dark_disk = disk_count[0]
     light_disk = disk_count[1]
     if color == 1:
         return dark_disk - light_disk
     elif color == 2:
         return  light_disk - dark_disk



############ MINIMAX ###############################

def minimax_min_node(board, color):
    if board in move_dictionary:
        return move_dictionary[board]
    else:
        min_next_nodes = get_possible_moves(board, 3-color)
        utility_list = []
        if(len(min_next_nodes) == 0):
            return compute_utility(board, color)

        for items in min_next_nodes:
            successor_board = play_move(board, 3-color, items[0], items[1])
            curr_utility = minimax_max_node(successor_board, color)
            utility_list.append(curr_utility)

        move_dictionary.update({board : min(utility_list)})
        return  min(utility_list)


def minimax_max_node(board, color):
    if board in move_dictionary:
        return move_dictionary[board]
    else:
        max_next_nodes = get_possible_moves(board, color)
        utility_list = []
        if(len(max_next_nodes) == 0):
            return compute_utility(board, color)

        for items in max_next_nodes:
            successor_board = play_move(board, color, items[0], items[1])
            curr_utility = minimax_min_node(successor_board, color)
            utility_list.append(curr_utility)

        move_dictionary.update({board : min(utility_list)})
        return max(utility_list)


def select_move_minimax(board, color):
    """
    Given a board and a player color, decide on a move.
    The return value is a tuple of integers (i,j), where
    i is the column and j is the row on the board.
    """
    possible_moves = get_possible_moves(board, color)
    utility_list = []
    for items in possible_moves:
        successor_board = play_move(board, color, items[0], items[1])
        utility =  minimax_min_node(successor_board, color)
        utility_list.append(utility)

    max_index = utility_list.index(max(utility_list))
    return possible_moves[max_index][0], possible_moves[max_index][1]

############ ALPHA-BETA PRUNING #####################

#alphabeta_min_node(board, color, alpha, beta, level, limit)
def alphabeta_min_node(board, color, alpha, beta, level, limit):
    if board in move_dictionary:
        return move_dictionary[board]       # Retrieval from cached board states
    else:
        min_next_nodes = get_possible_moves(board, 3-color)
        utility_list = []
        if(len(min_next_nodes) == 0 or limit <= level):
            return compute_utility(board, color)            # Leaf node reached

        v = float("inf")
        successor_dict = dict()
        for items in min_next_nodes:
            successor_board = play_move(board, 3-color, items[0], items[1])
            successor_dict.update({successor_board: compute_utility(successor_board,color)})

        #alpha-beta pruning logic - with node ordering heuristic
        for key in sorted(successor_dict, key=successor_dict.get):
            v = min(v, alphabeta_max_node(successor_board, color, alpha, beta, level+1, limit))
            if v <= alpha:
                return v;
            beta = min(beta,v)

        move_dictionary.update({board : v})    #Caching of the board states
        return v


#alphabeta_max_node(board, color, alpha, beta, level, limit)
def alphabeta_max_node(board, color, alpha, beta, level, limit):
    if board in move_dictionary:
        return move_dictionary[board]       # Retrieval from cached board states
    else:
        max_next_nodes = get_possible_moves(board, color)

        utility_list = []
        if(len(max_next_nodes) == 0 or limit <= level):
            return compute_utility(board, color)            # Leaf node reached

        v = float("-inf")
        successor_dict = dict()
        for items in max_next_nodes:
            successor_board = play_move(board, color, items[0], items[1])
            successor_dict.update({successor_board:compute_utility(successor_board,color)})

        #alpha-beta pruning logic - with node ordering heuristic
        for key in sorted(successor_dict, key=successor_dict.get):
            v = max(v, alphabeta_min_node(key, color, alpha, beta, level+1, limit))
            if v >= beta:
                return v;
            alpha = max(alpha,v)

        move_dictionary.update({board : v})     #Caching of the board states
        return v


def select_move_alphabeta(board, color):
    possible_moves = get_possible_moves(board, color)
    utility_list = []
    for items in possible_moves:
        successor_board = play_move(board, color, items[0], items[1])
        # The max depth limit reached within 10 seconds - 7
        utility =  alphabeta_min_node(successor_board, color, float("-inf"), float("inf"), 0, 7)
        utility_list.append(utility)

    max_index = utility_list.index(max(utility_list))
    return possible_moves[max_index][0], possible_moves[max_index][1]


####################################################
def run_ai():
    """
    This function establishes communication with the game manager.
    It first introduces itself and receives its color.
    Then it repeatedly receives the current score and current board state
    until the game is over.
    """
    print("Suthello AI") # First line is the name of this AI
    color = int(input()) # Then we read the color: 1 for dark (goes first),
                         # 2 for light.

    while True: # This is the main loop
        # Read in the current game status, for example:
        # "SCORE 2 2" or "FINAL 33 31" if the game is over.
        # The first number is the score for player 1 (dark), the second for player 2 (light)
        next_input = input()
        status, dark_score_s, light_score_s = next_input.strip().split()
        dark_score = int(dark_score_s)
        light_score = int(light_score_s)

        if status == "FINAL": # Game is over.
            print
        else:
            board = eval(input()) # Read in the input and turn it into a Python
                                  # object. The format is a list of rows. The
                                  # squares in each row are represented by
                                  # 0 : empty square
                                  # 1 : dark disk (player 1)
                                  # 2 : light disk (player 2)

            # Select the move and send it to the manager
            #movei, movej = select_move_minimax(board, color)
            movei, movej = select_move_alphabeta(board, color)
            print("{} {}".format(movei, movej))


if __name__ == "__main__":
    run_ai()
