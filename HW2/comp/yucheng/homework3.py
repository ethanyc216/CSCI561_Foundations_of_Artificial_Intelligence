#!/usr/bin/python3

import time

global myCamp, eneCamp
myCamp = []
eneCamp = []

def readFile(fileName):
	board = []
	f = open(fileName, 'r')
	content = f.readlines()
	f.close()
	gameMode = content[0].strip()
	color = content[1].strip()
	if color == "WHITE":
		eneColor = "BLACK"
		myCamp = [[11,14],[11,15],[12,13],[12,14],[12,15],[13,12],[13,13],[13,14],[13,15],[14,11],[14,12],[14,13],[14,14],[14,15],[15,11],[15,12],[15,13],[15,14],[15,15]]
		eneCamp = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[4,0],[4,1]]
	else:
		eneColor = "WHITE"
		myCamp = [[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0],[2,1],[2,2],[2,3],[3,0],[3,1],[3,2],[4,0],[4,1]]
		eneCamp = [[11,14],[11,15],[12,13],[12,14],[12,15],[13,12],[13,13],[13,14],[13,15],[14,11],[14,12],[14,13],[14,14],[14,15],[15,11],[15,12],[15,13],[15,14],[15,15]]
	rTime = content[2].strip()
	for i in range(3, 19):
		board.append(content[i].strip())
	return gameMode, color, eneColor, float(rTime), board, myCamp, eneCamp

# Check if player camp is empty. If not, return list of locations of pieces still in camp
def checkCamp(board, color):
	pos = []
	if color == "BLACK":
		for i in range(0, 5):
			if board[0][i] == "B":
				pos.append([0, i])
		for i in range(1, 5):
			for j in range(5-i, -1, -1):
				if board[i][j] == "B":
					pos.append([i, j])
	else:
		for i in range(11, 16):
			if board[15][i] == "W":
				pos.append([15, i])
		for i in range(11, 15):
			for j in range(1, i-8):
				if board[i][-j] == "W":
					pos.append([i, 16-j])
	if len(pos) == 0:
		return False
	return pos

# Get the location for all pieces on the given board(mine and my opponent's)
def getPiecePos(board, color):
	piecePos = []
	enePiecePos = []
	if color == "WHITE":
		for i in range(0, 16):
			for j in range(0, 16):
				if board[i][j] == "W":
					piecePos.append([i, j])
				elif board[i][j] == "B":
					enePiecePos.append([i, j])
	else:
		for i in range(0, 16):
			for j in range(0, 16):
				if board[i][j] == "B":
					piecePos.append([i, j])
				elif board[i][j] == "W":
					enePiecePos.append([i, j])
	return piecePos, enePiecePos

# Assign a score for each position on the board, my scoreboard and my opponent's scoreboard would be different
def assignScore(color):
	myScoreBoard = []
	eneScoreBoard = []
	if color == "BLACK":
		for i in range(0, 16):
			tem = []
			for j in range(0, 16):
				score = (i+1)*(j+1)
				tem.append(score)
			myScoreBoard.append(tem)

		for i in range(0, 16):
			tem = []
			for j in range(0, 16):
				score = (16-i)*(16-j)
				tem.append(score)
			eneScoreBoard.append(tem)
	else:
		for i in range(0, 16):
			tem = []
			for j in range(0, 16):
				score = (16-i)*(16-j)
				tem.append(score)
			myScoreBoard.append(tem)

		for i in range(0, 16):
			tem = []
			for j in range(0, 16):
				score = (i+1)*(j+1)
				tem.append(score)
			eneScoreBoard.append(tem)
	return myScoreBoard, eneScoreBoard

# score variable represents my advantage over my opponent, it could be negative
def eval(piecePos, enePiecePos, myScoreBoard, eneScoreBoard):
	myScore = 0
	eneScore = 0
	for i in range(0, 19):
		myScore += myScoreBoard[piecePos[i][0]][piecePos[i][1]]
	for i in range(0, 19):
		eneScore += eneScoreBoard[enePiecePos[i][0]][enePiecePos[i][1]]
	score = myScore - eneScore
	return score

# Move pieces in camp out of camp
def moveCamp(piecePos, board, color, myCamp, eneCamp, myScoreBoard, eneScoreBoard):
	allLegalMoves = []
	for i in range(0, len(piecePos)):
		allLegalMoves += checkLegalMove(piecePos[i], board, myCamp, eneCamp)
	bestMove = None
	secondBestMove = None
	maxValue = float("-inf")
	secondMaxValue = float("-inf")
	for i in allLegalMoves:
		oldPos = [i[1], i[2]]
		newPos = [i[-2], i[-1]]
		oldScore = myScoreBoard[oldPos[0]][oldPos[1]]
		newScore = myScoreBoard[newPos[0]][newPos[1]]
		diff = newScore - oldScore
		if diff > maxValue and newPos not in myCamp:
			maxValue = diff
			bestMove = i
		elif diff > secondMaxValue and newPos in myCamp and moveWithinCamp(oldPos, newPos, color):
			secondMaxValue = diff
			secondBestMove = i
	if bestMove != None:
		return bestMove
	return secondBestMove

# Check if a piece is moving away from the camp
def moveWithinCamp(oldPos, newPos, color):
	horiDiff = newPos[0] - oldPos[0]
	verDiff = newPos[1] - oldPos[1]
	if color == "BLACK":
		if horiDiff >= 0 and verDiff >= 0:
			return True
		else:
			return False
	else:
		if horiDiff <= 0 and verDiff <= 0:
			return True
		else:
			return False 
	return False

def checkEndGame(piecePos, myCamp, eneCamp):
	result = []
	target = eneCamp.copy()
	for i in piecePos:
		if i not in eneCamp:
			result.append(i)
		else:
			target.remove(i)
	if len(result) > 1:
		return False, None
	else:
		return result[0], target[0]

def moveLastPiece(color, curBoard, lastPiece, target, myCamp, eneCamp):
	allLegalMoves = checkLegalMove(lastPiece, curBoard, myCamp, eneCamp)
	distance = float('inf')
	bestMove = allLegalMoves[0]
	for i in allLegalMoves:
		newPos = [i[-2], i[-1]]
		tem = (target[0] - newPos[0])**2 + (target[1] - newPos[1])**2
		if tem < distance:
			bestMove = i
			distance = tem
	return bestMove

def minMax(board, color, piecePos, myCamp, eneCamp, myScoreBoard, eneScoreBoard, rTime):
	allLegalMoves = []
	bestMove = None
	maxValue = float("-inf")
	alpha = float("-inf")
	beta = float("inf")
	level = 0
	lastPiece, target = checkEndGame(piecePos, myCamp, eneCamp)
	if lastPiece != False:
		bestMove = moveLastPiece(color, board, lastPiece, target, myCamp, eneCamp)
		return bestMove
	if rTime <= 280 and rTime >= 150:
		maxLevel = 2
	else:
		maxLevel = 1
	
	for i in range(0, len(piecePos)):
		allLegalMoves += checkLegalMove(piecePos[i], board, myCamp, eneCamp)
	goodMove = []
	for i in allLegalMoves:
		if isMoveGood(i, myScoreBoard):
			goodMove.append(i)
	if len(goodMove) > 0:
		bestMove = goodMove[0]
		for i in goodMove:
			temBoard = board.copy()
			tem = eneTurn(color, updateBoard(i, temBoard), level, maxLevel, myCamp, eneCamp, myScoreBoard, eneScoreBoard, alpha, beta)
			if tem > maxValue:
				maxValue = tem
				bestMove = i
	else:
		bestMove = allLegalMoves[0]
		for i in allLegalMoves:
			temBoard = board.copy()
			tem = eneTurn(color, updateBoard(i, temBoard), level, maxLevel, myCamp, eneCamp, myScoreBoard, eneScoreBoard, alpha, beta)
			if tem > maxValue:
				maxValue = tem
				bestMove = i
	return bestMove

def myTurn(color, curBoard, level, maxLevel, myCamp, eneCamp, myScoreBoard, eneScoreBoard, alpha, beta):
	piecePos, enePiecePos = getPiecePos(curBoard, color)
	if level >= maxLevel:
		return eval(piecePos, enePiecePos, myScoreBoard, eneScoreBoard)
	allLegalMoves = []
	for i in range(0, len(piecePos)):
		allLegalMoves += checkLegalMove(piecePos[i], curBoard, myCamp, eneCamp)
	goodMove = []
	for i in allLegalMoves:
		if isMoveGood(i, myScoreBoard):
			goodMove.append(i)
	if len(goodMove) > 0:
		for i in goodMove:
			temBoard = curBoard.copy()
			tem = eneTurn(color, updateBoard(i, temBoard), level+1, maxLevel, eneCamp, myCamp, myScoreBoard, eneScoreBoard, alpha, beta)
			if tem > alpha:
				alpha = tem
			if alpha >= beta:
				break
	else:
		for i in allLegalMoves:
			temBoard = curBoard.copy()
			tem = eneTurn(color, updateBoard(i, temBoard), level+1, maxLevel, eneCamp, myCamp, myScoreBoard, eneScoreBoard, alpha, beta)
			if tem > alpha:
				alpha = tem
			if alpha >= beta:
				break
	return alpha

def eneTurn(color, curBoard, level, maxLevel, eneCamp, myCamp, myScoreBoard, eneScoreBoard, alpha, beta):
	piecePos, enePiecePos = getPiecePos(curBoard, color)
	if level >= maxLevel:
		return eval(piecePos, enePiecePos, myScoreBoard, eneScoreBoard)
	allLegalMoves = []
	for i in range(0, len(enePiecePos)):
		allLegalMoves += checkLegalMove(enePiecePos[i], curBoard, eneCamp, myCamp)
	goodMove = []
	for i in allLegalMoves:
		if isMoveGood(i, eneScoreBoard):
			goodMove.append(i)
	if len(goodMove) > 0:
		for i in goodMove:
			temBoard = curBoard.copy()
			tem = myTurn(color, updateBoard(i, temBoard), level+1, maxLevel, myCamp, eneCamp, myScoreBoard, eneScoreBoard, alpha, beta)
			if tem < beta:
				beta = tem
			if beta <= alpha:
				break
	else:
		for i in allLegalMoves:
			temBoard = curBoard.copy()
			tem = myTurn(color, updateBoard(i, temBoard), level+1, maxLevel, myCamp, eneCamp, myScoreBoard, eneScoreBoard, alpha, beta)
			if tem < beta:
				beta = tem
			if beta <= alpha:
				break
	return beta
	

# Update the board given a move
def updateBoard(move, board):
	oldPos = [move[1], move[2]]
	newPos = [move[-2], move[-1]]
	board[newPos[0]] = board[newPos[0]][:newPos[1]] + board[oldPos[0]][oldPos[1]] + board[newPos[0]][newPos[1]+1:]
	board[oldPos[0]] = board[oldPos[0]][:oldPos[1]] + '.' + board[oldPos[0]][oldPos[1]+1:]
	return board

# Check all legal moves given a position, return a 2D array
def checkLegalMove(pos, board, myCamp, eneCamp):
	avaiPos = []
	temBoard = board.copy()
	for i in range(pos[0]-1, pos[0]+2):
		for j in range(pos[1]-1, pos[1]+2):
			if pos != [i, j]:
				if checkValidPos([i, j]):
					if temBoard[i][j] == '.':
						move = ["E", pos[0], pos[1], i, j]
						if checkValidMove(move, myCamp, eneCamp):
							avaiPos.append(["E", pos[0], pos[1], i, j])
					else:
						tem = checkJump(pos, [i,j], [], temBoard, [pos], [], myCamp, eneCamp)
						if tem != None:
							avaiPos += tem
	return avaiPos

# Check all legal jump moves given a position, returns a 2D array
def checkJump(pos1, pos2, avaiPos, board, prevPos, hist, myCamp, eneCamp):
	xDiff = pos2[1] - pos1[1]
	yDiff = pos2[0] - pos1[0]
	newPos = [pos2[0] + yDiff, pos2[1] + xDiff]
	if checkValidPos(newPos) and board[newPos[0]][newPos[1]] == '.' and newPos not in prevPos and checkValidMove(["J", pos1[0], pos1[1], newPos[0], newPos[1]], myCamp, eneCamp):
		if len(hist) == 0:
			#avaiPos += ["J", pos1[0], pos1[1], newPos[0], newPos[1]]
			hist += ["J", pos1[0], pos1[1], newPos[0], newPos[1]]
			avaiPos.append(["J", pos1[0], pos1[1], newPos[0], newPos[1]])
		else:
			#tem = avaiPos[-1].copy()
			#tem += [newPos[0], newPos[1]]
			hist += [newPos[0], newPos[1]]
			avaiPos.append(hist)
		#avaiPos += ["J", pos1[0], pos1[1], newPos[0], newPos[1]]
		board = updateBoard(["J", pos1[0], pos1[1], newPos[0], newPos[1]], board)
		prevPos.append(newPos)
		adjPiece = getAdjacentPiece(newPos, board)
		if len(adjPiece) != 0:
			for i in range(0, len(adjPiece)):
				temBoard = board.copy()
				temHist = hist.copy()
				checkJump(newPos, adjPiece[i], avaiPos, temBoard, prevPos, temHist, myCamp, eneCamp)
		else:
			return
	else:
		return
	return avaiPos

# Get position of all adjacent pieces
def getAdjacentPiece(pos, board):
	adjPiece = []
	for i in range(pos[0]-1, pos[0]+2):
		for j in range(pos[1]-1, pos[1]+2):
			if pos != [i, j]:
				if checkValidPos([i, j]) and board[i][j] != '.':
					adjPiece.append([i, j])
	return adjPiece

# Check if this position is within the boundaries of the game board
def checkValidPos(pos):
	if pos[0] < 0 or pos[0] > 15 or pos[1] < 0 or pos[1] > 15:
		return False
	return True

# Check if move is valid
def checkValidMove(move, myCamp, eneCamp):
	oldPos = [move[1], move[2]]
	newPos = [move[-2], move[-1]]
	# Check if piece is moved out from enemy camp
	if oldPos in eneCamp and newPos not in eneCamp:
		return False
	# Check if piece is moved back to my camp
	if oldPos not in myCamp and newPos in myCamp:
		return False
	return True

def isMoveGood(move, myScoreBoard):
	oldScore = myScoreBoard[move[1]][move[2]]
	newScore = myScoreBoard[move[-2]][move[-1]]
	diff = newScore - oldScore
	if diff >= 0:
		return True
	else:
		return False

# Break down jump move
def digestJumpMove(move):
	result = []
	move.pop(0)
	while len(move) > 2:
		tem = 'J %s,%s %s,%s'%(str(move[1]), str(move[0]), str(move[3]), str(move[2]))
		result.append(tem)
		move.pop(0)
		move.pop(0)
	return result

# Produce output file
def giveOutput(move):
	output = ''
	f=open("./output.txt", "w")
	if move[0] == "E" or len(move) <= 4:
		output = '%s %s,%s %s,%s'%(move[0], str(move[2]), str(move[1]), str(move[4]), str(move[3]))
		f.write(output + '\n')
		f.close()
	else:
		result = digestJumpMove(move)
		for i in result:
			f.write(i + '\n')
		f.close()
	return

def main(fileName):
	gameMode, color, eneColor, rTime, board, myCamp, eneCamp = readFile(fileName)
	piecePos, enePiecePos = getPiecePos(board, color)
	myScoreBoard, eneScoreBoard = assignScore(color)
	pieceInCamp = checkCamp(board, color)
	if not pieceInCamp: #If every piece has left camp
		bestMove = minMax(board, color, piecePos, myCamp, eneCamp, myScoreBoard, eneScoreBoard, rTime)
		giveOutput(bestMove)
	else:
		piecePosCamp = pieceInCamp.copy()
		bestMove = moveCamp(piecePosCamp, board, color, myCamp, eneCamp, myScoreBoard, eneScoreBoard)
		if bestMove == None:
			pieceOutCamp = []
			for i in piecePos:
				if i not in piecePosCamp:
					pieceOutCamp.append(i)
			bestMove = minMax(board, color, pieceOutCamp, myCamp, eneCamp, myScoreBoard, eneScoreBoard, rTime)
		giveOutput(bestMove)
	return
main("input.txt")