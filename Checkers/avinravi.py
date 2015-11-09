#Name: Avinash Ravi
#Email id: avinravi@indiana.edu

import gamePlay
import random
from decimal import Decimal
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves

#Stores the weight for each valid position on the board
weightedBoard = [
		    [0, 4, 0, 4, 0, 4, 0, 4],
                    [4, 0, 3, 0, 3, 0, 3, 0],
		    [0, 3, 0, 2, 0, 2, 0, 4],
		    [4, 0, 2, 0, 1, 0, 3, 0],
		    [0, 3, 0, 1, 0, 2, 0, 4],
		    [4, 0, 2, 0, 2, 0, 3, 0],
		    [0, 3, 0, 3, 0, 3, 0, 4],
		    [4, 0, 4, 0, 4, 0, 4, 0]
		]


#Stores my color and opponents color for using in evaluation function
myColor = None
opponentColor = None
#Stores the initial board state
currentBoard = None
#Stores the best move possible
best_move = None
#Stores the max_depth of minmax tree. Defaulting it to 7
maxDepth = 7
#Checks if the move is the first move
initialMove = True
#Stores the initial time and total moves
timeStarted = 0
totMoves = 0


#The evaluation function is determined based on the number of moves remaining.
#In the beginning of game, the strategy is attacking
#In the middle of the game, the strategy is a combination of attacking and defensive ((More of defensive)
#In the ending of game, the strategy is more defensive


'''
This evaluation function is computed based on the position of my coins on the board.
The sum of weights of all my coins on the board are computed. The same value is computed for my opponents coins.
The difference of these sums is the value returned by the evaluation function.
The weights are assigned as: 
The distance from the center squares of the board is the weight of a position.
15, 18, position left of 15, position right of 18 are the center squares. These are allocated weight of 1.
The positions adjacent to center squares has weight 2 and so on.
Double the weight if the coin is a king
'''
def evaluationDefensive(board):
    # Weight Based Evaluation function
    # Count how many safe pieces I have than the opponent

    value = 0

    # Loop through all board positions
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]

        if board[x][y] == myColor:
            value += weightedBoard[x][y]
        elif board[x][y] == myColor.upper():
            value += 2 * weightedBoard[x][y]
        elif board[x][y] == opponentColor.upper():
            value -= 2 * weightedBoard[x][y]
        else:
            value -= weightedBoard[x][y]

    return value

'''
Returns the distance of a given coin from king line
'''
def getDistance(color, x):
    if color.upper() == 'R':
        return 7-x
    else:
        return x

'''
This evaluation determines the coin's distance from becoming the king. If the coin is already a king,
then give it a higher value than maxmimum distance for a coin to  become a king.
'''
def evaluationAttacking(board):
    value = 0

    # Loop through all board positions
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]

        if board[x][y] == myColor.upper():
            value += 8
        elif board[x][y] == myColor:
            value += getDistance(myColor, x)
        elif board[x][y] == opponentColor.upper():
            value -= 8
        elif board[x][y] == opponentColor:
            value -= getDistance(opponentColor, x)

    return value

'''
Uses this evaluation function in middle of the game
'''
def evaluationCombination(board):
    return 5 * evaluationAttacking(board) + 2 * evaluationDefensive(board)

'''
Uses this evaluation function at the end of game
'''
def evaluationCombination2(board):
    return 3 * evaluationAttacking(board) + 2 * evaluationDefensive(board)

def nextMove(board, color, time, movesRemaining):
    global myColor, opponentColor, best_move, currentBoard, maxDepth
    global initialMove, totMoves, timeStarted

    #Store initial board state as global variables
    currentBoard = board

    #Store the initial time, moves, my color and opponents color in the initial move
    if initialMove:
        myColor = color
        opponentColor = gamePlay.getOpponentColor(color)
        timeStarted = time
        totMoves = movesRemaining
        initialMove = False

    #Calculates the 1/15th part of time, 1/6th parts of time
    time15 = timeStarted / 15
    time6 = timeStarted / 6

    #Modify the maximum depth based on the time available
    #If timeStarted = 150 
    #time > 140
    if time > (timeStarted - time15):
        maxDepth = 5
    #time > 130
    if time > (timeStarted - 2 * time15):
        maxDepth = 6
    #time > 60
    elif time > 6 * time15:
        maxDepth = 7
    #time > 30
    elif time > 3 * time15:
        maxDepth = 6
    #time > 20
    elif time > 2 * time15:
        maxDepth = 5
    #time < 20
    else:
        maxDepth = 4

    myPieces = gamePlay.countPieces(board, myColor)
    opponentPieces = gamePlay.countPieces(board, opponentColor)

    #if maxDepth < 7 and myPieces < opponentPieces:
    #    maxDepth += 1

    #If there is a single move, return that move
    moves = getAllPossibleMoves(board, myColor)
    if (len(moves)) == 1:
        return moves[0]
    
    #Determines the evaluation function based on number of moves remaining
    if movesRemaining < totMoves/10:
        evaluationFunc = evaluationCombination2
        if myPieces < opponentPieces:
            evaluationFunc = evaluationCombination
    elif movesRemaining <= (totMoves - totMoves/10):
        evaluationFunc = evaluationCombination
    else:
        evaluationFunc = evaluationAttacking

    #Call the minimax algorithm with alphabeta pruning
    moveVal = alphaBeta(board, maxDepth, Decimal('-Infinity'), Decimal('Infinity'), True, evaluationFunc)

    #Returns the global best move variable
    return best_move

def alphaBeta(board, depth, alpha, beta, maxPlayer, evaluationFunc):
    global best_move, repeat_move

    #If the max depth has reached or there are no possible moves, then calculate the heuristic value for the board
    if depth == 0:
        return evaluationFunc(board)

    #If the current depth level is Max's turn
    if maxPlayer:
        best = Decimal('-Infinity')
        #Get all the possible moves
        moves = getAllPossibleMoves(board, myColor)
        if(len(moves) == 0):
            return evaluationFunc(board)
        for move in moves:
            newBoard = deepcopy(board)
            #Play the next legal move
            gamePlay.doMove(newBoard,move)
            #Do alphabeta pruning for next depth level
            val = alphaBeta(newBoard, depth - 1, alpha, beta, False, evaluationFunc)
            best = max(best, val)
            if best > alpha:
                alpha = best
                #Update the best possible move if we are present at the first level
                if currentBoard == board:
                    best_move = move
            #Beta cut off
            if alpha >= beta:
                break
        return best

    #If the current depth level is Min's turn
    else:
        best = Decimal('Infinity')
        #Get all the possible moves
        moves = getAllPossibleMoves(board, opponentColor)
        if(len(moves) == 0):
            return evaluationFunc(board)
        for  move in moves:
            newBoard = deepcopy(board)
            #Play the next legal move
            gamePlay.doMove(newBoard,move)
            #Do alphabeta pruning for next depth level
            val = alphaBeta(newBoard, depth - 1, alpha, beta, True, evaluationFunc)
            if val < best:
                best = val
            best = min(best, val)
            beta = min(beta, best)
            #alpha cut off
            if beta <= alpha:
                break
        return best
