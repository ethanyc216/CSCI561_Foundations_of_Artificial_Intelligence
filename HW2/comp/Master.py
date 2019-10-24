#!/usr/bin/env python 

#import tkinter as tk
import argparse
#from HalmaGUI import HalmaGUI
from HalmaBoard import HalmaBoard
from subprocess import call
from timeit import timeit

import time
import homework


# def read_input(fn):
#     with open(fn) as f:
#         mode = None
#         player = None
#         board = []
#         for line_count, line in enumerate(f):
#             if line_count == 0:
#                 mode = line.strip()
#             elif line_count == 1:
#                 player = line.strip()
#             elif line_count == 2:
#                 time = float(line.strip())
#             else:
#                 board.append(line.strip().split())
record = []

def initialize_board(board):
    board.black_pieces = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),           # black chess pieces
                         (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                         (2, 0), (2, 1), (2, 2), (2, 3),
                         (3, 0), (3, 1), (3, 2),
                         (4, 0), (4, 1)}
    board.white_pieces = {(15, 15), (15, 14), (15, 13), (15, 12), (15, 11), # white chess pieces
                          (14, 15), (14, 14), (14, 13), (14, 12), (14, 11),
                          (13, 15), (13, 14), (13, 13), (13, 12),
                          (12, 15), (12, 14), (12, 13),
                          (11, 15), (11, 14)}
    board.update_layout()                                                   # board layout

def read_output(output_file):
    type = None
    moves = []
    with open(output_file) as f:

        # first line of output
        for line_count, line in enumerate(f):
            if line_count == 0:
                if len(line) == 0:
                    print('Master: ERROR: Invalid output:{}.'.format(line))
                    return None
                info = line.strip().split(' ')
                if len(info) != 3:
                    print('Master: ERROR: Invalid output:{}.'.format(line))
                    return None
                type = info[0]
                move = [(int(info[1].split(',')[1]), int(info[1].split(',')[0])), (int(info[2].split(',')[1]), int(info[2].split(',')[0]))]
                moves.append(move)

            # if output more than one line, must be jump
            else:
                if type == 'E':
                    print('Master: ERROR: Invalid output: cannot move twice!')
                    return
                elif type == 'J':
                    info = line.strip().split(' ')
                    if (int(info[1].split(',')[1]), int(info[1].split(',')[0])) != moves[line_count - 1][1]:
                        print('Master: ERROR: Invalid output: false jump output!')
                        return
                    move = [(int(info[1].split(',')[1]), int(info[1].split(',')[0])), (int(info[2].split(',')[1]), int(info[2].split(',')[0]))]
                    moves.append(move)
                else:
                    print('Master: ERROR: Invalid output: invalid move type:{}'.format(info[0]))
                    return
    return type, moves

def run_single_move(input_file, output_file, total_time, agent):
    print('Master: Running a single step!')
    halma_board = HalmaBoard()
    halma_board.read_input(input_file)
    halma_board.mode = 'SINGLE'  # a whole game
    halma_board.time = total_time  # 5 mins given

    print('Agent homework3 is playing a {} mode on {} side, with {} seconds left.'.format(halma_board.mode, halma_board.player, halma_board.time))
    elapsed = timeit(stmt="subprocess.call(" + str(agent1) + ")", setup="import subprocess", number=1)
    print('Master: Agent ran {}s'.format(elapsed))

    # check if move is valid
    type, moves = read_output(output_file)
    valid_move = False
    if type == 'E':
        valid_move = halma_board.is_valid_move(moves[0])
    elif type == 'J':
        valid_move = halma_board.is_valid_jump(moves)
    else:
        print('Master: FAILED: Invalid output: invalid move type:{}'.format(type))
    if not valid_move:
        print('Master: FAILED: Invalid output: invalid output movement {} {}'.format(type, moves))
        return
    # update the board
    # input('Master: Press any key to update the board')
    if halma_board.player == 'BLACK':
        halma_board.move_piece(moves[0][0], moves[len(moves) - 1][1])
        halma_board.player = 'WHITE'
        halma_board.time -= elapsed
    else:
        halma_board.move_piece(moves[0][0], moves[len(moves) - 1][1])
        halma_board.player = 'BLACK'
        halma_board.time -= elapsed

    # write output
    halma_board.write_input(input_file)

    # check whether time used up
    if halma_board.time < 0:
        print('Master: FAILED: time usage more than allowed!!!')
        return

    # check whether one side has won
    win_condition = halma_board.has_won()
    if win_condition == 'WHITE':
        print('Master: White won!!!')
        return
    if win_condition == 'BLACK':
        print('Master: Black won!!!')
        return



def run_full_game(input_file, output_file, total_time, agent1, agent2, manual = False):
    print('Master: Running a full Halma game!')
    halma_board = HalmaBoard()
    initialize_board(halma_board)           # initialize board

    halma_board.player = 'BLACK'
    halma_board.mode = 'GAME'               # a whole game
    halma_board.time = total_time           # 5 mins given
    halma_board.write_input(input_file)     # ready the file for the agent

    black_time = total_time
    white_time = total_time
    if manual:
        input('Master: Board initialized, press any key to continue.')

    count = 0
    while(True):
        print('-' * 60)
        count += 1
        print('Master: Move {}'.format(count))
        if count == 44:
            print(record)
            # return


        if halma_board.player == 'BLACK':
            print('Agent {} is playing a {} mode on {} side, with {} seconds left.'.format(agent1[1], halma_board.mode, halma_board.player, halma_board.time))
            elapsed = timeit(stmt="subprocess.call(" + str(agent1) + ")", setup="import subprocess", number=1)
        else:
            print('Agent {} is playing a {} mode on {} side, with {} seconds left.'.format(agent2[1], halma_board.mode, halma_board.player, halma_board.time))
            elapsed = timeit(stmt="subprocess.call(" + str(agent2) + ")", setup="import subprocess", number=1)

        print('Master: Agent ran {}s'.format(elapsed))

        type, moves = read_output(output_file)
        valid_move = False
        if type == 'E':
            valid_move = halma_board.is_valid_move(moves[0])
        elif type == 'J':
            valid_move = halma_board.is_valid_jump(moves)
        else:
            print('Master: ERROR: Invalid output: invalid move type:{}'.format(type))
        if not valid_move:
            print('Master: ERROR: Invalid output: invalid output movement {} {}'.format(type, moves))
            return

        if halma_board.player == 'BLACK':
            record.append((type, moves))

        # update halma_board
        if manual:
            input('Master: Press any key to update the board')
        if halma_board.player == 'BLACK':
            # halma_board.player = 'WHITE'
            halma_board.time -= elapsed
            black_time = halma_board.time
            halma_board.time = white_time
            halma_board.move_piece(moves[0][0], moves[len(moves) - 1][1])
            halma_board.player = 'WHITE'
            # halma_board.black_pieces.remove(moves[0][0])
            # halma_board.black_pieces.add(moves[len(moves) - 1][1])
            # halma_board.update_layout()
        else:
            halma_board.time -= elapsed
            white_time = halma_board.time
            halma_board.time = black_time
            halma_board.move_piece(moves[0][0], moves[len(moves) - 1][1])
            halma_board.player = 'BLACK'
            # halma_board.white_pieces.remove(moves[0][0])
            # halma_board.white_pieces.add(moves[len(moves) - 1][1])
            # halma_board.update_layout()

        # write output
        halma_board.write_input(input_file)

        # check whether time used up
        if black_time < 0:
            print('Master: time used up for Black, White won!!!')
            print(record)
            return
        if white_time < 0:
            print('Master: time used up for White, Black won!!!')
            return

        # check whether one side has won
        win_condition = halma_board.has_won()
        if win_condition == 'WHITE':
            print('Master: White won!!!')
            return
        if win_condition == 'BLACK':
            print('Master: Black won!!!')
            return

        if manual:
            input('Master: Agent finished, press any key to continue.')





if __name__ == "__main__":
    input_file = 'input.txt'  # to be given to the agents
    output_file = 'output.txt'  # output from the agents
    agent1 = ['python','homework.py']
    agent1 = ['python','homework.py']

    run_full_game(input_file, output_file, 300, agent1, agent1, manual=False)
    # run_single_move(input_file, output_file, 5, agent1)

    # board = HalmaBoard()
    # initialize_board(board)
    # board.player = 'BLACK'
    # board.mode = 'GAME'  # a whole game
    # board.time = 300  # 5 mins given
    # type, moves = read_output(output_file)
    # print(board.is_valid_jump(moves))


    # parser = argparse.ArgumentParser()
    # parser.add_argument('-visual', action='store_true')
    # args = parser.parse_args()
    # visual = args.visual



