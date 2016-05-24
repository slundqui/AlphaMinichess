import numpy as np
import pdb
from tfMLP import evalMLP
from chessData import chessObj

trainDataFile = [
        "trainDataset/ab5I2Data.npy",
        "trainDataset/ab5I3Data.npy",
        "trainDataset/ab5I3Data_2.npy",
        "trainDataset/rI5Data.npy",
        "trainDataset/r5Data_2.npy",
        ]
trainGtFile = [
        "trainDataset/ab5I2GT.npy",
        "trainDataset/ab5I3GT.npy",
        "trainDataset/ab5I3GT_2.npy",
        "trainDataset/rI5GT.npy",
        "trainDataset/r5GT_2.npy",
        ]
testDataFile = [
        "testDataset/rI5Data.npy",
        "testDataset/r5Data_2.npy",
        "testDataset/ab5I3Data.npy",
        ]
testGtFile = [
        "testDataset/rI5GT.npy",
        "testDataset/r5GT_2.npy",
        "testDataset/ab5I3GT.npy",
        ]

outputDir = "tfOutput/"
checkpointDir = "checkpoints/"
loadFile = True
loadFilename = checkpointDir + "/save_99.ckpt"

dataObj = chessObj(trainDataFile, trainGtFile, testDataFile, testGtFile)
print "NumTrain: ", dataObj.numTrainData
print "NumTest: ", dataObj.numTestData
tfObj = evalMLP(dataObj)

if(loadFile):
    tfObj.loadModel(loadFilename)
else:
    tfObj.initSess()

tfObj.writeSummary(outputDir)

numTrain = 1000
numEpoch = 100
batchSize = 256

for e in range(numEpoch):
    saveFile = checkpointDir + "/save_" + str(e) + ".ckpt"
    tfObj.trainModel(numTrain, saveFile, batchSize)
    tfObj.writeTestEval()

tfObj.closeSess()
