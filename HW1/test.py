#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

############################
##   CSCI 561 Fall 2019   ##
##       Homework 1       ##
##       Yifan Chen       ##
##  ethanyc216@gmail.com  ##
##     Sep. 26th 2019     ##
############################

# input: input.txt
# output: output.txt

import argparse
#import time

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

    #vals = []
    #for line in lines[5+numG:]:
    #    vals += [int(i) for i in line.split()]
    #inputInfo['vals'] = np.array(vals).reshape(gridHeight, gridWidth)
    inputInfo['vals'] = []
    for line in lines[5+numG:]:
        inputInfo['vals'].append(list(map(int, filter(None, line.split()))))

    return inputInfo


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
                print 'The answer vs output for BFS:\n{}, {}'.format(len(answers), len(outputs))

            elif inputInfo['alg'] == 'UCS' or inputInfo['alg'] == 'A*':
                answerVal = getPathValue(answers)
                outputVal = getPathValue(outputs)
                if answerVal == outputVal:
                    continue
                print 'The answer vs output for UCS or A*:\n{}, {}'.format(answerVal, outputVal)

            res = False

    print (res)

def getCostUCS(x1, y1, nextCoord):
    if (x1-1, y1-1) == nextCoord:
        return 14
    elif (x1-1, y1+1) == nextCoord:
        return 14
    elif (x1+1, y1-1) == nextCoord:
        return 14
    elif (x1+1, y1+1) == nextCoord:
        return 14
    else:
        return 10

def getPathValue(pathList):
    pre = None
    score = 0
    for coord in pathList:
        if not pre:
            pre = tuple(map(int, coord.split(',')))
        coord = tuple(map(int, coord.split(',')))
        getCostUCS(pre[0], pre[1], coord)
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

    #print time.time() - start

    # compare answers
    compareAnswers(args.output, args.answers)
