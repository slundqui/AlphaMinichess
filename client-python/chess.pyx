import random
import pdb

##########################################################

#Debug variable, turn off for speed
DEBUG = True

#Parameters
#Chess board is 6x5 board
numY = 6
numX = 5
maxTurnsDraw = 40

#Defines the score for each piece.
#Note that since the game is symetrical, only lowercase pieces are evaluated
#Range goes from 1 to 100 with the exception of the king
#TODO, adjust this with maybe the positions of each piece as well
pieceToPoint= {
    'k': 10000,
    'q': 10,
    'b': 4,
    'n': 4,
    'r': 5,
    'p': 1
}

#Global state variables
#Initializing as all empty spaces
g_board = [["." for i in range(numX)] for j in range(numY)]
g_turnNum = 1
g_whosTurn = "W"

#Data structure for storing history of moves
g_moveHistory = []

#Function to return point diff for moving into "move"
def getPointDiff(move):
    if(isEmpty(move)):
        return 0
    elif(isEnemy(move)):
        return pieceToPoint[g_board[move[0]][move[1]].lower()]
    else:
        #Illegal move
        assert(0)

#Function to change from a string to an index, e.g. a1 to (5, 0)
def moveToIdx(inStr):
    if(DEBUG):
        assert(len(inStr) == 2)
    #Note that the matrix is indexed by row first then column
    #whereas the instring is indexed by column first than row
    #Additionally, rows are labeled from bottom to top in string,
    #but from top to bottom in matrix format

    #This works out since inStr is 1 indexed.
    yIdx = numY - int(inStr[1])
    #Ord changes a letter to the corresponding ascii number, with an offset of 97
    xIdx = ord(inStr[0]) - 97

    return (yIdx, xIdx)

#Function to change from an index to a string, e.g. (5, 0) to a1
def idxToMove(inMove):
    if(DEBUG):
        assert(len(inMove) == 2)
    (yIdx, xIdx) = inMove
    strLabel = chr(xIdx + ord('a'))
    numLabel = str(numY - yIdx)
    return strLabel + numLabel

# reset the state of the game / your internal variables - note that this function is highly dependent on your implementation
def chess_reset():
    #These global declarations are required if we're updating global variables
    global g_board
    global g_turnNum
    global g_whosTurn
    global g_moveHistory
    #Lowercase is black, uppercase is white
    g_board = [['k', 'q', 'b', 'n', 'r'],
               ['p', 'p', 'p', 'p', 'p'],
               ['.', '.', '.', '.', '.'],
               ['.', '.', '.', '.', '.'],
               ['P', 'P', 'P', 'P', 'P'],
               ['R', 'N', 'B', 'Q', 'K']]
    g_turnNum = 1
    g_whosTurn = 'W'
    g_moveHistory = []

# return the state of the game - one example is given below - note that the state has exactly 40 or 41 characters
def chess_boardGet():
    strOut = ''
    strOut += str(g_turnNum) + " " + g_whosTurn + "\n"
    #Rows first
    for y in range(numY):
        for x in range(numX):
            strOut += g_board[y][x]
        strOut += "\n"

    return strOut


# read the state of the game from the provided argument and set your internal variables accordingly - note that the state has exactly 40 or 41 characters
def chess_boardSet(strIn):
    #These global declarations are required if we're updating global variables
    global g_board
    global g_turnNum
    global g_whosTurn
    global g_moveHistory

    #Clear boardSet
    g_moveHistory = []

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
        winner = 'W'
    elif(not whiteKFound):
        winner = 'B'
    else:
        winner = '?'

    #If move number is greater than 40, the game is a draw
    if(g_turnNum > maxTurnsDraw and winner == "?"):
        return '='
    else:
        return winner


#Various wrapper functions for taking tuples as moves
def isValid(move):
    return chess_isValid(move[1], move[0])
def isEmpty(move):
    return chess_isNothing(g_board[move[0]][move[1]])
def isOwn(move):
    return chess_isOwn(g_board[move[0]][move[1]])
def isEnemy(move):
    return chess_isEnemy(g_board[move[0]][move[1]])

def chess_isValid(intX, intY):
    if intX < 0:
        return False
    elif intX > numX-1:
        return False
    if intY < 0:
        return False
    elif intY > numY-1:
        return False
    return True


# with reference to the state of the game, return whether the provided argument is a piece from the side not on move - note that we could but should not use the other is() functions in here but probably
def chess_isEnemy(strPiece):
    if(DEBUG):
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
    if(DEBUG):
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
    if(DEBUG):
        assert(len(strPiece) == 1)
    if(strPiece == '.'):
        return True
    else:
        return False

# with reference to the state of the game, return the the evaluation score of the side on move - note that positive means an advantage while negative means a disadvantage
def chess_eval():
    evalScore = int(0) #API requires this value to be an integer
    #Eval is associated with the remaining pieces left in the game
    #Depending on who's turn it is
    for i in range(numY):
        for pieceVal in g_board[i]:
            #Check for empty space first
            if(chess_isNothing(pieceVal)):
                pass
            #We subtract from the score for every enemy piece, and vice versa
            elif(chess_isOwn(pieceVal)):
                evalScore += pieceToPoint.get(pieceVal.lower())
            elif(chess_isEnemy(pieceVal)):
                evalScore -= pieceToPoint.get(pieceVal.lower())
            else:
                #Sanity check
                assert(0)
    #Score is the absence of pieces
    return evalScore

#Code for tracing rays given a direction
def generateRayMoves(startPos, rayDirection):
    (yDiff, xDiff) = rayDirection
    (yPos, xPos) = startPos
    outPos = []
    while(True):
        #Update new position
        yPos = yPos + yDiff
        xPos = xPos + xDiff
        #If new position is not valid, break
        if(not isValid((yPos, xPos))):
            break
        #If empty, add and continue loop
        if(isEmpty((yPos, xPos))):
            outPos.append((yPos, xPos))
        #If enemy, add current position and break
        elif(isEnemy((yPos, xPos))):
            outPos.append((yPos, xPos))
            break
        #Otherwise, own piece. Break
        else:
            break
    return outPos

#Generates moves for piece inVal at position pos
def generateValidMoves(inVal, pos):
    if DEBUG:
        assert(chess_isOwn(inVal))
        assert(isOwn(pos))

    posOutputs = []
    (yPos, xPos) = pos

    #Pawns
    if(inVal == 'p' or inVal == 'P'):
        #Black pawns
        if(inVal == 'p'):
            yDiff = 1
        #White pawns
        else:
            yDiff = -1

        #Black pawns can move vertically by 1
        move = (yPos + yDiff, xPos)
        #Python is short-circuit, so checking for validity
        #first will not execute second statement
        if(isValid(move) and isEmpty(move)):
            posOutputs.append(move)

        #capture diagonally
        move = (yPos + yDiff, xPos + 1)
        if(isValid(move) and isEnemy(move)):
            posOutputs.append(move)

        move = (yPos + yDiff, xPos - 1)
        if(isValid(move) and isEnemy(move)):
            posOutputs.append(move)

    #Kings
    elif(inVal == 'k' or inVal == 'K'):
        for yDiff in range(-1, 2, 1):
            for xDiff in range(-1, 2, 1): #Skip the case where both yDiff and xDiff is 0
                if(yDiff == 0 and xDiff == 0):
                    continue
                move = (yPos + yDiff, xPos + xDiff)
                if(isValid(move) and (isEmpty(move) or isEnemy(move))):
                    posOutputs.append(move)

    #Queens
    elif(inVal == 'q' or inVal == 'Q'):
        #Left
        posOutputs.extend(generateRayMoves(pos, (0, -1)))
        #Right
        posOutputs.extend(generateRayMoves(pos, (0, 1)))
        #Up
        posOutputs.extend(generateRayMoves(pos, (-1, 0)))
        #Down
        posOutputs.extend(generateRayMoves(pos, (1, 0)))
        #UpLeft
        posOutputs.extend(generateRayMoves(pos, (-1, -1)))
        #UpRight
        posOutputs.extend(generateRayMoves(pos, (-1, 1)))
        #DownLeft
        posOutputs.extend(generateRayMoves(pos, (1, -1)))
        #DownRight
        posOutputs.extend(generateRayMoves(pos, (1, 1)))

    #Bishops
    elif(inVal == 'b' or inVal == 'B'):
        #UpLeft
        posOutputs.extend(generateRayMoves(pos, (-1, -1)))
        #UpRight
        posOutputs.extend(generateRayMoves(pos, (-1, 1)))
        #DownLeft
        posOutputs.extend(generateRayMoves(pos, (1, -1)))
        #DownRight
        posOutputs.extend(generateRayMoves(pos, (1, 1)))
        #Additional rule for moving one spot to the left/right/up/down
        #Can't capture piece moving that direction
        #Up
        move = (yPos - 1, xPos)
        if(isValid(move) and (isEmpty(move))):
            posOutputs.append(move)
        #Down
        move = (yPos + 1, xPos)
        if(isValid(move) and (isEmpty(move))):
            posOutputs.append(move)
        #Left
        move = (yPos, xPos - 1)
        if(isValid(move) and (isEmpty(move))):
            posOutputs.append(move)
        #Right
        move = (yPos, xPos + 1)
        if(isValid(move) and (isEmpty(move))):
            posOutputs.append(move)

    #Rook
    elif(inVal == 'r' or inVal == 'R'):
        #Left
        posOutputs.extend(generateRayMoves(pos, (0, -1)))
        #Right
        posOutputs.extend(generateRayMoves(pos, (0, 1)))
        #Up
        posOutputs.extend(generateRayMoves(pos, (-1, 0)))
        #Down
        posOutputs.extend(generateRayMoves(pos, (1, 0)))

    #Knight
    elif(inVal == 'n' or inVal == 'N'):
        #L shapes
        #Top Left
        move = (yPos-1, xPos-2)
        if(isValid(move) and (isEmpty(move) or isEnemy(move))):
            posOutputs.append(move)
        move = (yPos-2, xPos-1)
        if(isValid(move) and (isEmpty(move) or isEnemy(move))):
            posOutputs.append(move)

        #Top Right
        move = (yPos-1, xPos+2)
        if(isValid(move) and (isEmpty(move) or isEnemy(move))):
            posOutputs.append(move)
        move = (yPos-2, xPos+1)
        if(isValid(move) and (isEmpty(move) or isEnemy(move))):
            posOutputs.append(move)

        #Bottom Left
        move = (yPos+1, xPos-2)
        if(isValid(move) and (isEmpty(move) or isEnemy(move))):
            posOutputs.append(move)
        move = (yPos+2, xPos-1)
        if(isValid(move) and (isEmpty(move) or isEnemy(move))):
            posOutputs.append(move)

        #Bottom Right
        move = (yPos+1, xPos+2)
        if(isValid(move) and (isEmpty(move) or isEnemy(move))):
            posOutputs.append(move)
        move = (yPos+2, xPos+1)
        if(isValid(move) and (isEmpty(move) or isEnemy(move))):
            posOutputs.append(move)
    return posOutputs

# with reference to the state of the game and return the possible moves - one example is given below - note that a move has exactly 6 characters
def chess_moves():
    strOut = []
    #Loop through pieces
    for yIdx in range(numY):
        for xIdx, pieceVal in enumerate(g_board[yIdx]):
            #Generate list of moves per own piece
            if(chess_isOwn(pieceVal)):
                movesList = generateValidMoves(pieceVal, (yIdx, xIdx))
                for move in movesList:
                    moveStr = idxToMove((yIdx, xIdx)) + "-" + idxToMove(move) + "\n"
                    strOut.append(moveStr)
    return strOut


# with reference to the state of the game, determine the possible moves and shuffle them before returning them- note that you can call the chess_moves() function in here
def chess_movesShuffled():
    #Generate all possible moves
    movesList = chess_moves()
    #Shuffle and return
    random.shuffle(movesList)
    return movesList

# with reference to the state of the game, determine the possible moves and sort them in order of an increasing evaluation score before returning them - note that you can call the chess_movesShuffled() function in here
def chess_movesEvaluated():
    #Generate all possible moves, but we want to shuffle them in case there are ties
    movesList = chess_movesShuffled()
    #We calculate point differentials
    pointDiffList = [getPointDiff(moveToIdx(m[3:5])) for m in movesList]

    #Check for pawn promotions
    for (i, move) in enumerate(movesList):
        srcIdx = moveToIdx(move[0:2])
        dstIdx = moveToIdx(move[3:5])
        if((g_board[srcIdx[0]][srcIdx[1]] == 'p' and dstIdx[0] == numY-1) or #black pawn
           (g_board[srcIdx[0]][srcIdx[1]] == 'P' and dstIdx[0] == 0)): #White pawn
              #Point differential is any captures plus
              #losing a pawn and gaining a queen
              pointDiffList[i] += pieceToPoint['q'] - pieceToPoint['p']

    #We want to sort this list from largest (biggest capture) to smallest (smallest capture)
    #but we only want the indices
    sortIdx = [i[0] for i in sorted(enumerate(pointDiffList), key=lambda x:x[1], reverse=True)]
    #Return new movesList with sortIdx
    outList = [movesList[i] for i in sortIdx]

    return outList


# perform the supplied move (for example 'a5-a4\n') and update the state of the game / your internal variables accordingly - note that it advised to do a sanity check of the supplied move
def chess_move(strIn):
    #Updating global variables, so need these definitions
    global g_board
    global g_turnNum
    global g_whosTurn
    global g_moveHistory

    #Parse string for a src and target positions
    srcStr = strIn[0:2]
    dstStr = strIn[3:5]

    #Convert to index
    srcMove = moveToIdx(srcStr)
    dstMove = moveToIdx(dstStr)

    #Sanity checks
    if(DEBUG):
        #This breaks the system test for chess_movesEvaluated
        assert(isOwn(srcMove))
        moves = generateValidMoves(g_board[srcMove[0]][srcMove[1]], srcMove)
        assert(dstMove in moves)


    #Get source and dest pieces
    srcPiece = g_board[srcMove[0]][srcMove[1]]
    dstPiece = g_board[dstMove[0]][dstMove[1]]

    #Store move into stack
    #Stack element contains a 4 tuple: (srcPiece, srcMove, dstPiece, dstMove)
    g_moveHistory.append((srcPiece, srcMove, dstPiece, dstMove))

    #Move piece
    g_board[dstMove[0]][dstMove[1]] = srcPiece
    g_board[srcMove[0]][srcMove[1]] = '.'

    #Check for pawn promotions
    if(g_board[dstMove[0]][dstMove[1]] == 'p' and dstMove[0] == numY - 1):
        g_board[dstMove[0]][dstMove[1]] = 'q'
    elif(g_board[dstMove[0]][dstMove[1]] == 'P' and dstMove[0] == 0):
        g_board[dstMove[0]][dstMove[1]] = 'Q'

    #Update turnNum and whosTurn
    #Note that turnNum only increments after black's turn
    if(g_whosTurn == "W"):
        g_whosTurn = "B"
    else:
        g_whosTurn = "W"
        g_turnNum += 1

def chess_moveRandom():
    possMoves = chess_movesShuffled()
    if(len(possMoves)):
        targetMove = possMoves[0]
        chess_move(targetMove)
    else:
        targetMove = ""
    return targetMove

# perform a greedy move and return it - one example output is given below - note that you can call the chess_movesEvaluated() function as well as the chess_move() function in here
def chess_moveGreedy():
    possMoves = chess_movesEvaluated()
    if(len(possMoves)):
        targetMove = possMoves[0]
        chess_move(targetMove)
    else:
        targetMove = ""
    return targetMove

#Depth first search
def rec_negamax(depth):
    #If we run out of depth or winners, we evaluate the current board and return
    if(depth == 0 or chess_winner() != "?"):
        return chess_eval()
    score = -float("inf")
    moves = chess_movesEvaluated()
    for move in moves:
        chess_move(move)
        score = max(score, -rec_negamax(depth-1))
        chess_undo()
    return score

def chess_moveNegamax(intDepth, intDuration):
    # perform a negamax move and return it - one example output is given below - note that you can call the the other functions in here
    score = -float("inf")
    moves = chess_movesEvaluated()
    if(len(moves) == 0):
        return ""
    bestMove = moves[0]
    for move in moves:
        chess_move(move)
        recScore = -rec_negamax(intDepth-1)
        chess_undo()
        if(recScore > score):
            bestMove = move
            score = recScore
    chess_move(bestMove)
    return bestMove

def rec_alphabeta(depth, alpha, beta):
    #If we run out of depth or winners, we evaluate the current board and return
    if(depth == 0 or chess_winner() != "?"):
        return chess_eval()
    score = -float("inf")
    moves = chess_movesEvaluated()
    for move in moves:
        chess_move(move)
        score = max(score, -rec_alphabeta(depth-1, -beta, -alpha))
        chess_undo()
        alpha = max(alpha, score)
        if(alpha >= beta):
            break
    return score

def chess_moveAlphabeta(intDepth, intDuration):
    # perform a negamax move and return it - one example output is given below - note that you can call the the other functions in here
    score = -float("inf")
    moves = chess_movesEvaluated()
    if(len(moves) == 0):
        return ""
    bestMove = moves[0]
    for move in moves:
        chess_move(move)
        recScore = -rec_alphabeta(intDepth-1, -float("inf"), float("inf"))
        chess_undo()
        if(recScore > score):
            bestMove = move
            score = recScore
    chess_move(bestMove)
    return bestMove

# undo the last move and update the state of the game / your internal variables accordingly - note that you need to maintain an internal variable that keeps track of the previous history for this
def chess_undo():
    #Updating global variables, so need these definitions
    global g_board
    global g_turnNum
    global g_whosTurn
    global g_moveHistory
    if(len(g_moveHistory) == 0):
        #Do nothing
        return

    #Update turnNum and whosTurn
    #Note that turnNum only decrements after whites's turn
    if(g_whosTurn == "B"):
        g_whosTurn = "W"
    else:
        g_whosTurn = "B"
        g_turnNum -= 1

    #Pop move off stack
    (srcPiece, srcMove, dstPiece, dstMove) = g_moveHistory.pop()
    #Place srcPiece first, as srcMove is guarenteed to be currently '.'
    if DEBUG:
        assert(isEmpty(srcMove))
    g_board[srcMove[0]][srcMove[1]] = srcPiece
    g_board[dstMove[0]][dstMove[1]] = dstPiece

#if __name__ == "__main__":
#    chess_reset()
#    chess_move('a2-a3\n')
#    outStr = chess_moves()
#    print outStr
#    pdb.set_trace()

