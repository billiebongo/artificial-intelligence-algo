

import copy



DISCOUNT = 1
plain_action_template=[
["*","*","*","*"],
["*","*","*","*"],
["*","*","*","*"],
]


def pretty_print_grid(GRID):
	for r in range(3):
		print([round(val, 3)for val in GRID[r]])
	return

def is_wall(GRID,row,col):
	"""Return value of current grid if next move is a wall"""
	if row < 0 or row > 2:
		return True
	if col<0 or col>3:
		return True
	if GRID[row][col]==-99:
		return True
	return False

def get_utility(GRID, r,c,action):
	"""get utility given action and curr position"""
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


def calc_expected_utility(GRID,j,k, show_calc=False):
	"""Calc expected utility given position by chooseing best action"""
	#up
	up_EU = 0.8*get_utility(GRID,j,k, "up") + 0.1*get_utility(GRID,j,k, "left") +0.1*get_utility(GRID,j,k, "right")

	#down
	down_EU = 0.8*get_utility(GRID,j,k,"down") + 0.1*get_utility(GRID,j,k, "left") +0.1*get_utility(GRID,j,k,  "right")
	left_EU = 0.8*get_utility(GRID, j,k, "left") + 0.1*get_utility(GRID, j,k,"up") +0.1*get_utility(GRID, j,k, "down")
	right_EU = 0.8*get_utility(GRID,j,k,  "right") + 0.1*get_utility(GRID,j,k,  "up") +0.1*get_utility(GRID, j,k,"down")

	if show_calc==True:
		print(down_EU)
		print(down_EU)
		print("up EU:")
		print("{}=0.8*{}+0.1*{}+0.1*{}".format(up_EU,get_utility(GRID,j,k, "up"), get_utility(GRID,j,k, "left"), get_utility(GRID,j,k, "right")))
		print("down EU:")
		print("{}=0.8*{}+0.1*{}+0.1*{}".format(down_EU, get_utility(GRID,j,k,"down"), get_utility(GRID,j,k, "left"), get_utility(GRID,j,k,  "right")))
		print("left EU:")
		print("{}=0.8*{}+0.1*{}+0.1*{}".format(left_EU, get_utility(GRID,j,k,"left"), get_utility(GRID,j,k, "up"), get_utility(GRID,j,k,  "down")))
		print("right EU:")
		print("{}=0.8*{}+0.1*{}+0.1*{}".format(right_EU, get_utility(GRID,j,k,"right"), get_utility(GRID,j,k, "up"), get_utility(GRID,j,k,  "down")))




	dict={"up":up_EU, "down": down_EU, "left": left_EU, "right":right_EU}

	best_action = max(dict.keys(), key=(lambda key: dict[key]))
	best_utility = dict[best_action]
	policies = {'^': up_EU,
				'v': down_EU,
				'<': left_EU,
				'>': right_EU}

	best_action = ''
	for action, utility in policies.items():
		if utility > best_utility:
			best_utility = utility
			best_action = action
		elif utility == best_utility:
			best_action += action

	#if best_action == "up":
	#	return up_EU, "^"
	#if best_action == "down":
	#	return down_EU, "v"
	#if best_action == "left":
	#	return left_EU, "<"
	#if best_action == "right":
	#	return right_EU, ">"
	return best_utility, best_action

def pretty_print_best_action(act_grid):
	for r in range(3):
		print(act_grid[r])
	return

def highlight_if_state_changed(prev_state, curr_state,j,k):
	if prev_state != curr_state:
		print("State at {}{} changed from {} to {}".format(j+1,k+1, prev_state, curr_state))
	return

def bellman_update(GRID, R, i,action_grid):
	""" bellman equation """
	NEW_GRID = copy.deepcopy(GRID)
	prev_action_grid=copy.deepcopy(action_grid)
	action_grid = copy.deepcopy(plain_action_template)
	if i==3:
		print("Init value of U2(s13)")
		print(GRID[0][2])
		for j in range(3):
			for k in range(4):
				prev_action =  prev_action_grid[j][k]
				if (GRID[j][k] != -99) and (GRID[j][k] != 1) and (GRID[j][k] != -1):
					show_calc=True if (j == 0 and k== 2) else False
					exp_util_grid, best_action = calc_expected_utility(GRID, j, k, show_calc=show_calc)

					new_value = R + DISCOUNT * exp_util_grid
					NEW_GRID[j][k] = new_value
					action_grid[j][k] = best_action
					highlight_if_state_changed( prev_action ,best_action, j,k)
		print("After update at U3(s13)")
		print(NEW_GRID[0][2])
	else:
		for j in range(3):
			for k in range(4):
				prev_action = prev_action_grid[j][k]

				if (GRID[j][k] != -99) and (GRID[j][k] != 1) and (GRID[j][k] != -1):
					exp_util_grid, best_action =calc_expected_utility(GRID,j,k)

					new_value = R + DISCOUNT * exp_util_grid
					NEW_GRID[j][k] = new_value
					action_grid[j][k]=best_action
					highlight_if_state_changed( prev_action ,best_action, j,k)


	return NEW_GRID, action_grid



def main():
	"""R(s)=-0.05"""
	GRID = [
		[0, 0, 0, 0],
		[0, -99, 0, -1],
		[0, 0, 0, 1]
	]
	print("********************* Q1 **************************")
	R = -0.05
	print("~~~~Iteration 0~~~~")

	pretty_print_grid(GRID)
	ACTION_GRID=copy.deepcopy(plain_action_template)
	for i in range(1,11):

		#iterate whole grid
		print("~~~~Iteration {}~~~~".format(i))

		GRID, ACTION_GRID=bellman_update(GRID, R, i, ACTION_GRID)
		pretty_print_best_action(ACTION_GRID)
		pretty_print_grid(GRID)


	print("********************* Q2 ************************")
	GRID = [
		[0, 0, 0, 0],
		[0, -99, 0, -1],
		[0, 0, 0, 1]
	]

	print("~~~~Iteration 0~~~~")

	R = -0.1
	pretty_print_grid(GRID)
	ACTION_GRID=plain_action_template
	for i in range(1,11):

		#iterate whole grid
		print("~~~~Iteration {}~~~~".format(i))

		GRID, ACTION_GRID=bellman_update(GRID, R, i, ACTION_GRID)
		pretty_print_grid(GRID)
		pretty_print_best_action(ACTION_GRID)

# question 1

if __name__ == '__main__':
	main()
