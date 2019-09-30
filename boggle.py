# @author ALiu
# @date 3/20/18 - 4/9/18
# Boggle Program

# Note: to improve time efficiency, think about caching constant data (e.g. dictionary words)
# Or, maybe perform binary search on word set

import sys
import math
import re

'''
Assignment: Make a program that finds all words given a boggle configuration
Notes: 
- For 4x4 configuration, words need to be at least:
    - 3 letters in length for a 4x4 board
    - 4 letters in length for anything else
- Words cannot have any weird (including periods, dashes, apostrophes, and spaces) or capital characters
- Special scenario: if there is a number, then the following group of letters (with length of number) as a square
'''

# Defining methods here:

# Basic method: Brute force
# Arguments: wordList -- the current list of words that are valid, row coord, column coord
def bruteForce(board, wordSet, r, c, dim, myDict):
    ret = set()
    myQ = []
    start = ((r, c), "", set())  # coordinates + word
    # visited = set()
    myQ.append(start)
    indexSet = {i for i in range(dim)}
    while myQ:
        removed = myQ.pop(0)
        visited = removed[2]
        coords = removed[0]
        currword = removed[1]
        if len(currword) > dim**2:
            continue
        r = coords[0]
        c = coords[1]
        newLetter = board[r][c]
        tempword = currword + newLetter
        if tempword in myDict[len(tempword)][1]:
            ret.add(tempword)
        for x in {-1, 0, 1}:
            if r+x in indexSet:
                for y in {-1, 0, 1}:
                    tempSet = visited.copy()
                    tempSet.add(coords)
                    if (x, y) != (0, 0) and c+y in indexSet and (x+r, c+y) not in tempSet and tempword in myDict[len(tempword)][0]:
                        myQ.append(((r+x, c+y), tempword, tempSet))
    return ret

def bF(board, wordSet, dim):
    ret = set()
    trie = maketrie(wordSet)
    for r in range(dim):
        for c in range(dim):
            temp = bruteForce(board, wordSet, r, c, dim, trie)
            ret = ret | temp
    return ret

# # V2: Create a trie (prefix tree) with all of the words

def maketrie(wordSet):
    ret = {}
    for myWord in wordSet:
        for i, letter in enumerate(myWord):
            if i+1 not in ret:
                ret[i+1] = ({myWord[:i+1]}, set())
            else:
                ret[i+1][0].add(myWord[:i+1])
        ret[len(myWord)][1].add(myWord)
    return ret

def trieSearch(word, wordSet):
    return False

##################################################

def main():
    # Purpose of this block of code: Input Processing
    # - Command line processing
    # - Filtering out faulty boards
    # - File input (words)
    # - Variable declarations
    # Afterwards, there should be:
    # - tile set (the set of letters, includes the grouped letters)
    # - Dimension of the board
    # - Minimum length of words that need to found

    # Board processing
    board = sys.argv[1].lower()
    dim = 0
    letters = []
    processIndex = 0
    processChar = ''
    while processIndex < len(board):
        nextChar = board[processIndex]
        if board[processIndex] in "1234567890":
            nextChar = board[processIndex+1:processIndex+1+int(board[processIndex])]
            processIndex += int(board[processIndex])
        letters.append(nextChar)
        processIndex += 1
    if math.sqrt(len(letters)) - int(math.sqrt(len(letters))) > 0:
        print("This board is invalid. Re-run this program with a valid board.")
        exit(0)
    else:
        dim = int(len(letters)**0.5)
    minLength = 4 if dim >= 5 else 3 if dim == 4 else 3 # min word requirement
    boggle = [letters[i*dim:i*dim+dim] for i in range(dim)]  # make a 2D representation of the board

    # Dictionary processing
    # dictFile = "wordss"
    dictFile = "scrabble.txt"
    words = set()  # maybe turn into list
    boggleRgx = re.compile(r'^[a-z]{' + re.escape(str(minLength)) + ',}$')
    with open(dictFile, 'r+') as f:
        for line in f.readlines():
            # word = line.strip()
            word = line.strip().lower()  # use if using scrabble dictionary
            if boggleRgx.search(word):
                words.add(word)

    results = bF(boggle, words, dim)
    # for result in results:
    #     print(result)
    alphaOrder = sorted(results)
    scoringDict = {}
    for result in results:
        score = 0
        length = len(result)
        if length <= 4:
            score = 1
        elif length == 5:
            score = 2
        elif length == 6:
            score = 3
        elif length == 7:
            score = 5
        else:
            score = 11
        if score not in scoringDict:
            scoringDict[score] = {result}
        else:
            scoringDict[score].add(result)
    boardScore = sum([key * len(scoringDict[key]) for key in scoringDict])
    print("Score of board with {} dictionary: {}".format(dictFile, boardScore))
    print("\nListing of words by score order")
    for scoreKey in scoringDict:
        print("{}-point words: {}".format(scoreKey, scoringDict[scoreKey]))
    print("\nListing of words in alphabetic order:")
    for item in alphaOrder:
        print(item)
    print(len(alphaOrder))

    '''
    Some results: (using wordss)
    - abcdefghijklmnop: fie, fin, fink, glop, ink, knife, lop, mink, pol
    - 
    '''

if __name__ == '__main__':
    main()

# { Program written by: 2019aliu }

'''
Original Assignment:
  
- Given a square (normally 4x4, 5x5, or 6x6) board, determine all (scrabble proper) words according to the rules of Boggle.  
- For 4x4 boards, words must be of length 3 or more. For boards that are 5x5 or larger words should be at least 4 characters in length.  
- As with Scrabble, no foreign characters, capital letters, or any punctuation (including periods, dashes, apostrphes, or spaces) are permitted.  
- Abbreviations are also not permitted, but our dictionary may not differentiate on this basis (so you don't have to worry about it).
- Two special cases for the input:
    - An underscore (rather than a dash) means that the die in question shows no letter.
    - If the die shows more than one letter, than indicate it with a digit specifying the number of letters that die is to have.  
      The usual example here is 2qu.  3thr is another example.
Due date: Due on the Monday after we return from spring break (9 Apr)
'''
