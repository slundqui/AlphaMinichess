from chess import *
from util import *
import time
import numpy as np

#Here, an epoch is generated from one game
epochs = 100

#How to initialize the board. Either random or through alphabeta
boardInit = "random" #"alphabeta"
#This is number of moves as defined by the board, such that it's always whites move after init
numInitMoves = 20
abDepth = 5 #Depth of alphabeta to train on

outDataFilename= "dataset/trainData.npy"
outGTFilename= "dataset/trainGT.npy"

#We store only index for space, will expand when read
trainData = None
trainGT = None

for e in range(epochs):
    print "Epoch", e
    #Reset game
    chess_reset()
    for i in range(numInitMoves):
        if boardInit == "random":
            chess_moveRandom()
        elif boardInit == "alphabeta":
            chess_moveAlphabeta(abDepth, 1000000)
        else:
            assert(0)
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
