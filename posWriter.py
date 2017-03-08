from collections import Counter 
import glob, os, re 
from collections import defaultdict    
import nltk 
import sys  

#define the reader
def read_file(filename):
    infile = open(filename) 
    contents = infile.read()
    infile.close()
    return contents  

import nltk 
import sys  

#Need to download all the NLTK data and functions, including the Brown corpus
#nltk.download() 

from nltk.corpus import brown  

word_tagUNIV_pairs = [] 
for sent in brown.tagged_sents(tagset='universal'): 
    #Need to add the start node - a word and tag for beginning point
    word_tagUNIV_pairs.append(("INIT","INIT"))  
    #Loop over all pairs and add them to the list
    word_tagUNIV_pairs.extend([ (tag, word) for (word, tag) in sent]) 
    #Need to add the end node - a word and tag for ending point
    word_tagUNIV_pairs.append(("ENDING","ENDING"))  

#First create conditional counts
cond_TagUNIV = nltk.ConditionalFreqDist(word_tagUNIV_pairs)  

#Convert the conditional counts to probabilities 
prob_TagUNIV = nltk.ConditionalProbDist(cond_TagUNIV, nltk.MLEProbDist)  

#First create lists containing the sequences of tags
tagSeqUNIV = [tag for (tag, word) in word_tagUNIV_pairs]  

#Then turn them into tag bi-pairs and compute the conditional freqency 
condSeqUNIV = nltk.ConditionalFreqDist(nltk.bigrams(tagSeqUNIV))  

#And convert the conditional counts to probabilities 
probSeqUNIV = nltk.ConditionalProbDist(condSeqUNIV, nltk.MLEProbDist)  

#I'm going to need all the unique tags later on so I define them here for both tag sets
uniqueTagsUNIV = set(tagSeqUNIV)  


#The hidden markov model is trained and parts of speech can be predicted using this #function
def getPosPredictions(query): 
    queryLen = len(query) 

    #Container for a dictionary at each state that has the best forward sequence
    forwardMap = [] 

    #Container fr a dictionary at each state that has the best backward sequence
    backwardMap = [] 

    #Need to add in that pesky initial state and see the probabilities of transitioning to all tags
    firstForwardState = {} 
    firstBackwardState = {} 
    for tag in uniqueTagsUNIV: 
        if tag == "INIT":continue 
        firstForwardState[tag] = probSeqUNIV["INIT"].prob(tag) * prob_TagUNIV[tag].prob(query[0]) 
        firstBackwardState[tag] = "INIT" 

    #This gives the hidden Markov model its initial state. Add this state to the forward and backward  
    #maps then begin iterating forward until I have to deal with the end state 

    forwardMap.append(firstForwardState) 
    backwardMap.append(firstBackwardState) 

    #Something going wrong in this loop
    for i in range(1,queryLen): 
        currentForwardState = {}  
        currentBackwardState = {} 
        prevForwardState = forwardMap[-1] 


        #For each tag, look at the previous tag state and  
        #transition based on the best probability for the sequence ending in the current state 

        for tag in uniqueTagsUNIV:
            if tag == "INIT":continue 
            bestPrior = max(prevForwardState.keys(),key = lambda prevtag: prevForwardState[prevtag] * probSeqUNIV[prevtag].prob(tag) * prob_TagUNIV[tag].prob(query[i])) 
            currentForwardState[tag] = prevForwardState[bestPrior] * probSeqUNIV[bestPrior].prob(tag) * prob_TagUNIV[tag].prob(query[i]) 
            currentBackwardState[tag] = bestPrior  

        forwardMap.append(currentForwardState) 
        backwardMap.append(currentBackwardState)  

    #Now handle the end states - this sets up the position where we start looking backward through the map
    prevState = forwardMap[-1] 
    bestEndState = max(prevState.keys(), key = lambda prevtag: prevState[prevtag] * probSeqUNIV[prevtag].prob("ENDING")) 
    probEndTags = prevState[bestEndState] * probSeqUNIV[bestEndState].prob("ENDING") 
    bestEndTag = ["ENDING", bestEndState] 

    #Defined the state before the end, so start there and work through the backward map 
    #Reverse the backward map and step through one state at a time
    backwardMap.reverse() 

    currentBestTag = bestEndState
    for state in backwardMap: 
        bestEndTag.append(state[currentBestTag]) 
        currentBestTag = state[currentBestTag] 

    #After stepping backward through the list and recording the tags, reverse that recorded 
    #list and we have the best sequence!
    bestEndTag.reverse()  
    
    finalTags = bestEndTag[1:-1]
    wordTagPairs = zip(query, finalTags) 
    return wordTagPairs 


#Write the docs
import io 


for i in range(1,1401):   
    wordTags = []
    n = str(i)
    curName = "data/CranfieldDocsParse/parsed" +  str(n.rjust(4, '0'))
    text = read_file(str("data/CranfieldDocsParse/parsed" + str(n.rjust(4,'0')) + ".txt"))  
    text2 = text.split('.')   
    for sent in text2: 
        #parseSent = sent.split(' ')   
        #preds = getPosPredictions(parseSent)   
        parseSent = nltk.word_tokenize(sent)
        preds = nltk.pos_tag(parseSent) 
        nounsOnly = [t[0] for t in preds if t[1] == 'NN']  
        nounString = ' '.join(nounsOnly)
        wordTags.append(nounString) 
    outText = str(''.join(wordTags))
    with io.open("data/CranfieldDocsPOS/posDoc" + str(n.rjust(4,'0')) + ".txt", 'wb') as f: 
        f.write(outText) 
    i += 1

