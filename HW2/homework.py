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
#import numpy as np 
import util
#import time

colors = {'WHITE': ('W', 'B'), 'BLACK': ('B', 'W')}

class Node(object):
    def __init__(self, coord, path, cost):
        self.coord = coord
        self.path = path 
        self.cost = cost


def processInput(fileName): 
    # play mode 
    # team
    # remainingTime
    # the board 16 * 16
    with open(fileName) as f: 
        lines = f.read().splitlines() 
    inputInfo = {} 

    inputInfo['mode'] = lines[0] 
    inputInfo['color'] = lines[1]
    inputInfo['remainingTime'] = float(lines[2])

    inputInfo['mine'] = set()
    inputInfo['theirs'] = set()
    for y, line in enumerate(lines[3:19]):
        for x, state in enumerate(line):
             
        inputInfo['board'].append((x, y))

    #vals = []
    #for line in lines[5+numG:]:
    #    vals += [int(i) for i in line.split()]
    #inputInfo['vals'] = np.array(vals).reshape(gridHeight, gridWidth)
    inputInfo['vals'] = []
    for line in lines[5+numG:]:
        inputInfo['vals'].append(list(map(int, filter(None, line.split()))))

    return inputInfo


def goalTest(targetCoord, currCoord):
    return targetCoord == currCoord


def getPossibleMoves((x, y)):
    w, h = inputInfo['grid']
    maxDiff = inputInfo['maxDiff']
    vals = inputInfo['vals']
    currVal = vals[y][x]

    validMoves = []
    i1, i2 = max(0, x-1), min(x+2, w)
    j1, j2 = max(0, y-1), min(y+2, h)
    for j in range(j1, j2):
        for i in range(i1, i2):
            if (i, j) == (x, y):
                continue
            if abs(currVal - vals[j][i]) <= maxDiff:
                validMoves.append((i, j))
    return validMoves



def compareAnswers(outputFile, answersFile):
    #print 'The startCoord is: {},\nThe targets are {},\nThe maxDiff is {},\n The grid is:\n{}.\n'.format(inputInfo['startCoord'], inputInfo['targetsCoord'], inputInfo['maxDiff'], inputInfo['vals'])
    res = True
    with open(answersFile) as f:
        answers = f.read().splitlines()
    with open(outputFile) as f:
        outputs = f.read().splitlines()
    if len(answers) != len(outputs):
        res = False
    for answer, output in zip(answers, outputs):
        if not answer == output:
            #print 'The answer vs output:\n{}\n{}'.format(answer, output)
            answers = answer.split()
            outputs = output.split()
            if inputInfo['alg'] == 'BFS':
                if len(answers) == len(outputs):
                    continue
                print 'The answer vs output for BFS:\n{}\n{}'.format(len(answers), len(outputs))

            elif inputInfo['alg'] == 'UCS' or inputInfo['alg'] == 'A*':
                answerVal = getPathValue(answers)
                outputVal = getPathValue(outputs)
                if answerVal == outputVal:
                    continue
                print 'The answer vs output for UCS or A*:\n{}\n{}'.format(answerVal, outputVal)
            
            res = False

    print res


def getPathValue(pathList):
    pre = None
    score = 0
    for coord in pathList:
        if not pre:
            pre = tuple(map(int, coord.split(',')))
        coord = tuple(map(int, coord.split(',')))
        getCostUCS(pre, coord)
        pre = coord
    return score


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
    res = []
    
    #start = time.time()

    '''
    if inputInfo['alg'] == 'BFS':
        for targetCoord in inputInfo['targetsCoord']:
            path = breadthFirstSearch(targetCoord)
            res.append(path)
    elif inputInfo['alg'] == 'UCS':
        for targetCoord in inputInfo['targetsCoord']:
            path = uniformCostSearch(targetCoord)
            res.append(path)
    '''
    if inputInfo['alg'] == 'BFS':
        resDict = breadthFirstSearchList(inputInfo['targetsCoord'])
    elif inputInfo['alg'] == 'UCS':
        resDict = uniformCostSearchList(inputInfo['targetsCoord'])
    elif inputInfo['alg'] == 'A*':
        for targetCoord in inputInfo['targetsCoord']:
            path = aStarSearch(targetCoord)
            res.append(path)
    else:
        res.append('FAIL')

    with open(args.output, 'w') as f:
        if  inputInfo['alg'] == 'BFS' or inputInfo['alg'] == 'UCS':
            for i in range(inputInfo['numG']):
                target = inputInfo['targetsCoord'][i]
                path = resDict.get(target, 'FAIL')
                if i == inputInfo['numG'] -1:
                    f.write(path)
                else:
                    f.write(path+'\n')
        else:
            for i in range(inputInfo['numG']):
                path = res[i]
                if i == inputInfo['numG'] -1:
                    f.write(path)
                else:
                    f.write(path+'\n')
        f.close()

    #print time.time() - start

    # compare answers
    #compareAnswers(args.output, args.answers)
