#!/usr/bin/python

import csv, random


#-------------------------------
# import raw data file to list
def importCSVAsList():
    with open('spambase.data.csv','rb') as raw_file:
        reader = csv.reader(raw_file)
        raw_list = list(reader)
    return raw_list

#------------------------------------------
# split sourceList into 3 subsets. Also, return probability of pos
# set 1. test set = 40 pos: 60 neg
# set 2. train_pos = 40 pos
# set 3. train_neg = 60 neg
def splitList(sourceList):
    zeroes = []
    zeroes_len = 0
    heroes = []
    heroes_len = 0
    max_size = 0
    training_pos = []
    training_neg = []
    training_set_prob_spam = 0
    test_set = []
    
    # group instances by class
    for line in sourceList:
        if int(line[57]) == 0:
            zeroes.append(line)
        else:
            heroes.append(line)
    
    # capture size of larger set
    #  int division will round down and make max_size even
    max_size = (len(zeroes) + len(heroes)) / 2
    zeroes_half_size = len(zeroes) / 2
    heroes_half_size = len(heroes) / 2
    # add one instance from each classification to training,test set
    # until max_size is reached
    count_zeroes = 0
    count_heroes = 0
    while (len(training_pos) + len(training_neg)) < max_size:
        if count_zeroes < zeroes_half_size:
            zeroes_max_index = len(zeroes) - 1
            zeroes_index = random.randint(0,zeroes_max_index)
            training_neg.append(zeroes.pop(zeroes_index))
            count_zeroes = count_zeroes + 1
        if count_heroes < heroes_half_size:
            heroes_max_index = len(heroes) - 1
            heroes_index = random.randint(0,heroes_max_index)
            training_pos.append(heroes.pop(heroes_index))
            count_heroes = count_heroes + 1
       
    count_zeroes = 0
    count_heroes = 0
    while len(test_set) < max_size:
        if count_zeroes < zeroes_half_size:
            zeroes_max_index = len(zeroes) - 1
            zeroes_index = random.randint(0,zeroes_max_index)
            test_set.append(zeroes.pop(zeroes_index))
            count_zeroes = count_zeroes + 1
        if count_heroes < heroes_half_size:
            heroes_max_index = len(heroes) - 1
            heroes_index = random.randint(0,heroes_max_index)
            test_set.append(heroes.pop(heroes_index))
            count_heroes = count_heroes + 1
    
    return training_pos, training_neg, test_set

#------------------------------------------
# helper: takes set, returns list of means
def meanHelper(sourceList):
    size_of_list = len(sourceList)
    meanList = [0.0]*58
    
    # sum all the feature values
    for instance in sourceList:
        for index_of_feature in range(len(instance)):
            meanList[index_of_feature] = float(meanList[index_of_feature]) + float(instance[index_of_feature])
    # divide by size_of_list
    for index_of_feature in range(len(meanList)):
        meanList[index_of_feature] = meanList[index_of_feature] / size_of_list 
   
    return meanList

#---------------------------------------------
# helper: takes set, returns list of sDev
def sDevHelper(sourceList, meanList):
    size_of_list = len(sourceList)
    varianceList = [0.0] * 58
    sDevList = [0.0] * 58
    
    for instance in sourceList:
        for index_of_feature in range(len(instance)):
            thisDifference = (meanList[index_of_feature] - float(instance[index_of_feature]))
            varianceList[index_of_feature] = varianceList[index_of_feature] + (thisDifference * thisDifference)
    
    for index_of_feature in range(len(varianceList)):
        sDevList[index_of_feature] = varianceList[index_of_feature] / size_of_list
    
    return sDevList

#---------------------
# process the dataz
def createProbabilisticModel(train_pos, train_neg):
    probModel = {}
    probModel['p_prob_pos'] = len(training_pos) / (float(len(train_pos)) + float(len(train_neg)))
    probModel['p_prob_pos'] = len(training_neg) / (float(len(train_neg)) + float(len(train_pos)))   
    probModel['mean_pos'] = meanHelper(train_pos)
    probModel['mean_neg'] = meanHelper(train_neg)
    probModel['sDev_pos'] = sDevHelper(train_pos, probModel['mean_pos'])
    probModel['sDev_neg'] = sDevHelper(train_neg, probModel['mean_neg'])
    
    return probModel

#----------------------
# main            
if __name__ == "__main__":
    training_pos, training_neg, test_set, = splitList(importCSVAsList())
    prob_model = createProbabilisticModel(training_pos, training_neg)
