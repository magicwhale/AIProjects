#!/usr/bin/python
import time
import random
#Potential Heuristics
'''
    highest value on board
    "Closeness" of high numbers
    most combinations performed within x turns
    
'''
from random import randint
from BaseAI_3 import BaseAI
import numpy as np

class State():
    def __init__(self, direction, grid, utility):
        self.direction = direction
        self.grid = grid
        self.utility = utility

class PlayerAI(BaseAI):

    finalResult = State(None, None, None)
    maxDepth = 3
    currentDepth = 0
    highestRunTime = 0

    def monotonicity2(self, board):
        score = 0
        for i in range(4):
            for j in range(4):
                score += (i+j) * ((board[i][j])**1.1)
        return score

    def smoothness2(self, board):
        smoothness = 0
        for i in range(4):
            for j in range(4):
                currentVal = board[i][j]
                if currentVal != 0:
                    #check up
                    if i > 0:
                        up = board[i-1][j]
                        smoothness += abs(currentVal - up)
                    #check left 
                    if j > 0:
                        left = board[i][j-1]
                        smoothness += abs(currentVal - left)
        return 0 - smoothness               

    def diagonals(self, board):
        diags = []
        for x in range(4):
            i = x
            j = 0
            diag = []
            while(i >= 0):
                diag.append(board[i][j])
                i -= 1
                j += 1
            diags.append(diag)
        for x in range(1, 4):
            i = x
            j = 3
            diag = []
            while (i < 4):
                diag.append(board[i][j])
                i += 1
                j -= 1
            diags.append(diag)
        return diags

    def monotonicity(self, board):
        matrix = np.array(board)
        currDiagonal = 0
        diagonalAvg = []
        #Find averages of diagonals
        for diagonal in self.diagonals(board):
            total = 0
            size = 0
            for item in diagonal:
                if item != 0:
                    total += item
                    size += 1
            if size == 0:
                diagonalAvg.append(0)
            else:
                diagonalAvg.append(total/size)
        score = 0
        diagArray = np.array(diagonalAvg)
        sortedDiags = np.argsort(diagArray)
        for index in range(7):
            if index == sortedDiags[index]:
                score += 2**(7-index)
        return score * .04

    def freeTiles(self, board):
        freeTiles = 0
        for i in range(4):
            for j in range(4):
                if board[i][j] == 0:
                    freeTiles += 1
        return freeTiles

    def smoothness(self, board):
        smoothness = 0
        for i in range(4):
            for j in range(4):
                currentVal = board[i][j]
                if currentVal != 0:
                    #check up
                    if i > 0:
                        up = board[i-1][j]
                        if up == currentVal:
                            smoothness += up
                    #check left 
                    if j > 0:
                        left = board[i][j-1]
                        if left == currentVal:
                            smoothness += left
        return smoothness

    def maxNum(self, board):
        maxN = 0
        for row in board:
            for item in row:
                if item > maxN:
                    maxN = item
        return maxN / 204.8
            
    def landLockedLows(self, board):
        locked = 0
        for i in range(4):
            for j in range(4):
                curr = board[i][j]
                if curr == 2 or curr == 4:
                    if i > 0:
                       if board[i - 1][j] == curr:
                           break
                    if i < 3:
                        if board[i + 1][j] == curr:
                            break
                    if j > 0:
                        if board[i][j - 1] == curr:
                            break
                    if j < 3:
                        if board[i][j + 1] == curr:
                            break
                    locked += 1
        return 0-locked

    def evaluate(self, grid):
        board = grid.map
        #maxItem = self.maxNum(board)
        #mon = self.monotonicity(board)
        free = self.freeTiles(board)
        #smooth = self.smoothness(board) * 10 / 2048
        locked = self.landLockedLows(board)
        smooth2 = self.smoothness2(board)
        mon2 = self.monotonicity2(board)
        return mon2 + smooth2 #+ 4*free + 8*locked
        #return 0*maxItem + 0*mon + 0*free + 0*smooth - 0*locked + smooth2 + mon2

    #returns the children of a state
    def findMaxChildren(self, grid):
        children = []
        moves = grid.getAvailableMoves()
        for x in moves:
            newGrid = grid.clone()
            newGrid.move(x)

            children.append(State(x, newGrid, None))
        return children

    def findMinChildren(self, grid):
        children = []
        spaces = grid.getAvailableCells()
        for pos in spaces:
            for value in (2,4):
                newGrid = grid.clone()
                newGrid.insertTile(pos, value)
                children.append(State(None, newGrid, None))
        return children
            
    def maxormin(self, state, isMax, alpha, beta, depth):
#        print("running maxormin")
#        print(self.currentDepth)
#        print(self.maxDepth)
        if depth == self.maxDepth:
            #print("exceeded depth")
            return State(None, state.grid, self.evaluate(state.grid))

        if isMax:
            children = self.findMaxChildren(state.grid)
            if len(children) == 0:
                return State(state.direction, state.grid, 0)

            #return State(None, state.grid, self.evaluate(state.grid))
            maxUtility = State(None, None, float("-inf"))

            for child in children:
                childUtility = self.maxormin(child, False, alpha, beta, depth + 1)
                if childUtility.utility > maxUtility.utility:
                   maxUtility = State(child.direction, child.grid, childUtility.utility)

                if maxUtility.utility >= beta:
                    break

                if maxUtility.utility > alpha:
                    alpha = maxUtility.utility

            return maxUtility
        else:
            children = self.findMinChildren(state.grid)

            if len(children) == 0:
                return State(state.direction, state.grid, 0)
            #return State(None, state.grid, self.evaluate(state.grid))
            minUtility = State(None, None, float("inf"))

            for child in children:
                childUtility = self.maxormin(child, True, alpha, beta, depth + 1)
                if childUtility.utility < minUtility.utility:
                    minUtility = State(child.direction, child.grid, childUtility.utility)

                if minUtility.utility <= alpha:
                    break

                if minUtility.utility < beta:
                    beta = minUtility.utility
            
            return minUtility

    def CalculateDecision(self, state):
        result = self.maxormin(state, True, float("-inf"), float("inf"), 0)
        return result

    def getMove(self, grid):
        startTime = time.clock();
        '''
        print("runtime")
        print(self.highestRunTime)
        print("monotonicity")
        print(self.monotonicity(grid.map))
        print("freeTiles")
        print(self.freeTiles(grid.map))
        print("smoothness")
        print(self.smoothness(grid.map))
        print("Depth")
        print(self.maxDepth)
        '''
        self.maxDepth = 3
        #run decision with increasing depth until time runs out
        while (time.clock() - startTime <= .04):
            startIDS = time.clock()
            finalResult = self.CalculateDecision(State(None, grid.clone(), None))
            self.highestRunTime = max(self.highestRunTime, time.clock() - startIDS)
            if self.highestRunTime <= .05: #originally .18
                self.maxDepth += 1
        return finalResult.direction

