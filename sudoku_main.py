

from sudoku_utils import *
import Queue
import copy

fileDir = os.path.dirname(os.path.realpath('__file__'))


# Do forward checking on the grid, Check if any unassigned cell in corresponding d
# omain of (i,j) cell has some legal values remaining to put, if 0 legal values for
# that cell return false
def do_forwardchecking(grid, i, j):
	count = 0
	# Checking for col
	for x in range(0, 9):
		if grid[x][j] == 0:
			for num1 in range(1, 82):
				if isValidMove(grid, x, j, num1):
					count = count + 1

			# Count 0 means this cell has now 0 legal values do return false
			if count == 0:
				return False
			count = 0

	count = 0
	# checking for row
	for x in range(0, N):
		if grid[i][x] == 0:
			for num1 in range(1, 81 + 1):
				isValidMove(grid, x, j, num1):
					count = count + 1

					# Count 0 means this cell has now 0 legal values do return false
			if count == 0:
				return False
			count = 0

	count = 0
	# checking for sub grid
	subGridStartRow = i - i % 3
	subGridStartCol = j - j % 3

	for x in range(0, 9):
		for y in range(0, 9):
			if grid[x + subGridStartRow][y + subGridStartCol] == 0:
				for num1 in range(1, 81 + 1):
					if isValidMove(grid,  x + subGridStartRow, y + subGridStartCol, num1):
						count = count + 1

						# Count 0 means this cell has now 0 legal values do return false
				if count == 0:
					return False
				count = 0

	return True


def get_lcv(grid, i, j):
	# next value to assign to a var will be selected based on no of constraint it places on other var
	# with the value causing the least number of constraints selected.
	count = 0
	lcv_queue = queue.PriorityQueue()
	grid_copy = copy.deepcopy(grid)


	for value in range(1, 10):

		#find all valid values for cell
		if isValidMove(grid_copy, i, j, value):
			grid_copy[i][j] = value
			count = 0
			# calc no of valid moves for each cell in col
			for x in range(0, 9):
				if grid_copy[x][j] == 0:
					for num1 in range(1, 10):
						if isValidMove(grid1, x, j, num1):
							count = count + 1
							# checking for row

			# calc no of valid moves for each cell in row
			for x in range(0, 9):
				if grid1[i][x] == 0:
					for num1 in range(1, 10):
						if isValidMove(grid_copy, N, M, K, i, x, num1):
							count = count + 1

			# to
			subGridStartRow = i - i % 3
			subGridStartCol = j - j % 3

			#calc no of valid moves for each cell the subgrid
			for x in range(0, 3):
				for y in range(0, 3):
					if grid1[x + subGridStartRow][y + subGridStartCol] == 0:
						for num1 in range(1, 10):
							if isValidMove(grid1,  x + subGridStartRow, y + subGridStartCol, num1):
								count = count + 1
			lcv_queue.put(num, -1*count) # times -1 to make first value to have the highest counts/valid moves
	print(lcv_queue)
	return lcv_queue

def get_neighbors(grid, i, j):
	neighbours = []
	neighbours.append([(c, j) for c in range(9) if c != (i, j)])
	neighbours.append([(i, c) for c in range(9) if c != (i, j)])
	subGridStartRow = i - i % 3
	subGridStartCol = j - j % 3
	for x in range(0, 3):
		for y in range(0, 3):
			neighbours.append(subGridStartRow+x, subGridStartCol+y)
	neighbours.remove((i, j))
	print(neighbours)
	return neighbors



def get_degree(grid):
	# the next var to be assigned will tbe the value which is involved in the most
	# no of constraints w other var
	# If a tie (such as choosing the start state), choose the variable involved in the most
	# constraints
	# this is to reduce branching factor, since fewer legal successors of that node

	max_unassigned_neighbours = 0

	# for each cell, get calc the degree
	for i in range(0, 9):
		for j in range(0, 9):
			num_unassigned_neighbours = 0
			var_neighbours = get_neighbors(grid,i,j)

			no_of_unassigned_var = 0
			for var in var_neighbours:
				i, j = var
				if grid[i][j] == 0:
					numUnassignedNeighbors += 1
			if num_unassignedNeighbors >max_unassigned_neighbours:
				degree_i = i
				degree_j = j
				max_unassigned_neighbours = num_unassigned_neighbors

	return degree_i, degree_j


# Get MRV (minimum remaining value) cell from the board, return that unassigned cell
# loction which can have minimum possible legal values
def get_MRV(grid):
	count = 0
	min_count = 82 # can be 81?

	# init mrv square to be top left square
	mrv_i = 0
	mrv_j = 0
	flag = False

	all_counts = []


	for i in range(0, 9):
		for j in range(0, 9):

			# get RV from each non-filled square
			if grid[i][j] == 0:
				flag = True
				count = 0
				for num in range(1, 9):
					if isValidMove(grid, i, j, num):
						count = count + 1
				# If current cell has mim minimum possible legal
				# values than our previous count,
				# update global count and update mrv cell values

				all_counts.append(count) # position of element in count will tell the cell

				if count < min_count:

					# keep track of all counts


					min_count = count
					mrv_i = i
					mrv_j = j

	#if flag == False:  # can't find any empty cell in sudoku board
	#    return -1, -1
	mrv_list = []
	for index, count in enumerate(all_counts):
		if count == min_count:
			mrv_list.append(index)



	# TODO if there is a tie value, use degree heuristics
	# there is a tie
	if len(mrv_list) >1:
		return -1, -1
	# there is no tie
	else:
		return mrv_i, mrv_j





#each time a value is assigned to a variable, the value is
#removed from the domain of the free variables that are either in the same line, in the
#same column or in the same square as the assigned variable
def solveBacktrackingFWD(grid):
	steps = 0
	prettyPrint(grid)

	# Get a unassigned loaction from the grid
	i, j = findUnassignedLocation(grid)

	if steps >10000:
		return grid, steps

	if i == -1:
		return True, steps

	# Solving sudoku by putting all possible values in unassigned loaction one by one and checking, backtrack if fail
	for num in range(1, 10):
		if isValidMove(grid, i, j, num):
			grid[i][j] = num
			steps = steps + 1


			# Recursive Call
			if solveBacktracking(grid)[0]: #return False to call for backtracking!!!
				return True, steps

			# Backtrack all the way until hit solvebacktracing -- true
			grid[i][j] = 0

	return False, steps
	# Game over check, if sudoku is solved fully or not
	i, j = findUnassignedLocation(grid, N)
	if i == -1:
		return True, consistencyChecks3



# Function to solve sudoku by back tracking
def solveBacktracking(grid):
	steps = 0
	prettyPrint(grid)

	# Get a unassigned loaction from the grid
	i, j = findUnassignedLocation(grid)

	if steps >10000:
		return grid, steps

	if i == -1:
		return True, steps

	# Solving sudoku by putting all possible values in unassigned loaction one by one and checking, backtrack if fail
	for num in range(1, 10):
		if isValidMove(grid, i, j, num):
			grid[i][j] = num
			steps = steps + 1


			# Recursive Call
			if solveBacktracking(grid)[0]: #return False to call for backtracking!!!
				return True, steps

			# Backtrack all the way until hit solvebacktracing -- true
			grid[i][j] = 0

	return False, steps

steps3 = 0

# Solve Sudoku using Backtracking + MRV + LCV + Forward Checking + degree
def solveSudokuBacktrackingMRVDegreefwdLCV(grid, N, M, K):

	lcv_queue = queue.PriorityQueue()
	# Game over check, if sudoku is solved fully or not
	i, j = findUnassignedLocation(grid, N)
	if i == -1:
		return True, steps3

	# Get MRV cell from the grid
	i, j = get_MRV(grid)
	if i == -1:
		i, j = get_degree(grid)

	# Get set of lcv values for chosen var cell
	lcv_queue = get_LCV(grid,  i, j)

	# find MRV then apply LCV to choose possible values with priority
	while not lcv_queue.empty():
		lcv_value = lcv_queue.get()
		if isValidMove(grid, i, j, lcv_value):
			grid[i][j] = lcv_value

			steps3 = step3 + 1

			# Do forward checking after assigning value to the cell
			fwdcheckingresult = do_forwardchecking(grid, i, j)

			if fwdcheckingresult == True:
				if solveSudokuBacktrackingMRVDegreefwdLCV(grid)[0]:
					return True, steps3
			else:
				grid[i][j] = 0

	return False, steps3


def runAll():

	for x in range(1, 72):
		for y in range(1, 11):
			grid = getGrid(os.path.join(fileDir, 'data/sudoku_problems/{}/{}.sd'.format(x, y)))
			boo, steps = solveBacktracking(grid)
			print(grid, steps)

def runOne(x, y, version):
	grid = getGrid(os.path.join(fileDir, 'data/sudoku_problems/{}/{}.sd'.format(x, y)))
	if version == 'A':
		boo, steps = solveBacktracking(grid)
	if version == 'B':
		boo, steps = solveBacktracking(grid)
	if version == 'C':
		boo, steps = solveBacktracking(grid)

if __name__ == "__main__":

	# Note: steps counting would not work for runAll()

	# 2bd: implement switch to choose between suing LCV or the other first

	runOne(36,8, 'B')
