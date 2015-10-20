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
#Stores the previous move
prevMove = [0,0]
#Stores the move before previous move
prePrevMove = [7,7]
#Stores the move that is repeated
repeat_move = [0,0]
#Checks if the move is the first move
initialMove = True
#Stores the initial time and total moves
timeStarted = 0
totMoves = 0
#Stores the previous time stamp
prevTime = 0


#The evaluation function is determined based on the number of moves remaining.
#In the beginning of game, the strategy is attacking
#In the middle of the game, the strategy is a combination of attacking and defensive ((More of defensive)
#In the ending of game, the strategy is defensive


'''
This evaluation function is computed based on the position of my coins on the board.
The sum of weights of all my coins on the board are computed. The same value is computed for my opponents coins.
The difference of these sums is the value returned by the evaluation function.
The weights are assigned as: 
The distance from the center squares of the board is the weight of a position.
15, 18, position left of 15, position right of 18 are the center squares. These are allocated weight of 1.
The positions adjacent to center squares has weight 2 and so on.
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

        if board[x][y].upper() == myColor.upper():
            value += weightedBoard[x][y]
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
    return 2 * evaluationAttacking(board) + 3 * evaluationDefensive(board)

def nextMove(board, color, time, movesRemaining):
    global myColor, opponentColor, best_move, currentBoard, maxDepth
    global prePrevMove, prevMove, repeat_move
    global initialMove, totMoves, timeStarted, prevTime

    #Store my color, opponents color and initial board state as global variables
    myColor = color
    opponentColor = gamePlay.getOpponentColor(color)
    currentBoard = board

    #Store the initial time and moves in the initial move
    if initialMove:
        timeStarted = time
        totMoves = movesRemaining
        initialMove = False
        #If the player color is red and it is an initial move, then return a random best move
        if myColor == 'r':
            #Possible first moves for a red coin
            moves = [[10, 15], [9, 13], [10, 14], [11, 15], [11, 16], [12, 16]]
            prePrevMove = prevMove
            prevMove = moves[random.randint(0, 5)]
            return prevMove

    #Calculates the 1/15th part of time, 1/6th parts of time
    time15 = timeStarted / 15
    time6 = timeStarted / 6

    #Modify the maximum depth based on the time available
    #If timeStarted = 150 
    #time > 140 
    if time > (timeStarted - time15):
        maxDepth = 5
    #time > 120
    elif time > (timeStarted - 3 * time15):
        maxDepth = 6
    #time > 50
    elif time > 5 * time15:
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

    #Readjust the max depth if the time consumed for a move is greater than 15 seconds
    if (prevTime - time > timeStarted/7.5):
        maxDepth -= 1

    #Updating the time stamp value
    prevTime = time

    #If there is a single move, return that move
    moves = getAllPossibleMoves(board, myColor)
    if (len(moves)) == 1:
        prePrevMove = prevMove
        prevMove = moves[0]
        return moves[0]

    #Determines the evaluation function based on number of moves remaining
    if gamePlay.countPieces(board, myColor) < gamePlay.countPieces(board, opponentColor) or movesRemaining < totMoves/3:
        evaluationFunc = evaluationDefensive
    elif movesRemaining <= (totMoves - totMoves/10):
        evaluationFunc = evaluationCombination
    else:
        evaluationFunc = evaluationAttacking

    #Call the minimax algorithm with alphabeta pruning
    moveVal = alphaBeta(board, maxDepth, Decimal('-Infinity'), Decimal('Infinity'), True, evaluationFunc)

    #Checks if the next_move is returning the same moves repeatedly
    if ((prePrevMove == best_move) and
        (prevMove[0] == best_move[1] and prevMove[1] == best_move[0])):
        repeat_move = best_move
        #Call alpha beta pruning with depth 4 again
        moveVal = alphaBeta(board, 4, Decimal('-Infinity'), Decimal('Infinity'), True, evaluationFunc)

    #Returns the global best move variable
    prePrevMove = prevMove
    prevMove = best_move
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
            #Checks if the current move is a move repeated in previous steps
            if move == repeat_move:
                repeat_move = [0,0]
                continue
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
