from chess import *
import time

#Reset game
chess_reset()

#Start with time allowed in milliseconds
whiteTime = 300000
blackTime = 300000

#Set game seed for reporducability
#setSeed("11234234567890")

#Play until winner
while chess_winner() == "?":
    #Keep timer
    whosTurn = getWhosTurn()
    timeStart = time.clock()
    if(whosTurn == "W"):
        chess_moveAlphabeta(-1, whiteTime)
    elif(whosTurn == "B"):
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
        break
    if(blackTime <= 0):
        print "BLACK OUT OF TIME"
        break

    print boardState[:-1]
    print "timeTaken: ", timeE
    print "WHITETIME: ", whiteTime
    print "blacktime: ", blackTime, "\n"

print "Winner: ", chess_winner()
