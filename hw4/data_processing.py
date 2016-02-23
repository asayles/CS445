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
# split list into four similar parts
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
    training_set_prob_spam = float(len(training_pos))/(float(len(training_pos)) + float(len(training_neg)))    
    
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
    
    return training_pos, training_neg, test_set, training_set_prob_spam

#---------------------
# process the dataz
def createProbabilisticModel(training_pos, training_neg, test_set, prob_of_spam):
    print len(training_pos), len(training_neg), len(test_set), prob_of_spam
    mean_pos = []
    mean_neg = []
    sDev_pos = []
    sDev_neg = []

#----------------------
# main            
if __name__ == "__main__":
    training_pos, training_neg, test_set, prob_of_spam = splitList(importCSVAsList())
    createProbabilisticModel(training_pos, training_neg, test_set, prob_of_spam)
