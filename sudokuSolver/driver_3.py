#!/usr/bin/python
import sys
import queue
import time

def main1(argv):
    f = open(argv[1], 'r')
    outputFile = open('output.txt', 'w') 
    lines = f.read().splitlines()
    for line in lines:
        start = time.time()
        boardDict = stringToBoard(line)
        result = backtrack(boardDict)
        if result:
            outputFile.write(boardToString(result))
            outputFile.write("\n")
            print("Solution: " + boardToString(result))
        print("Time taken: " + time.time() - start)
        print('')

def boardToString(boardDict):
    result = []
    rows = "ABCDEFGHI"
    for row in rows:
        for col in range(1,10):
            result.append(str(boardDict[row + str(col)]))
    return ''.join(result)

def backtrack(boardDict):
    domains = domainOfBoard(boardDict)
    assignments = initializeAssignments(boardDict)
    domains = forwardCheck(assignments, domains)
    if domains != None:
        return backtrackHelper(assignments, domains)
    else:
        return False

def backtrackHelper(assignments, domains):
    if(len(assignments) == 81):
        return assignments
    var = selectUnassignedVariable(assignments, domains)
#    print(domains[var])
    for value in sortByCV(var, domains, assignments):
        if consistent(var, value, assignments):
            assignments[var] = value
            modifiedDomains = forwardCheck(assignments, domains)
            if modifiedDomains != None:
                result = backtrackHelper(assignments, modifiedDomains)
                if result:
                    return result
        if var in assignments:
            del assignments[var]
    return False

def sortByCV(var, domains, assignments):
    varsWithCV = []
    for value in domains[var]:
        varsWithCV.append((value, getCV(var, domains, assignments, value)))
    varsWithCV = sorted(varsWithCV, key=lambda tup: tup[1])
    sortedVars = []
    for pair in varsWithCV:
        sortedVars.append(pair[0])
    return sortedVars

def getCV(var, domains, assignments, value):
    CV = 0
    for key in neighbors(var):
        if value in domains[key]:
            CV -= 1
    return CV

def forwardCheck(assignments, domains):
    newDomains = {}
    for key in domains:
        newDomains[key] = set()
        for value in domains[key]:
            if consistent(key, value, assignments):
                newDomains[key].add(value)
        if len(newDomains[key]) == 0:
            return None
    return newDomains

def consistent(var, value, assignments):
    for key in neighbors(var):
        if key in assignments:
            if value == assignments[key]:
                return False
    return True

def selectUnassignedVariable(assignments, domains):
    minRemainingValue = 10
    minKey = ""
    for key in domains:
        if key not in assignments:
#            if len(domains[key]) == 2:
#                return key
            if len(domains[key]) < minRemainingValue:
                minKey = key
                minRemainingValue = len(domains[key])
    return minKey
    
def initializeAssignments(boardDict):
    assignments = {}
    for key in boardDict:
        if int(boardDict[key]) != 0:
            assignments[key] = int(boardDict[key])
    return assignments

def main2(argv):
    start = time.time()
    f = open(argv[1], 'r')
    lines = f.read().splitlines()
    totalSolved = 0
    for line in lines:
        boardDict = stringToBoard(line)
        result = AC3(boardDict)
        solved = True
        for key in result:
            if len(result[key]) != 1:
                solved = False
                break
        if solved:
            totalSolved += 1
            print(boardToString(boardDict))
    print(totalSolved)
    print("total time:" + str(time.time() - start))

def AC3(boardDict):
    domains = domainOfBoard(boardDict)
    localVars, varSet = initializeArcs()
#    print(localVars.qsize())
    while not localVars.empty():
        currArc = localVars.get()
        Xi = currArc[0]
        Xj = currArc[1]
        #varSet.remove(Xi + Xj)
        if revise(Xi, Xj, domains):
            if len(domains[Xi]) == 0:
                return False
            for neighbor in neighbors(Xi):
                #if not (Xi + neighbor) in varSet:
                localVars.put((Xi, neighbor))
                localVars.put((neighbor, Xi))
                #varSet.add(Xi + neighbor)
#    displaySudoku(domains)
#    print('')
    return domains


def revise(Xi, Xj, domains):
#    print(Xi + "," +Xj)
#    print(domains)
    revised = False  
    XiDomains = domains[Xi].copy()
    for x in XiDomains:
        satisfied = False
        for y in domains[Xj]:
            if x != y:
                satisfied = True
        if not satisfied:
            domains[Xi].remove(x)
            revised = True
    return revised

    '''    if len(domains[Xj]) == 1:
        XjValue = list(domains[Xj])[0]
        if XjValue in domains[Xi]:
            domains[Xi].remove(XjValue)
            revised = True
    return revised
'''  

def domainOfBoard(boardDict):
    domainDict = {}
    for key, value in boardDict.items():
        if value == 0:
            domainDict[key] = set(range(1,10))
        else:
            domainDict[key] = set([value])
    return domainDict

def neighbors(index):
    rows = "ABCDEFGHI"
    row = index[0]
    col = index[1]
    neighbors = []

    #Add row neighbors
    for otherCol in range(1, 10):
        otherVar = row + str(otherCol)
        if index != otherVar:
            neighbors.append(otherVar)

    #Add col arcs
    for otherRow in rows:
        otherVar = otherRow + str(col)
        if index != otherVar:
            neighbors.append(otherVar)

    #add block neighbors
    blockRows = getBlockRows(row)
    blockCols = getBlockCols(col)
    for otherRow in blockRows:
        for otherCol in blockCols:
            if otherRow != row and otherCol != str(col):
                otherVar = otherRow + otherCol
                neighbors.append(otherVar)

    return neighbors

def initializeArcs():
    rows = "ABCDEFGHI" 
    arcs = queue.Queue()
    arcSet = set()
    for row in rows:
        for col in range(1, 10):
            currVar = row + str(col)

            #Add block arcs
            blockRows = getBlockRows(row)
            blockCols = getBlockCols(col)
            for otherRow in blockRows:
                for otherCol in blockCols:
                    otherVar = otherRow + str(otherCol)
                    if currVar != otherVar and (currVar + otherVar) not in arcSet:
                        arcs.put((currVar, otherVar))
                        arcSet.add(currVar + otherVar)

            #Add row arcs
            for otherCol in range(1, 10):
                otherVar = row + str(otherCol)
                if currVar != otherVar and (currVar + otherVar) not in arcSet:
                    arcs.put((currVar, otherVar))
                    arcSet.add(currVar + otherVar)

            #Add col arcs
            for otherRow in rows:
                otherVar = otherRow + str(col)
                if currVar != otherVar and (currVar + otherVar) not in arcSet:
                    arcs.put((currVar, otherVar))
                    arcSet.add(currVar + otherVar)
    return arcs, arcSet

def getBlockRows(row):
    if row <= 'C':
        return ['A', 'B', 'C']
    elif row <= 'F':
        return ['D', 'E', 'F']
    elif row <= 'I':
        return ['G', 'H', 'I']

def getBlockCols(col):
    col = int(col)
    if col <= 3:
        return ['1', '2', '3']
    elif col <= 6:
        return ['4', '5', '6']
    elif col <= 9:
        return ['7', '8', '9']

def stringToBoard(string):
    row = 'A'
    col = 1
    boardDict = {}
    for entry in string:
        boardDict[row + str(col)] = int(entry)
        if col == 9:
            col = 1
            row = chr(ord(row) + 1)
        else:
            col += 1
    return boardDict

def displaySudoku(sudokuDict):
    for row in "ABCDEFGHI":
        for col in range(1, 10):
            print('%17s' % sudokuDict[row+str(col)], end = '')
        print('')

#Uncomment to run BTS
main1(sys.argv)

#Uncomment to run AC3
#main2(sys.argv) 