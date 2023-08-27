# Puzzle class is used to create the puzzle
# it generates the answer word
# it receives guesses and returns the clues 
# The clues reveals letters in the word and whether it is in the correct location
# puzzle is solved until the corret word is received
# input word must obey the rules
# add function to print debug messages.
# add option to print messages to terminal or the log file 
# if messages preinted to log file a it should create a log file
from random import randint
from string import ascii_lowercase

class Puzzle(object):

    def __init__(self,wordlist,wordlength,maxguess):
        self.__answer = ""                      # stores answer to the puzzle
        self.__statusflag = 0                   # 0 = in play, 1 = max guess, 2 = solved
        self.__guesslist = []                   # list to store all input guesses
        self.__guessclues = []                  # list of clues 0 = not in word, 1 = in word but not in position, 2 = in word and position
        self.__wordslist = wordlist             # list of all possible words
        self.__puzzlenumber = 0                 # puzzle number set to zero when class is initialized 
        self.__letters = dict()                 # dictionary containing key 0 - good letters key 1 - bad letters
        self.__initializeletters()              # initialize good letters to all alphabets and bad letters to empty list
        self.__WORDLENGTH = wordlength          # number of letters in the word
        self.__MAXGUESS = maxguess              # maximum number of guesses

    def __initializeletters(self):    
        self.__letters[0] = [i for i in ascii_lowercase]
        self.__letters[1] = []

    def newpuzzle(self):                        # method to generate new puzzle
        self.__answer = self.__wordslist[randint(0,len(self.__wordslist))]      #selects random word
        self.__statusflag = 0                   # 0 = unsolved, 1 = solved
        self.__guesslist = []                   # list to store the guesses
        self.__guessclues = []                  # list of clues 0 = not in word, 1 = in word but not in position, 2 = in word and position  
        self.__initializeletters()              # initialize good letters to all alphabets and bad letters to empty list
        self.__puzzlenumber += 1                # update puzzle number

    def acceptword(self,guessword):                     # receive guess word and update clues and lists
        self.__guesslist.append(guessword)                  # add guess word to list
        self.__guessclues.append("")                        # initialize guess clue    
        for i in range(self.__WORDLENGTH):                   # update clues and good/bad letters
            if guessword[i] in self.__answer:                # is guess letter in answer
                if guessword[i] == self.__answer[i]:         # is guess letter in the correct position
                    self.__guessclues[-1] += "2"             # green tile
                else:
                    self.__guessclues[-1] += "1"            # yellow tile
            else:                                           # guess letter not in answer word (grey tile)        
                self.__guessclues[-1] += "0"
                if guessword[i] not in self.__letters[1]:   # current letter not in bad letter list?    
                    self.__letters[1].append(guessword[i])  # add guess letter to bad letter
                    self.__letters[1].sort()                # sort bad letters
                    self.__letters[0].remove(guessword[i])  # remove guess letter from good letters
    
    def getstatusflag(self):
        if len(self.__guesslist) > 0:
            if self.__guessclues[-1] == "2"*self.__WORDLENGTH:
                self.__statusflag = 2                       # game is won
            else:
                if len(self.__guesslist) >= self.__MAXGUESS:
                    self.__statusflag = 1                    # game is lost
                else:
                    self.__statusflag = 0                  # game is still in play
        else:
            self.__statusflag = 0
        return self.__statusflag

    def getanswer(self):
        return self.__answer

    def getguessnumber(self):
        return len(self.__guesslist)

    def getguesslist(self):
        return self.__guesslist

    def getguessclues(self):
        return self.__guessclues
    
    def getgoodletters(self):
        return self.__letters[0]

    def getbadletters(self):
        return self.__letters[1]

    def getpuzzlenumber(self):
        return self.__puzzlenumber
