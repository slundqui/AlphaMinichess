#Has utility functions that both dataset making and training functions need

#A dictionary for translating character piece to numpy index
#Assuming numpy array is (6, 5, 13)
pieceToIdx = {
    ".": 0,
    "K": 1,
    "Q": 2,
    "N": 3,
    "B": 4,
    "R": 5,
    "P": 6,
    "k": 7,
    "q": 8,
    "n": 9,
    "b": 10,
    "r": 11,
    "p": 12
}
