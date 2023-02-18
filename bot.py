#wordle bot class

import logging
from random import randint
import numpy as np
from string import ascii_lowercase

class Bot(object):

    def __init__(self,wordlist,wordlength,maxguess):						       # initialize bot class
        self.__MAXGUESS = maxguess											   # max numbmber of guesses
        self.__WORDLENGTH = wordlength										   # max word length        
        self.__wordlist = [wordlist[:]]										   # list of allowable words for a particular guess
        self.__lettercolor = dict()											   # dict to store letter color clues
        self._initializelettercolors()										   # initialize letter color clues 
        self.__guesslist = []												   # stores all guesses made
        self.__guessclues = []												   # stores guess color code
        self.__playhistory = []												   # stores status of each game
        self.__evalue = 0													   # mean win guess if game is won
        self.__winhistory = np.zeros(self.__MAXGUESS+1)						   # stores number of wins based on number of guesses. guess 0 = game was lost
        self.__successrate = 0												   # number of wins / number of games played
        self.__avgguestime = np.zeros(self.__MAXGUESS)                          # average guess time for each guess         
        self.__guesscount = np.zeros(self.__MAXGUESS)                           # number of 
        
    def botreset(self):											               # reset bot class		
        self.__wordlist = self.__wordlist[1][:]							       # word list reset to first guess
        self.__initializelettercolors()										   # clear guess color clues
        self.__guesslist = []												   # guess list cleared
        self.__guessclues = []												   # guess clues cleared											

    def _initializelettercolors(self):										   # stores clue color info for each letter and position for each clue
        self.__lettercolor["2"] = {1:"",2:"",3:"",4:"",5:""}                    # green letter values: key - position, value - letters
        self.__lettercolor["1"] = {1:set(),2:set(),3:set(),4:set(),5:set()}     # yellow letter clues: key - position, value - letters
        self.__lettercolor["0"] = set()                        				   # grey letter stores only letters
        self.__lettercolor["-1"] = set(list(ascii_lowercase))      		       # letter color unknown
                
    def _updateguessinfo(self):									               # updates color clue and positon based on guesslist and guessclues
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

    def updatestats(self,gamestatus):										   # update game status after a game is over
        ret = True
        if gamestatus == 2 or gamestatus == 1:								   # if game won or lost
            if gamestatus == 1:												   # if game lost
                self.__playhistory.append(0)								       # append 0
                self.__winhistory[0] += 1									   # increment 1 to index 0 (lost)
            elif gamestatus == 2:											   # if game won
                self.__playhistory.append(len(self.__guesslist))			       # append guess win number
                self.__winhistory[len(self.__guesslist)] += 1				   # increment 1 the guess win number index
            played = len(self.__playhistory)								       # update number of games played
            wins = np.sum(self.__winhistory[1:])							       # get number of games won
            self.__successrate = wins/played								       # calculate success rate
            winprob = self.__winhistory/wins								       # calculate probability of winning at a particular guess number
            self.__evalue = np.dot(winprob,np.arange(1,self.__MAXGUESS+1))	   # calculate expectation value
        else:
            ret = False
        return ret

    def _resettemplist(self):
        self.__templist1 = self.__templist2[:]
        self.__templist2 = []

    def __copytotemplist(self):
        self.__templist1 = self.__wordlist[-1][:]
        self.__templist2 = []

    def __updatewordlist(self):
        self.__wordlist.append(self.__templist1[:])
        self.__templist1 = []
        self.__templist2 = []

    def selectrandomword(self):
        word = self.__wordlist[-1][randint(0,len(self.__wordlist[-1]))]
        ret = False
        if word not in self.__guesslist:
          #  self.__guesslist.append(word)
            ret = True
        return ret
    
    def sendword(self,word):

    def filteroutyellowletters(self):
        	ret = false
        if len(self.__templist1) > 1 and self.__templist2 == []
        	if len(self.__lettercolor["1"].keys()) > 0:
		        for word in self.__templist1:
		            if all([bl not in word for bl in self.__lettercolor["0"].keys()]):
		                self.__templist2.append(word)
			ret = True
		else:
			#logging.debug("")
		return ret 

    def filteroutbadletters(self):
    	ret = false
        if len(self.__templist1) > 1 and self.__templist2 == []
        	if len(self.__lettercolor["0"].keys()) > 0:
		        for word in self.__templist1:
		            if all([bl not in word for bl in self.__lettercolor["0"].keys()]):
		                self.__templist2.append(word)
			ret = True
		else:
			#logging.debug("")
		return ret 
		
    def filteringreenletters(self):
        if len(self.__templist1) > 1 and len(self.__lettercolor["2"].keys()) > 0:
            for word in self.__wordlist[[-1]]:
                if all(gl[glpos] == word[glpos] and )
