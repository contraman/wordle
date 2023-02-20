#wordle bot class

import logging
from random import randint
import numpy as np
from string import ascii_lowercase

class Bot(object):

    def __init__(self,wordlist,wordlength,maxguess):                            # initialize bot class
        self.__MAXGUESS = maxguess                                              # max numbmber of guesses
        self.__WORDLENGTH = wordlength                                          # max word length        
        self.__wordlist = [wordlist[:]]                                         # list of allowable words for a particular guess
        self.__lettercolor = dict()                                             # dict to store letter color clues
        self._initializelettercolors()                                          # initialize letter color clues 
        self.__guesslist = []                                                   # stores all guesses made
        self.__guessclues = []                                                  # stores guess color code
        self.__playhistory = []                                                 # stores status of each game
        self.__evalue = 0                                                       # mean win guess if game is won
        self.__winhistory = np.zeros(self.__MAXGUESS+1)                         # stores number of wins based on number of guesses. guess 0 = game was lost
        self.__successrate = 0                                                  # number of wins / number of games played
        self.__avgguestime = np.zeros(self.__MAXGUESS)                          # average guess time for each guess         
        self.__guesscount = np.zeros(self.__MAXGUESS)                           # number of 
        
    def botreset(self):                                                         # reset bot class        
        self.__wordlist = self.__wordlist[1][:]                                 # word list reset to first guess
        self.__initializelettercolors()                                         # clear guess color clues
        self.__guesslist = []                                                   # guess list cleared
        self.__guessclues = []                                                  # guess clues cleared                                            

    def _initializelettercolors(self):                                          # stores clue color info for each letter and position for each clue
        self.__lettercolor["2"] = {1:"",2:"",3:"",4:"",5:""}                    # green letter values: key - position, value - letters
        self.__lettercolor["1"] = {1:set(),2:set(),3:set(),4:set(),5:set()}     # yellow letter clues: key - position, value - letters
        self.__lettercolor["0"] = set()                                         # grey letter stores only letters
        self.__lettercolor["-1"] = set(list(ascii_lowercase))                   # letter color unknown
                
    def _updateguessinfo(self):                                                 # updates color clue and positon based on guesslist and guessclues
        ret = 0
        for i in range(self.__WORDLENGTH):
            guesscluei = self.__guessclues[-1][i]                               # ith guess color of latest guess        
            guesswordi = self.__guesslist[-1][i]                                # ith letter of latest guess     
            self.__lettercolor["-1"].discard(guesswordi)                        # remove letter from unknown clue
            if  guesscluei == "0":                                              # if letter is not in word
                self.__lettercolor["0"].add(guesswordi)                         # add to grey letter set
            elif guesscluei == "1":                                             # if clue is yellow
                self.__lettercolor["1"][i].add(guesswordi)                      # add letter to yellow clue dict
            elif guesscluei == "2":                                             # if clue is green
                if self.__lettercolor["2"][i] == "":                            # if letter was not enter previously
                    self.__lettercolor["2"][i].add(guesswordi)                  # add letter to green clue dict
                else:
                    ret = 1                                                     # error 1: cannot add letter, position is filled
            else:
                    ret = 2                                                     # error 2 : cannot determine clue ]
        return ret                                                              # if update failed return False else True

    def updatestats(self,gamestatus):                                           # update game status after a game is over
        ret = 0
        if gamestatus == 2 or gamestatus == 1:                                  # if game won or lost
            if gamestatus == 1:                                                 # if game lost
                self.__playhistory.append(0)                                    # append 0
                self.__winhistory[0] += 1                                       # increment 1 to index 0 (lost)
            elif gamestatus == 2:                                               # if game won
                self.__playhistory.append(len(self.__guesslist))                # append guess win number
                self.__winhistory[len(self.__guesslist)] += 1                   # increment 1 the guess win number index
            played = len(self.__playhistory)                                    # update number of games played
            wins = np.sum(self.__winhistory[1:])                                # get number of games won
            self.__successrate = wins/played                                    # calculate success rate
            winprob = self.__winhistory/wins                                    # calculate probability of winning at a particular guess number
            self.__evalue = np.dot(winprob,np.arange(1,self.__MAXGUESS+1))      # calculate expectation value
        else:                                                                  
            ret = 1                                                             # error 1: game is not finished
        return ret

    def selectrandomword(self):                                                 # pops word from latest word list
        ret = 0
        listlength = len(self.__wordlist[-1])                                   # get length of latest word list
        if listlength > 1:                                                         # if length more than 1
            wordindex = randint(0,listlength)                                   # select random index
            self.__guesslist.append(self.__wordlist.pop(wordindex))             # select randome word and append to guest list
        elif listlength == 1:                                                      # if only one word left
            self.__guesslist.append(self.__wordlist.pop(0))                     # select last word
        else:               
            ret = 1                                                             # error 1 : no words remaining in guess list
        return ret
    
    def newwordlist(self):
        self.__wordlist.append(self.__wordlist[-1])
    
    def filteryellowletters(self):
        ret = 0
        templist = []                                                           # temp list to store filtered words
        listlength = len(self.__wordlist[-1])                                   # get length of latest word list
        if listlength > 1:                                                      # if word list more than 1
            for word in self.__wordlist[-1]:                                    # loop over word list
                for i in range(self.__WORDLENGTH):                              # loop over position
                    yellowletteri = self.__lettercolor["1"][i]                  # get yellow letters at position i
                    if yellowletteri != word[i]:                                # if position of yellow letter not in word
                        templist.append(word)                                   # add to temp list
            self.__wordlist[-1]=[word for word in self.__wordlist[-1] 
                                 if word not in templist]                       # remove words that are in temp list
            if len(self.__wordlist[-1]) == 0:
                ret = 2                                                         # error 2: no word left in word list
        elif listlength == 1:
            ret = 1                                                             # error 1:  one word left, filter cancelled
        else:
            ret = 2                                                             # error 2: no word left in word list
        return ret

    def filterbadletters(self):
        ret = 0
        templist = []                                                           # temp list to store filtered words
        listlength = len(self.__wordlist[-1])                                   # get length of latest word list
        if listlength > 1:                                                      # if word lis more than 1
            for word in self.__wordlist[-1]:                                    # loop over word list
                if self.__lettercolor["0"].isdisjoint(set(word)):               # if no bad letter in word
                        templist.append(word)                                   # add to temp list
            self.__wordlist[-1] = templist                                      # remove words that are in temp list
            if len(self.__wordlist[-1]) == 0:
                ret = 2                                                         # error 2: no word left in word list
        elif listlength == 1:
            ret = 1                                                             # error 1:  one word left, filter cancelled
        else:
            ret = 2                                                             # error 2: no word left in word list
        return ret
        
    def filtergreenletters(self):
        ret = 0
        templist = []                                                           # temp list to store filtered words
        listlength = len(self.__wordlist[-1])                                   # get length of latest word list
        if listlength > 1:                                                      # if word list more than 1
            for word in self.__wordlist[-1]:                                    # loop over word list
                for i in range(self.__WORDLENGTH):                              # loop over position
                    greenletteri = self.__lettercolor["2"][i]                   # get green letter at position i
                    if greenletteri.islower() and greenletteri != word[i]:      # if position of green letter not in word
                        templist.append(word)                                   # add to temp list
            self.__wordlist[-1]=[word for word in self.__wordlist[-1] 
                                 if word not in templist]                       # remove words that are in temp list
            if len(self.__wordlist[-1]) == 0:
                ret = 2                                                         # error 2: no word left in word list
        elif listlength == 1:
            ret = 1                                                             # error 1:  one word left, filter cancelled
        else:
            ret = 2                                                             # error 2: no word left in word list
        return ret
                            