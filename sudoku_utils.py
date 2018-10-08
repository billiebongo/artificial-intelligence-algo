#Goal:
#solve one problem first with backtracking

import os

# Function for Checking validity of putting num value in (i,j) in corresponding row i
def isRowOK(grid, i,num):
    for x in range(0, 9):
        if grid[i][x] == num:
            return False

    return True


# Function for Checking validity of putting num value in (i,j) in corresponding coilum j
def isColOK(grid, j,num):
    for x in range(0, 9):
        if grid[x][j] == num:
            return False

    return True


# Function for Checking validity of putting num value in (i,j) in corresponding subgrid in which (i,j) lies
def isSubGridOK(grid, i, j, num):
    subGridStartRow = i - i % 3
    subGridStartCol = j - j % 3

    for x in range(0, 3):
        for y in range(0, 3):
            if grid[x + subGridStartRow][y + subGridStartCol] == num:
                return False

    return True

def prettyPrint(grid):
    for line in grid:
        print(line)
    print("*******************************")


# Function for Checking validity of putting num value in (i,j) in corresponding its row, column and subgrid
def isValidMove(grid, i, j, num):
    if isRowOK(grid, i, num) and isColOK(grid, j, num) and isSubGridOK(grid, i, j, num):
        return True

    return False


def check_row_constraint():

    return False

    return True

def check_square_constraint():

    return False

    return True



def print_matrix(matrix):
    return


# Function for finding first unassigned loction in the grid
def findUnassignedLocation(grid):
    print(grid)
    print("CANT FIND UNASS")
    for i in range(0, 9):
        for j in range(0, 9):
            if grid[i][j] == 0:
                return i, j

    return -1, -1


# Function to read the game state, returning N, M, K and grid as tuple
def getGrid(filename):
    # Reading file


    with open(filename) as f:
        contents = f.readlines()



    grid = []

    for line in contents:
        if len(line)>5:
            grid.append([int(x) for x in line.replace('\n', '')[:-1].split(' ')])

        # matrix of integers

    return grid

if __name__ == "__main__":
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    grid = getGrid(os.path.join(fileDir,'data/sudoku_problems/9/9.sd'))
    print(grid)