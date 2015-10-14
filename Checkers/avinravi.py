#Name: Avinash Ravi
#Email id: avinravi@indiana.edu

import gamePlay
from decimal import Decimal
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves

#Stores the weight for each valid position on the board
weightedBoard = [
		    [0, 2, 0, 2, 0, 2, 0, 2],
                    [2, 0, 1, 0, 1, 0, 1, 0],
		    [0, 1, 0, 1, 0, 1, 0, 2],
		    [2, 0, 1, 0, 1, 0, 1, 0],
		    [0, 1, 0, 1, 0, 1, 0, 2],
		    [2, 0, 1, 0, 1, 0, 1, 0],
		    [0, 1, 0, 1, 0, 1, 0, 2],
		    [2, 0, 2, 0, 2, 0, 2, 0]
		]

#Stores my color and opponents color for using in evaluation function
myColor = None
opponentColor = None
#Stores the initial board state
currentBoard = None
#Stores the best move possible
best_move = None
#Stores the max_depth. Modify this value to change the maximum depth of the minimax tree
maxDepth = 7

'''
This evaluation function is computed based on the position of my coins on the board.
The sum of weights of all my coins on the board are computed. The same value is computed for my opponents coins.
The difference of these sums is the value returned by the evaluation function.
The weights are assigned as: 
The coin that is present in one of the corner row/column has less chance to be attacked. Hence these positions have higher weight.
In all other board positions, the coin can be attacked. Hence less weight at all other positions.
When the coin is a king, then double the assigned weights.
'''
def evaluation(board):
    # Weight Based Evaluation function
    # Count how many safe pieces I have than the opponent

    value = 0

    # Loop through all board positions
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y] == myColor.upper():
            value = value + (2 * weightedBoard[x][y])
        elif board[x][y] == myColor:
            value = value + weightedBoard[x][y]
        elif board[x][y] == opponentColor.upper():
            value = value - (2 * weightedBoard[x][y])
        elif board[x][y] == opponentColor:
            value = value - weightedBoard[x][y]

    return value

def nextMove(board, color, time, movesRemaining):
    global myColor, opponentColor, best_move, currentBoard

    #Store my color, opponents color and initial board state as global variables
    myColor = color
    opponentColor = gamePlay.getOpponentColor(color)
    currentBoard = board

    #Call the minimax algorithm with alphabeta pruning
    moveVal = alphaBeta(board, maxDepth, Decimal('-Infinity'), Decimal('Infinity'), True)

    #Returns the global best move variable
    return best_move

def alphaBeta(board, depth, alpha, beta, maxPlayer):
    global best_move

    #If the max depth has reached or there are no possible moves, then calculate the heuristic value for the board
    if depth == 0:
        return evaluation(board)

    #If the current depth level is Max's turn
    if maxPlayer:
        best = Decimal('-Infinity')
        #Get all the possible moves
        moves = getAllPossibleMoves(board, myColor)
        for move in moves:
            newBoard = deepcopy(board)
            #Play the next legal move
            gamePlay.doMove(newBoard,move)
            #Do alphabeta pruning for next depth level
            val = alphaBeta(newBoard, depth - 1, alpha, beta, False)
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
        for  move in moves:
            newBoard = deepcopy(board)
            #Play the next legal move
            gamePlay.doMove(newBoard,move)
            #Do alphabeta pruning for next depth level
            val = alphaBeta(newBoard, depth - 1, alpha, beta, True)
            if val < best:
                best = val
            best = min(best, val)
            beta = min(beta, best)
            #alpha cut off
            if beta <= alpha:
                break
        return best
