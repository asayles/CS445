#!/usr/bin/python

import csv, math, sys
from pprint import pprint as pp
from random import randint



def createCentroids(size_of_centroids, num_of_centroids):
    #create size number of centroids "m"
    centroids = []
    for i in range(num_of_centroids):
        foo = []
        for j in range(size_of_centroids):
            foo.append(randint(0,CENTROID_RANGE))
        centroids.append(foo)    
    return centroids

def loadFile(file_name):
    with open(file_name,'a+') as raw_file:
        reader = csv.reader(raw_file)
        raw_list = list(reader)
    return raw_list 
    

def euclidianDistance(centroids, instance):
    # return list of distances to each centroid
    distances = []
    for centroid in centroids:
        sum = 0
        # find the distance to each centroid for this instance
        for index in range((len(instance) - 1)):
            sum += math.pow(centroid[index] - int(instance[index]), 2)
        distances.append(sum)
    return distances


def findClosestCentroid(distances):
    # return index of highest number 
    # first wins, no tie breaking
    winner = 0
    for i in range(len(distances)):
        if distances[i] < distances[winner]:
            winner = i
    return winner

 
def findYourCenter(train_data, centroids):
    # create a list of instances that belong to a centroid
    centroid_groups = []
    for i in range(len(centroids)):
        centroid_groups.append([])
    counter = 0
    for instance in train_data:
        # get the distance from each centroid
        distances = euclidianDistance(centroids, instance)

        # find the centroid that's closest
        my_centroid = findClosestCentroid(distances)

        # add the instances index to the list of it's closest centroid
        centroid_groups[my_centroid].append(counter)
        counter += 1
    return centroid_groups


def adjustOneCentroid(centroid_group, train_data):
    # sum all the features for this centroid group, then divide by size
    centroid_sum = [0] * (len(train_data[0]) - 1)
    for i in centroid_group:
        instance = []
        for j in range(len(train_data[i]) - 1):
            instance.append(int(train_data[i][j]))
        centroid_sum = [x + y for x, y in zip(centroid_sum, instance)]
    
    for k in range(len(centroid_sum)):
        centroid_sum[k] = int(centroid_sum[k]) / len(centroid_group)
    
    return centroid_sum


def adjustCentroids(centroid_groups, train_data):
    # return list of new centroids
    num_groups = len(centroid_groups)
    centroids = []
    for i in range(num_groups):
        centroids.append(adjustOneCentroid(centroid_groups[i], train_data))
    return centroids


def findSSE(centroids,centroid_groups, instances):
    sum = 0
    for i in range(len(centroids)):
        for j in centroid_groups[i]:
            for k in range(len(centroids[i])):
                sum += math.pow(centroids[i][k] - int(instances[j][k]),2)
    return sum


#==============
# EXPR 1
#=============
K = 10
num_features = 64
CENTROID_RANGE = 16

train_data = loadFile('optdigits/optdigits.train')
# print"data: ", train_data

new_centroids = []
centroid_groups = []

centroids = createCentroids(num_features,K)
# centroids = [[1,0],[4,4]]
# print "centroids: ",centroids

while centroids != new_centroids:
    if new_centroids:
        centroids = new_centroids
    empty_group_found = True
    while empty_group_found:
        empty_group_found = False
        centroid_groups = findYourCenter(train_data, centroids)
        for i in centroid_groups:
            if len(i) == 0:
                print "found a weasel"
                empty_group_found = True
                centroids = createCentroids(num_features,K)
                

    new_centroids = adjustCentroids(centroid_groups, train_data)
    # print "centroids: ", centroids
    # print "nCentroids: ", new_centroids

sse = findSSE(new_centroids, centroid_groups, train_data)
print "sse: ", sse
print "\n"
