#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

############################
##   CSCI 561 Fall 2019   ##
##       Homework 2       ##
##       Yifan Chen       ##
##  ethanyc216@gmail.com  ##
##     Oct. 11th 2019     ##
############################

# input: input.txt
# output: output.txt

import argparse 
import copy
import halma
import player
#import time

colors = {'WHITE': 'W', 'BLACK': 'B'}
#depths = [0, 1, 2, 3]

def processInput(fileName): 
    # play mode 
    # team
    # remainingTime
    # the board 16 * 16
    with open(fileName) as f: 
        lines = f.read().splitlines() 
    inputInfo = {} 

    inputInfo['mode'] = lines[0] 
    inputInfo['color'] = colors[lines[1]]
    inputInfo['remainingTime'] = float(lines[2])

    whiteSet = set()
    blackSet = set()
    for y, line in enumerate(lines[3:19]):
        for x, state in enumerate(line):
            if state == '.':
                continue
            elif state == 'W':
                whiteSet.add((x, y))
            else:
                blackSet.add((x, y))

    inputInfo['whiteSet'] = whiteSet
    inputInfo['blackSet'] = blackSet

    return inputInfo


def getoutput(moves):
    if moves[0] == 'E':
        return 'E {},{} {},{}'.format(moves[1][0], moves[1][1], moves[2][0], moves[2][1])
    elif moves[0] == 'J':
        outputString = ''
        total = len(moves) - 1
        pre = moves[1]
        for i in range(2, total):
            cur = moves[i]
            outputString = '{}J {},{} {},{}\n'.format(outputString, pre[0], pre[1], cur[0], cur[1])
            pre = cur
        cur = moves[-1]
        outputString = '{}J {},{} {},{}'.format(outputString, pre[0], pre[1], cur[0], cur[1])
        return outputString


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='input.txt',
                        help='input file name')

    parser.add_argument('--output', type=str, default='output.txt',
                        help='output file name')

    parser.add_argument('--answers', type=str, default='output.txt',
                        help='answers file name')
    args = parser.parse_args()

    inputInfo = processInput(args.input)
    remainingTime = inputInfo['remainingTime']
    color = inputInfo['color']

    halmaGame = halma.HalmaGame(inputInfo['whiteSet'], inputInfo['blackSet'])
    halmaGame.updateCamp()
    
    '''
    if inputInfo['mode'] == 'SINGLE':
        for depth in depths:
            myAgent = player.AlphaBetaAgent(color, depth)
            moves = myAgent.getAction(halmaGame)
            outputString = getoutput(moves)
            with open(args.output, 'w') as f:
                f.write(outputString)
                f.close()
    
    else:
    '''
    if len(halmaGame.camp[color]) > 1:
        depths = [1]
    else:
        depths = [1]

    if remainingTime < 3:
        depths = [0, 1]
        
    for depth in depths:
        #startTime = time.time()
        myAgent = player.AlphaBetaAgent(color, depth)
        moves = myAgent.getAction(halmaGame)
        #print depth, time.time() - startTime

        outputString = getoutput(moves)
        #print outputString
        with open(args.output, 'w') as f:
            f.write(outputString)
            f.close()
