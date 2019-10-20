#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

############################
##   CSCI 561 Fall 2019   ##
##       Homework 2       ##
##       Yifan Chen       ##
##  ethanyc216@gmail.com  ##
##     Oct. 11th 2019     ##
############################

import argparse 
import copy

opponents = {'W': 'B', 'B': 'W'}
goals = {'W': 0, 'B': 15}
camps = {'W': set([(14, 11), (15, 12), (13, 12), (15, 13), (13, 13), (14, 12), (12, 13), (13, 15), (12, 15), (14, 13), (15, 11), (14, 15), (13, 14), (11, 14), (14, 14), (11, 15), (15, 14), (15, 15), (12, 14)]),
    'B': set([(0, 1), (1, 2), (3, 2), (0, 0), (0, 3), (3, 0), (3, 1), (2, 1), (0, 2), (2, 0), (1, 3), (2, 3), (1, 4), (2, 2), (0, 4), (1, 0), (4, 1), (1, 1), (4, 0)])}

class AlphaBetaAgent(object):

    def __init__(self, playerplayer, depth = 2):
        self.player = playerplayer
        self.depth = int(depth)


    def decodeCoord(self, allMoves, player):
        # todo, how to speeadup, close to goal first!
        actions = []
        campsActions = []
        opengoalsActions = []
        goalCamp = camps[opponents[player]]

        for startCoord in allMoves:
            curAllMovesDict = allMoves[startCoord]
            for endCoord in curAllMovesDict:
                jump = curAllMovesDict[endCoord][0]
                if (startCoord in camps[player]) and (endCoord not in camps[player]):
                    campsActions.append((startCoord, endCoord, jump))
                if startCoord in goalCamp:
                    opengoalsActions.append((startCoord, endCoord, jump))
                else:
                    actions.append((startCoord, endCoord, jump))

        #actions.sort(key=lambda x: (x[1][0]-goals[player])**2 + (x[1][1]-goals[player])**2)
        if len(campsActions) > 0:
            #campsActions.sort(key=lambda x: (x[0][0]-goals[player])**2 + (x[0][1]-goals[player])**2)
            campsActions.sort(key=lambda x: (x[1][0]-goals[player])**2 + (x[1][1]-goals[player])**2)
            return campsActions
        #actions.sort(key=lambda x: (x[0][0]-goals[player])**2 + (x[0][1]-goals[player])**2)
        actions.sort(key=lambda x: (x[1][0]-goals[player])**2 + (x[1][1]-goals[player])**2)
        opengoalsActions.sort(key=lambda x: (x[1][0]-goals[player])**2 + (x[1][1]-goals[player])**2)
        return actions + opengoalsActions


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        alpha = float('-inf')
        beta  = float('inf')
        score = float('-inf')

        # Choose one of the best actions
        allMoves = gameState.getPossibleMoves(self.player)
        for action in self.decodeCoord(allMoves, self.player):
            successorState = gameState.makeMove(self.player, action[0], action[1], action[2])
            minScore = self.minimizer(successorState, 0, opponents[self.player], alpha, beta)
            if minScore == (19 * 2 + 1):
                return allMoves[action[0]][action[1]]
            if minScore > score:
                score = minScore
                move = action
            '''
            elif minScore == score:
                if ((move[1][0] - goals[self.player])**2 + (move[1][1] - goals[self.player])**2) > ((action[1][0] - goals[self.player])**2 + (action[1][1] - goals[self.player])**2):
                    move = action
            '''
            alpha = max(alpha, minScore)
        return allMoves[move[0]][move[1]]


    def maximizer(self, gameState, currentDepth, alpha, beta):
        if self.depth == currentDepth or gameState.isLose(self.player) or gameState.isWin(self.player):
            return gameState.getScores(self.player)
        maxScore = float('-inf')
        allMoves = gameState.getPossibleMoves(self.player)
        d1 = copy.deepcopy(gameState.board['total'])
        for action in self.decodeCoord(allMoves, self.player):
            successorState = gameState.makeMove(self.player, action[0], action[1], action[2])
            maxScore = max(maxScore, self.minimizer(successorState, currentDepth + 1, opponents[self.player], alpha, beta))
            if maxScore > beta:
                return maxScore
            alpha = max(alpha, maxScore)
        return maxScore


    def minimizer(self, gameState, currentDepth, player, alpha, beta):
        if self.depth == currentDepth or gameState.isLose(self.player) or gameState.isWin(self.player):
            return gameState.getScores(self.player)
        minScore = float('inf')
        allMoves = gameState.getPossibleMoves(player)
        for action in self.decodeCoord(allMoves, player):
            successorState = gameState.makeMove(player, action[0], action[1], action[2])
            minScore = min(minScore, self.maximizer(successorState, currentDepth + 1, alpha, beta)) 
            if minScore < alpha:
                return minScore
            beta = min(minScore, beta)
        return minScore

