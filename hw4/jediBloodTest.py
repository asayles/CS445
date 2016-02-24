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
    # hackery fix for divide by 0 and domain errors
    if sDev == 0.0:
        sDev = 1 * math.pow(10,-20)

    exp_frac_num = math.pow((value - mean),2)
    exp_frac_dem = 2 * math.pow(sDev,2)
    exponent = exp_frac_num / exp_frac_dem
    term_one = math.exp(-(exponent))
    term_two = (math.sqrt(2 * math.pi) * sDev)
    
    if term_one == 0.0:
        return exponent, term_two
    else:
        return term_one, term_two

#---------------------
# sum the log things
def midichlorianTest(instance, prior_prob, meanList, sDevList):
    # initialize the sum with prior prob
    midichlorian_count = math.log(prior_prob)
    # add each feature prob to the sum
    for i in range(57):
        # hackery fix for domain errors
        # log(termOne / termTwo) == log(termTwo) - log(termOne)
        term_one, term_two = probOfFeatureGivenClass(float(instance[i]), meanList[i], sDevList[i])
        foo = math.log(term_one)
        bar = math.log(term_two)
        prob_for_this_feature =  foo - bar
        midichlorian_count = midichlorian_count + prob_for_this_feature
    
    return midichlorian_count

#-----------------------------------
# get the metrics for the test set
def getMetrics():
    is_pos_chose_pos = 0
    is_pos_chose_neg = 0
    is_neg_chose_neg = 0
    is_neg_chose_pos = 0
    
    for instance in test_set:
        this_class = int(instance[57])
        sith = midichlorianTest(instance, prob_model['p_prob_neg'], prob_model['mean_neg'], prob_model['sDev_neg'])
        jedi = midichlorianTest(instance, prob_model['p_prob_pos'], prob_model['mean_pos'], prob_model['sDev_pos'])
        
        if this_class == 0:
            if jedi < sith:
                is_neg_chose_neg += 1
            else:
                is_neg_chose_pos += 1
        else:
            if jedi > sith:
                is_pos_chose_pos += 1
            else:
                is_pos_chose_neg += 1
    return is_pos_chose_pos, is_pos_chose_neg, is_neg_chose_neg, is_neg_chose_pos
#---------------------------
# because fun...
def outputYoda():
    print "          .--."
    print "  \`--._,'.::.`._.--'/    "
    print "    .  ` __::__ '  .      "
    print "      -:.`'..`'.:-        "
    print "        \ `--' /          "
    print "\n \"The Force is strong with this one\""
    print "                  - YODA"
    
#----------------------------------------------
# make a pretty confusion matrix to display
def outputConfusionMatrix(pos_chose_pos, pos_chose_neg, neg_chose_neg, neg_chose_pos):
    print "\n\n----- CONFUCIUS SAYS ----"
    print "       pos     neg  "
    print "     _______________"
    print "pos | ", pos_chose_pos," | ", pos_chose_neg
    print "    |_______|_______"
    print "neg | ", neg_chose_pos," | ", neg_chose_neg
    print "    |_______|_______"

#------------------------
# show the accuracy in the best way possible
def outputAccuracy(pos_chose_pos, pos_chose_neg, neg_chose_neg, neg_chose_pos):

    accuracy = (pos_chose_pos + float(neg_chose_neg)) / (pos_chose_pos + pos_chose_neg + neg_chose_neg + neg_chose_pos)
    percent = int(accuracy * 100)
    precision = float(pos_chose_pos) / (pos_chose_pos + neg_chose_pos)
    recall = float(pos_chose_pos) / (pos_chose_pos + pos_chose_neg)
    
    
    print "\n\n    ,-\'\"\"\"`-,    .-----------------." 
    print "  ,' \ _|_ / `.  | ACCURACY =",percent,"% |"    
    print " /`.,'\ | /`.,'\ '--------|--------'"   
    print "(  /`. \|/ ,'\  )      |  H "       
    print "|--|--;=@=:--|--|   |  H  U "      
    print "(  \,' /|\ `./  )   H  U  | "     
    print " \,'`./ | \,'`./    U  | (|)"    
    print "  `. / \"\"\" \ ,'     | (|)"
    print "    '-._|_,-`      (|)"
    print "\n .-----------------." 
    print " | PRECISION =",precision    
    print " '-----------------'" 
    print " .-----------------." 
    print " | RECALL =",recall    
    print " '-----------------'" 
#----------------------
# output results of jediBloodTest
def outputResults(pos_chose_pos, pos_chose_neg, neg_chose_neg, neg_chose_pos):
    outputConfusionMatrix(pos_chose_pos, pos_chose_neg, neg_chose_neg, neg_chose_pos)
    outputAccuracy(pos_chose_pos, pos_chose_neg, neg_chose_neg, neg_chose_pos)

#========
# MAIN  |
#========
if __name__ == "__main__":
    outputYoda()
    pos_chose_pos, pos_chose_neg, neg_chose_neg, neg_chose_pos = getMetrics()
    outputResults(pos_chose_pos, pos_chose_neg, neg_chose_neg, neg_chose_pos)