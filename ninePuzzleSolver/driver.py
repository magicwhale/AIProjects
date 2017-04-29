#!/usr/bin/python
import sys
import queue
from collections import deque
import timeit
import resource
from heapq import heapify, heappush, heappop
import math

#Priority of directions
directions = {'Up': 0, 'Down': 1, 'Left': 2, 'Right': 3}
#dimension
#global dimension #= 0
#global correctList #= []

class Node:
	def __init__(self, state, prevDir, parent, depth):
		self.state = state
		self.previousDir = prevDir
		self.parent = parent
		self.depth = depth

class HeapNode:
	def __init__(self, state, prevDir, parent, depth, cost):
		self.state = state
		self.previousDir = prevDir
		self.parent = parent
		self.depth = depth
		self.cost = cost

	def __lt__(self, other):
		if self.cost == other.cost:
			#Return in UDLR order
			if self.previousDir == other.previousDir:
				#Return other if both same previous direction
				return other
			else:
				return directions[self.previousDir] < directions[other.previousDir]
		else:
			return self.cost < other.cost

def main(argv):
	searchType = argv[1]
	start = argv[2].split(",")

	global dimension
	dimension = int(math.sqrt(len(start)))

	global correctList
	correctList = []
	for number in range(len(start)):
		correctList.append(str(number))

	results = {'path_to_goal': [], 
	'cost_of_path': 0,
	'nodes_expanded': 0,
	'fringe_size': 0,
	'max_fringe_size': 0,
	'search_depth': 0,
	'max_search_depth': 0,
	'running_time': 0,
	'max_ram_usage': 0.0}

	if searchType == "bfs":
		bfs(start, results)
	elif searchType == "dfs":
		dfs(start, results)
	elif searchType == "ast":
		ast(start, results)
	elif searchType == "ida":
		ida(start, results)

	usage = resource.getrusage(resource.RUSAGE_SELF)
	results['max_ram_usage'] = getattr(usage, 'ru_maxrss') / (1024 * 1024)

	file = open('output.txt', 'w')
	for item in ['path_to_goal', 
	'cost_of_path',
	'nodes_expanded',
	'fringe_size',
	'max_fringe_size',
	'search_depth',
	'max_search_depth',
	'running_time',
	'max_ram_usage']:
		file.write(item + ': ' + str(results[item]) + '\n')

def bfs(start, results):
	startTime = timeit.default_timer()
	explored = set()
	frontierset = set()
	frontier = deque()
	startNode = Node(start, None, None, 0)
	frontier.append(startNode)
	frontierset.add(','.join(start))
	nodesExpanded = 0
	maxFringe = 0
	maxDepth = 0

	while frontier:
		fringeSize = len(frontier)
		curr = frontier.popleft()
		frontierset.remove(','.join(curr.state))
		explored.add(','.join(curr.state))

		if fringeSize > maxFringe:
			maxFringe = fringeSize
			
		if curr.state == correctList:
			results['path_to_goal'] = getPath(curr)
			results['cost_of_path'] = len(results['path_to_goal'])
			results['nodes_expanded'] = nodesExpanded
			results['fringe_size'] = fringeSize - 1
			results['max_fringe_size'] = maxFringe
			results['search_depth'] = curr.depth
			results['max_search_depth'] = maxDepth
			results['running_time'] = timeit.default_timer() - startTime
			return

		nodesExpanded += 1

		for neighbor in neighbors(curr):
			stateString = ','.join(neighbor.state)
			if (stateString not in frontierset and 
			    stateString not in explored):
				if neighbor.depth > maxDepth:
					maxDepth = neighbor.depth
				frontier.append(neighbor)
				frontierset.add(stateString)

def dfs(start, results):
	startTime = timeit.default_timer()
	explored = set()
	frontierset = set()
	frontier = deque()
	startNode = Node(start, None, None, 0)
	frontier.append(startNode)
	frontierset.add(','.join(start))
	nodesExpanded = 0
	maxFringe = 0
	maxDepth = 0

	while frontier:
		fringeSize = len(frontier)
		curr = frontier.pop()
		frontierset.remove(','.join(curr.state))
		explored.add(','.join(curr.state))

		if fringeSize > maxFringe:
			maxFringe = fringeSize

		if curr.state == correctList:
			results['path_to_goal'] = getPath(curr)
			results['cost_of_path'] = len(results['path_to_goal'])
			results['nodes_expanded'] = nodesExpanded
			results['fringe_size'] = fringeSize - 1
			results['max_fringe_size'] = maxFringe
			results['search_depth'] = curr.depth
			results['max_search_depth'] = maxDepth
			results['running_time'] = timeit.default_timer() - startTime
			return


		nodesExpanded += 1

		for neighbor in reversed(neighbors(curr)):
			stateString = ','.join(neighbor.state)
			if (stateString not in frontierset and 
			    stateString not in explored):
				if neighbor.depth > maxDepth:
					maxDepth = neighbor.depth
				frontier.append(neighbor)
				frontierset.add(stateString)

def ast(start, results):
	startTime = timeit.default_timer()
	explored = set()
	frontierset = set()
	frontier = []
	startCost = costOf(start, 0)
	startNode = HeapNode(start, None, None, 0, startCost)
	heappush(frontier, startNode)
	frontierset.add(','.join(start))
	nodesExpanded = 0
	maxFringe = 0
	maxDepth = 1

	while frontier:
		fringeSize = len(frontier)
		curr = heappop(frontier)
		frontierset.remove(','.join(curr.state))
		explored.add(','.join(curr.state))

		if fringeSize > maxFringe:
			maxFringe = fringeSize

		if curr.state == correctList:
			results['path_to_goal'] = getPath(curr)
			results['cost_of_path'] = len(results['path_to_goal'])
			results['nodes_expanded'] = nodesExpanded
			results['fringe_size'] = fringeSize - 1
			results['max_fringe_size'] = maxFringe
			results['search_depth'] = curr.depth
			results['max_search_depth'] = maxDepth
			results['running_time'] = timeit.default_timer() - startTime
			return

		nodesExpanded += 1

		for neighbor in neighborsWithCost(curr):
			stateString = ','.join(neighbor.state)
			#Check if stateString is in explored
			#If stateString is in frontier set update if cost lower
			if (stateString not in frontierset and 
			    stateString not in explored):
				if neighbor.depth > maxDepth:
					maxDepth = neighbor.depth
				heappush(frontier, neighbor)
				frontierset.add(stateString)

			if (stateString in frontierset):
				# Find matching state
				for item in frontier:
					if item.state == neighbor.state:
						if item.cost > neighbor.cost:
							if neighbor.depth > maxDepth:
								maxDepth = neighbor.depth
							item.cost = neighbor.cost
							heapify(frontier)
						break

#"Cost limited search" 
def cls(start, cost, results):
	frontierset = set()
	frontier = deque()
	startCost = costOf(start, 0)
	startNode = HeapNode(start, None, None, 0, startCost)
	frontier.append(startNode)
	frontierset.add(','.join(start))

	while frontier:
		fringeSize = len(frontier)
		curr = frontier.pop()
		explored = set()

		child = curr
		while child.parent is not None:
			explored.add(','.join(child.state))
			child = child.parent

		if fringeSize > results['max_fringe_size']:
			results['max_fringe_size'] = fringeSize

		if curr.state == correctList:
			results['path_to_goal'] = getPath(curr)
			results['cost_of_path'] = len(results['path_to_goal'])
			results['fringe_size'] = fringeSize - 1
			results['search_depth'] = curr.depth
			return

		results['nodes_expanded'] += 1

		for neighbor in reversed(neighborsWithCost(curr)):
			stateString = ','.join(neighbor.state)
			if(neighbor.cost <= cost and stateString not in explored):
				if neighbor.depth > results['max_search_depth']:
					results['max_search_depth'] = neighbor.depth
				frontier.append(neighbor)

def ida(start, results):
	startTime = timeit.default_timer()
	currCost = 0

	while True:
		if len(results['path_to_goal']) > 0:
			results['running_time'] = timeit.default_timer() - startTime
			break

		cls(start, currCost, results)
		currCost += 1

def neighbors(node):
	state = node.state
	depth = node.depth + 1

	result = []
	#Find the empty space
	space = 0
	for i in range(len(state)):
		if state[i] == '0':
			space = i
			break
	#Add up
	if space > dimension - 1:
		up = state[:]
		upValue = state[space - 3]
		up[space] = upValue
		up[space - 3] = '0'
		upNode = Node(up, 'Up', node, depth)
		result.append(upNode)
	#Add down
	if space < (dimension * (dimension - 1)):
		down = state[:]
		downValue = state[space + 3]
		down[space] = downValue
		down[space + 3] = '0'
		downNode = Node(down, 'Down', node, depth)
		result.append(downNode)
	#Add left
	if (space % dimension) != 0:
		left = state[:]
		leftValue = state[space - 1]
		left[space] = leftValue
		left[space - 1] = '0'
		leftNode = Node(left, 'Left', node, depth)
		result.append(leftNode)
	#Add right
	if ((space + 1) % dimension) != 0:
		right = state[:]
		rightValue = state[space + 1]
		right[space] = rightValue
		right[space + 1] = '0'
		rightNode = Node(right, 'Right', node, depth)
		result.append(rightNode)

	return result

def neighborsWithCost(node):
	state = node.state
	depth = node.depth + 1

	result = []
	#Find the empty space
	space = 0
	for i in range(len(state)):
		if state[i] == '0':
			space = i
			break
	#Add up
	if space > dimension - 1:
		up = state[:]
		upValue = state[space - 3]
		up[space] = upValue
		up[space - 3] = '0'
		upNode = HeapNode(up, 'Up', node, depth, costOf(up, depth))
		result.append(upNode)
	#Add down
	if space < (dimension * (dimension - 1)):
		down = state[:]
		downValue = state[space + 3]
		down[space] = downValue
		down[space + 3] = '0'
		downNode = HeapNode(down, 'Down', node, depth, costOf(down, depth))
		result.append(downNode)
	#Add left
	if (space % dimension) != 0:
		left = state[:]
		leftValue = state[space - 1]
		left[space] = leftValue
		left[space - 1] = '0'
		leftNode = HeapNode(left, 'Left', node, depth, costOf(left, depth))
		result.append(leftNode)
	#Add right
	if ((space + 1) % dimension) != 0:
		right = state[:]
		rightValue = state[space + 1]
		right[space] = rightValue
		right[space + 1] = '0'
		rightNode = HeapNode(right, 'Right', node, depth, costOf(right, depth))
		result.append(rightNode)

	return result

def stateIsIn(item, list):
	for n in list:
		if n.state == item.state:
			return True
	return False

def getPath(node):
	curr = node
	steps = []
	while(True):
		if curr.previousDir is not None:
			steps.append(curr.previousDir)
		if curr.parent is not None:
			curr = curr.parent
		else:
			break
	steps.reverse()
	return steps

def costOf(state, depth):
	return manhattan(state) + depth

def manhattan(state):
	total = 0
	for i in range(len(state)):
		total += distanceFromSol(state[i], i)
	return total

def distanceFromSol(number, position):
	if number == 0: 
		return 0
	rowNow = getRow(position)
	colNow = getCol(position)
	rowSol = getRow(int(number))
	colSol = getCol(int(number))
	return abs(rowSol - rowNow) + abs(colSol - colNow)

def getRow(position):
	for row in range(dimension):
		if position < (row + 1) * dimension:
			return row

def getCol(position):
	return position % dimension


main(sys.argv)
