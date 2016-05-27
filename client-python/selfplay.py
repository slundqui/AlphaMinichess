from chess import *
import time


numGames = 10
whiteWins = 0
blackWins = 0
whiteOutOfTime = 0
blackOutOfTime = 0
ties = 0

for g in range(numGames):

    #Reset game
    chess_reset()

    #Start with time allowed in milliseconds
    whiteTime = 300000
    blackTime = 300000

    #Play until winner
    while chess_winner() == "?":
        #Keep timer
        whosTurn = getWhosTurn()
        timeStart = time.clock()
        if(whosTurn == "W"):
            setMLPEval(False)
            chess_moveAlphabeta(-1, whiteTime)
        elif(whosTurn == "B"):
            setMLPEval(True)
            chess_moveAlphabeta(-1, blackTime)
        else:
            assert(0)
        timeStop = time.clock()
        #Find elapsted time in milliseconds
        timeE = (timeStop - timeStart)*1000
        boardState = chess_boardGet()
        whosTurn = getWhosTurn()

        #since we're updating the state in this, whos turn it is CURRENTLY determins whos timer to add
        #which should be opposite
        if(whosTurn == "W"):
            blackTime -= timeE
        elif(whosTurn == "B"):
            whiteTime -= timeE
        else:
            assert(0)

        if(whiteTime <= 0):
            print "WHITE OUT OF TIME"
            whiteOutOfTime += 1
            break
        if(blackTime <= 0):
            print "BLACK OUT OF TIME"
            blackOutOfTime += 1
            break

        print boardState[:-1]
        print "timeTaken: ", timeE
        print "WHITETIME: ", whiteTime
        print "blacktime: ", blackTime, "\n"

    winner = chess_winner()
    print "Winner: ", winner
    if(winner == "W"):
        whiteWins += 1
    elif(winner == "B"):
        blackWins += 1
    else:
        ties += 1

    print "White (no-mlp) wins: ", whiteWins
    print "Black (mlp) wins: ", blackWins
    print "White (no-mlp) out of time: ", whiteOutOfTime
    print "Black (mlp) out of time: ", blackOutOfTime
    print "Ties: ", ties

