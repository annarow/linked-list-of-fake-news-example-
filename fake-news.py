import csv
import string
import sys
"""
    File: fake-news.py
    Author: Anna Rowena Waldron
    Purpose: To analyze recent data about fake news articles by taking titles
        and seeing which words are used the most to distinguish topics.
    Course/Sect: CSC 120, Spring 2018, 1G
"""
class Node:
    """This class creates nodes containing informating about a word that is
    used in the titles of fake news articles. Holds attributes of the word,
    the number of times the word appears in titles, and a next attribute
    that links the node to another node."""
    def __init__(self, word):
        self._word = word
        self._count = 1
        self._next = None
    def word(self):
        return self._word
    def count(self):
        return self._count
    def next(self):
        return self._next
    def set_next(self, target):
        """Method sets the next variable. """
        self._next = target
    def incr(self):
        """Method incriments the count of appearences."""
        self._count += 1
    def __str__(self):
        return "{} : {}".format(self._word, self._count)
    
class LinkedList:
    """Class that creates a linked list of node objects. Attirbutes are the
    head of the linked list and the length of the linked list."""
    def __init__(self):
        self._head = None
        self._length = 0
    def is_empty(self):
        return self._head == None
    def head(self):
        return self._head
    def update_count(self, word):
        """Method that takes in a parameter as a string which is a word and
        iterates through the linked list to find that word and increment
        its' count if found if not creates a new node object of the word."""
        orig = self._head
        temp = self._head
        while temp != None:
            prev = temp
            nex = prev.next()
            if word == temp.word():
                temp.incr()
                return
            temp = nex
        c = Node(word)  
        c.set_next(orig)
        self._head = c
        self._length += 1
        if orig == None and self._length == 0:
            self._head = Node(word)
            self._length += 1
        return
    def rm_from_hd(self):
        """Method borrowed from the short problem tweaked to fit this program.
        Removes the head element of the linked list and returns it."""
        r = self._head
        self._head = r.next()
        r.set_next(None)
        return r
    def insert_after(self, node1, node2):
        """Method borrowed from the short problem tweaked to fit this program.
        Inserts a node2 infront of the original node1 and adjusts the next
        attributes."""
        if node1 != None:
            node2.set_next(node1.next())
            node1.set_next(node2)
    def add(self, node):
        """Method borrowed from the short problem tweaked to fit this program.
        Adds a node to the front of the linked list."""
        node.set_next(self._head)
        self._head = node
    def sort(self):
        """Method borrowed from the short problem tweaked to fit this program.
        Sorts the linked list by count of word occurences from greatest to
        least. Creates a new linked list by removing node objects from the
        original list and adds and inserts the objects in correct order to
        the new linked list. sets the head of the linked list class to the
        head node of the sorted linked list."""
        if self._head == None:
            return
        curr_element = self.rm_from_hd()
        sorted_L = LinkedList()
        sorted_L.add(curr_element)
        if self._head != None:
            curr_element = self.rm_from_hd()
        else:
            curr_element = None
        while curr_element != None:
            E = sorted_L._head
            
            if E.count() <= curr_element.count():
                sorted_L.add(curr_element)
            else:
                while E.next() != None and curr_element.count() <= E.count():
                    sorted_E = E
                    E = E.next()
                sorted_L.insert_after(sorted_E, curr_element)
            if (self._head != None):
                curr_element = self.rm_from_hd()
            else:
                curr_element = None
        self._head = sorted_L._head
    def get_nth_highest_count(self, n):
        """Method which takes a value n for the position of a node in the
        linked list. Uses try and excepts and assert to decide if n is a
        valid input. Iterates through the sorted linked list to find the
        node at position n and returns the node when its found."""
        try:
            n = int(n)
        except ValueError:
            print("ERROR: Could not read N")
        assert n >= 0
        orig = self.head()
        play = orig
        place = 0
        while play != None:
            if place == n:
                N_head = play
                return N_head
            place += 1
            prev = play
            nex = prev.next()
            play = nex
    def print_up_to(self, K):
        """Method which takes a value K which is the count of word occurences
        of the node at position n found from the previous method. Prints out
        the node object words that are greater than or equal to the value K.
        """
        orig = self.head()
        play = orig
        place = 0
        while play != None:
            place = play.count()
            if place < K:
                return 
            prev = play
            nex = prev.next()
            print(play)
            play = nex
    def __str__(self):
        return "{} : {}".format(self._head.word(), self._head.count())
    
def creation(words):
    """Function which creates a linked list object then enters a for loop
    to create and update node objects counts by calling the method of the
    linkedlist class. Calls the sort method to sort the newly created
    list.
    Parameters: word is a list of words in titles of fake news articles.
    Returns: a linked list of sorted node objects.
    Pre-Condition: words is a list of strings.
    Post-Condition: link is a linked list of sorted nodes."""
    link = LinkedList()
    for j in words:
        link.update_count(j)
    link.sort()
    return link

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

def main():
    """Main function that calls all other functions. Calls the process
    function and catches the returned list of stringss. Calls the creation
    function with parameter of the list of string and catches the linked
    list as its return. Uses user input to get he value N of the position
    then passes that value as a parameter to linked list's method to find
    the node at the position and catches the returned node. Calls the
    method of linked list to print all the node objects with counts greater
    than or equal to the value K found in the previous method. """
    words = process()
    link = creation(words)
    N = input('N: ')
    node_at_n = link.get_nth_highest_count(N)
    link.print_up_to(node_at_n.count())
    
"""Calls main. """   
main()
