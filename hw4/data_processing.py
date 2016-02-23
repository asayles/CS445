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
    heroes = []
    max_size = 0
    training_set = []
    test_set = []
    
    # group instances by class
    for line in sourceList:
        if int(line[57]) == 0:
            zeroes.append(line)
        else:
            heroes.append(line)
    
    # capture size of smaller set
    if len(zeroes) > len(heroes):
        max_size = len(heroes)
    else:
        max_size = len(zeroes)
    # keep it even cowboy
    if (max_size % 2) == 1:
        max_size = max_size - 1

    # add one instance from each classification to training,test set
    # until max_size is reached
    while max_size > 0:
        index_training = random.randint(0,max_size)
        training_set.append(zeroes[index_training])
        training_set.append(heroes[index_training])
        max_size = max_size - 1
        
        index_test = random.randint(0,max_size)
        test_set.append(zeroes[index_test])
        test_set.append(heroes[index_test])
        max_size = max_size - 1

    return training_set,test_set

#---------------------
# process the dataz
def makeNormal


#----------------------
# main            
if __name__ == "__main__":
    splitList(importCSVAsList())
