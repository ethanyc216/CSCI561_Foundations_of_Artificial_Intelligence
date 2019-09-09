#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

############################
##   CSCI 561 Fall 2019   ##
##       Homework 1       ##
##       Yifan Chen       ##
##  ethanyc216@gmail.com  ##
############################

# input: input.txt
# output: output.txt

import argparse 
import numpy as np 
import util

class Node(object):
    def __init__(self, coord, path, cost):
        self.coord = coord
        self.path = path 
        self.cost = cost


def processInput(fileName): 
    # algorithm 
    # width, height 
    # start coordinate, 0<=x<=w-1, 0<=y<=h-1
    # max diff allowed 
    # num of targets
    # the list of targets' coordinate, 0<=x<=w-1, 0<=y<=h-1
    # the array of the grid
    with open(fileName) as f: 
        lines = f.read().splitlines() 
    inputInfo = {} 

    inputInfo['alg'] = lines[0] 

    gridWidth, gridHeight = [int(i) for i in lines[1].split()] 
    inputInfo['grid'] = (gridWidth, gridHeight) 

    sX, sY = [int(i) for i in lines[2].split()] 
    inputInfo['startCoord'] = (sX, sY)

    inputInfo['maxDiff'] = int(lines[3])

    numG = int(lines[4])
    inputInfo['numG'] = numG

    inputInfo['targetsCoord'] = []
    for line in lines[5:5+numG]:
        x, y = [int(i) for i in line.split()] 
        inputInfo['targetsCoord'].append((x, y))

    vals = []
    for line in lines[5+numG:]:
        vals += [int(i) for i in line.split()]
    inputInfo['vals'] = np.array(vals).reshape(gridHeight, gridWidth)

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
            if (j, i) == (x, y):
                continue
            if abs(currVal - vals[j][i]) <= maxDiff:
                validMoves.append((i, j))
    return validMoves


def breadthFirstSearch(targetCoord):
    closedSet = set()
    queue = util.Queue()

    startCoord = inputInfo['startCoord']
    startNode = Node(startCoord, [startCoord], 0)
    queue.push(startNode)

    while not queue.isEmpty():
        currNode = queue.pop()
        currCoord = currNode.coord
        currPath = currNode.path
        closedSet.add(currCoord)

        if goalTest(targetCoord, currCoord):
            output = ''
            for x, y in currNode.path:
                output += '{},{} '.format(x, y)
            return output[:-1]
        else:
            nextCoords = getPossibleMoves(currCoord) 
            for nextCoord in nextCoords:
                if (nextCoord not in closedSet) and (nextCoord not in currPath):
                    closedSet.add(nextCoord)
                    nextPath = currPath[:]
                    nextPath.append(nextCoord)
                    nextCost = currNode.cost + 1
                    nextNode = Node(nextCoord, nextPath, nextCost)
                    queue.push(nextNode)
    return 'FAIL'


def compareAnswers(outputFile, answersFile):
    res = True
    with open(answersFile) as f:
        answers = f.read().splitlines()
    with open(outputFile) as f:
        outputs = f.read().splitlines()
    for answer, output in zip(answers, outputs):
        if not answer == output:
            print 'The answer vs output:\n{}\n{}'.fomate(answer, output)
            res = False
    print res


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, default='input5.txt',
                        help='input file name')

    parser.add_argument('--output', type=str, default='output.txt',
                        help='output file name')

    parser.add_argument('--answers', type=str, default='output5.txt',
                        help='answers file name')
    args = parser.parse_args()

    inputInfo = processInput(args.input)
    res = []
    if inputInfo['alg'] == 'BFS':
        for targetCoord in inputInfo['targetsCoord']:
            path = breadthFirstSearch(targetCoord)
            res.append(path)

    with open(args.output, 'w') as f:
        for path in res:
            f.write(path+'\n')
        f.close()

    # compare answers
    compareAnswers(args.output, args.answers)
