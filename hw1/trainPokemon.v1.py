#!/usr/bin/env python
import json, math, csv, sys
from string import ascii_lowercase
from optparse import OptionParser
from pprint import pprint
from random import shuffle

####################
# argparser:      ##
####################
parser = OptionParser()

parser.add_option("-p", dest="perceptronsJSON",
                  help="load perceptrons from JSON", metavar="<filename.json>")
                  
parser.add_option("-t", dest="trainingSet",
                  help="data file to train with", metavar="<filename>")
                  
parser.add_option("-i", action="store_true", dest="initialize", default=False,
                  help="initialize a set of perceptrons", metavar="none")                  

parser.add_option("-l", dest="learningRate", default=0.2,
                  help="set learning rate. (default 0.2)", metavar="<float>")
                  
parser.add_option("-s", dest="scaler", default=15,
                  help="divide training data by this scaler. (default 15)", metavar="<int>")                  
                  
(options, args) = parser.parse_args()

#########################
# FUNCTIONS:           ##
#########################

def loadPerceptronsFromJSON(filename):
    # creates a dict from JSON file
    perceptrons = {}
    with open(filename) as HDD:
        perceptrons = json.load(HDD)[0]
    return perceptrons


def buildPerceptronDict():
    # iterates over all 26 aplphabet letters and makes each unique tuple as key for dict
    # seeds dict with values
    perceptrons = {}
    for c1 in ascii_lowercase:
        for c2 in ascii_lowercase:
            if c1 != c2:
                if c2+c1 not in perceptrons:
                    perceptrons[c1+c2]= {"w0": -0.09,"w1": -0.08,"w2": -0.07,"w3": -0.06,"w4": -0.05,"w5": -0.04,"w6": -0.03,"w7": -0.02,"w8": -0.01,
                                         "w9": 0.01,"w10": 0.02,"w11": 0.03,"w12": 0.04,"w13": 0.05,"w14": 0.06,"w15": 0.07,"w16": 0.08,"w17": 0.09}        
    
    return perceptrons
     

def savePerceptronsToJSON(perceptrons,filename):
    # gets a dict and stores it as a json
    payload = []
    payload.append(perceptrons)
    
    with open(filename,'w') as HDD:
        json.dump(payload, HDD)


def loadTrainingSet(trainingFile):
    # use any ptron.json you'd like
    with open(trainingFile,'rb') as f:
        reader = csv.reader(f)
        trainingSet = list(reader)
        
    return trainingSet


def trainPtron(ptron_id):
    # runs a ptron through epoch's until there is no improvement in accuracy between epoch's
    epochPosChange = True
    # print "----------" + ptron_id
    while epochPosChange:
        epochPosChange = runEpoch(ptron_id)



def runEpoch(ptron_id): 
    # if ptron isn't 100% accurate, adjust weights, if new weights are more accurate commit change and return True
    shuffle(trainingSet)
    accuracyOne = getAccuracy(ptron_id, perceptrons[ptron_id]) # let's see where we are at
    # print "epoch accuracy: " + str(accuracyOne)
    if accuracyOne < 1: # only adjust weights if not perfect already
        adjustedPtron = adjustWeights(ptron_id) # give me a better one
        accuracyTwo = getAccuracy(ptron_id, adjustedPtron) # how are we now?
        if accuracyTwo > accuracyOne: # there is improvement, commit change
            perceptrons[ptron_id].update(adjustedPtron)
            return True
    else: # adjustment not needed
        return False
    

def getAccuracy(ptron_id, ptron):
    # tests one ptron with all matching featureVectors in the training list
    correct = float(0) 
    total = float(0)
    decision = str
    
    for featureVector in trainingSet:
        target = featureVector[0].lower()
        
        if target in str(ptron_id): # decides if a trainingVector is right for this ptron
            decision = signumToAlpha(ptron_id, testFeatureVector(ptron, featureVector))
            
            total += 1 # increment the total for this featureVector   
            if  decision == target: # ptron decided correctly 
                correct += 1 # increment correct counter
    # incase there were no training examples for this prton. Mainly durning dev.
    if total > 0: return float(correct)/float(total)
    else: return 0.0
    

def testFeatureVector(ptron, featureVector):
    # sums the ptron with the inputs from a trainingVector
    sum = ptron['w0'] # init sum with the bias
    
    for j in range(1,len(featureVector)):
        weight = "w" + str(j) # nameing convention fix, could have used a list instead.
        scaledInput = float(featureVector[j]) / float(trainingDataScaler)
        sum += ptron[weight] * scaledInput # iterate over the weights and inputs to sum
    
    if sum < 0: return -1
    else: return 1


def signumToAlpha(ptron_id, signum):
    # for reuse
    if signum < 0: return ptron_id[0]
    else: return ptron_id[1]
               

def adjustWeights(ptron_id):
    # test the perceptron with each matching trainingVector and makes an adjustment if it's wrong
    adjustedPtron = perceptrons[ptron_id]
    
    for featureVector in trainingSet: # iterate through the training set
        targetAlpha = featureVector[0].lower()
        
        if targetAlpha in str(ptron_id): # decides if this.trainingVector is right for this.ptron
            if targetAlpha == ptron_id[0]: targetNum = float(-1)
            else: targetNum = float(1)
            signum = testFeatureVector(adjustedPtron, featureVector)
            decision = signumToAlpha(ptron_id, signum)
            
            if decision != targetAlpha: # ptron was wrong :-(
                adjustedPtron['w0'] += learningRate * 1 * targetNum
                
                for j in range(1,len(featureVector)):
                    weight = "w" + str(j) # nameing convention fix, could have used a list instead.
                    scaledInput = float(featureVector[j]) / float(trainingDataScaler)
                    adjustedPtron[weight] = float(adjustedPtron[weight]) + float(learningRate) * float(scaledInput) * float(targetNum)
                               
    return adjustedPtron  
        
###############
# MAIN:      ##
############### 

#--------------------------------
# create a JSON of ptrons       |
#--------------------------------
if options.initialize:
    print "initializing <perceptronsYoung.json> "
    perceptrons = buildPerceptronDict()
    savePerceptronsToJSON(perceptrons, "perceptronsYoung.json")
    print "the deed is done, shhhhhh"
    sys.exit()
#-------------------
# Train ptrons     |
#-------------------
if options.perceptronsJSON and options.trainingSet:
    perceptrons = loadPerceptronsFromJSON(options.perceptronsJSON)
    trainingSet = loadTrainingSet(options.trainingSet)
    learningRate = options.learningRate    
    trainingDataScaler = options.scaler
    progressCounter = 0
    
    for key in perceptrons:
        progressCounter += 1
        text = "\rprogress: " + str(progressCounter) + " of 325"
        sys.stdout.write(text)
        
        trainPtron(key)

    savePerceptronsToJSON(perceptrons, "perceptronsMoreWiser.json")    

else:        
    parser.error('REQUIRED -p <filename.json> -t <filename>')        
