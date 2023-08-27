#wordle bot class

import logging
from random import randint
import numpy as np
from string import ascii_lowercase

class Bot(object):

    def __init__(self,wordlist,wordlength,maxguess):                               # initialize bot class
        self.__MAXGUESS = maxguess                                               # max numbmber of guesses
        self.__WORDLENGTH = wordlength                                           # max word length        
        self.__wordlist = [wordlist[:]]                                           # list of allowable words for a particular guess
        self.__lettercolor = dict()                                               # dict to store letter color clues
        self._initializelettercolors()                                           # initialize letter color clues 
        self.__guesslist = []                                                   # stores all guesses made
        self.__guessclues = []                                                   # stores guess color code
        self.__filterflag = 0                                                   # filter done = 1
        self.__winhistory = np.zeros(self.__MAXGUESS+1)                           # stores number of wins based on number of guesses. index 0 = number of lost games
        self.__guestime = -1*ones(self.__MAXGUESS)                              # average guess time for each guess  -1= guess not made because game already won       
        self.__evalue = 0                                                       # mean win guess if game is won
        self.__prefilter = []                                                   # clear pre filtered list
        self.__postfilter = []                                                  # clear post filtered list
        
    def botreset(self):                                                           # reset bot class        
        self.__wordlist = self.__wordlist[1][:]                                   # word list reset to first guess
        self.__initializelettercolors()                                           # clear guess color clues
        self.__guesslist = []                                                   # guess list cleared
        self.__guessclues = []                                                   # guess clues cleared                                            
        self.__filterflag = 0 
        self.__prefilter = []                                                   # clear pre filtered list
        self.__postfilter = []                                                  # clear post filtered list
        
    def __initializelettercolors(self):                                           # stores clue color info for each letter and position for each clue
        self.__lettercolor["2"] = {1:"",2:"",3:"",4:"",5:""}                    # green letter values: key - position, value - letters
        self.__lettercolor["1"] = {1:set(),2:set(),3:set(),4:set(),5:set()}     # yellow letter clues: key - position, value - letters
        self.__lettercolor["0"] = set()                                           # grey letter stores only letters
        self.__lettercolor["-1"] = set(list(ascii_lowercase))                     # letter color unknown
                
    def __updateguessinfo(self):                                                   # updates color clue and positon based on guesslist and guessclues
        ret = True
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
                    ret = False                                                 # cannot add letter is position is filled
            else:
                    ret = False                                                 # cannot determine clue 
        return ret                                                              # if update failed return False else True

    def updatestats(self,gamestatus):                                           # update game status after a game is over
        ret = True
        if gamestatus == 2 or gamestatus == 1:                                   # if game won or lost
            if gamestatus == 1:                                                   # if game lost
                self.__winhistory[0] += 1                                       # increment 1 to index 0 (lost)
            elif gamestatus == 2:                                               # if game won
                self.__winhistory[len(self.__guesslist)] += 1                   # increment 1 the guess win number index
            played = sum(self.__winhistory)                                       # update number of games played
            wins = np.sum(self.__winhistory[1:])                                   # get number of games won
            self.__successrate = wins/played                                       # calculate success rate
            winprob = self.__winhistory/wins                                       # calculate probability of winning at a particular guess number
            self.__evalue = np.dot(winprob,np.arange(1,self.__MAXGUESS+1))       # calculate expectation value
        else:
            ret = False
        return ret

    def __resettemplist(self):                                                  # use after first filter
        self.__prefilter = self.__postfilter[:]                                 # copy post filtered list to pre filtered list    
        self.__postfilter = []                                                  # clear post filtered list

    def __copytotemplist(self):                                                 # use before first filter
        self.__prefilter = self.__wordlist[-1][:]                               # copy latest word list to pre filter list
        self.__postfilter = []                                                  # clear post filtered list

    def __updatewordlist(self):                                                 # use after filtering is complete
        self.__wordlist.append(self.__prefilter[:])                             # copy post filtered list to update latest word list 
        self.__prefilter = []                                                   # clear pre filtered list
        self.__postfilter = []                                                  # clear post filtered list

    def selectrandomword(self):
        word = self.__wordlist[-1][randint(0,len(self.__wordlist[-1])-1)]       # Select word from latest word list after filtering
        ret = False
        if word not in self.__guesslist:                                        # word not guessed before?
            self.__wordlist[-1].remove(word)                                    # remove word from latest guess list
            self.__guesslist.append(word)                                       # add word to guest list
            ret = True
        return ret

    def filteroutyellowletters(self):                                           # filter out words with letters in yellow position
        ret = False
        if len(self.__prefilter) > 1 and self.__postfilter == []:               # if pre filter updated and post filter cleared
            if len(self.__lettercolor["1"].keys()) > 0:                         # if yellow letter dict not empty
                for word in self.__templist1:
                    if all([bl not in word for bl in self.__lettercolor["1"].keys()]):
                        self.__templist2.append(word)
            ret = True
        return ret 

    def filteroutbadletters(self):
        ret = False
        if len(self.__prefilter) > 1 and self.__postfilter == []:
            if len(self.__lettercolor["0"]) > 0:
                for word in self.__prefilter:
                    if all([bl not in word for bl in self.__lettercolor["0"]]):
                        self.__templist2.append(word)
            ret = True
        return ret 
        
    def filteringreenletters(self):
        if len(self.__templist1) > 1 and len(self.__lettercolor["2"].keys()) > 0:
            for word in self.__wordlist[[-1]]:
                if all(gl[glpos] == word[glpos] and )
