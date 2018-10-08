

from sudoku_utils import *
from queue import Queue
import queue
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
	for x in range(0, 9):
		if grid[i][x] == 0:
			for num1 in range(1, 81 + 1):
				if isValidMove(grid, x, j, num1):
					count = count + 1

					# Count 0 means this cell has now 0 legal values do return false
			if count == 0:
				return False
			count = 0

	count = 0
	# checking for sub grid
	subGridStartRow = i - i % 3
	subGridStartCol = j - j % 3

	for x in range(0, 3):
		for y in range(0, 3):

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
						if isValidMove(grid_copy, x, j, num1):
							count = count + 1


			# calc no of valid moves for each cell in row
			for x in range(0, 9):
				if grid_copy[i][x] == 0:
					for num1 in range(1, 10):
						if isValidMove(grid_copy, i, x, num1):
							count = count + 1

			# to
			subGridStartRow = i - i % 3
			subGridStartCol = j - j % 3

			#calc no of valid moves for each cell the subgrid
			for x in range(0, 3):
				for y in range(0, 3):
					if grid_copy[x + subGridStartRow][y + subGridStartCol] == 0:
						for num1 in range(1, 10):
							if isValidMove(grid_copy,  x + subGridStartRow, y + subGridStartCol, num1):
								count = count + 1

			lcv_queue.put(value, -1*count) # times -1 to make first value to have the highest counts/valid moves
	if lcv_queue.empty() == True:
		return None


	return lcv_queue

def get_neighbors(grid, i, j):

	neighbours = []
	neighbours += [(c, j) for c in range(9) if c != (i, j)]
	neighbours += [(i, c) for c in range(9) if c != (i, j)]
	subGridStartRow = i - i % 3
	subGridStartCol = j - j % 3
	for x in range(0, 3):
		for y in range(0, 3):
			neighbours.append((subGridStartRow+x, subGridStartCol+y))
	neighbours.remove((i, j))

	return neighbours



def get_degree(grid, min_count_cells):
	# the next var to be assigned will tbe the value which is involved in the most
	# no of constraints w other var
	# If a tie (such as choosing the start state), choose the variable involved in the most
	# constraints, this is to reduce branching factor, since fewer legal successors of that node

	max_unassigned_neighbours = 0

	# for each cell, get calc the degree

	for cell in min_count_cells:

		num_unassigned_neighbours = 0
		var_neighbours = get_neighbors(grid,cell[0],cell[1])

		no_of_unassigned_var = 0
		for var in var_neighbours:

			i, j = var[0], var[1]
			if grid[i][j] == 0:
				num_unassigned_neighbours += 1
		if num_unassigned_neighbours >max_unassigned_neighbours:
			#does not consider ties, just takes last one with count == maxcoutn

			degree_i = cell[0]
			degree_j = cell[1]
			max_unassigned_neighbours = num_unassigned_neighbours


	return degree_i, degree_j


# Get MRV (minimum remaining value) cell from the board, return that unassigned cell
# loction which can have minimum possible legal values
def get_MRV(grid):
	count = 0
	min_count = 82 # can be 81?
	flag = False

	min_count_cells = []
	for i in range(0, 9):
		for j in range(0, 9):
			# get RV from each non-filled square
			if grid[i][j] == 0:
				flag = True
				count = 0
				for num in range(1, 10):
					if isValidMove(grid, i, j, num):
						count = count + 1
				# If current cell has mim minimum possible legal
				# values than our previous count,
				# update global count and update mrv cell values

				#keep track of cells with the min_count. need tp refresh when a new min_count found

				if count ==  min_count:
					min_count_cells.append([i,j])

				if count < min_count:

					# keep track of all counts
					min_count_cells = []
					min_count_cells.append([i,j])
					min_count = count


	#if flag == False:  # can't find any empty cell in sudoku board
	#    return -1, -1


	if len(min_count_cells) >1:
		return True, min_count_cells # list of 2-element lists
	# there is no tie
	elif len(min_count_cells) == 1:
		return  False, min_count_cells # list of 1 2-element list
	else:
		print("Error, min count cells cant be 0")
		raise







#each time a value is assigned to a variable, the value is
#removed from the domain of the free variables that are either in the same line, in the
#same column or in the same square as the assigned variable
def solveBacktrackingFWD(grid):
	# Get a unassigned loaction from the grid
	i, j = findUnassignedLocation(grid)
	steps = 0

	#prettyPrint(grid)
	if i == -1:
		print("DONE!")
		print("wow")
		return True, steps

	# Solving sudoku by putting all possible values in unassigned loaction one by one and checking, backtrack if fail
	for num in range(1, 10):
		if isValidMove(grid, i, j, num):
			grid[i][j] = num
			steps = steps + 1
			# Recursive Call
			# Backtrack all the way until hit solvebacktracing -- true

			if do_forwardchecking(grid, i,j) == True:
				if solveBacktrackingFWD(grid)[0]:  # return False to call for backtracking!!!
					return True, steps
			#else:

			grid[i][j] = 0
	#print("sry no opt for {},{}! backrack".format(i,j))
	return False, steps
	# Game over check, if sudoku is solved fully or not
	#i, j = findUnassignedLocation(grid, N)
	#if i == -1:
#		return True, consistencyChecks3



# Function to solve sudoku by back tracking
def solveBacktracking(grid):


	# Get a unassigned loaction from the grid
	i, j = findUnassignedLocation(grid)
	steps=0
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


def get_MRV2(grid):
	count = 0
	global_count = 82
	mrv_i = 0
	mrv_j = 0
	flag = False

	for i in range(0, 9):
		for j in range(0, 9):
			if grid[i][j] == 0:
				flag = True
				count = 0
				for num in range(1, 10):
					if isValidMove(grid, i, j, num):
						count = count + 1
				# If current cell has mim minimum possible legal values than our previous count, update global count and update mrv cell values
				if count < global_count:
					global_count = count
					mrv_i = i
					mrv_j = j

	if flag == False:  # can't find any empty cell in sudoku board
		return -1, -1


	return mrv_i, mrv_j

# Solve Sudoku using Backtracking + MRV + LCV + Forward Checking
def solveSudokuBacktrackingMRVfwd(grid):
	global consistencyChecks3
	lcv_queue = queue.PriorityQueue()
	# Game over check, if sudoku is solved fully or not
	i, j = findUnassignedLocation(grid)
	if i == -1:
		prettyPrint(grid)
		return True, consistencyChecks3

	# Get MRV cell from the grid
	i, j = get_MRV2(grid)

	# Get set of lcv values for mrv cell
	lcv_queue = get_lcv(grid, i, j)
	if lcv_queue.empty():
		print("OMG")
	# Check by putting all lcv_values in MRV cell one by one and try to solve sudoku by backtracking and forward checking
	while not lcv_queue.empty():
		lcv_value = lcv_queue.get()
		if isValidMove(grid, i, j, lcv_value):
			grid[i][j] = lcv_value
			consistencyChecks3=3
			consistencyChecks3 = consistencyChecks3 + 1

			# Do forward checking after assigning value to the cell
			fwdcheckingresult = do_forwardchecking(grid,  i, j)

			if fwdcheckingresult == True:
				if solveSudokuBacktrackingMRVfwd(grid)[0]:
					return True, consistencyChecks3
			else:
				grid[i][j] = 0


	return False, consistencyChecks3
# Solve Sudoku using Backtracking + MRV + LCV + Forward Checking + degree
def solveSudokuBacktrackingMRVDegreefwdLCV(grid):

	lcv_queue = queue.PriorityQueue()
	# Game over check, if sudoku is solved fully or not
	i, j = findUnassignedLocation(grid)
	steps3=0
	# done
	if i == -1:
		return True, steps3
	# Get MRV cell from the grid
	tie, min_count_cells = get_MRV(grid)

	if tie == True:
		i, j = get_degree(grid, min_count_cells)
		#need to make sure only return one set? no ties
	else:

		i, j = min_count_cells[0][0], min_count_cells[0][1]

	# Get set of lcv values for chosen var cell
	lcv_queue = get_lcv(grid,  i, j)
	# find MRV then apply LCV to choose possible values with priority
	if lcv_queue != None:
		while not lcv_queue.empty():
			lcv_value = lcv_queue.get()

			if isValidMove(grid, i, j, lcv_value):
				grid[i][j] = lcv_value
				steps3=0
				steps3 += 1

				# Do forward checking after assigning value to the cell
				fwdcheckingresult = do_forwardchecking(grid, i, j)

				if fwdcheckingresult == True:
					if solveSudokuBacktrackingMRVDegreefwdLCV(grid)[0]:
						return True, steps3

				grid[i][j] = 0

	steps3 = 2132
	return False, steps3


def runAll(version):
	if version == 'A':


		for x in range(12, 13):
			for y in range(3, 5):
				grid = getGrid(os.path.join(fileDir, 'data/sudoku_problems/{}/{}.sd'.format(x, y)))
				boo, steps = solveBacktracking(grid)
				prettyPrint(grid)
	if version == 'B':
		for x in range(4, 6):
			for y in range(1, 7):
				print("NEW PROBLEM B!!!: {}/{}".format(str(x), str(y)))
				grid = getGrid(os.path.join(fileDir, 'data/sudoku_problems/{}/{}.sd'.format(x, y)))
				boo, steps = solveBacktrackingFWD(grid)
				prettyPrint(grid)
	if version == 'C':
		for x in range(10,12):
			for y in range(4, 7):
				print("NEW PROBLEM: {}/{}".format(str(x), str(y)))

				grid = getGrid(os.path.join(fileDir, 'data/sudoku_problems/{}/{}.sd'.format(x, y)))

				boo, steps = solveSudokuBacktrackingMRVDegreefwdLCV(grid)
				prettyPrint(grid)
	if version == 'C':
		for x in range(60, 70):
			for y in range(1, 5):
				print("NEW PROBLEM: {}/{}".format(str(x), str(y)))

				grid = getGrid(os.path.join(fileDir, 'data/sudoku_problems/{}/{}.sd'.format(x, y)))

				#boo, steps = solveSudokuBacktrackingMRVDegreefwdLCV(grid)
				boo, steps = solveSudokuBacktrackingMRVDegreefwdLCV(grid)
				prettyPrint(grid)


def runOne(x, y, version):
	grid = getGrid(os.path.join(fileDir, 'data/sudoku_problems/{}/{}.sd'.format(x, y)))
	if version == 'A':
		boo, steps = solveBacktracking(grid)
	if version == 'B':
		prettyPrint(grid)
		boo, steps = solveBacktrackingFWD(grid)
	if version == 'C':
		steps3 = 0

		boo, steps3 =  solveSudokuBacktrackingMRVDegreefwdLCV(grid)



if __name__ == "__main__":

	# Note: steps counting would not work for runAll()

	# 2bd: implement switch to choose between suing LCV or the other first

	#runOne(46,2, 'B')
	runAll('C')

	#runAll('B')
	#runAll('C')
