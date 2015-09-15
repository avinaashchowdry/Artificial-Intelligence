#Name: Avinash Ravi
#Username: avinravi
#========================================================

import random

#Loops the map and prints the current state of the board
def print_board():
    for i in range(0,3):
        for j in range(0,3):
            print map[2-i][j],
            if j != 2:
                print "|",
        print ""


#Checks if the game is over or a draw
def check_done():
    for i in range(0,3):
        if map[i][0] == map[i][1] == map[i][2] != " " \
        or map[0][i] == map[1][i] == map[2][i] != " ":
            print_board()
            print ""
            if currentPlayer == 0:
                print "You won!!!"
            else:
                print "Computer Won!!!"
            return True

    if map[0][0] == map[1][1] == map[2][2] != " " \
    or map[0][2] == map[1][1] == map[2][0] != " ":
        print_board()
        print ""
        if currentPlayer == 0:
            print "You won!!!"
        else:
            print "Computer Won!!!"
        return True

    if " " not in map[0] and " " not in map[1] and " " not in map[2]:
        print_board()
        print
        print "Draw"
        return True

    return False


#Swaps the turn value
def SwapTurn():
    global turn
    if turn == "X":
        turn = "O"
    else:
        turn = "X"


#Gets the matrix indices for a given position on the board
def GetBoardIndices(position):
    Y = position/3
    X = position%3
    if X != 0:
        X -=1
    else:
        X = 2
        Y -= 1

    return X,Y


#Takes an input from the User and prints the board
def MakeAMove():
    global done
    global turn
    global map

    moved = False
    while moved != True:
        print "Please select position by typing in a number between 1 and 9, see below for which number that is which position..."
        print "7|8|9"
        print "4|5|6"
        print "1|2|3"
        print

        try:
            pos = input("Select: ")
            #For a valid input value, calculates the index of 2-dimensional array for the given location on the board
            if pos <=9 and pos >=1:
                lastUserMove = pos
                X,Y = GetBoardIndices(pos)

                #If the given location is empty, fills the location on the board with the players symbol
                if map[Y][X] == " ":
                    map[Y][X] = turn
                    moved = True
                    done = check_done()

                    if done == False:
                        SwapTurn()

        except Exception,e:
            print str(e)
            print "You need to add a numeric value"


#Generates a random position for a given move
 #positionList holds the list of possible positions on the board
def GenerateRandomPosition(positionList):
    global map
    pos = random.randint(0,len(positionList)-1)
    X,Y = GetBoardIndices(positionList[pos])
    map[Y][X] = turn
    return True


#Generates an appropriate first move for the computer
def GenerateFirstMove():
    global map

    #If the computer starts first
    if human == "O":
        #Computer places in one of the corners or center ([1,3,7,9] are the possible corners on the board and 5 is the center of board)
        GenerateRandomPosition([1,3,5,7,9])

    #If the user starts first
    else:
        #If user has starts with center of board
        if map[1][1] == "X":
            #Computer places in one of the corners 
            GenerateRandomPosition([1,3,7,9])

        #If user has started with any of the corners, Computer places in the opposite corner
        elif map[0][0] == "X":
            map[2][2] = turn
        elif map[0][2] == "X":
            map[2][0] = turn
        elif map[2][0] == "X":
            map[0][2] == turn
        elif map[2][2] == "X":
            map[0][0] = turn

        #If the user has started with an edge, Computer randomly selects a corner or center
        else:
            GenerateRandomPosition([1,3,5,7,9])


#If the computer starts with "X" and in the second move, if the opposite corner is not placed by the opponent, then computer plays the opposite corner
def GetOppositeCornerSecondMove():
    global turn
    global map

    isMoveDone = False

    if map[0][0] == turn and map[2][2] == " ":
        map[2][2] = turn
        isMoveDone = True
    elif map[2][2] == turn and map[0][0] == " ":
        map[0][0] = turn
        isMoveDone = True
    elif map[0][2] == turn and map[2][0] == " ":
        map[2][0] = turn
        isMoveDone = True
    elif map[2][0] == turn and map[0][2] == " ":
        map[0][2] = turn
        isMoveDone = True

    if isMoveDone == True:
        SwapTurn()

    return isMoveDone

#Checks if the player(user/computer) has a chance of winning. If yes, returns the winning position else returns 0
def CheckForGame(player):
    winningPosition = 0;

    if (map[0][2] == player and map[0][0] == " " and map[0][1] == player) or \
         (map[1][0] == player and map[0][0] == " " and map[2][0] == player) or \
         (map[1][1] == player and map[0][0] == " " and map[2][2] == player):
        winningPosition = 1
    elif (map[0][0] == player and map[0][1] == " " and map[0][2] == player) or \
         (map[1][1] == player and map[0][1] == " " and map[2][1] == player):
        winningPosition = 2
    elif (map[0][0] == player and map[0][1] == player and map[0][2] == " ") or \
         (map[1][1] == player and map[0][2] == " " and map[2][0] == player) or \
         (map[1][2] == player and  map[0][2] == " " and map[2][2] == player):
        winningPosition = 3
    elif (map[0][0] == player and map[1][0] == " " and map[2][0] == player) or \
         (map[1][1] == player and map[1][0] == " " and map[1][2] == player):
        winningPosition = 4
    elif (map[0][0] == player and map[1][1] == " " and map[2][2] == player) or \
         (map[0][1] == player and map[1][1] == " " and map[2][1] == player) or \
         (map[0][2] == player and map[1][1] == " " and map[2][0] == player) or \
         (map[1][0] == player and map[1][1] == " " and map[1][2] == player):
        winningPosition = 5
    elif (map[0][2] == player and map[1][2] == " " and map[2][2] == player) or \
         (map[1][0] == player and map[1][1] == player and map[1][2] == " "):
        winningPosition = 6
    elif (map[0][0] == player and map[1][0] == player and map[2][0] == " ") or \
         (map[0][2] == player and map[1][1] == player and map[2][0] == " ") or \
         (map[2][0] == " " and map[2][1] == player and map[2][2] == player):
        winningPosition = 7
    elif (map[0][1] == player and map[1][1] == player and map[2][1] == " ") or \
         (map[2][0] == player and map[2][1] == " " and map[2][2] == player):
        winningPosition = 8
    elif (map[0][0] == player and map[1][1] == player and map[2][2] == " ") or \
         (map[0][2] == player and map[1][2] == player and map[2][2] == " ") or \
         (map[2][0] == player and map[2][1] == player and map[2][2] == " "):
        winningPosition = 9

    return winningPosition


#Gets the probable position to place to create a fork, returns 0 when no such move
#Below are the two probable forks checked by the function. There is one more possible fork combination I did not check
#  | | X    ||     | |    
#  | |      ||     |X|    
# X| | X    ||    X| |X   
def GetForkPosition(player):
    forkPosition = 0
    if map[0][0] == player:
        if map[0][2] == player and map[2][2] == " ":
            if (map[0][1] == " " and map[1][2] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][2] == " " and map[1][1] == " "):
                forkPosition = 9
        elif map[0][2] == " " and map[2][2] == player:
            if (map[0][1] == " " and map[1][2] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][2] == " " and map[1][1] == " "):
                forkPosition = 3
        if map[0][2] == player and map[2][0] == " ":
            if (map[0][1] == " " and map[1][0] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 7
        elif map[0][2] == " " and map[2][0] == player:
            if (map[0][1] == " " and map[1][0] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 3
        if map[2][2] == player and map[2][0] == " ":
            if (map[2][1] == " " and map[1][0] == " ") or (map[2][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 7
        elif map[2][2] == " " and map[2][0] == player:
            if (map[2][1] == " " and map[1][0] == " ") or (map[2][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 9
        if map[0][2] == " " and map[1][1] == player:
            if (map[0][1] == " " and map[2][2] == " ") or (map[0][1] == " " and map[2][0] == " ") or (map[2][2] == " " and map[2][0] == " "):
                forkPosition = 3
        if map[2][0] == " " and map[1][1] == player:
            if (map[1][0] == " " and map[2][2] == " ") or (map[1][0] == " " and map[0][2] == " ") or (map[2][2] == " " and map[0][2] == " "):
                forkPosition = 7
    if map[0][2] == player:
        if map[0][0] == player and map[2][2] == " ":
            if (map[0][1] == " " and map[1][2] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][2] == " " and map[1][1] == " "):
                forkPosition = 9
        elif map[0][0] == " " and map[2][2] == player:
            if (map[0][1] == " " and map[1][2] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][2] == " " and map[1][1] == " "):
                forkPosition = 1
        if map[2][2] == player and map[2][0] == " ":
            if (map[1][1] == " " and map[1][2] == " ") or (map[1][1] == " " and map[2][1] == " ") or (map[1][2] == " " and map[2][1] == " "):
                forkPosition = 7
        elif map[2][2] == " " and map[2][0] == player:
            if (map[1][1] == " " and map[1][2] == " ") or (map[1][1] == " " and map[2][1] == " ") or (map[1][2] == " " and map[2][1] == " "):
                forkPosition = 9
        if map[0][0] == player and map[2][0] == " ":
            if (map[0][1] == " " and map[1][0] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 7
        elif map[0][0] == " " and map[2][0] == player:
            if (map[0][1] == " " and map[1][0] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 1
        if map[2][2] == " " and map[1][1] == player:
            if (map[0][0] == " " and map[2][0] == " ") or (map[0][0] == " " and map[1][2] == " ") or (map[1][2] == " " and map[2][0] == " "):
                forkPosition = 9
        if map[0][0] == " " and map[1][1] == player:
            if (map[2][0] == " " and map[2][2] == " ") or (map[0][1] == " " and map[2][2] == " ") or (map[2][0] == " " and map[0][1] == " "):
                forkPosition = 1
    if map[2][0] == player:
        if map[0][0] == player and map[2][2] == " ":
            if (map[1][0] == " " and map[2][1] == " ") or (map[1][0] == " " and map[1][1] == " ") or (map[2][1] == " " and map[1][1] == " "):
                forkPosition = 9
        elif map[0][0] == " " and map[2][2] == player:
            if (map[1][0] == " " and map[2][1] == " ") or (map[1][0] == " " and map[1][1] == " ") or (map[2][1] == " " and map[1][1] == " "):
                forkPosition = 1
        if map[2][2] == player and map[0][2] == " ":
            if (map[1][1] == " " and map[1][2] == " ") or (map[1][1] == " " and map[2][1] == " ") or (map[1][2] == " " and map[2][1] == " "):
                forkPosition = 3
        elif map[2][2] == " " and map[0][2] == player:
            if (map[1][1] == " " and map[1][2] == " ") or (map[1][1] == " " and map[2][1] == " ") or (map[1][2] == " " and map[2][1] == " "):
                forkPosition = 9
        if map[0][0] == player and map[0][2] == " ":
            if (map[0][1] == " " and map[1][0] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 3
        elif map[0][0] == " " and map[0][2] == player:
            if (map[0][1] == " " and map[1][0] == " ") or (map[0][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 1
        if map[2][2] == " " and map[1][1] == player:
            if (map[0][0] == " " and map[2][1] == " ") or (map[0][0] == " " and map[0][2] == " ") or (map[0][2] == " " and map[2][1] == " "):
                forkPosition = 9
        if map[0][0] == " " and map[1][1] == player:
            if (map[1][0] == " " and map[2][2] == " ") or (map[0][2] == " " and map[2][2] == " ") or (map[1][0] == " " and map[0][2] == " "):
                forkPosition = 1
    if map[2][2] == player:
        if map[2][0] == player and map[0][2] == " ":
            if (map[1][2] == " " and map[2][1] == " ") or (map[1][2] == " " and map[1][1] == " ") or (map[2][1] == " " and map[1][1] == " "):
                forkPosition = 3
        elif map[2][0] == " " and map[0][2] == player:
            if (map[1][2] == " " and map[2][1] == " ") or (map[1][2] == " " and map[1][1] == " ") or (map[2][1] == " " and map[1][1] == " "):
                forkPosition = 7
        if map[0][0] == player and map[0][2] == " ":
            if (map[1][1] == " " and map[1][2] == " ") or (map[1][1] == " " and map[0][1] == " ") or (map[1][2] == " " and map[0][1] == " "):
                forkPosition = 3
        elif map[0][0] == " " and map[0][2] == player:
            if (map[1][1] == " " and map[1][2] == " ") or (map[1][1] == " " and map[0][1] == " ") or (map[1][2] == " " and map[0][1] == " "):
                forkPosition = 1
        if map[0][0] == player and map[2][0] == " ":
            if (map[2][1] == " " and map[1][0] == " ") or (map[2][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 7
        elif map[0][0] == " " and map[2][0] == player:
            if (map[2][1] == " " and map[1][0] == " ") or (map[2][1] == " " and map[1][1] == " ") or (map[1][0] == " " and map[1][1] == " "):
                forkPosition = 1
        if map[0][2] == " " and map[1][1] == player:
            if (map[0][0] == " " and map[1][2] == " ") or (map[0][0] == " " and map[2][0] == " ") or (map[1][2] == " " and map[2][0] == " "):
                forkPosition = 3
        if map[2][0] == " " and map[1][1] == player:
            if (map[0][0] == " " and map[2][1] == " ") or (map[0][0] == " " and map[0][2] == " ") or (map[2][1] == " " and map[0][2] == " "):
                forkPosition = 7

    return forkPosition


#Checks if there is an unblocked winning combination still present and returns one of the probable winning position
def GetNextBestMove():
    turnOver = False
    if map[1][1] == turn and map[0][0] == " " and map[2][2] == " ":
        turnOver = GenerateRandomPosition([1,9]) #Both the corners 1,9 are not filled and there is a chance of winning in later move if next move is placed in one of them
    elif map[1][1] == turn and map[0][2] == " " and map[2][0] == " ":
        turnOver = GenerateRandomPosition([3,7])
    elif map[1][1] == turn and map[0][1]== " " and map[2][1] == " ":
        turnOver = GenerateRandomPosition([2,8])
    elif map[1][1] == turn and map[1][2]== " " and map[1][2] == " ":
        turnOver = GenerateRandomPosition([4,6])
    elif map[0][0] == turn and map[1][0] == " " and map[2][0] == " ":
        turnOver = GenerateRandomPosition([4,7])
    elif map[0][0] == turn and map[0][1] == " " and map[0][2] == " ":
        turnOver = GenerateRandomPosition([2,3])
    elif map[0][0] == turn and map[1][1] == " " and map[2][2] == " ":
        turnOver = GenerateRandomPosition([5,9])
    elif map[0][1] == turn and map[0][0] == " " and map[0][2] == " ":
        turnOver = GenerateRandomPosition([1,3])
    elif map[0][1] == turn and map[1][1] == " " and map[2][1] == " ":
        turnOver = GenerateRandomPosition([5,8])
    elif map[0][2] == turn and map[0][0] == " " and map[0][1] == " ":
        turnOver = GenerateRandomPosition([1,2])
    elif map[0][2] == turn and map[1][2] == " " and map[2][2] == " ":
        turnOver = GenerateRandomPosition([6,9])
    elif map[0][2] == turn and map[1][1] == " " and map[2][0] == " ":
        turnOver = GenerateRandomPosition([5,7])
    elif map[1][2] == turn and map[0][2] == " " and map[2][2] == " ":
        turnOver = GenerateRandomPosition([3,9])
    elif map[1][2] == turn and map[1][1] == " " and map[1][0] == " ":
        turnOver = GenerateRandomPosition([4,5])
    elif map[2][2] == turn and map[0][2] == " " and map[1][2] == " ":
        turnOver = GenerateRandomPosition([3,6])
    elif map[2][2] == turn and map[2][0] == " " and map[2][1] == " ":
        turnOver = GenerateRandomPosition([7,8])
    elif map[2][2] == turn and map[1][1] == " " and map[0][0] == " ":
        turnOver = GenerateRandomPosition([1,5])
    elif map[2][1] == turn and map[2][0] == " " and map[2][1] == " ":
        turnOver = GenerateRandomPosition([7,9])
    elif map[2][1] == turn and map[1][1] == " " and map[0][1] == " ":
        turnOver = GenerateRandomPosition([2,5])
    elif map[2][0] == turn and map[2][1] == " " and map[2][2] == " ":
        turnOver = GenerateRandomPosition([8,9])
    elif map[2][0] == turn and map[0][0] == " " and map[1][0] == " ":
        turnOver = GenerateRandomPosition([1,4])
    elif map[2][0] == turn and map[1][1] == " " and map[0][2] == " ":
        turnOver = GenerateRandomPosition([3,5])
    elif map[1][0] == turn and map[0][0] == " " and map[2][0] == " ":
        turnOver = GenerateRandomPosition([1,7])
    elif map[1][0] == turn and map[1][1] == " " and map[1][2] == " ":
        turnOver = GenerateRandomPosition([5,6])

    return turnOver;



#Generates the best moves for the computer
def MoveGenerator():
    global firstMove
    global secondMove
    global done

    #The first move depends on who starts first
    if firstMove == True:
        GenerateFirstMove()
        firstMove = False        
    #For all the other moves
    else:
        #Check for second move if computer starts first
        if turn == "X" and secondMove == True:
            secondMove = False
            secondMovePlayed = GetOppositeCornerSecondMove()
            if secondMovePlayed == True:
                return
            
        #Check if the computer has chance of winning
        winningPos = CheckForGame(turn)

        #Checks if the user has chance of winning and stores the position to block it
        blockingPos = CheckForGame(human)

        if winningPos != 0:
            X,Y = GetBoardIndices(winningPos)
            if map[Y][X] == " ":
                map[Y][X] = turn

        #Check if the user has a chance of winning. If yes, block that.
         #(Not checking for Fork since the assignment instruction says that the program can block either 
         #in case of fork and I'm choosing to block the first detected winning position)
        elif blockingPos != 0:
            X,Y = GetBoardIndices(blockingPos)
            if map[Y][X] == " ":
                map[Y][X] = turn

        #Check if the center of the board is not filled. If yes, then computer places in the center
        elif map[1][1] == " ":
            map[1][1] = turn

        else:
            #Check if the computer can create a fork
            forkPos = GetForkPosition(turn)
            userForkPos = GetForkPosition(human)
            if forkPos != 0:
                X,Y = GetBoardIndices(forkPos)
                if map[Y][X] == " ":
                    map[Y][X] = turn

            #Check if the user has a chance of creating a fork, block that
            elif userForkPos != 0:
                X,Y = GetBoardIndices(userForkPos)
                if map[Y][X] == " ":
                    map[Y][X] = turn

            else:
                #If there is no winning or blocking position and no forks can be created, get the best move where there is a chance of winning
                nextMoveDone = GetNextBestMove()

                #If none of the best moves are available, then generate a random move
                if nextMoveDone == False:
                    while True:
                        newPos = random.randint(0,8) + 1
                        X,Y = GetBoardIndices(newPos)
                        if map[Y][X] == " ":
                            map[Y][X] = turn
                            break

        done = check_done()
    SwapTurn()


#Global variables - 'turn' keeps track of the current players symbol; 'map' keeps track of the board;
# 'done' tracks the game status; 'firstMove' is to track the first move of the computer; 'currentPlayer' determines the current player (0- Human, 1 - Computer)
# 'human' stores the turn of the user
turn = "X"
map = [[" "," "," "],
       [" "," "," "],
       [" "," "," "]]
done = False
firstMove = True
secondMove = True
currentPlayer = 1
human = "X"
lastUserMove = 0


#Takes the input from the user. The program loops until a valid input is entered
validInput = False
while validInput != True:
    try:
        human = raw_input("Please select your turn - X or O: ").upper()
        if human == "X" or human == "O":
            validInput = True
            if(human == "X"):
                currentPlayer = 0
        else:
            print "Please select a valid turn."
    except:
        print "Please select a valid turn."


#Logic to call appropriate methods based on turns. This loops until there is a winner or the board is full
while done != True:
    print_board()
    print

    #If the current turn is computer's turn, MoveGenerator() method is called
    if(currentPlayer == 1):
        print "Computer's Turn"
        print
        MoveGenerator()
        currentPlayer -= 1

    #If the current turn is human's turn, MakeAMove() method is called
    else:
        print "Your Turn"
        print
        MakeAMove()
        currentPlayer += 1
