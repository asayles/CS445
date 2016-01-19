#!/usr/bin/env python
import json, math, csv, operator
from string import ascii_lowercase
from optparse import OptionParser
from pprint import pprint

####################
# argparser:      ##
####################
parser = OptionParser()

parser.add_option("-p", dest="perceptronsJSON",
                  help="load perceptrons from JSON", metavar="<filename.json>")
                  
parser.add_option("-t", dest="testingSet",
                  help="data file to test with", metavar="<filename>")   

(options, args) = parser.parse_args()

#########################
# FUNCTIONS:           ##
#########################

def signumToAlpha(ptron_id, signum):
    # for reuse
    if signum < 0: return ptron_id[0]
    else: return ptron_id[1]


def getVoterBallot(instance, ptron_id):
    # return the vote of one perceptron
    sum = perceptrons[ptron_id]['w0'] # init sum with the bias
    
    for j in range(1,len(instance)):
        weight = "w" + str(j) # nameing convention fix, could have used a list instead.
        sum += perceptrons[ptron_id][weight] * float(instance[j]) # iterate over the weights and inputs to sum
    
    return signumToAlpha(ptron_id, sum)


def countBallots(instance):
    # tally up the ballots, return the highest vote
    votes = {}
    for ptron_id in perceptrons: # get one ptron
        votes[getVoterBallot(instance, ptron_id)] += 1 # add ballot result to votes for this instance        
    # return the highest value in the votes dict
    return max(votes.iteritems(), key=operator.itemgetter(1))[0]


def etchInStone(target, vote):
    # insert in to the confusion matrix
    

###############
# MAIN:      ##
############### 

#-------------------
# Test ptrons     |
#-------------------
if options.perceptronsJSON and options.trainingSet:
    perceptrons = loadPerceptronsFromJSON(options.perceptronsJSON)
    testSet = loadTrainingSet(options.testSet)
    stoneTablet = []
    
    for instance in testSet:
        target = instance[0]
        vote = countBallots(instance) # survey says?
        etchInStone(target, vote) # record in confusion matrix


else:        
    parser.error('REQUIRED -p <filename.json> -t <filename>')        
