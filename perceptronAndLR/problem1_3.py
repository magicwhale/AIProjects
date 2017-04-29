#!/usr/bin/python
import sys
import csv
import numpy as np
from matplotlib import pyplot as plt

def main(argv):
    inputName = argv[1]
    outputName = argv[2]
    outputFile = open(outputName, 'w')
    csvWriter = csv.writer(outputFile)
    weights = [0,0,0]

    while(True):
        #plt.clf()
        #plotPoints(inputName)
        #plotLine(weights)
        writeWeights(csvWriter, weights)
        #plt.show()
        prevWeights = weights[:]
        iterate(inputName, weights)
        if converges(prevWeights, weights):
            writeWeights(csvWriter, weights)
            break;

def plotLine(weights):
    x = np.linspace(0, 16, 2)
    plt.plot(x, -1*(weights[0]*x+weights[2])/weights[1])

def plotPoints(inputName):
    x1 = []
    x2 = []
    y1 = []
    y2 = []
    with open(inputName, 'r') as inputFile:
        csvReader = csv.reader(inputFile)
        for rowText in csvReader:
            row = [int(x) for x in rowText]
            if row[-1] == 1:
                x1.append(row[0])
                y1.append(row[1])
            else:
                x2.append(row[0])
                y2.append(row[1])
    plt.scatter(x1, y1, color='red')
    plt.scatter(x2, y2, color='blue')

def iterate(inputName, weights):
    with open(inputName, 'r') as inputFile:
        csvReader = csv.reader(inputFile)
        for rowText in csvReader:
            row = [int(x) for x in rowText]
            if row[- 1] * function(row, weights) <= 0:
                update(row, weights)


def converges(previousWeights, newWeights):
    for i in range(len(previousWeights)):
        if previousWeights[i] != newWeights[i]:
            return False
    return True

def function(row, weights):
    total = 0;
    for d in range(len(weights) - 1): 
        total += weights[d] * row[d]
    total += weights[len(weights) - 1]
    if total > 0:
        return 1
    elif total < 0:
        return -1
    else:
        return 0

def update(row, weights):
    y = row[- 1]
    for j in range(len(weights)-1):
        weights[j] += y * row[j] 
    weights[-1] += y


def writeWeights(csvWriter, weights):
    csvWriter.writerow(weights)

main(sys.argv)