#!/usr/bin/env python
import json, math, csv, sys
from string import ascii_uppercase
from optparse import OptionParser
from pprint import pprint
from random import randint

####################
# argparser:      ##
####################
parser = OptionParser()

parser.add_option("-p", dest="perceptronsJSON",
                  help="load perceptrons from JSON", metavar="<filename.json>")
                  
parser.add_option("-t", dest="testSet",
                  help="data file to test with", metavar="<filename>")

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


def loadTestSet(testFile):
    # use any ptron.json you'd like
    with open(testFile,'rb') as f:
        reader = csv.reader(f)
        testSet = list(reader)
        
    return testSet  


def signumToAlpha(ptron_id, signum):
    # for reuse
    if signum < 0: return ptron_id[0]
    else: return ptron_id[1]


def getVoterBallot(instance, ptron_id):
    # return the vote of one perceptron
    sum = float(perceptrons[ptron_id]['w0']) # init sum with the bias
    
    for j in range(1,len(instance)):
        weight = "w" + str(j) # nameing convention fix, could have used a list instead.
        scaledInput = float(instance[j]) / float(trainingDataScaler)
        sum += float(perceptrons[ptron_id][weight]) * scaledInput # iterate over the weights and inputs to sum
    
    return signumToAlpha(ptron_id, sum)


def countBallots(instance):
    # tally up the ballots, return the highest vote
    votes = {}
    for ptron_id in perceptrons: # get one ptron
        key = getVoterBallot(instance, ptron_id)
        if votes.has_key(key):
            votes[key] += 1 # add ballot result to votes for this instance
        else:
            votes[key] = 1
            peoplesChoice = key

    # return the highest value in the votes dict
    for key in votes:
        if votes[key] == votes[peoplesChoice]:
            if randint(0,9) > 4:
                peoplesChoice = key
        
        elif votes[key] > votes[peoplesChoice]:
            peoplesChoice = key

    return peoplesChoice


def printStoneTablet():
    # print the matrix
    header = ["   "," A "," B "," C "," D "," E "," F "," G "," H "," I "," J "," K "," L "," M ",
              " N "," O "," P "," Q "," R "," S "," T "," U "," V "," W "," X "," Y "," Z "]
    print (header)
    
    for actual in ascii_uppercase:
        localList = []
        localList.append(" "+actual+" ")
        
        for predict in ascii_uppercase:
            key = actual + predict
            
            if stoneTablet.has_key(key):
                value = str(stoneTablet[key])
                if len(str(value)) == 1: value = " "+value+" "
                elif len(str(value)) == 2: value = " "+value
                
                localList.append(value)
            else:
                localList.append("   ")
        print localList


def printAccuracy():
    # fun stats
    total = 0.0 
    correct = 0.0
    for actual in ascii_uppercase:
        for predict in ascii_uppercase:
            key = actual + predict
            
            if stoneTablet.has_key(key):
                total += stoneTablet[key]
                if actual == predict:
                    correct += stoneTablet[key]
        
    print "[correct : "+str(correct)+"],[total : "+str(total)+"]"
    print "[accuracy : "+str(correct/total)+"]"


###############
# MAIN:      ##
############### 

#---------------------
# Test instances     |
#---------------------
if options.perceptronsJSON and options.testSet:
    perceptrons = loadPerceptronsFromJSON(options.perceptronsJSON)
    testSet = loadTestSet(options.testSet)
    trainingDataScaler = options.scaler
    stoneTablet = {}
    progress = len(testSet)
    progressCounter = 0
    
    for instance in testSet:
        progressCounter += 1
        text = "\rprogress: " + str(progressCounter) + " of " + str(progress)
        sys.stdout.write(text)
        
        actual = instance[0]
        predicted = countBallots(instance).upper() # survey says?
        stoneTabletKey = actual + predicted
        
        if stoneTablet.has_key(stoneTabletKey):
            stoneTablet[stoneTabletKey] += 1
        else:
            stoneTablet[stoneTabletKey] = 1
    
    print " DONE!"
    print options
    printAccuracy()    
    printStoneTablet()

else:        
    parser.error('REQUIRED -p <filename.json> -t <filename>')        
