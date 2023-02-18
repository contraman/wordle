from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.error import URLError 
import string
from time import time

answerfile = "answerfile.txt"
WORDLISTFILE = "words.txt"                  # word list file name

wordlist = []

def loadwordlist():
  wordfile = open(WORDLISTFILE,"r")
  totalwords = int(wordfile.readline().strip("\n"))
  [wordlist.append(wordfile.readline().strip("\n")) for i in range(totalwords)]

s=time()
loadwordlist()
try:
    url = "https://www.rockpapershotgun.com/wordle-past-answers"
    page = urlopen(url,timeout = 3)
    html = page.read().decode("utf-8")
    soup = BeautifulSoup(html, "html.parser")
    pagetext = soup.get_text()
    headertext = "All Wordle answers"
    startpos = pagetext.find(headertext) + len(headertext) + 2
    answerlist = []
    while(pagetext[startpos] != "\n"):
    	word=pagetext[startpos : startpos + 5].lower()
    	if word not in wordlist:
    		break
    	answerlist.append(word)
    	startpos += 6        
    print(len(answerlist))

except URLError as err:
    print("No internet connection")
    
print(time()-s)

