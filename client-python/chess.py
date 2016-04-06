import random
import pdb

##########################################################

#Global variables
#Chess board is 6x5 board
#Initializing as all empty spaces
numY = 6
numX = 5
maxTurnsDraw = 40

g_board = [["." for i in range(numX)] for j in range(numY)]
g_turnNum = 1
g_whosTurn = "W"


# reset the state of the game / your internal variables - note that this function is highly dependent on your implementation
def chess_reset():
    #These global declarations are required if we're updating global variables
    global g_board
    global g_turnNum
    global g_whosTurn
    g_board = [['k', 'q', 'b', 'n', 'r'], ['p', 'p', 'p', 'p', 'p'], ['.', '.', '.', '.', '.'], ['.', '.', '.', '.', '.'], ['P', 'P', 'P', 'P', 'P'], ['R', 'N', 'B', 'Q', 'K']]
    g_turnNum = 1
    g_whosTurn = 'W'

# return the state of the game - one example is given below - note that the state has exactly 40 or 41 characters
def chess_boardGet():

    strOut = ''
    strOut += str(g_turnNum) + " " + g_whosTurn + "\n"
    #Rows first
    for y in range(numY):
        for x in range(numX):
            strOut += g_board[y][x]
        strOut += "\n"

    #strOut += 'kqbnr\n'
    #strOut += 'ppppp\n'
    #strOut += '.....\n'
    #strOut += '.....\n'
    #strOut += 'PPPPP\n'
    #strOut += 'RNBQK\n'

    return strOut


# read the state of the game from the provided argument and set your internal variables accordingly - note that the state has exactly 40 or 41 characters
def chess_boardSet(strIn):
    #These global declarations are required if we're updating global variables
    global g_board
    global g_turnNum
    global g_whosTurn

    #Split string by newline
    strSplit = strIn.split("\n")
    #First split contains turn number and whos turn it is
    firstSplit = strSplit[0].split(" ")
    g_turnNum = int(firstSplit[0])
    g_whosTurn = firstSplit[1]

    #Go through rest of splits to get board positions
    #Skipping first split since that's taken care of
    for (y, isplit) in enumerate(range(1, len(strSplit))):
        lineSplit = strSplit[isplit]
        #Loop through characters
        for (x, c) in enumerate(lineSplit):
            g_board[y][x] = c


# determine the winner of the current state of the game and return '?' or '=' or 'W' or 'B' - note that we are returning a character and not a string
def chess_winner():
    #If move number is greater than 40, the game is a draw
    if(g_turnNum > maxTurnsDraw):
        return '='

    #Check if a k or K DOES NOT exist on board
    #Capital letters are white, lowercase letters are black
    #Need to loop through y loop
    blackKFound = False
    whiteKFound = False
    for y in range(numY):
        if('k' in g_board[y]):
            blackKFound = True
        if('K' in g_board[y]):
            whiteKFound = True

    if(not blackKFound):
        return 'W'
    elif(not whiteKFound):
        return 'B'
    else:
        return '?'

def chess_isValid(intX, intY):
    if intX < 0:
        return False

    elif intX > 4:
        return False

    if intY < 0:
        return False

    elif intY > 5:
        return False

    return True


# with reference to the state of the game, return whether the provided argument is a piece from the side not on move - note that we could but should not use the other is() functions in here but probably
def chess_isEnemy(strPiece):
    assert(len(strPiece) == 1)
    #If white, black is enemy and vice versa
    if(g_whosTurn == "W"):
        if(strPiece.islower()):
            return True
        else:
            return False
    else:
        if(strPiece.isupper()):
            return True
        else:
            return False

# with reference to the state of the game, return whether the provided argument is a piece from the side on move - note that we could but should not use the other is() functions in here but probably
def chess_isOwn(strPiece):
    assert(len(strPiece) == 1)
    #If white, black is enemy and vice versa
    if(g_whosTurn == "W"):
        if(strPiece.isupper()):
            return True
        else:
            return False
    else:
        if(strPiece.islower()):
            return True
        else:
            return False


# return whether the provided argument is not a piece / is an empty field - note that we could but should not use the other is() functions in here but probably
def chess_isNothing(strPiece):
    assert(len(strPiece) == 1)
    if(strPiece == '.'):
        return True
    else:
        return False

def chess_eval():
    # with reference to the state of the game, return the the evaluation score of the side on move - note that positive means an advantage while negative means a disadvantage

    return 0


# with reference to the state of the game and return the possible moves - one example is given below - note that a move has exactly 6 characters
def chess_moves():
    strOut = []

    strOut.append('a2-a3\n')
    strOut.append('b2-b3\n')
    strOut.append('c2-c3\n')
    strOut.append('d2-d3\n')
    strOut.append('e2-e3\n')
    strOut.append('b1-a3\n')
    strOut.append('b1-c3\n')

    return strOut


def chess_movesShuffled():
    # with reference to the state of the game, determine the possible moves and shuffle them before returning them- note that you can call the chess_moves() function in here

    return []


def chess_movesEvaluated():
    # with reference to the state of the game, determine the possible moves and sort them in order of an increasing evaluation score before returning them - note that you can call the chess_moves() function in here

    return []


def chess_move(strIn):
    # perform the supplied move (for example 'a5-a4\n') and update the state of the game / your internal variables accordingly - note that it advised to do a sanity check of the supplied move

    pass


def chess_moveRandom():
    # perform a random move and return it - one example output is given below - note that you can call the chess_movesShuffled() function as well as the chess_move() function in here

    return 'a2-a3\n'


def chess_moveGreedy():
    # perform a greedy move and return it - one example output is given below - note that you can call the chess_movesEvaluated() function as well as the chess_move() function in here

    return 'a2-a3\n'


def chess_moveNegamax(intDepth, intDuration):
    # perform a negamax move and return it - one example output is given below - note that you can call the the other functions in here

    return 'a2-a3\n'


def chess_moveAlphabeta(intDepth, intDuration):
    # perform a alphabeta move and return it - one example output is given below - note that you can call the the other functions in here

    return 'a2-a3\n'


def chess_undo():
    # undo the last move and update the state of the game / your internal variables accordingly - note that you need to maintain an internal variable that keeps track of the previous history for this

    pass
