
# Hill climbing to solve tsp
from random import shuffle
#hill climbing, hill climbing with sideway moves/tabu list, hill climbing with
#random restarts and simulated annealing

import math

# choose the next step via variants of hill-climbing


def calc_squared_distance(p1, p2): #p1 and p2 are 2-element lists
    # squared distance to shave off computational time
    return math.sqrt((int(p1[0])-int(p2[0]))**2 + (int(p1[1])-int(p2[1]))**2)

def swap(current, i):
    """swap pos i and i+1"""
    a=current[i]
    current[i]=current[i+1]
    current[i+1]=a
    return current

def calc_cost(path, nodes_dict):
    """has to calc return to start"""
    cost = 0
    for i in range(len(path)):
        if i != (len(path)-1):
            cost += calc_squared_distance(nodes_dict[path[i]],nodes_dict[path[i+1]])
        else:
            #add cost of dist from end point to starting point

            cost += calc_squared_distance(nodes_dict[path[0]], nodes_dict[path[i]])
    return cost



def get_best_neighbour(current, nodes_dict):
    """generate all neighbours by swapping adj cities """
    swap_count = len(current) -2
    # eg for len of 3, swap (0,1) and (1,2)
    smallest_cost = 999999999999
    smallest_cost_path = None
    for i in range(swap_count):
        #total num of swaps is (len of path -1)
        neighbour_path=swap(current, i)
        #print("neighbour PATH")
        #print(neighbour_path)
        cost = calc_cost(neighbour_path, nodes_dict)
        #print(cost)
        if cost< smallest_cost:
            smallest_cost = cost
            smallest_cost_path = neighbour_path
    #print("SMALLEST COST")
    #print(smallest_cost)
    return smallest_cost_path, smallest_cost





# neighbour is list of coordinates tuple
# current is a tuple
#version A
def hill_climbing(nodes_dict):
    count = 0
    curr = list(nodes_dict.keys())
    shuffle(curr)
    print(curr)
    print(nodes_dict)
    cost = calc_cost(curr, nodes_dict)
    init_cost = cost
    while True:
        next_path, next_cost = get_best_neighbour(curr, nodes_dict)
        if cost <= next_cost:
            print("local opt reached!")
            break
        print(next_cost)
        print("moving to the neighbour")
        print("new path")
        print(next_path)
        curr = next_path
        count+=1
        cost=next_cost
    print("init cost: "+str(init_cost))
    print("final cost:"+str(cost))
    print("count"+str(count))
    return curr, cost

#tabu list means dont go back to <= 100 recently visited nodes
#keep track via queue

#version B
def hill_climbing_sideway_moves():
    """
    curr =  random_statr
    while true:
        next = get_next_best_neighbour(curr)
        if cost(curr) < cost(next):
            print("strict local min")
            break
        if cost(curr) == cost(next):
            #if not over sideway limit
                then move to neighbour and increment sideway count
            else:
                break
        move to neighbour
        reset sideway count
        """
    return

#version C
def hill_climbing_random_restarts():

    pass

#versionD
def hill_climbing_simulated_annealing():
    """
    curr = initial
    T =  99999999
    while T >0:
        next = a random neighbour
        change in E = curr.cost -  next.cost
        if change in E>0
            curr = next
        else curr = next with prob p=e to the power of change of E divide T
        dec T
    """
    return



def versionA(nodes_dict):
    """basic hill climbing"""


    best_path =  hill_climbing(nodes_dict) #pass in A as need to calc dist to end point

    return best_path


def get_problem(no_of_cities, instance):
    """
    open file given the no of cities and the file name
    return file contents in format function solve_problem(nodes_dict) needs
    """
    file_dir = "data/tsp_problems/{}/instance_{}.txt".format(str(no_of_cities), instance)
    with open(file_dir) as f:
        content = f.readlines()

    # all the file input converted into a nodes dictionary
    nodes_dict = {}
    # change the city_id from alphabet to numerical immediately after reading the file
    #index = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6', "G":'7',
    #         'H': '8', "I":'9', "J":'10', "K":'11', "L":'12', "M":'13', "N":'14', "O":'15', "P":'16'}
    for line in content[1:]:
        parts = line.split()
        nodes_dict[parts[0]] = [int(parts[1]), int(parts[2])]
    return nodes_dict

def main():
    #for no_of_cities in range(14,17):
    #    for problem_id in range(7,11):
    no_of_cities, problem_id = 15,4
    nodes_dict = get_problem(no_of_cities, problem_id)
    best_path = versionA(nodes_dict)
    print("NO OF CITIES: {}, PROB_ID: {}".format(no_of_cities, problem_id))


if __name__ == '__main__':
    main()