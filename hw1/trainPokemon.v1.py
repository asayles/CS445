#!/usr/bin/env python
import json

#read first char of line to get letter
perceptrons = {}

def loadPerceptrons():
    with open('perceptrons.data') as HDD:
        perceptrons = json.load(HDD)
         
def savePerceptrons(perceptrons):
    with open('perceptrons.data','w') as HDD:
        json.dump(perceptrons, HDD)

def trainPerceptrons():
    # for line in file
        # store letter
        # store expected output
        # load inputs x16
        # load weights x16
        # math for t
        # compare t to expected value
    

perceptrons = loadPerceptrons()

   
savePerceptrons(perceptrons)
