import pdb
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

#For initializing weights and biases
#For initializing weights and biases
def weight_variable(shape, inName, inStd):
    initial = tf.truncated_normal_initializer(stddev=inStd)
    return tf.get_variable(inName, shape, initializer=initial)

def bias_variable(shape, inName, biasInitConst=.01):
   initial = tf.constant(biasInitConst, shape=shape, name=inName)
   return tf.Variable(initial)

def node_variable(shape, inName):
   return tf.placeholder("float", shape=shape, name=inName)

class evalMLP:
    #Initialize tf parameters here
    progress = 10
    learningRate = 1e-3
    timestep = 0
    inputShape = (6, 5, 13)

    def __init__(self, dataObj):
        #dataObj may be None, in which case we're in eval mode
        self.dataObj = dataObj
        self.sess = tf.Session()
        self.buildModel()

    def buildModel(self):
        numInputs = self.inputShape[0] * self.inputShape[1] * self.inputShape[2]
        with tf.name_scope("inputOps"):
            #Get convolution variables as placeholders
            self.inputBoard = node_variable([None, self.inputShape[0], self.inputShape[1], self.inputShape[2]], "inputBoard")
            inputFlat = tf.reshape(self.inputBoard, [-1, numInputs], name="inputFlat")
            self.gt = node_variable([None, 1], "gt")

        with tf.name_scope("FC1"):
            self.W_fc1 = weight_variable([5*6*13, 512], "w_fc1", 1e-3)
            self.B_fc1 = bias_variable([512], "b_fc1")
            self.h_fc1 = tf.nn.relu(tf.matmul(inputFlat, self.W_fc1, name="fc1") + self.B_fc1, "fc1_relu")

        with tf.name_scope("FC2"):
            self.W_fc2 = weight_variable([512, 128], "w_fc2", 1e-3)
            self.B_fc2 = bias_variable([128], "b_fc2")
            self.h_fc2 = tf.nn.relu(tf.matmul(self.h_fc1, self.W_fc2, name="fc2") + self.B_fc2, "fc3_relu")

        with tf.name_scope("FC3"):
            self.W_fc3 = weight_variable([128, 16], "w_fc3", 1e-3)
            self.B_fc3 = bias_variable([16], "b_fc3")
            self.h_fc3 = tf.nn.relu(tf.matmul(self.h_fc2, self.W_fc3, name="fc3") + self.B_fc3, "fc3_relu")

        #Finally, fc4 condenses into 1 output value
        with tf.name_scope("FC4"):
            self.W_fc4 = weight_variable([16, 1], "w_fc4", 1e-3)
            self.B_fc4 = bias_variable([1], "b_fc4")
            self.est = tf.tanh(tf.matmul(self.h_fc3, self.W_fc4, name="est") + self.B_fc4)

        #Define loss
        with tf.name_scope("loss"):
            self.loss = tf.reduce_mean(tf.square(self.gt - self.est))/2

        #Summaries
        tf.scalar_summary('l2 loss', self.loss)
        tf.histogram_summary('input', self.inputBoard)
        tf.histogram_summary('gt', self.gt)
        tf.histogram_summary('fc1', self.h_fc1)
        tf.histogram_summary('fc2', self.h_fc2)
        tf.histogram_summary('fc3', self.h_fc3)
        tf.histogram_summary('est', self.est)
        tf.histogram_summary('w_fc1', self.W_fc1)
        tf.histogram_summary('b_fc1', self.B_fc1)
        tf.histogram_summary('w_fc2', self.W_fc2)
        tf.histogram_summary('b_fc2', self.B_fc2)
        tf.histogram_summary('w_fc3', self.W_fc3)
        tf.histogram_summary('b_fc3', self.B_fc3)
        tf.histogram_summary('w_fc4', self.W_fc4)
        tf.histogram_summary('b_fc4', self.B_fc4)

        #Define optimizer
        self.optimizer = tf.train.AdamOptimizer(self.learningRate).minimize(self.loss)

        #Define saver
        self.saver = tf.train.Saver()

    def initSess(self):
        self.sess.run(tf.initialize_all_variables())

    def writeSummary(self, summaryDir):
        self.mergedSummary = tf.merge_all_summaries()
        self.train_writer = tf.train.SummaryWriter(summaryDir+"/train", self.sess.graph)
        self.test_writer = tf.train.SummaryWriter(summaryDir+"/test")

    def closeSess(self):
        self.sess.close()

    def trainModel(self, numSteps, saveFile, batchSize):
        #Define session
        for i in range(numSteps):
            #Get data from dataObj
            data = self.dataObj.getTrainData(batchSize)
            feedDict = {self.inputBoard: data[0], self.gt: data[1]}
            #Run optimizer
            self.sess.run(self.optimizer, feed_dict=feedDict)
            summary = self.sess.run(self.mergedSummary, feed_dict=feedDict)
            self.train_writer.add_summary(summary, self.timestep)
            self.timestep+=1
            if(i%self.progress == 0):
                print "Timestep ", self.timestep

        save_path = self.saver.save(self.sess, saveFile)
        print("Model saved in file: %s" % save_path)

    def writeTestEval(self):
        data = self.dataObj.getTestData()
        feedDict = {self.inputBoard: data[0], self.gt: data[1]}
        summary = self.sess.run(self.mergedSummary, feed_dict=feedDict)
        self.test_writer.add_summary(summary, self.timestep)

    def evalModel(self, inData):
        tfInVals = inData
        feedDict = {self.inputBoard: tfInVals}
        tfOutVals = self.est.eval(feed_dict=feedDict, session=self.sess)
        #Return output data
        return tfOutVals

    def loadModel(self, loadFile):
        self.saver.restore(self.sess, loadFile)
        print("Model %s loaded" % loadFile)

    #def saveModel(self, saveFile):
    #    #Save model


        #TO load:
        #saver.restore(sess, "/tmp/model.ckpt")
        #print("Model restored.")

