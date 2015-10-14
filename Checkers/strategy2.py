import gamePlay
from decimal import Decimal
from copy import deepcopy
from getAllPossibleMoves import getAllPossibleMoves

#Stores my color and opponents color for using in evaluation function
myColor = 'w'
opponentColor = 'r'
#Stores the initial board state
currentBoard = None
#Stores the best move possible
best_move = None
#Stores the max_depth
maxDepth = 8

def evaluation(board):
    
    value = 0

    # Loop through all board positions
    for piece in range(1, 33):
        xy = gamePlay.serialToGrid(piece)
        x = xy[0]
        y = xy[1]
                
        if board[x][y] == myColor.upper():
            value = value + 5
	elif board[x][y] == myColor:
	    value = value + 3
        elif board[x][y] == opponentColor.upper():
            value = value - 5
	elif board[x][y] == opponentColor:
            value = value - 3

    return value

def nextMove(board, color, time, movesRemaining):
    global myColor, opponentColor, best_move, currentBoard
    #Store my color and opponents color in global variables
    myColor = color
    opponentColor = gamePlay.getOpponentColor(color)
    currentBoard = board
    #moveVal = minimax(board, maxDepth, True)

    #Call the minimax algorithm with alphabeta pruning
    moveVal = alphabeta(board, maxDepth, Decimal('-Infinity'), Decimal('Infinity'), True)

    #Returns the global best move variable
    return best_move

def alphabeta(board, depth, alpha, beta, maxPlayer):
    global best_move
    #print 'depth' + str(depth)
    #If the max depth has reached or there are no possible moves, then calculate the heuristic value for the board
    if depth == 0: #or not gamePlay.isAnyMovePossible(board, myColor) or not gamePlay.isAnyMovePossible(board, opponentColor):
        #print 'Evaluation'
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
            val = alphabeta(newBoard, depth - 1, alpha, beta, False)
            #Update the best possible move
            if val > best:
                best = val
            if best > alpha:
                alpha = best
                if currentBoard == board:
                    best_move = move
            #alpha = max(alpha, best)
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
            val = alphabeta(newBoard, depth - 1, alpha, beta, True)
            #Update the best possible move
            if val < best:
                best = val
            beta = min(beta, best)
            #alpha cut off
            if beta <= alpha:
                break
        return best
