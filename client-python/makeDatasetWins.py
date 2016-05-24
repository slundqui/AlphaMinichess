from chess import *
from util import *
import time
import numpy as np
import random

#Here, an epoch is generated from one game
epochs = 10000

#How to initialize the board. Either random or through alphabeta
abDepth = 3 #Depth of alphabeta to train on

outDataFilename= "trainWinDataset/mlpData.npy"
outGTFilename= "trainWinDataset/mlpGt.npy"

#We store only index for space, will expand when read
trainData = None
trainGT = None

#Setting MLP usage
setMLPEval(True)

lossCost = float(1)/80
tieCost = -float(1)/8

for e in range(epochs):
    print "Epoch", e, "out of", epochs
    #Reset game
    chess_reset()
    #Play a game
    while(chess_winner() == "?"):
        #We give advantage to one player to avoid ties
        if(getWhosTurn() == "W"):
            chess_moveAlphabeta(abDepth-1, 400000)
        else:
            chess_moveAlphabeta(abDepth, 400000)

    #Get turn number
    totalTurns = getTurnNum() * 2
    #Get move stack
    moveHistory = getHistory()

    winner = chess_winner()

    #For every move in history, we get the board and value
    #This is always with respect to the white side
    #So for every black turn, we flip board around y and swap black for white
    offset = len(moveHistory)
    tmpDataArray = np.zeros((2*offset, 6, 5))
    tmpGtArray = np.zeros((2*offset))


    chess_reset()
    for i, (drop, src, drop, dst) in enumerate(moveHistory):
        #Get whos turn before move
        whosTurn = getWhosTurn()
        moveStr = idxToMove(src) + "-" + idxToMove(dst) + "\n"
        #Move piece
        chess_move(moveStr)
        #Get board and translate
        board = getBoard()
        #Make both board positions

        if whosTurn == "B":
            #Reverse y axis
            board = board[::-1]
            tmpDataArray[i,:,:] = np.array([[pieceToIdx[c.swapcase()] for c in r] for r in board])
            subMult = totalTurns - i + 1
            #Winner
            if(winner == "B"):
                tmpGtArray[i] = 1 - (subMult * lossCost)
            #Tie
            elif(winner == "="):
                tmpGtArray[i] = tieCost * (float(i)/totalTurns)
            #Loser
            else:
                tmpGtArray[i] = -(1 - (subMult * lossCost))

            #Make another set based on reverse of board
            tmpDataArray[i+offset,:,:] = np.array([[pieceToIdx[c] for c in r] for r in board])
            #Winner
            if(winner == "W"):
                tmpGtArray[i+offset] = 1 - (subMult * lossCost)
            #Tie
            elif(winner == "="):
                tmpGtArray[i+offset] = tieCost * (float(i)/totalTurns)
            #Loser
            else:
                tmpGtArray[i+offset] = -(1 - (subMult * lossCost))

        else:
            tmpDataArray[i,:,:] = np.array([[pieceToIdx[c] for c in r] for r in board])
            subMult = totalTurns - i + 1
            #Winner
            if(winner == "W"):
                tmpGtArray[i] = 1 - (subMult * lossCost)
            #Tie
            elif(winner == "="):
                tmpGtArray[i] = tieCost * (float(i)/totalTurns)
            #Loser
            else:
                tmpGtArray[i] = -(1 - (subMult * lossCost))

            #Make another set based on reverse of board
            #Reverse y axis
            board = board[::-1]
            tmpDataArray[offset+i,:,:] = np.array([[pieceToIdx[c.swapcase()] for c in r] for r in board])
            subMult = totalTurns - i + 1
            #Winner
            if(winner == "B"):
                tmpGtArray[i+offset] = 1 - (subMult * lossCost)
            #Tie
            elif(winner == "="):
                tmpGtArray[i+offset] = tieCost * (float(i)/totalTurns)
            #Loser
            else:
                tmpGtArray[i+offset] = -(1 - (subMult * lossCost))

    #Concatenate to trainData and trainGT
    if(trainData == None):
        trainData = tmpDataArray
        trainGT = tmpGtArray
    else:
        trainData = np.concatenate((trainData, tmpDataArray), axis=0)
        trainGT = np.concatenate((trainGT, tmpGtArray), axis=0)

np.save(outDataFilename, trainData)
np.save(outGTFilename, trainGT)
