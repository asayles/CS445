#!/usr/bin/env python
import json
from string import ascii_lowercase

#####
# Have to store outcomes in confusion matrix
# Have to save previous weights incase change is not good 
#####


#read first char of line to get letter
perceptrons = {
        "ab":{"w0": 0.1,"w1": 0.2},
                "ac":{"w0": 0.1,"w1": 0.2},
                "ad":{"w0": 0.1,"w1": 0.2}
}



def loadPerceptrons():
    with open('perceptrons.json') as HDD:
        perceptrons = json.load(HDD)
        print perceptrons
         
def savePerceptrons(perceptrons):
    print "saving this thing"
    print len(perceptrons.keys())
    # print perceptrons
    with open('perceptrons.data','w') as HDD:
        json.dump(perceptrons, HDD)

def trainPerceptrons():
    f = open('data','r')
    for line in f: # for line in file
        featureVector = line.rstrip('\n').split(',')
        target = featureVector[0]
    
    #### create perceptron combos
    for c1 in ascii_lowercase:
        for c2 in ascii_lowercase:
            if c1 != c2:
                if c2+c1 not in perceptrons:
                    perceptrons[c1+c2 ]= "{\"w0\": 0.1,\"w1\": 0.2,\"w2\": 0.3,\"w3\": 0.1,\"w4\": 0.2,\"w5\": 0.3,\"w6\": 0.1,\"w7\": 0.2,\"w8\": 0.3,\"w9\": 0.1,\"w10\": 0.2,\"w11\": 0.3,\"w12\": 0.1,\"w13\": 0.2,\"w14\": 0.3\"w15\": 0.1,\"w16\": 0.2,\"w17\": 0.3}"
        
        # load weights x16
        # math for t
        # compare t to expected value
    

#perceptrons = loadPerceptrons()
trainPerceptrons()
   
savePerceptrons(perceptrons)
