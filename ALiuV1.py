# @author AvocadoLiu
# @date 1/23/18
# Smartly play a move

import sys
import random
import time

inittime = time.clock()

game = "...........................OX......XO..........................."
player = "X"
moves = []

playerchanged = False  # To keep track of whether current player is accurate or not

# Enter and process all arguments
for entry in sys.argv[1:]:
    if entry.upper() in ("X", "O"):
        player = entry.upper()
        playerchanged = True
    elif len(entry) < 3:
        try:
            moves.append(int(entry))
        except:
            row = int(entry[1])-1
            column = ord(entry[0].lower())-97
            index = row*8 + column
            moves.append(index)
    else:
        game = entry.upper()

# Adjust player appropriately
if playerchanged == False:
    countX = sum([1 for myChr in game if myChr == "."])
    if countX & 1 == 0:
        player = "X"
    else:
        player = "O"

print("Original state of board:")
# Display the game
print("\n".join('\t'.join(game[i * 8:i * 8 + 8]) for i in range(int(len(game) ** 0.5))))
print(game, sum([1 for myC in game if myC == "X"]), "/", sum([1 for myC in game if myC == "O"]))
print()

xMoves = {-1, 0, 1}
yMoves = {-1, 0, 1}
possibleIndexes = set(range(8))
indexesToFlip = set()

def withinBounds(index):
    exists = index >= 0 and index <= 63  # check whether index exists on board
    row = index // 8
    column = index % 8
    return exists and row in possibleIndexes and column in possibleIndexes

def nextToOpponent(game, player, index):
    enemyToken = "X" if player == "O" else "O"
    row = index // 8
    column = index % 8
    for X in xMoves:
        for Y in yMoves:
            temp = index + X + Y * 8
            row += Y
            column += X
            if withinBounds(temp) and row >= 0 and row <= 7 and column >= 0 and column <= 7 and game[temp] == enemyToken:
                return True
            row -= Y
            column -= X
    return False

def flanksOpp(board, player, index):
    enemy = "X" if player == "O" else "O"
    game = board[:index] + player + board[index+1:]
    indexesToFlip = set()
    for x in xMoves:
        for y in yMoves:
            direction = x + y * 8
            temp = index
            tokensToFlip = set()
            row = temp // 8  # refers to vertical (y) position, horizontal line across
            column = temp % 8  # refers to horizontal (x) position, vertical line down
            while withinBounds(temp):
                temp += direction
                row += y
                column += x
                if row < 0 or row > 7 or column < 0 or column > 7:
                    break
                currchar = game[temp]
                if currchar == player and len(tokensToFlip) > 0:
                    temp = indexesToFlip | tokensToFlip  # take union of sets to increase indexes to flip
                    indexesToFlip = temp
                    break
                elif currchar != enemy:
                    break
                else:
                    tokensToFlip.add(temp)
    return len(indexesToFlip) > 0

def validMoveSet(game, player):
    validMoves = []
    for i, char in enumerate(game):
        if char == "." and nextToOpponent(game, player, i) and flanksOpp(game, player, i):
            validMoves.append(i)
    return validMoves

##################################################
##################################################

# Lab 6 strategies

def heurmove(game, player):
    corners = {0, 7, 56, 63}
    edges = {1, 2, 3, 4, 5, 6, 8, 15, 16, 23, 24, 31, 32, 39, 40, 47, 48, 55, 57, 58, 59, 60, 61, 62}
    move = -1
    mademove = False
    validMoves = set(validMoveSet(game, player))

    # Strategy 1: Play to corner if at all possible
    if validMoves & corners:
        move = random.sample(validMoves & corners, 1)[0]
        mademove = True

    # Strategy 2: Play to edge if it makes a path with own token to the corners
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]  # (x, y) --> down, right, up, down
    def secureEdge(index):  # any move that passes through here will automatically be an edge
        myStack = []
        for direction in directions:
            row = int(index / 8)
            column = index % 8
            row += direction[0]
            column += direction[1]
            while row >= 0 and row < 8 and column >= 0 and column < 8:
                tIndex = row*8+column
                if game[tIndex] == player and myStack and "." not in myStack and player not in myStack:
                    return True
                myStack.append(game[tIndex])
                row += direction[0]
                column += direction[1]
        return False

    if not mademove:
        for pos in validMoves:
            if pos in edges and secureEdge(pos):
                move = pos
                mademove = True
                break

    # Strategy 3: Don't play C or X the corresponding corner is unprotected (of course, if this is an available option)
    dictC = {0: (1, 8), 7: (6, 15), 56: (48, 57), 63: (55, 62)}
    setC = {1, 8, 6, 15, 48, 57, 55, 62}
    dictX = {0: 9, 7: 14, 56: 49, 63: 54}
    setX = {9, 14, 49, 54}

    noCX = validMoves - setC
    noCX = noCX - setX
    if len(noCX) > 0:
        for corner in corners:
            if game[corner] != player:
                validMoves = validMoves - {dictC[corner][0], dictC[corner][1], dictX[corner]}

    # Strategy 4: If Strategies 1 and 2 don't apply, then try not to move on an edge
    if not mademove:
        noEdges = validMoves - edges
        if len(noEdges) > 0:
            validMove = noEdges
            move = random.sample(validMoves, 1)[0]
        elif len(validMoves) > 0:
            move = random.sample(validMoves, 1)[0]

    if move >= 0:
        return move
    else:
        return -1

####################################################################################################
####################################################################################################

# Lab 7 addition: Negamax

validMoves = validMoveSet(game, player)
print("Legal moves: {}".format(validMoves))

def negamaxTerminal(brd, token, improvable, hardBound):
    lm = validMoveSet(brd, token)
    enemy = "X" if token == "O" else "O"
    if not lm:
        lm = validMoveSet(brd, enemy)
        if not lm:
            return [evalBoard(brd, token), -3]  # game over (score is by evalBoard)
            # otherwise
        else:
            nm = negamaxTerminal(brd, enemy, -hardBound, -improvable) + [-1] # -1 for pass, swap and negate bounds (alpha and beta) specifically for negamax
            return [-nm[0]] + nm[1:]
    # this is the main part of the code
    best = [] # what gets returned
    newHB = -improvable # find new hardbound
    for mv in lm:
        # need a new board ==> take old board, 
        nm = negamaxTerminal(makeMove(brd, token, mv)[0], enemy, -hardBound, newHB) + [mv]
        if not best or nm[0] < newHB: #  CAREFUL: understand the nm[0] < newHB part, especially the "<" part
            best = nm  # code can be streamlined somehow
            if nm[0] < newHB:
                newHB = nm[0]
            if -newHB > hardBound: 
                return [-best[0]] + best[1:] # if improvable bound gets above the hard bound
    return [-best[0]] + best[1:]

def evalBoard(board, token):
    enemy = "X" if token == "O" else "O"
    playerCount = 0
    opponentCount = 0
    for char in board:
        if char == token:
            playerCount += 1
        elif char == enemy:
            opponentCount += 1
    return playerCount - opponentCount

def makeMove(board, player, index):
    enemy = "X" if player == "O" else "O"
    if not validMoveSet(board, player):
        temp = player
        player = enemy
        enemy = temp
    game = board[:index] + player + board[index+1:]
    indexesToFlip = set()
    for x in xMoves:
        for y in yMoves:
            direction = x + y * 8
            temp = index
            tokensToFlip = set()
            row = temp // 8  # refers to vertical (y) position, horizontal line across
            column = temp % 8  # refers to horizontal (x) position, vertical line down
            while withinBounds(temp):
                temp += direction
                row += y
                column += x
                if row < 0 or row > 7 or column < 0 or column > 7:
                    break
                currchar = game[temp]
                if currchar == player and len(tokensToFlip) > 0:
                    temp = indexesToFlip | tokensToFlip  # take union of sets to increase indexes to flip
                    indexesToFlip = temp
                    break
                elif currchar != enemy:
                    break
                else:
                    tokensToFlip.add(temp)

    for index in indexesToFlip:
        game = game[:index] + player + game[index+1:]
    return game, player

def bestmove(game, player):
    mademove = False
    hMove = heurmove(game, player)
    print("Time taken for heuristic move:", time.clock() - inittime)
    if hMove >= 0:
        print("My heuristic choice is {}".format(hMove))
        mademove = True
    else:
        print("Pass")
    if mademove and game.count('.') <= 10:
        # level = 1
        while time.clock() - inittime < 5:
            nm = negamaxTerminal(game, player, -65, 65)
            print("Time taken:", time.clock()-inittime)
            print("The score for this move is:", nm[0])
            print("Negamax gives {}, the score is {}, and I choose to move at {}".format(nm, nm[0], nm[-1]))
            print()
            # level += 1

bestmove(game, player)
