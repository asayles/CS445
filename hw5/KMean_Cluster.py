#!/usr/bin/python

import csv, math, sys, json, array
from pprint import pprint as pp
from random import randint



def createCentroids(size_of_centroids, num_of_centroids, range_of_centroids):
    #create size number of centroids "m"
    centroids = []
    for i in range(num_of_centroids):
        foo = []
        for j in range(size_of_centroids):
            foo.append(randint(0,range_of_centroids))
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

 
def findYourCenter(data, centroids):
    # create a list of instances that belong to a centroid
    centroid_groups = []
    for i in range(len(centroids)):
        centroid_groups.append([])
    counter = 0
    for instance in data:
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


def findSSE(centroids, centroid_groups, instances):
    sum = 0
    for i in range(len(centroids)):
        for j in centroid_groups[i]:
            for k in range(len(centroids[i])):
                sum += math.pow(centroids[i][k] - int(instances[j][k]),2)
    return sum

def the_D(m1, m2):
    sum = 0
    for i in range(len(m1)):
        sum += math.pow(m1[i] - m2[i],2)
    return sum

def findSSSep(centroids):
    sum = 0
    for i in range((len(centroids)-1)):
        for j in range((i+1),len(centroids)):
            sum += the_D(centroids[i],centroids[j])
    return sum

def findSingleEntropy(centroid, group, instances):
    occurence = [0] * K
    # find most occuring
    for i in group:
        this_class = instances[i][-1]
        occurence[int(this_class)] += 1
            
    # do some math
    term_two = 0.0
    for i in occurence:
        sub_term = i/float(len(group))
        if sub_term != 0:
            term_two += -1 * (sub_term * math.log(sub_term, 2))
    term_one = len(group)/float(len(instances))
    return term_one * term_two

def findEntropy(centroids, centroid_groups, instances):
    sum = 0
    for i in range(len(centroids)):
        sum += findSingleEntropy(centroids[i], centroid_groups[i], instances)
    return sum


#=============
# EXPR 1
#=============
def main_one():
    best_SSE = 0
    best_SSSep = 0 
    best_mEntropy = 0
    best_centroids = []
    
    for run_num in range(1):
        print "run: ", run_num
        train_data = loadFile('optdigits/optdigits.train')
        num_training_instances = len(train_data)

        new_centroids = []
        centroid_groups = []

        centroids = createCentroids(num_features,K, CENTROID_RANGE)

        while centroids != new_centroids:
            if new_centroids:
                centroids = new_centroids
            empty_group_found = True
            while empty_group_found:
                empty_group_found = False
                centroid_groups = findYourCenter(train_data, centroids)
                for i in centroid_groups:
                    if len(i) == 0:
                        empty_group_found = True
                        centroids = createCentroids(num_features,K, CENTROID_RANGE)
            new_centroids = adjustCentroids(centroid_groups, train_data)

        this_SSE = findSSE(new_centroids, centroid_groups, train_data)
        this_SSSep = findSSSep(new_centroids)
        this_mEntropy = findEntropy(new_centroids, centroid_groups, train_data)
        print this_SSE
        if this_SSE > best_SSE:
            best_SSE = this_SSE
            best_SSSep = this_SSSep
            best_mEntropy = this_mEntropy
            best_centroids = new_centroids
    print best_SSE
    return best_SSE, best_SSSep, best_mEntropy, best_centroids

def findYourClass(groups, instances):
    most_freq_class = []
    for i in range(len(groups)):
        class_dict = {}
        for j in groups[i]:
            instance = instances[j]
            this_class = instance[-1]
            if this_class in class_dict:
                class_dict[this_class] += 1
            else:
                class_dict[this_class] = 1
        
        highest_class = 'none'
        highest_value = 0
        for key in class_dict:
            if class_dict[key] > highest_value:
                highest_class = key
                highest_value = class_dict[key]
    
        most_freq_class.append(highest_class)
    return most_freq_class

def print_confusion_matrix(centroid_classes, centroid_groups_test, instances):
    matrix_row_headers = [0,1,2,3,4,5,6,7,8,9]
    matrix_column_headers = [0,1,2,3,4,5,6,7,8,9]
    confusion_matrix = [[0,0,0,0,0,0,0,0,0,0,0] for i in range(10)]
    correct = 0
    total = 0
    for i in range(len(centroid_groups_test)):
        for j in centroid_groups_test[i]:
            row = int(instances[j][-1])
            column = int(centroid_classes[i])
            confusion_matrix[row][column] += 1
            if row == column:
                correct += 1
            total += 1
    
    print correct, total
    print "accuracy: ", correct/float(total)
    print " ", matrix_column_headers
    for i in range(len(confusion_matrix)):
        print matrix_row_headers[i], confusion_matrix[i]
        
def print_as_pgm(one_cluster_center, the_index, file_prefix):
    # print "one center: "

    # define the width  (columns) and height (rows) of your image
    width = 8
    height = 8

    # declare 1-d array of unsigned char and assign it random values
    buff=array.array('B')

    for i in range(0, width*height):
      buff.append(int(round(one_cluster_center[i])) * 16)


    # open file for writing
    filename = file_prefix + "." + str(the_index) + ".pgm"

    try:
      fout=open("results/"+filename, 'wb')
    except IOError, er:
      print "Cannot open file "
      sys.exit()


    # define PGM Header
    pgmHeader = 'P5' + '\n' + str(width) + '  ' + str(height) + '  ' + str(255) + '\n'

    # write the header to the file
    fout.write(pgmHeader)

    # write the data to the file
    buff.tofile(fout)

    # close the file
    fout.close()

#=============
# MAIN:
#=============
K = 10
num_features = 64
CENTROID_RANGE = 16

SSE, SSSep, mEntropy, centroids = main_one()
test_data = loadFile('optdigits/optdigits.train')
centroid_groups_test = findYourCenter(test_data, centroids)
centroid_classes = findYourClass(centroid_groups_test, test_data)
print_confusion_matrix(centroid_classes, centroid_groups_test, test_data)
for i in range(len(centroids)):
    print_as_pgm(centroids[i],i, 'expr1')
