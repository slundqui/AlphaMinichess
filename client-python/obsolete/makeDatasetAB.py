from chess import *
from util import *
import time
import numpy as np
import random

#Here, an epoch is generated from one game
epochs = 100

#How to initialize the board. Either random or through alphabeta
boardInit = "random"
#This is number of moves as defined by the board, such that it's always whites move after init
numInitMoves = 30
abDepth = 5 #Depth of alphabeta to train on
initDepth = 3

outDataFilename= "testDataset/r5Data_2.npy"
outGTFilename= "testDataset/r5GT_2.npy"

#We store only index for space, will expand when read
trainData = None
trainGT = None

for e in range(epochs):
    print "Epoch", e, "out of", epochs
    #Reset game
    chess_reset()
    #Numbers must be even to make sure dataset is always white
    randNum = random.randint(0, numInitMoves-1)
    for i in range(randNum):
        if boardInit == "random":
            chess_moveRandom()
            chess_moveRandom()
        elif boardInit == "alphabeta":
            chess_moveAlphabeta(initDepth, 1000000)
            chess_moveAlphabeta(initDepth, 1000000)
        else:
            assert(0)
    #If someone wins, skip
    if(chess_winner() != "?"):
        continue
    assert(getWhosTurn() == "W")

    #Generate moves and moveScores
    (moves, score) = evalMovesAlphabeta(abDepth)
    #Write score and state for each move
    tmpDataArray = np.zeros((len(moves), 6, 5))
    tmpGtArray = np.zeros((len(moves)))
    for i, move in enumerate(moves):
        chess_move(move)
        board = getBoard()
        chess_undo()
        #Change board values to index values
        tmpDataArray[i,:,:] = np.array([[pieceToIdx[c] for c in r] for r in board])
        tmpGtArray[i] = score[i]
    #Concatenate to trainData and trainGT
    if(trainData == None):
        trainData = tmpDataArray
        trainGT = tmpGtArray
    else:
        trainData = np.concatenate((trainData, tmpDataArray), axis=0)
        trainGT = np.concatenate((trainGT, tmpGtArray), axis=0)

np.save(outDataFilename, trainData)
np.save(outGTFilename, trainGT)
