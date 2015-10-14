def minimax(board, depth, maxPlayer):
    global best_move
    print 'depth' + str(depth)
    #If the max depth has reached or there are no possible moves, then calculate the heuristic value for the board
    if depth == 0 or not gamePlay.isAnyMovePossible(board, myColor) or not gamePlay.isAnyMovePossible(board, opponentColor):
        print 'EValuation'
        return evaluation(board)

    if maxPlayer:
        best = Decimal('-Infinity')
        moves = getAllPossibleMoves(board, myColor)
        for move in moves:
            newBoard = deepcopy(board)
            gamePlay.doMove(newBoard,move)
            moveVal = minimax(newBoard, depth - 1, False)
            if(moveVal > best):
                best_move = move
                best = moveVal
        return best
    else:
        best = Decimal('Infinity')
        moves = getAllPossibleMoves(board, opponentColor)
        for move in moves:
            newBoard = deepcopy(board)
            gamePlay.doMove(newBoard,move)
            moveVal = minimax(newBoard, depth - 1, True)
            if(moveVal < best):
                #best_move = move
                best = moveVal
        return best
