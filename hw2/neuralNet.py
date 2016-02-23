#!usr/bin/env python

import csv, sys, math
from optparse import OptionParser
from random import randint
from pprint import pprint
from string import ascii_uppercase, find


####################
# argparser:      ##
####################
parser = OptionParser()

parser.add_option("-p", dest="perceptronsJSON",
                  help="load perceptrons from JSON", metavar="<filename.json>")

parser.add_option("-t", dest="trainingSet",
                  help="data file to train with", metavar="<filename>")

parser.add_option("-l", dest="learningRate", default=0.2,
                  help="set learning rate. (default 0.2)", metavar="<float>")

parser.add_option("-n", dest="numHiddenNodes", default=4,
                  help="set number of hidden layers. (default 4)", metavar="<int>")

parser.add_option("-m", dest="momentum", default=0.3,
                  help="set momentum. (default 0.3)", metavar="<float>")
(options, args) = parser.parse_args()

if not options.trainingSet:
    parser.error("Need training set -t <filename>")

#########################
# FUNCTIONS:           ##
#########################
def loadTrainingSet(trainingFile):
    # use any ptron.json you'd like
    with open(trainingFile, 'rb') as f:
        reader = csv.reader(f)
        trainingSet = list(reader)

    return trainingSet


def preProcess(trainingSet):
    #
    numInstances = len(trainingSet) #10,000
    featureMean = []
    featureVar = []
    featureStandardDev = []
       
    for i in range (numFeatures):
        featureMean.append(0)
        featureVar.append(0)
        featureStandardDev.append(0)
    
    for instance in trainingSet:
        features = instance[1:]
        for i in range(numFeatures):
            featureMean[i] += float(features[i]) / float(numInstances)        
    #print "Mean: ", featureMean
    
    for instance in trainingSet:
        features = instance[1:]
        for i in range(numFeatures):
            featureVar[i] += math.pow(float(features[i]) - featureMean[i], 2)
    
    for i in range(numFeatures):
        featureStandardDev[i] = math.sqrt(featureVar[i])
    #print "sDev: ", featureStandardDev

    for instance in trainingSet:
        for i in range(numFeatures):
            instance[(i + 1)] = (int(instance[(i + 1)]) - featureMean[i]) / featureStandardDev[i]
    return trainingSet


def initLayer(numNodes, numWeights):
    #
    Layer = []
    for i in range(int(numNodes) + 1):
        weightVal = []
        for j in range(numWeights + 1):
            # build list of random weights
            randWeight = randint(-25, 25)
            weightVal.append(randWeight / float(100))
        randWeight = randint(-25, 25)
        Layer.append({'weight': weightVal, 'activation': 0})
    return Layer


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


def forwardPropagate(features):
    #
    #print "\npropagating ------------------"
    for j in range(numHiddenNodes): # for each node in hiddenLayer
        #print "hiddenLayer ", j
        #print "\nold activation ", hiddenLayer[j]['activation']
        hiddenLayer[j]['activation'] = hiddenLayer[j]['weight'][numFeatures] # initialize with bias
        #print "new activation ", hiddenLayer[j]['activation']
        for i in range(numFeatures):
            hiddenLayer[j]['activation'] += features[i] * hiddenLayer[j]['weight'][i] # add input * weight to activation
        hiddenLayer[j]['activation'] = sigmoid(hiddenLayer[j]['activation']) # run sumation through sigmoid function
    
    for k in range(numOutputs): # for each node in outputLayer
        outputLayer[k]['activation'] = outputLayer[k]['weight'][numHiddenNodes] # init with bias
        
        for j in range(numHiddenNodes): 
            outputLayer[k]['activation'] += hiddenLayer[j]['activation'] * outputLayer[k]['weight'][j] # add inupt * weight to activation
        outputLayer[k]['activation'] = sigmoid(outputLayer[k]['activation']) # run activation through sigmoid function
    return

def setTargets(targetLtr):
    # add target for each node in outputLayer
    highTarget = find(ascii_uppercase, targetLtr)
    for k in range(numOutputs):
        outputLayer[k]['target'] = 0.1
    
    outputLayer[highTarget]['target'] = 0.9
    return


def calculateErrorTerms():
    #outputLayer[errorterm] = k[activation] * (1-activation) * (target - activation)
    for k in range(numOutputs): # for each output node
        termTwo = 1 - outputActivation[k]
        termThree = outputLayer[k]['target'] - outputLayer[k]['activation']
        outputLayer[k]['errorTerm'] = outputLayer[k]['activation'] * termTwo * termThree
    
    #hiddenLayer[errorterm] = h[activation] * (1-h[activation]) * (sum(k[weight]*k[errorTerm]))
    for j in range(numHiddenNodes): # for each hidden node
        termTwo = 1 - hiddenLayer[j]['activation']
        termThree = 0
        for k in range(numOutputs):
            termThree += outputLayer[k]['weight'][j] * outputLayer[k]['errorTerm']
        
        hiddenLayer[j]['errorTerm'] = hiddenLayer[j]['activation'] * termTwo * termThree




def runEpoch():
    #
    counter = 0
    total = len(trainingSet) -1
    accuracyOld = 0
    #print " running epoch-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="
    print ""
    for instance in trainingSet:
        text = "\repoch progress: " + str(counter) + " out of " + str(total)
        sys.stdout.write(text)
        counter += 1
        target = instance[0]
        features = instance[1:len(instance)]
        
        setTargets(target) # new target gets set
        forwardPropagate(features) # activation changes
        calculateErrorTerms() # errorTerm changes
        updateWeights(features)
        # for k in range(numOutputs):
        #     print outputLayer[k]['weight'][numHiddenNodes]
        
        
    return 


def trainNeuralNet():
    #
    progress = True
    runEpoch()
    old = getAccuracy()
    while progress:
        runEpoch()
        new = getAccuracy()
        if new > old: 
            progress = True
            old = new
        else: 
            progress = False
    return


def highestActivation():
    #
    activationEnergy = 0
    indexActivated = 0
    
    for k in range(numOutputs):
        if outputLayer[k]['activation'] > activationEnergy:
            indexActivated = k
            activationEnergy = outputLayer[k]['activation']
    return ascii_uppercase[indexActivated]

def getAccuracy():
    #
    correct = 0
    total = 0
    print ""
    for instance in trainingSet:
        text = "\raccuracy: " + str(correct) + " out of " + str(total)
        sys.stdout.write(text)
        
        target = instance[0]
        features = instance[1:len(instance)]
        setTargets(target)
        forwardPropagate(features)
        choice = highestActivation()
        if choice == target:
            correct += 1
            print choice, target
        total += 1
    return (correct / float(total))

###############
# MAIN:      ##
###############

numFeatures = 16
numHiddenNodes = int(options.numHiddenNodes)
numOutputs = 26
learningRate = float(options.learningRate)
biasActivation = 1

print options
trainingSet = preProcess(loadTrainingSet(options.trainingSet))
hiddenLayer = initLayer(numHiddenNodes, numFeatures)
outputLayer = initLayer(numOutputs, numHiddenNodes)
#pprint (hiddenLayer)
trainNeuralNet()
