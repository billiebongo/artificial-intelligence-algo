

import copy
#GRID=[
 #   [0, 0, 0, 0],
 #   [0, 99, 0, -1],
  #  [0, 0, 1, 1]
#]
#testing


DISCOUNT = 1

R=-0.04

def pretty_print_grid(GRID):
	for r in range(3):
		print(GRID[r])
	return

def is_wall(GRID,row,col):
	if row < 0 or row > 2:
		return True
	if col<0 or col>3:
		return True
	if GRID[row][col]==-99:
		return True
	return False

def get_utility(GRID, r,c,action):
    #if is wall
    if action == "up":
        if is_wall(GRID,r-1,c):
            return GRID[r][c]
        else:
            return GRID[r-1][c]
    if action == "down":
        if is_wall(GRID,r+1,c):
            return GRID[r][c]
        else:
            return GRID[r+1][c]
    if action == "left":
        if is_wall(GRID,r,c-1):
            return GRID[r][c]
        else:
            return GRID[r][c-1]
    if action == "right":
        if is_wall(GRID,r,c+1):
            return GRID[r][c]
        else:
            return GRID[r][c+1]


def calc_expected_utility(GRID,j,k):
	#up
	up_EU = 0.8*get_utility(GRID,j,k, "up") + 0.1*get_utility(GRID,j,k, "left") +0.1*get_utility(GRID,j,k, "right")

	#down
	down_EU = 0.8*get_utility(GRID,j,k,"down") + 0.1*get_utility(GRID,j,k, "left") +0.1*get_utility(GRID,j,k,  "right")
	left_EU = 0.8*get_utility(GRID, j,k, "left") + 0.1*get_utility(GRID, j,k,"up") +0.1*get_utility(GRID, j,k, "down")
	right_EU = 0.8*get_utility(GRID,j,k,  "right") + 0.1*get_utility(GRID,j,k,  "up") +0.1*get_utility(GRID, j,k,"down")


	dict={"up":up_EU, "down": down_EU, "left": left_EU, "right":right_EU}

	best_action = max(dict.keys(), key=(lambda key: dict[key]))

	if best_action == "up":
		return up_EU
	if best_action == "down":
		return down_EU
	if best_action == "left":
		return left_EU
	if best_action == "right":
		return right_EU



def bellman_update(GRID):
	NEW_GRID = copy.deepcopy(GRID)
	for j in range(3):
		for k in range(4):
			if (GRID[j][k] != -99) and (GRID[j][k] != 1) and (GRID[j][k] != -1):
				new_value = R + DISCOUNT * calc_expected_utility(GRID,j,k)
				NEW_GRID[j][k] = new_value
			else:
				print("IM OUT")
	return NEW_GRID



def q1():
	"""R(s)=-0.05"""
	GRID = [
		[0, 0, 0, 0],
		[0, -99, 0, -1],
		[0, 0, 0, 1]
	]
	for i in range(5):

		#iterate whole grid
		print("""iteration""")
		pretty_print_grid(GRID)
		GRID=bellman_update(GRID)




# question 1

if __name__ == '__main__':
	q1()
