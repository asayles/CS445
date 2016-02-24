#!/usr/bin/python

import data_processing as dp
import math


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
    termOne = 1 / (math.sqrt(2 * math.pi) * sDev)
    expFracNum = math.pow((value - mean),2)
    expFracDem = 2 * math.pow(sDev,2)
    termTwo = math.exp(expFracNum/expFracDem)
    
    return termOne * termTwo

#---------------------
# sum the log things
def midichlorianTest(instance, prior_prob, meanList, sDevList):
    # initialize the sum with prior prob
    midichlorian_count = log(prior_prob)
    # add each feature prob to the sum
    for i in range(57):
        midichlorian_count = midichlorian_count + log(probOfFeatureGivenClass(float(instance[i]), meanList[i], sDevList[i]))
    
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
        