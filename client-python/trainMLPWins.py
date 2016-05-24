import numpy as np
import pdb
from tfMLP import evalMLP
from chessDataWins import chessObj

trainDataFile = [
        #"trainWinDataset/data.npy",
        #"trainWinDataset/data_2.npy",
        "trainWinDataset/data_3.npy",
        "trainWinDataset/mlpData.npy",
        ]
trainGtFile = [
        #"trainWinDataset/gt.npy",
        #"trainWinDataset/gt_2.npy",
        "trainWinDataset/gt_3.npy",
        "trainWinDataset/mlpGt.npy",
        ]
testDataFile = [
        #"testWinDataset/data.npy",
        "testWinDataset/data_2.npy",
        ]
testGtFile = [
        #"testWinDataset/gt.npy",
        "testWinDataset/gt_2.npy",
        ]

outputDir = "tfWinsOutput/"
checkpointDir = "checkpointsWins/"
loadFile = True
loadFilename = checkpointDir + "/saved/save.ckpt"

dataObj = chessObj(trainDataFile, trainGtFile, testDataFile, testGtFile)
print "NumTrain: ", dataObj.numTrainData
print "NumTest: ", dataObj.numTestData
tfObj = evalMLP(dataObj)

if(loadFile):
    tfObj.loadModel(loadFilename)
else:
    tfObj.initSess()

tfObj.writeSummary(outputDir)

numTrain = 100
numEpoch = 100
batchSize = 256

for e in range(numEpoch):
    saveFile = checkpointDir + "/save_" + str(e) + ".ckpt"
    tfObj.trainModel(numTrain, saveFile, batchSize)
    tfObj.writeTestEval()

tfObj.closeSess()
