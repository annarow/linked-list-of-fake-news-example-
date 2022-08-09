import csv
import string
import sys
sys.setrecursionlimit(2500)
"""
    File: fake-news-ms.py
    Author: Anna Rowena Waldron
    Purpose: To analyze recent data about fake news articles by taking titles
        and seeing which words are used the most to distinguish topics.
    Course/Sect: CSC 120, Spring 2018, 1G
"""

class Word:
    """Class creates objects containing informating about a word that is
    used in the titles of fake news articles. Holds attributes of the word,
    the number of times the word appears in titles."""
    def __init__(self, word):
        self._word = word
        self._count = 1
    def word(self):
        return self._word
    def count(self):
        return self._count
    def incr(self):
        self._count += 1
    def __str__(self):
        return "{} : {}".format(self._word, self._count)
    
    
def process():
    """Function which uses user input to take a file and process the titles
    of the file into a list of cleaned words of length 3 or more. Uses try
    and except for opening the file then processes each title line to strip
    words of punctuation and white space and appends to a list.
    Returns: a list of cleaned words of titles.
    Post-Condition: the list contains lower case words of length 3 or more."""
    filename = input('File: ')
    try:
        file = open(filename)
    except FileNotFoundError:
        print('ERROR: Could not open file ' + filename)
        sys.exit()
    read_csv = csv.reader(file)
    new = []
    for itemlist in read_csv:
        if itemlist[0][0] == '#':
            continue
        words = itemlist[4].lower().split()
        for j in words:
            word = ''
            for letter in j:
                if letter in string.punctuation or letter in string.whitespace:
                    if len(word) > 2:
                        new.append(word)
                        word = ''
                    if len(word) < 2:
                        word = ''
                else:
                    word += letter
            if len(word) > 2:    
                new.append(word)
    file.close()
    return new

def creation(clean):
    """Function which creates a list of word objects and incriments the
    number of times the word appears. Takes paramter of a list of cleaned
    words with no punctuation. Retuns the list of objects."""
    prime = []
    for j in clean:
        check = 0 
        for i in prime:
            if i.word() == j:
                i.incr()
                check = 1
                break
        if check == 0 or len(prime) == 0:
            new = Word(j)
            prime.append(new)

    return prime

def msort(L):
    """Recursive function taken from class notes which sorts the objects
    in the list. Takes the list as a parameter and calls another recursive
    function merge. Returns the merged list."""
    if len(L) <= 1:
        return L
    else:
        split = len(L) // 2
        L1 = L[:split]
        L2 = L[split:]
        sortedL1 = msort(L1)
        sortedL2 = msort(L2)
        return merge(sortedL1, sortedL2, [])

def funny(M1, M2):
    """Helper function which determines which object should be ahead
    of another depending on count and alphabet. Returns a boolean and
    takes two word objects as parameters."""
    if M1[0].count() > M2[0].count():
        return True
    elif M1[0].count() == M2[0].count() and M1[0].word() < M2[0].word():
            return True
    else:
        return False

def merge(L1, L2, merged):
    """Recursive function taken from class notes which is called in msort
    recursive function. Takes two word objects lists and combines them
    with the already merged list. Returns the merged list."""
    if L1 == [] or L2 == []:
        return merged + L1 + L2
    else:
        if funny(L1, L2) == True:
            n_merge = merged + [L1[0]]
            new_L1 = L1[1:]
            new_L2 = L2
        else:
            n_merge = merged + [L2[0]]
            new_L1 = L1
            new_L2 = L2[1:]
        return merge(new_L1, new_L2, n_merge)
            
def printing(tot, n):
    """Function which takes a list of word objects tot and a value n and
    determines if n is an integer which is the count of word occurences
    of the word at position n found from the previously. Prints out
    the word object words that have counts that are greater than or equal
    to the value K."""
    try:
        n = int(n)
    except ValueError:
        print("ERROR: Could not read N")
        sys.exit()
    assert n >= 0
    b = tot
    value = tot[n]
    value = value.count()
    for j in b:
        if j.count() >= value:
            print(j)
        
    
            

def main():
    """Main function which calls all other functions. Catches returns of
    list of cleaned words, list of word objects, and sorted list of objects.
    Uses user input to find which words to print out."""
    new = process()
    w_list = creation(new)
    catch = msort(w_list)
    N = input('N: ')
    printing(catch, N)

    
    
"""calls main."""
main()
