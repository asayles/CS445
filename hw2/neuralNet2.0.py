import csv, sys, math
from optparse import OptionParser
from random import randint, shuffle
from pprint import pprint
from string import ascii_uppercase, find
#from sklearn import preprocessing
#import numpy as np


####################
# argparser:      ##
####################
parser = OptionParser()

parser.add_option("-e", dest="epochs", default=100,
                  help="number of epoch <int>. (default 100)")
                  
parser.add_option("-l", dest="learningRate", default=0.3,
                  help="learning rate <float>. (default 0.3)")

parser.add_option("-m", dest="momentum", default=0.3,
                  help="momentum <float>. (default 0.3)")

parser.add_option("-n",dest="hiddenNodes", default=4,
                  help="hiddenNodes <int>. (default 4)")

parser.add_option("--train", dest="trainingSet",
                  help="data file to train with <filename>")

parser.add_option("--test", dest="testSet",
                  help="data file to test with <filename>")

(options, args) = parser.parse_args()

if not options.trainingSet:
    parser.error("Need training set --train <filename>")
    
if not options.trainingSet:
    parser.error("Need test set --test <filename>")
    
#########################
# FUNCTIONS:           ##
#########################
def loadSet(File):
    with open(File, 'rb') as f:
        reader = csv.reader(f)
        rawSet = list(reader)
    return rawSet
    
    
    
# def preProcess(trainingSet):
#     X = trainingSet
#     X_scaled = preprocessing.scale(X)
#     return X_scaled
    

def getMean(trainingSet):
    numInstances = float(len(trainingSet)) #10,000
    featureMean = [] # init featureMean array
    for j in range(numFeatures):
        featureMean.append(0)
    for instance in trainingSet: # grab one instance
        features = instance[1:] # take off letter
        for i in range(numFeatures): # for each feature in feature set
            featureMean[i] += (float(features[i]) / numInstances) # add (feature / number of instances) to sum
    return featureMean


def getSDev(trainingSet, featureMean):
    numInstances = float(len(trainingSet)) #10,000
    featureVar = []
    featureStandardDev = []
    for p in range(numFeatures): # init some arrays
        featureVar.append(0)
        featureStandardDev.append(0)
    for instance in trainingSet: # grab an instance
        features = instance[1:] # take off the letter
        for i in range(numFeatures): # for each feature in feature set
            # add (distance from mean)^2 / number of instances, to total
            delta = float(features[i]) - featureMean[i]
            variance = math.pow(delta,2) / numInstances
            featureVar[i] += variance
    for i in range(numFeatures):
        featureStandardDev[i] = math.sqrt(featureVar[i])
    return featureStandardDev


def preProcess(trainingSet, featureMean, featureStandardDev):
    numInstances = len(trainingSet) #10,000 ish
    fullSet = []
    for instance in trainingSet:
        newInstance = instance
        for i in range(numFeatures):
            j = i + 1 # accomadate the letter in the begining
            delta = float(instance[j]) - featureMean[i]
            newInstance[j] = delta / featureStandardDev[i]
        fullSet.append(newInstance)   
    return fullSet
    

def initLayer(numNodes, numWeights):
    #
    Layer = []
    for i in range(int(numNodes) + 1):
        weightVal = []
        oldDelta = []
        for j in range(numWeights + 1):
            # build list of random weights
            randWeight = randint(-25, 25)
            weightVal.append(randWeight / float(100))
            oldDelta.append(0)
        randWeight = randint(-25, 25)
        Layer.append({'weight': weightVal, 'oldDelta' : oldDelta})
    return Layer


def setTargets(targetLtr):
    # add target for each node in outputLayer
    targetList = []
    highTarget = find(ascii_uppercase, targetLtr)
    for k in range(numOutputs):
        targetList.append(0.1)
    targetList[highTarget] = 0.9
    return targetList


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def highestActivation(outputActivation):
    #
    activationEnergy = 0
    indexActivated = 0
    for k in range(numOutputs):
       if outputActivation[k] >= activationEnergy:
            indexActivated = k
            activationEnergy = outputActivation[k]
    return ascii_uppercase[indexActivated]


def getHiddenActivation(features):
    # init new list to hold hiddenLayer activations
    hiddenActivation = []
    for i in range(numHiddenNodes):
        hiddenActivation.append(0)
    for j in range(numHiddenNodes): # for each node in hiddenLayer
        activation = hiddenNode[j]['weight'][numFeatures] # initialize this nodes activation with with biasWeight
        for i in range(numFeatures): # for each weight from this hidden node to an input node
            activation += features[i] * hiddenNode[j]['weight'][i] # add inputActivation * weight to activation
        hiddenActivation[j] = sigmoid(activation) # run sumation through sigmoid function
    # print "hiddenActivation: ", hiddenActivation
    return hiddenActivation


def getOutputActivation(hiddenActivation):
    outputActivation = []
    for i in range(numOutputs):
        outputActivation.append(0)
    for k in range(numOutputs): # for each node in outputLayer
        sum = outputNode[k]['weight'][numHiddenNodes] * 1 # init with bias
        for j in range(numHiddenNodes): # for each weight in output node 
            sum += hiddenActivation[j] * outputNode[k]['weight'][j] # add inupt * weight to activation
        outputActivation[k] = sigmoid(sum) # run activation through sigmoid function
    # print "outputActivation: ", outputActivation
    return outputActivation


def getAccuracy(setOfInterest):
    #
    correct = 0
    total = 0
    for instance in setOfInterest:
        target = instance[0]
        features = instance[1:len(instance)]

        targetActivation = setTargets(target) # new target gets set
        #forwardPropagate
        hiddenActivation = getHiddenActivation(features)
        outputActivation = getOutputActivation(hiddenActivation)
        #--------------------
        choice = highestActivation(outputActivation)
        #print targetLtr, choice
        if  choice == target:
            correct += 1.0000
        total += 1.0000
    return float(correct / total) 


def setTargets(targetLtr):
    # add target for each node in outputLayer
    temp = []
    highTarget = find(ascii_uppercase, targetLtr)
    for k in range(numOutputs):
        temp.append(0.1)
    
    temp[highTarget] = 0.9
    return temp


def getOutputErrorTerm(outputActivation,targetActivation):
    #outputLayer[errorterm] = k[activation] * (1-activation) * (target - activation)
    outputErrorTerm = []
    for i in range(numOutputs):
        outputErrorTerm.append(0)

    for k in range(numOutputs): # for each output node
        termTwo = 1 - outputActivation[k]
        termThree = targetActivation[k] - outputActivation[k]
        outputErrorTerm[k] = outputActivation[k] * termTwo * termThree
        #print outputActivation[k]," *", termTwo ,"*", termThree
    return outputErrorTerm
    

def getHiddenErrorTerm(hiddenActivation, outputErrorTerm):
    #hiddenLayer[errorterm] = h[activation] * (1-h[activation]) * (sum(k[weight]*k[errorTerm]))
    hiddenErrorTerm = []
    for i in range(numHiddenNodes):
        hiddenErrorTerm.append(0)
    
    for j in range(numHiddenNodes): # for each hidden node
        termTwo = 1 - hiddenActivation[j]
        termThree = 0
        for k in range(numOutputs): # for each weight in the hidden node
            termThree += outputNode[k]['weight'][j] * outputErrorTerm[k]
        
        hiddenErrorTerm[j] = hiddenActivation[j] * termTwo * termThree
    return hiddenErrorTerm


def updateWeights(instance):
    #outputLayer[k]['weight'][j] = outputLayer[k]['weight'][j] * delta
    #delta = learningRate * outputLayer[k]['errorTerm'] * hiddenLayer[j]['activation']
    target = instance[0]
    features = instance[1:len(instance)]
    
    targetActivation = setTargets(target) # new target gets set
    #forwardPropagate
    hiddenActivation = getHiddenActivation(features)
    outputActivation = getOutputActivation(hiddenActivation)
    #--------------------
    outputErrorTerm = getOutputErrorTerm(outputActivation,targetActivation)
    hiddenErrorTerm = getHiddenErrorTerm(hiddenActivation, outputErrorTerm)
    #print outputErrorTerm
    
    #backPropagate
    for k in range(numOutputs): # for each output
        biasDelta = learningRate * outputErrorTerm[k]
        outputNode[k]['weight'][numHiddenNodes] = outputNode[k]['weight'][numHiddenNodes] + biasDelta
        
        for j in range(numHiddenNodes): # for each weight from k to hidden node
            delta = learningRate * outputErrorTerm[k] * hiddenActivation[j]
            #print learningRate,"*",outputErrorTerm[k],"*",hiddenActivation[j]
            outputNode[k]['weight'][j] += delta + (momentum * outputNode[k]['oldDelta'][j])
            outputNode[k]['oldDelta'][j] = delta
        
    for j in range(numHiddenNodes):
        biasDelta = learningRate * hiddenErrorTerm[j]
        hiddenNode[j]['weight'][numFeatures] = hiddenNode[j]['weight'][numFeatures] + biasDelta

        for i in range(numFeatures):
            delta = learningRate * hiddenNode[j]['weight'][i] * features[i]
            hiddenNode[j]['weight'][i] += delta + (momentum * hiddenNode[j]['oldDelta'][i])
            hiddenNode[j]['oldDelta'][i] = delta    
    #--------------------
    return


def runEpoch(thisEpoch):
    #
    total = len(trainingSet) -1
    shuffle(trainingSet)
    # print "Weights ------------------------------------------------------------------"
    for instance in trainingSet:
        updateWeights(instance)
    # print outputNode[5]['weight']   
    # print "Training Accuracy --------------------------------------------------------"
    trainingAccuracy = getAccuracy(trainingSet)
    # print "Test Accuracy ------------------------------------------------------------"
    testAccuracy = getAccuracy(testSet)
    print thisEpoch,",",trainingAccuracy,",",testAccuracy    
    return 1


def trainNeuralNet():
    #
    increased = True
    thisEpoch = 0
    print "numEpoch,trainAccuracy,testAccuracy"
    while thisEpoch < numEpochs:
        thisEpoch += runEpoch(thisEpoch)
    return

    
###############
# MAIN:      ##
###############

numFeatures = 16
numOutputs = 26
biasActivation = 1

numEpochs = int(options.epochs)
numHiddenNodes = int(options.hiddenNodes)
learningRate = float(options.learningRate)
momentum = float(options.momentum)

print options

rawTrainingSet = loadSet(options.trainingSet)
featureMean = getMean(rawTrainingSet)
featureStandardDev =  getSDev(rawTrainingSet, featureMean)
trainingSet = preProcess(rawTrainingSet, featureMean, featureStandardDev)

rawTestSet = loadSet(options.testSet)
testSet = preProcess(rawTestSet, featureMean, featureStandardDev)

hiddenNode = initLayer(numHiddenNodes, numFeatures)
outputNode = initLayer(numOutputs, numHiddenNodes)

trainNeuralNet()

