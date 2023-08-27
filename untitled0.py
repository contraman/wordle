#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 23:33:59 2023

@author: dukes
"""

WORDLISTFILE = "words.txt"                  # word list file name
from string import ascii_lowercase
wordlist = []

def initializelettercolors():                                           # stores clue color info for each letter and position for each clue
    lettercolor["2"] = {1:"",2:"",3:"",4:"",5:""}                    # green letter values: key - position, value - letters
    lettercolor["1"] = {1:set(),2:set(),3:set(),4:set(),5:set()}     # yellow letter clues: key - position, value - letters
    lettercolor["0"] = set()                                           # grey letter stores only letters
    lettercolor["-1"] = set(list(ascii_lowercase))                     # letter color unknown

def loadwordlist():
    wordfile = open(WORDLISTFILE,"r")
    totalwords = int(wordfile.readline().strip("\n"))
    [wordlist.append(wordfile.readline().strip("\n")) for i in range(totalwords)]
  
def filteroutbadletters():
    ret = False
    if len(prefilter) > 1 and postfilter == []:
        if len(lettercolor["0"]) > 0:
            for word in prefilter:
                if all([bl not in word for bl in lettercolor["0"]]):
                    postfilter.append(word)
        ret = True
    return ret 
    
loadwordlist()
lettercolor = dict()                                               # dict to store letter color clues
initializelettercolors()                                           # initialize letter color clues 
prefilter=wordlist
s=time()
postfilter=[]
lettercolor["0"].add("a")
filteroutbadletters()
print(time()-s)