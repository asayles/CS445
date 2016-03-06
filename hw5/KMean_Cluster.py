#!/usr/bin/python

import csv
from random import randint

RANGE = 16

def createCentroids(size_of_centroids, num_of_centroids):
    #create size number of centroids "m"
    centroids = []
    for i in range(num_of_centroids):
        foo = []
        for j in range(size_of_centroids):
            foo.append(randint(0,RANGE))
        centroids.append(foo)    
    return centroids

def loadFile(file_name):
    with open(file_name,'a+') as raw_file:
        reader = csv.reader(raw_file)
        raw_list = list(reader)
    return raw_list 
    
def euclidHelper(a,b):
    print "helper"    

def euclidianDistance(centroids, instance):
    # return list of distances to each centroid
    print "===euclidD==="
    print len(centroids[0]), len(instance)
    sums = []
    for centroid in centroids:
        sum = 0
        for index in range(len(instance) - 1):
            sum += centroid[index] - int(instance[index])
        sums.append(sum)
    return sums


def findClosestCentroid(distances):
    # return index of highest number 
    # first wins, no tie breaking
    print "===findClosestCentroid==="
    winner = 0
    print "len distances: ", len(distances)
    for i in range(len(distances) - 1):
        print i
        if distances[i] > distances[winner]:
            winner = i
    return winner

 
def findYourCenter(train_data, centroids):
    # create a list of instances that belong to a centroid
    print "===findYourCenter==="
    print "len centroids", len(centroids)
    centroid_groups = [[]] * len(centroids)
    counter = 0
    print "num of centroid groups: ",len(centroid_groups)
    for instance in train_data:
        distances = euclidianDistance(centroids, instance)
        print "distances: ",distances
        myCentroid = findClosestCentroid(distances)
        centroid_groups[myCentroid].append(counter)
        counter += 1
    return centroid_groups

def adjustCentroids(centroid_groups, train_data):
    # return list of new centroids
    print "===adjustCentroids==="
    num_groups = len(centroid_groups)
    centroids = []
    for i in range(num_groups):
        centroids.append(adjustCentroidsHelper(centroid_groups[i], train_data))
    return centroids

def adjustCentroidsHelper(centroid_group, train_data):
    # return mean for all the features in the centroid group
    print "adjustCentroidsHelper"
    centroid_sum = [0] * len(train_data[0])
    
    for i in centroid_group:
        print centroid_sum
        print train_data[i]
        instance = []
        for j in range(len(train_data[i])):
            instance.append(int(train_data[i][j]))
        print instance
        centroid_sum = [x + y for x, y in zip(centroid_sum, instance)]
    
    for k in range(len(centroid_sum)):
        instance[k] = int(instance[k]) / len(centroid_group)
    
    return centroid_sum


# expr1 = k =10   b
train_data = loadFile('optdigits/optdigits.train')
centroids = createCentroids(64,10)
centroid_groups = findYourCenter(train_data, centroids)
centroids = adjustCentroids(centroid_groups, train_data)
