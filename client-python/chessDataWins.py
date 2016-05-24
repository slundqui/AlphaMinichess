import numpy as np
import pdb
from random import shuffle

def expandData(inData):
    if(inData.ndim == 2):
        shape = (6, 5, 13)
        outData = np.zeros(shape)
        for i in range(6):
            for j in range(5):
                outData[i, j, inData[i, j]] = 1
    elif(inData.ndim == 3):
        shape = (inData.shape[0], 6, 5, 13)
        outData = np.zeros(shape)
        for b in range(inData.shape[0]):
            for i in range(6):
                for j in range(5):
                    outData[b, i, j, inData[b, i, j]] = 1
    else:
        assert(0)
    return outData

class chessObj:
    inputShape = (6, 5, 13)

    def __init__(self, trainDataFile, trainGtFile, testDataFile, testGtFile):
        self.trainData = np.load(trainDataFile[0])
        self.trainGt = np.load(trainGtFile[0])[:, None].astype(float)
        self.testData = np.load(testDataFile[0])
        self.testGt = np.load(testGtFile[0])[:, None].astype(float)

        for iTrain in range(1, len(trainDataFile)):
            self.trainData = np.concatenate((self.trainData, np.load(trainDataFile[iTrain])), axis=0)
            self.trainGt = np.concatenate((self.trainGt, np.load(trainGtFile[iTrain])[:, None].astype(float)), axis=0)

        for iTest in range(1, len(testDataFile)):
            self.testData = np.concatenate((self.testData, np.load(testDataFile[iTest])), axis=0)
            self.testGt = np.concatenate((self.testGt, np.load(testGtFile[iTest])[:, None].astype(float)), axis=0)

        assert(len(self.trainData) == len(self.trainGt))
        assert(len(self.testData) == len(self.testGt))
        self.numTrainData = len(self.trainData)
        self.numTestData = len(self.testData)
        self.dataIdx = 0
        self.genShuffle()

    def genShuffle(self):
        #Generate shuffled index based on how many segments
        self.shuffleIdx = range(self.numTrainData)
        shuffle(self.shuffleIdx)

    #Crop image based on segments, give a label, and return both
    def nextData(self, shuffleIdx=True):
        if(shuffleIdx):
           nextIdx = self.shuffleIdx[self.dataIdx]
        else:
           nextIdx = self.dataIdx

        data = expandData(self.trainData[nextIdx, :, :])
        gt = self.trainGt[nextIdx, :]

        #Update dataIdx, and check if we to rewind
        self.dataIdx += 1
        if(self.dataIdx >= self.numTrainData):
            print "End of data, rewinding"
            self.genShuffle()
            self.dataIdx = 0
        return (data, gt)

    #Get all segments of current image
    def getTestData(self):
       return (expandData(self.testData), self.testGt)

    def getTrainData(self, numExample):
        outData = np.zeros((numExample, self.inputShape[0], self.inputShape[1], self.inputShape[2]))
        outGt = np.zeros((numExample, 1))
        for i in range(numExample):
            data = self.nextData()
            outData[i, :, :, :] = data[0]
            outGt[i, :] = data[1]
        return (outData, outGt)

