# @author ALiu
# tsp Permutations

# import tkinter
from tkinter import *  # Tk, Canvas
import itertools  # for permutations
from math import pi, acos, sin, cos
import pprint  # solely for testing

# Graphics scaling
width = 800
height = 600
xfactor = 1.15  # Scaling factor in x direction
yfactor = 1.75  # Scaling factor in y direction
xoffset = 40  # offset of the map in x direction
yoffset = 55  # offset of the map in y direction
radius = 5  # Set radius of the circle

# y1 = lat1, x1 = long1
# y2 = lat2, x2 = long2
# all assumed to be in decimal degrees
def calcd(y1, x1, y2, x2):
    # print(y1, x1, y2, x2)

    R = 3958.76 # miles = 6371 km

    y1 *= pi/180.0
    x1 *= pi/180.0
    y2 *= pi/180.0
    x2 *= pi/180.0

    # approximate great circle distance with law of cosines
    return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

def calcAllDist(nodeList):
    totalD = 0.0
    for n in range(len(nodeList)-1):
        currNode = nodeList[n]
        nextNode = nodeList[n+1]
        totalD += calcd(currNode[1], currNode[0], nextNode[1], nextNode[0])
    return totalD

def display():
    return

# def allPerm(n):  # do this later (when time permits)
#

def main():

    ##################################################

    # DATA PROCESSING

    ##################################################

    # Process coordinates, get edge lengths
    # coordinates are longitude, latitude
    # divide each coordinate to get degrees
    coordfile = "KAD.txt"
    # coordfile = "DAU.txt"
    # coordfile = "KADsmall.txt"
    with open(coordfile, 'r+') as f:
        inputNodes = [tuple(rawCoords.strip().split()) for rawCoords in f.readlines()[1:]]
        rawNodes = [(float(nodeIn[0])/1000, float(nodeIn[1])/1000) for nodeIn in inputNodes]
        nodeDict = {index: rawNodes[index] for index in range(len(rawNodes))}  # give nodes an index
        nodeDictRev = {rawNodes[index]: index for index in range(len(rawNodes))}
    rawEdges = {rNode: set() for rNode in rawNodes}
    edgeSet = set()
    for i in range(len(rawNodes)):
        temp = rawNodes[i]
        neighbors = rawNodes[:i] + rawNodes[i+1:]
        rawEdges[temp] = set(neighbors)
        for rawNeighbor in neighbors:
            edgeSet.add((temp, rawNeighbor))

    ##################################################

    # PART 1: Make any hamiltonian cycle

    ##################################################

    # Graphics setup
    root = Tk()
    root.title("Map of coordinates of {}".format(coordfile))
    scwidth = root.winfo_screenwidth()
    scheight = root.winfo_screenheight()
    # Use screen dimensions and window dimensions to place window
    xdim = (scwidth / 2) - (width / 2)
    ydim = (scheight * 5 / 12) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, xdim, ydim))  # Opens window in specified position and size
    canvas = Canvas(root, width=width, height=height)
    # Put a textbox for the title
    canvas.create_text(width / 2, 30, text="Map of coordinates of {}".format(coordfile))

    # Get ranges and min values ==> scaling factor
    minx = 999999.0
    maxx = 0.0
    miny = 999999.0
    maxy = 0.0
    for myNode in rawNodes:
        if myNode[0] < minx:
            minx = myNode[0]
        if myNode[0] > maxx:
            maxx = myNode[0]
        if myNode[1] < miny:
            miny = myNode[1]
        if myNode[1] > maxy:
            maxy = myNode[1]
    xrn = maxx - minx
    yrn = maxy - miny
    xscale = width / (xrn * xfactor)
    yscale = width / (yrn * yfactor)

    # Now display the points
    newcoord = set()
    oldToNew = {}  # original coordinates to graphics coordinates
    for aNode in rawNodes:
        xcenter = (aNode[0]-minx) * xscale + xoffset  # Fine tuning included
        ycenter = 600 - ((aNode[1]-miny) * yscale + yoffset)  # Fine tuning included
        oldToNew[aNode] = (xcenter, ycenter)
        newcoord.add((xcenter, ycenter))  # Add to set of points
        canvas.create_oval(xcenter-radius, ycenter-radius, xcenter+radius, ycenter+radius, fill="royal blue")

    startNode = nodeDict[0]
    order = []
    orderDict = {}
    totalDist = 0
    currNode = startNode[:]
    counter = 0
    # nodeDict: index --> rawnode
    while counter < len(nodeDict) - 1:
        counter += 1
        nextNode = nodeDict[counter]
        order.append(currNode)
        orderDict[currNode] = nextNode
        currX = oldToNew[currNode][0]
        currY = oldToNew[currNode][1]
        nextX = oldToNew[nextNode][0]
        nextY = oldToNew[nextNode][1]
        canvas.create_line(currX, currY, nextX, nextY, fill="green", width=1.5)
        totalDist += calcd(currNode[1], currNode[0], nextNode[1], nextNode[0])
        canvas.create_text(currX-20, currY, text=counter-1)
        currNode = nextNode[:]
    canvas.create_line(oldToNew[currNode][0], oldToNew[currNode][1], oldToNew[startNode][0], oldToNew[startNode][1], fill="green", width=1.5)
    canvas.create_text(oldToNew[currNode][0] - 20, oldToNew[currNode][1], text=counter)
    totalDist += calcd(currNode[1], currNode[0], startNode[1], startNode[0])
    order.append(currNode)
    orderDict[currNode] = startNode
    print("Original configuration:\n")
    indexOrder = []
    for node in order:
        indexOrder.append(nodeDictRev[node])
    print("Order of nodes:")
    print(indexOrder)
    print("\nThe total distance traversed in this path is "
          "{} miles, or {} kilometers.".format(totalDist, 1.60934*totalDist))

    # # More tkinter stuff
    canvas.pack()
    # simple lambda function to call root.destroy{) (can't call directly)
    root.bind("<Key>", lambda e: root.destroy())  # bind all keys to closing a window
    root.mainloop()

    ##################################################

    # Part 2: Untangling

    ##################################################


    print("\n========================================\n")
    print("Initial untangling:\n")

    Tng = True
    while Tng:
        for A in range(len(order)-1):
            Tng = False
            nodeA1 = order[A]
            nodeA2 = order[A+1]
            oldDistBase = calcd(nodeA1[1], nodeA1[0], nodeA2[1], nodeA2[0])
            for B in range(A+2, len(order)):
                nodeB1 = order[B]
                nodeB2 = order[B+1] if B+1 < len(order) else order[0]
                if nodeA1 in {nodeA2, nodeB1, nodeB2} or nodeA2 in {nodeA1, nodeB1, nodeB2} or nodeB1 in {nodeA1, nodeA2, nodeB2} or nodeB2 in {nodeA1, nodeA2, nodeB1}:
                    continue
                oldDist = oldDistBase + calcd(nodeB1[1], nodeB1[0], nodeB2[1], nodeB2[0])
                newDist = calcd(nodeA1[1], nodeA1[0], nodeB1[1], nodeB1[0]) + calcd(nodeA2[1], nodeA2[0], nodeB2[1], nodeB2[0])
                if oldDist > newDist:
                    temp = order[A+1:B+1]
                    order = order[:A+1] + temp[::-1] + order[B+1:]
                    Tng = True
                    break
            if Tng: # restart the search for tangle
                break

    indexOrder = []
    for node in order:
        indexOrder.append(nodeDictRev[node])
        print("Order of nodes:")
        print(indexOrder)

    # Graphics setup -- note: other stuff already in first drawings
    root2 = Tk()
    root2.title("Map of coordinates of {}".format(coordfile))
    root2.geometry("%dx%d+%d+%d" % (width, height, xdim, ydim))  # Opens window in specified position and size
    canvas2 = Canvas(root2, width=width, height=height)
    canvas2.create_text(width / 2, 30, text="Map of coordinates of {}".format(coordfile))

    newTotalDist = 0
    oldToNew2 = {}
    # Now display the points and edges
    for newNode in order:
        xcenter = (newNode[0] - minx) * xscale + xoffset  # Fine tuning included
        ycenter = 600 - ((newNode[1] - miny) * yscale + yoffset)  # Fine tuning included
        canvas2.create_oval(xcenter - radius, ycenter - radius, xcenter + radius, ycenter + radius,
                           fill="royal blue")
        oldToNew2[newNode] = (xcenter, ycenter)

    for i in range(len(order)-1):
        newNode = order[i]
        nextNode = order[i+1]
        canvas2.create_line(oldToNew2[newNode][0], oldToNew2[newNode][1], oldToNew2[nextNode][0], oldToNew2[nextNode][1], fill="green", width=1.5)
        newTotalDist += calcd(newNode[1], newNode[0], nextNode[1], nextNode[0])
        canvas2.create_text(oldToNew2[newNode][0] - 20, oldToNew2[newNode][1], text=nodeDictRev[newNode])
    newNode = order[len(order)-1]
    nextNode = order[0]
    canvas2.create_line(oldToNew2[newNode][0], oldToNew2[newNode][1], oldToNew2[nextNode][0], oldToNew2[nextNode][1],
                        fill="green", width=1.5)
    newTotalDist += calcd(currNode[1], currNode[0], nextNode[1], nextNode[0])
    canvas2.create_text(oldToNew2[newNode][0] - 20, oldToNew2[newNode][1], text=nodeDictRev[newNode])
    print("\nNew Distance is: {} miles, or {} kilometers".format(newTotalDist, newTotalDist*1.60934))

    # More tkinter stuff
    canvas2.pack()
    root2.bind("<Key>", lambda e: root2.destroy())  # bind all keys to closing a window
    root2.focus_force()
    root2.mainloop()

    ##################################################

    # Part 3: Permute edges until reaching optimal solution

    ##################################################

    print("\n========================================\n")
    print("Permutations:\n")

    n = 9
    allPerms = [perm for perm in itertools.permutations([banana for banana in range(n)])]
    for i in range(len(order)):
        # setup
        anchor1 = order[i]
        anchor2 = order[i+n+1] if i+n+1 < len(order) else order[i+n+1-len(order)]
        # find the best permutation
        permuteNodes = []
        indexes = []
        for t in range(n):
            permuteNodes.append(order[i+t+1] if i+t+1 < len(order) else order[i+t+1-len(order)])
            indexes.append(i+t+1 if i+t+1 < len(order) else i+t+1-len(order))
        allPermNodes = itertools.permutations(permuteNodes)
        bestPerm = tuple()
        permDist = 999999  # make this a large number, in reality I would make this the first dist total
        for perm in allPermNodes:
            # First, calculate the distance
            # print(perm)
            fullperm = [anchor1] + list(perm) + [anchor2]
            # print(fullperm)
            # tempDist = calcAllDist(order+[order[0]])
            tempDist = calcAllDist(fullperm)
            # If the permutation is better, change it to be like that
            if tempDist < permDist:
                permDist = tempDist
                bestPerm = perm

        # switch accordingly
        for index in range(n):
            tempindex = i+index+1 if i+index+1 < len(order) else i+index+1-len(order)
            order[tempindex] = bestPerm[index]
            # order[indexes[index]] = bestPerm[index]

    indexOrder = []
    for node in order:
        indexOrder.append(nodeDictRev[node])
    print("Order of nodes:")
    print(indexOrder)

    # Graphics
    root3 = Tk()
    root3.title("Map of coordinates of {}".format(coordfile))
    root3.geometry("%dx%d+%d+%d" % (width, height, xdim, ydim))  # Opens window in specified position and size
    canvas3 = Canvas(root3, width=width, height=height)
    canvas3.create_text(width / 2, 30, text="Map of coordinates of {}".format(coordfile))

    permDist = 0
    oldToNew3 = {}
    # Now display the points and edges
    for newNode in order:
        xcenter = (newNode[0] - minx) * xscale + xoffset  # Fine tuning included
        ycenter = 600 - ((newNode[1] - miny) * yscale + yoffset)  # Fine tuning included
        canvas3.create_oval(xcenter - radius, ycenter - radius, xcenter + radius, ycenter + radius,
                           fill="royal blue")
        oldToNew3[newNode] = (xcenter, ycenter)

    for i in range(len(order)-1):
        newNode = order[i]
        nextNode = order[i+1]
        canvas3.create_line(oldToNew3[newNode][0], oldToNew3[newNode][1], oldToNew3[nextNode][0], oldToNew3[nextNode][1], fill="green", width=1.5)
        permDist += calcd(newNode[1], newNode[0], nextNode[1], nextNode[0])
        canvas3.create_text(oldToNew3[newNode][0] - 20, oldToNew3[newNode][1], text=nodeDictRev[newNode])
    newNode = order[len(order)-1]
    nextNode = order[0]
    canvas3.create_line(oldToNew3[newNode][0], oldToNew3[newNode][1], oldToNew3[nextNode][0], oldToNew3[nextNode][1],
                        fill="green", width=1.5)
    permDist += calcd(currNode[1], currNode[0], nextNode[1], nextNode[0])
    canvas3.create_text(oldToNew3[newNode][0] - 20, oldToNew3[newNode][1], text=nodeDictRev[newNode])
    print("\nNew Distance is: {} miles, or {} kilometers".format(permDist, permDist*1.60934))

    # More tkinter stuff
    canvas3.pack()
    root3.bind("<Key>", lambda e: root3.destroy())  # bind all keys to closing a window
    root3.focus_force()
    root3.mainloop()

if __name__ == '__main__':
    main()

###########################################################################################################
