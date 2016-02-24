#!/usr/bin/python

import data_processing as dp
import math


#=============
# FUNCTIONS  |
#=============

#--------------------
# data processing and prep work
train_pos,train_neg,test_set = dp.splitList(dp.importCSVAsList())
prob_model = dp.createProbabilisticModel(train_pos,train_neg)

#-----------------------------------------
# wrapper function for clarity
def probOfFeatureGivenClass(value, mean, sDev):
    return N(value, mean,sDev)

#---------------------------
# do some terrible math   
def N(value, mean, sDev):
    # log(termOne / termTwo) == log(termTwo) - log(termOne)
    expFracNum = math.pow((value - mean),2)
    expFracDem = 2 * math.pow(sDev,2)
    exponent = expFracNum / expFracDem
    termOne = math.exp(-(exponent))
    termTwo = (math.sqrt(2 * math.pi) * sDev)

    if termOne == 0.0:
        return exponent - math.log(termTwo)
    else:
        return math.log(termOne) - math.log(termTwo)

#---------------------
# sum the log things
def midichlorianTest(instance, prior_prob, meanList, sDevList):
    # initialize the sum with prior prob
    midichlorian_count = math.log(prior_prob)
    # add each feature prob to the sum
    for i in range(57):
        midichlorian_count = midichlorian_count + probOfFeatureGivenClass(float(instance[i]), meanList[i], sDevList[i])
    
    return midichlorian_count

#-----------------------------------
# get the metrics for the test set
def getMetrics():
    is_pos_chose_pos = 0
    is_pos_chose_neg = 0
    is_neg_chose_neg = 0
    is_neg_chose_pos = 0
    
    for instance in test_set:
        this_class = instance[57]
        sith = midichlorianTest(instance, prob_model['p_prob_neg'], prob_model['mean_neg'], prob_model['sDev_neg'])
        jedi = midichlorianTest(instance, prob_model['p_prob_pos'], prob_model['mean_pos'], prob_model['sDev_pos'])
        
        print sith, jedi


#========
# MAIN  |
#========
if __name__ == "__main__":
    getMetrics()