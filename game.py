import logging
from puzzle import Puzzle
from sty import fg, bg, rs
import os

# game parameters :

WORDLENGTH = 5                                                                  # number of letters in word
MAXGUESSES = 6                                                                  # maximum guesses
LOGFILE = "human_game.log"                                                      # log file name
WORDLISTFILE = "words.txt"                                                      # word list file name
PRINTPUZZLE = True                                                              # print puzzle box
PRINTDEBUG = True                                                               # print all messages to log if True
SCREENCLEAR = True

# global variables :

wordlist = []
guesswords = []
guessclues = []
guessword = ""

# function definitions :

def screenclear():
    if SCREENCLEAR == True:
        # for mac and linux(here, os.name is 'posix')
        if os.name == 'posix':
            os.system('clear')
        else:
        # for windows platfrom
            os.system('cls')

def setlogger():
    if PRINTDEBUG == True:
        logging.basicConfig(filename=LOGFILE, filemode='w', level=logging.DEBUG)
    else:
        logging.basicConfig(filename=LOGFILE, filemode='w', level=logging.CRITICAL)

def loadwordlist():
  wordfile = open(WORDLISTFILE,"r")
  totalwords = int(wordfile.readline().strip("\n"))
  [wordlist.append(wordfile.readline().strip("\n")) for i in range(totalwords)]

def printerrormessage(errorcode):
    if errorcode == 1:
        print("***only alphabets allowed**")
        logging.debug("input should only contain alphabets")
    elif errorcode == 2:
        print("**word is too long**")
        logging.debug("input word is too long")
    elif errorcode == 3:    
        print("**word is too short**")
        logging.debug("input word is too short") 
    elif errorcode == 4:
        print("**word has been entered previously**")
        logging.debug("input word has already been entered previously")         
    elif errorcode == 5:
        print("**word is not found in word list**")
        logging.debug("input word is not found in word list")

def isalphacheck():
    return 1 if guessword.isalpha() == False else 0
    
def wordlengthcheck():
    ret = 0
    if len(guessword) > WORDLENGTH:
        ret = 2
    elif len(guessword) < WORDLENGTH:
        ret = 3
    return ret

def checknorepeatition():
    return 4 if guessword in guesswords else 0
        
def checkinwordslist():
    return 5 if guessword not in wordlist else 0

def checkguess():
    ret = isalphacheck()                            # check if only alphabets
    if ret == 0 :
            ret = wordlengthcheck()                 # check length                    
            if ret == 0 :
                ret = checknorepeatition()          # check repetition
                if ret == 0 : 
                    ret = checkinwordslist()        # check in dictionary
    return ret

def maketile(letter,color):
    tile = ""
    if color == "2":
        tile = " " + fg.white + bg.green + " " + letter.upper() + " " + rs.bg + rs.fg + " "
    if color == "1":
        tile = " " + fg.white + bg.yellow + " " + letter.upper() + " " + rs.bg + rs.fg + " "
    if color == "0":
        tile = " " + fg.black + bg.grey + " " + letter.upper() + " " + rs.bg + rs.fg + " "
    return tile

def printblanktiles():
    tile = " " + bg.black + "   " + rs.bg + " "
    print(tile * WORDLENGTH)

def newline():
    print("\n")

def printpuzzlebox():
    if PRINTPUZZLE == True:
        guessnumber = len(guesswords)
        for j in range(guessnumber):                    # print guess words first
            guesstileline = ""
            for k in range(WORDLENGTH):
                guesstileline +=  maketile(guesswords[j][k],guessclues[j][k])
            print(guesstileline)
            newline()
        for k in range(MAXGUESSES - guessnumber):       # print blank tiles next
            printblanktiles()
            newline()

def puzzleboxtolog():
    toprint = "\n"
    guessnumber = len(guesswords)
    for j in range(guessnumber):                                    # print guess words first
        for k in range(WORDLENGTH):
            if guessclues[j][k] == "0":
                toprint +=  " " + guesswords[j][k].lower() + "."    # not in word
            elif guessclues[j][k] == "1":
                toprint += " " + guesswords[j][k].lower() + " "     # wrong position
            elif guessclues[j][k] == "2":
                toprint += " " + guesswords[j][k].upper() + " "     # right position
        toprint += "\n"
    for k in range(MAXGUESSES - guessnumber):                       # print blank tiles next
        toprint += " _ " * WORDLENGTH
        toprint += "\n"
    toprint += "good letters: " + str(puzzle.getgoodletters()) + "\n"
    toprint += "bad letters: " + str(puzzle.getbadletters())
    logging.debug("%s",toprint)

# main code
playagain = "y"
screenclear()
print("Welcome to my wordle!\n")
loadwordlist()
setlogger()
puzzle = Puzzle(wordlist,WORDLENGTH,MAXGUESSES)
logging.debug("Wordle has started")
while(playagain == "y"): 
    puzzle.newpuzzle()
    guessclues = puzzle.getguessclues()
    guesswords = puzzle.getguesslist()
    logging.debug("Puzzle no %s has been initialized", puzzle.getpuzzlenumber())
    # print(puzzle.getanswer())
    while(puzzle.getstatusflag() == 0):
        printpuzzlebox()
        print("Good letters : " + str(puzzle.getgoodletters()))
        print("Bad letters  : " + str(puzzle.getbadletters()))
        guessword = input("Enter your guess  : ").lower()
        screenclear()
        errorcode = checkguess() 
        if errorcode == 0:
            logging.debug("\"%s\" has been entered to guess list", guessword)
            puzzle.acceptword(guessword)
        else:
            logging.debug("\"%s\" has not been entered to guess list", guessword)
            printerrormessage(errorcode)
            print("Try again:\n")
    result=puzzle.getstatusflag()
    printpuzzlebox()
    puzzleboxtolog()
    if result == 1:
        print("The answer is: " + puzzle.getanswer())
        print(" Better luck next time")
        logging.debug("You lost the game. Answer was \"%s\"", puzzle.getanswer())
    elif result == 2:
        print("great job!")
        logging.debug("you win the game")
    playagain = input("play again?[y/n]:")
    screenclear()
logging.debug("you exitted the game")
print("Goodbye!")


