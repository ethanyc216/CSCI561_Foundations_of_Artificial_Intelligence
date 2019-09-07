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

def processInput(fileName): 
    # algorithm 
    # width, height 
    # start coordinate
    # max diff allowed 
    # num of targets
    # the list of targets' coordinate 
    # the array of the grid
    with open(fileName) as f: 
        lines = f.read().splitlines() 
    inputInfo = {} 

    inputInfo['alg'] = lines[0] 

    gridWidth, gridHeight = [int(i) for i in lines[1].split()] 
    inputInfo['grid'] = (gridWidth, gridHeight) 

    sX, sY = [int(i) for i in lines[2].split()] 
    inputInfo['startCo'] = (sX, sY)

    inputInfo['maxDiff'] = int(lines[3])

    numG = int(lines[4])
    inputInfo['numG'] = numG

    inputInfo['targetsCo'] = []
    for line in lines[5:5+numG]:
        x, y = [int(i) for i in line.split()] 
        inputInfo['targetsCo'].append((x, y))

    vals = []
    for line in lines[5+numG:]:
        vals += [int(i) for i in line.split()]
    inputInfo['vals'] = np.array(vals).reshape(gridHeight, gridWidth)

    return inputInfo

def breadthFirstSearch(startCo, targetCo, path, cost):







if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--input', type=str, default='input1.txt',
                        help='input file name')

    parser.add_argument('--output', type=str, default='output.txt',
                        help='output file name')

    args = parser.parse_args()

    inputInfo = processInput(args.input)