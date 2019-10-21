#!/usr/bin/env python 
# -*- coding: utf-8 -*- 

############################
##   CSCI 561 Fall 2019   ##
##       Homework 2       ##
##       Yifan Chen       ##
##  ethanyc216@gmail.com  ##
##     Oct. 11th 2019     ##
############################

import copy
from math import sqrt

colors = {'WHITE': 'W', 'BLACK': 'B'}
opponents = {'W': 'B', 'B': 'W'}
goals = {'W': 0, 'B': 15}
camps = {'W': set([(14, 11), (15, 12), (13, 12), (15, 13), (13, 13), (14, 12), (12, 13), (13, 15), (12, 15), (14, 13), (15, 11), (14, 15), (13, 14), (11, 14), (14, 14), (11, 15), (15, 14), (15, 15), (12, 14)]),
    'B': set([(0, 1), (1, 2), (3, 2), (0, 0), (0, 3), (3, 0), (3, 1), (2, 1), (0, 2), (2, 0), (1, 3), (2, 3), (1, 4), (2, 2), (0, 4), (1, 0), (4, 1), (1, 1), (4, 0)])}


class HalmaGame(object):

    def __init__(self, whiteSet, blackSet):
        self.board = {'W': whiteSet, 'B': blackSet, 'total': whiteSet | blackSet}
        self.camp = None
        self.jump = False


    def updateCamp(self):
        self.camp = {'W': camps['W'] & self.board['W'], 'B': camps['B'] & self.board['B']}


    def isLose(self, color):
        goalPawns = self.board[opponents[color]] & camps[color]
        if len(goalPawns) > 0:
            goalPawns = self.board['total'] & camps[color]
        return len(goalPawns) == 19


    def isWin(self, color):
        goalPawns = self.board[color] & camps[opponents[color]]
        if len(goalPawns) > 0:
            goalPawns = self.board['total'] & camps[opponents[color]]
        return len(goalPawns) == 19


    def getPawns(self, color):
        return self.board[color]


    def getPossibleMovesPawn(self, color, (pawnX, pawnY)):
        validMoves = {}

        # jumps
        jumps = [((pawnX, pawnY), ['J'])]
        closedSet = set()
        while jumps:
            (x, y), path = jumps.pop()
            if (x, y) in closedSet:
                continue
            closedSet.add((x, y))
            if (x, y) not in camps[color]:
                validMoves[(x, y)] = path + [(x, y)]
            elif (x-pawnX) >= 0 and (y-pawnY) >= 0 and color == 'B' and len(path) > 1:
                validMoves[(x, y)] = path + [(x, y)]
            elif (x-pawnX) <= 0 and (y-pawnY) <= 0 and color == 'W' and len(path) > 1:
                validMoves[(x, y)] = path + [(x, y)]

            possibleJumps = self.getPossibleJumpsPawn((x, y), path)
            jumps += possibleJumps

        # normal moves
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x = pawnX + i
                y = pawnY + j
                if x < 0 or x > 15 or y < 0 or y > 15:
                    continue
                elif (x, y) in self.board['total']:
                    continue
                if (x, y) not in camps[color]:
                    validMoves[(x, y)] = ['E', (pawnX, pawnY), (x, y)]
                elif (x-pawnX) >= 0 and (y-pawnY) >= 0 and color == 'B':
                    validMoves[(x, y)] = ['E', (pawnX, pawnY), (x, y)]
                elif (x-pawnX) <= 0 and (y-pawnY) <= 0 and color == 'W':
                    validMoves[(x, y)] = ['E', (pawnX, pawnY), (x, y)]

        return validMoves


    def getPossibleMovesPawnFree(self, color, (pawnX, pawnY)):
        validMoves = {}

        # jumps
        jumps = [((pawnX, pawnY), ['J'])]
        closedSet = set()
        while jumps:
            (x, y), path = jumps.pop()
            if (x, y) in closedSet:
                continue
            closedSet.add((x, y))
            if (len(path) != 1) and ((x, y) not in camps[color]):
                validMoves[(x, y)] = path + [(x, y)]

            possibleJumps = self.getPossibleJumpsPawn((x, y), path)
            jumps += possibleJumps

        # normal moves
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x = pawnX + i
                y = pawnY + j
                if x < 0 or x > 15 or y < 0 or y > 15:
                    continue
                elif (x, y) in self.board['total']:
                    continue
                elif (x, y) not in camps[color]:
                    validMoves[(x, y)] = ['E', (pawnX, pawnY), (x, y)]

        return validMoves


    def getPossibleJumpsPawn(self, (pawnX, pawnY), path):
        # return landed spot and path
        path = copy.deepcopy(path)
        path.append((pawnX, pawnY))
        validMoves = []

        for i in range(-1, 2):
            for j in range(-1, 2):
                if i == 0 and j == 0:
                    continue
                x = pawnX + i * 2
                y = pawnY + j * 2
                if x < 0 or x > 15 or y < 0 or y > 15:
                    continue
                elif (x, y) not in self.board['total']:
                    jumpX = x - i
                    jumpY = y - j
                    if (jumpX, jumpY) in self.board['total']:
                        if (x, y) in path:
                            continue
                        validMoves.append(((x, y), path))

        return validMoves               


    def getPossibleMoves(self, color):
        validMoves = {}

        self.updateCamp()
        if self.camp[color]:
            for pawnX, pawnY in self.camp[color]:
                moves = self.getPossibleMovesPawn(color, (pawnX, pawnY))
                if moves:
                    validMoves[(pawnX, pawnY)] = moves

            if not validMoves:
                for pawnX, pawnY in (self.board[color] - self.camp[color]):
                    moves = self.getPossibleMovesPawnFree(color, (pawnX, pawnY))
                    if moves:
                        validMoves[(pawnX, pawnY)] = moves
                        
        else:
            for pawnX, pawnY in self.board[color]:
                moves = self.getPossibleMovesPawnFree(color, (pawnX, pawnY))
                if moves:
                    validMoves[(pawnX, pawnY)] = moves
     
        return validMoves


    def makeMove(self, color, ori, des, jump):
        state = copy.deepcopy(self)
        state.board[color].remove(ori)
        state.board[color].add(des)
        state.board['total'] = state.board['W'] | state.board['B']
        state.jump = jump == 'J'

        return state


    def getRecommendedMovesSingle(self, color, allMoves):
        recommendedMoves = None
        self.updateCamp()
        if self.camp[color]:  
            for startX, startY in allMoves:
                for desX, desY in allMoves[(startX, startY)]:
                    if (desX, desY) not in camps[color]:
                        recommendedMoves = allMoves[(startX, startY)][(desX, desY)]
                        return recommendedMoves

        for startX, startY in allMoves:
            for desX, desY in allMoves[(startX, startY)]:
                recommendedMoves = allMoves[(startX, startY)][(desX, desY)]
                return recommendedMoves


    def getScores(self, color):
        goalPawns = self.board[color] & camps[opponents[color]]
        score = len(goalPawns)
        if score > 0:
            goalPawns = self.board['total'] & camps[opponents[color]]
            score = len(goalPawns)

        if score == 19:
            return 19 * 2 + 1
        
        openPawns = self.board[color] - camps[opponents[color]]
        openGoals = camps[opponents[color]] - self.board['total'] 
        
        while openGoals:
            shortest = (None, None, float('inf'))
            for goal in openGoals:
                for pawn in openPawns:
                    dist = (pawn[0] - goal[0])**2 + (pawn[1] - goal[1])**2
                    if dist < shortest[2]:
                        shortest = (pawn, goal, dist)

            score += (1/ sqrt(shortest[2]))
            openPawns.remove(shortest[0])
            openGoals.remove(shortest[1])

        if self.jump:
            return score + 5

        return score

