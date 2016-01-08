#!/usr/bin/env python
import json
# open file with line delimited perceptron

# load perceptron info from json to list.


#read first char of line to get letter
perceptron = {}

def loadPerceptrons(perceptron):
    with open('perceptrons.data') as HDD:
        perceptron = json.load(HDD)
    print perceptron
    
def savePerceptrons():
    with open('perceptrons.data','w') as HDD:
        json.dump(perceptron, HDD)
    

loadPerceptrons(perceptron)    
#savePerceptrons()
