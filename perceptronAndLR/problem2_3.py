#!/usr/bin/python
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def main(argv):
    inputName = argv[1]
    outputName = argv[2]
    outputFile = open(outputName, 'w')
    csvWriter = csv.writer(outputFile)

    dataArray = np.array(csvToArray(inputName))
    y = extractY(dataArray)
    dataArray = np.delete(dataArray, len(dataArray[0]) - 1, 1)
    normalize(dataArray)

    learningRates = [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 1]
    iterationValues = [100, 100, 100, 100, 100, 100, 100, 100, 100, 16]
    for i in range(len(learningRates)):
        alpha = learningRates[i]
        weights = np.zeros(len(dataArray[0]))
        numIterations = iterationValues[i]
        iterations = 0

        while(iterations < numIterations):
            weights = gd(alpha, weights, dataArray, y)
            iterations += 1

        results = [alpha, numIterations]
        for weight in weights:
            results.append(weight)
        csvWriter.writerow(results)
        #print(risk(weights, dataArray, y))
        #plot(weights, dataArray, y)

def plot(weights, data, y):
    xx, yy = np.meshgrid(range(10), range(10))
    z = weights[0] + weights[1]*xx + weights[2]*yy
    plt3d = plt.figure().gca(projection='3d')
    plt3d.plot_surface(xx, yy, z)

    ax = plt.gca()
    ax.hold(True)

    ax.scatter(data[:,1], data[:,2] ,y)
    plt.show()

def risk(weights, data, yValues):
    total = 0
    for i in range(len(data)):
        dotProd = np.dot(data[i], weights)
        total += (dotProd - yValues[i])**2
    return total / len(data)

def gd(alpha, weights, data, yValues):
    for i in range(len(weights)):
        weights[i] = weights[i] - (alpha * grad(weights, data, yValues, i))
    return weights

def grad(weights, data, yValues, index):
    n = len(data)
    total = 0.0
    for i in range(n):
        total += data[i][index]*(np.dot(weights, data[i]) - yValues[i])
    return total / n

def csvToArray(inputName):
    array = []
    with open(inputName, 'r') as inputFile:
        csvReader = csv.reader(inputFile)
        for rowText in csvReader:
            row = [1]
            for x in rowText:
                row.append(float(x))
            array.append(row)
    return array

def normalize(data):
    stdArray = data.std(0)
    meanArray = data.mean(0)
    for i in range(len(data)):
        for j in range(1, len(data[i])):
            data[i][j] = scale(data[i][j], meanArray[j], stdArray[j])

def scale(x, mean, std):
    return (x - mean) / std

def extractY(data):
    j = len(data[0]) - 1
    yValues = np.zeros(len(data))
    for i in range(len(data)):
        yValues[i] = (data[i][j])
    return yValues

main(sys.argv)