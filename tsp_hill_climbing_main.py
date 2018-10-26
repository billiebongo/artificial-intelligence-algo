
# Hill climbing to solve tsp
from random import shuffle, randint
#hill climbing, hill climbing with sideway moves/tabu list, hill climbing with
#random restarts and simulated annealing

import math, time
from copy import deepcopy


# choose the next step via variants of hill-climbing

NEOS = [316.10358471577694672,323.74184111902809491,336.44117706454306926,319.03985563860504726,350.88477171906680496,310.65436274546681261,271.18108846868659612,358.51551945872574834,272.5668684593473472,321.91546526419000429,314.60641810464716173,315.67319555391827635,280.22569636412788441,325.61137238217770573,377.40807614384965518,290.98024642651364502,349.57186161285113712,342.88941622205408066,354.57378356556142762,326.24414680546965428,404.05976463101109175,354.05678074398855415,359.6415441018805268,345.81330305295165317,356.70815656201915544,345.88487686852585057,372.71499440859201968,356.22100951124315316,243.0194642572020598,329.95225502916144933]

#for q5
NEOS_2 = [318, 324, 314, 318, 404, 353]


def calc_squared_distance(p1, p2): #p1 and p2 are 2-element lists
    # squared distance to shave off computational time
    return math.sqrt((int(p1[0])-int(p2[0]))**2 + (int(p1[1])-int(p2[1]))**2)

def swap(copy, i):
    """swap pos i and i+1"""
    a=copy[i]
    copy[i]=copy[i+1]
    copy[i+1]=a
    return copy

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

    swap_count = len(current) -1
    # eg for len of 3, swap (0,1) and (1,2)
    smallest_cost = 999999999999
    smallest_cost_path = None
    for i in range(swap_count):
        #total num of swaps is (len of path -1)
        copy=deepcopy(current)

        neighbour_path=swap(copy, i)
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

    cost = calc_cost(curr, nodes_dict)
    init_cost = cost

    while True:
        next_path, next_cost = get_best_neighbour(curr, nodes_dict)
        if cost <= next_cost:
            break
        #print(next_cost)
        #print("moving to the neighbour")
        #print("new path")
        #print(next_path)
        curr = next_path
        count+=1
        cost=next_cost
    #print("init cost: "+str(init_cost))
    #print("final cost:"+str(cost))
    #print("count"+str(count))

    return curr, cost, count

#tabu list means dont go back to <= 100 recently visited nodes
#keep track via queue

#version B
def hill_climbing_sideway_moves(nodes_dict):
    """totally useless but will implement for evidence anyway"""


    count = 0
    curr = list(nodes_dict.keys())
    shuffle(curr)
    print(curr)
    print(nodes_dict)
    cost = calc_cost(curr, nodes_dict)
    init_cost = cost
    sideway_count = 0
    while True:
        next_path, next_cost = get_best_neighbour(curr, nodes_dict)
        if cost < next_cost:
            break
        if cost == next_cost:
            raise
            #if sideway_count <100:
            #    sideway_count += 1
            #else:
            #    raise

        print(next_cost)
        print("moving to the neighbour")
        print("new path")
        print(next_path)
        curr = next_path
        count+=1
        cost=next_cost
    #print("init cost: "+str(init_cost))
    #print("final cost:"+str(cost))
    #print("count"+str(count))
    return curr, cost, count


#version E
def hill_climbing_infinite_restarts(nodes_dict, NEOS_value):
    """
    check if the found local optimum has lower cost than currently-stored “best” local optimum, and replace it if so
    rerun hill climbing from another random start state
    restart if local opt found,
    With random restarts, hill climbing can explore different parts of the search space as opposed to being stuck at one local optimum.
    """
    count = 0
    restart_count = 0
    curr = list(nodes_dict.keys())
    shuffle(curr)

    cost = calc_cost(curr, nodes_dict)
    quality = 999
    while quality > 1.01:
        while True:
            next_path, next_cost = get_best_neighbour_swap(curr, nodes_dict)
            if cost <= next_cost:
                shuffle(curr)
                restart_count += 1

                break

            curr = next_path
            count+=1
            cost=next_cost

        quality=cost/NEOS_value
    print(curr)
    print(cost)
    return restart_count

#version C
def hill_climbing_random_restarts(nodes_dict, num_restarts):
    """
    check if the found local optimum has lower cost than currently-stored “best” local optimum, and replace it if so
    rerun hill climbing from another random start state
    restart if local opt found,
    With random restarts, hill climbing can explore different parts of the search space as opposed to being stuck at one local optimum.
    """
    count = 0
    restart_count = 0
    curr = list(nodes_dict.keys())
    shuffle(curr)

    cost = calc_cost(curr, nodes_dict)
    init_cost = cost
    while restart_count < num_restarts:
        while True:
            next_path, next_cost = get_best_neighbour(curr, nodes_dict)
            if cost <= next_cost:
                shuffle(curr)
                restart_count += 1
                break

            curr = next_path
            count+=1
            cost=next_cost

    return curr, cost, count


def get_random_neighbour(nodes_dict):
    # neighbour defined as swap adjacent
    path = list(nodes_dict.keys())
    r = randint(0,len(path)-2)
    path = swap(path, r)
    cost= calc_cost(path, nodes_dict)
    return path, cost

#versionD
def hill_climbing_simulated_annealing(nodes_dict, type):
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
        annealing schedules, for example, exponential, logarithmic, and linear.
    """
    T = 10000

    count = 0
    curr = list(nodes_dict.keys())
    shuffle(curr)
    cost = calc_cost(curr, nodes_dict)
    init_cost = cost
    while T>0:
        next_path, next_cost = get_random_neighbour(nodes_dict)
        E = cost -next_cost
        if E>0:
            curr = next_path
            cost = next_cost
        else:
            p=math.exp(E/T)
            if p > 0.5:
                curr=deepcopy(next_path)
                cost=next_cost


        if type == 'expo':
            T -= math.exp(- 0.00000000000000000000000000000000005 * T) #some random constant ??
        elif type == 'log':
            if T == 1:
                break

            T -= math.log(T)
        else:
            T -=5

        curr = next_path
        count+=1
        cost=next_cost

    return curr, cost

def versionE(nodes_dict, NEOS_value):
    """sideway count on hillclimbing"""
    restart_count = hill_climbing_infinite_restarts(nodes_dict, NEOS_value)

    return restart_count

def versionD(nodes_dict, schedule):
    """sideway count on hillclimbing"""
    best_path, cost = hill_climbing_simulated_annealing(nodes_dict, schedule)

    return best_path,cost

def versionC(nodes_dict, num_restarts):
    """sideway count on hillclimbing"""
    best_path = hill_climbing_random_restarts(nodes_dict, num_restarts)

    return best_path

def versionB(nodes_dict):
    """sideway count on hillclimbing"""
    best_path = hill_climbing_sideway_moves(nodes_dict)

    return best_path

def versionA(nodes_dict):
    """basic hill climbing"""


    best_path, cost, count =  hill_climbing(nodes_dict) #pass in A as need to calc dist to end point

    return best_path, cost, count


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

def q2():
    s = 0
    for no_of_cities in range(14,17):
        print("########### NO OF CITIES: " + str(no_of_cities) + "############")

        for problem_id in range(1,11):
            average_count = 0
            sum=0
            print("NO OF CITIES: {}, PROB_ID: {}".format(no_of_cities, problem_id))
            better_than_NEOS = 0
            nodes_dict = get_problem(no_of_cities, problem_id)
            for i in range(100):

                best_path, cost, count = versionA(nodes_dict)
                if cost <= NEOS[s]:
                    better_than_NEOS +=1
                sum += cost
                average_count += count
            C_ls = sum/100

            # number of instances out of 100 better than NEOS
            print(better_than_NEOS)

            #avg no of steps
            print(average_count/100)

            #performance measuremenbts
            print(C_ls/NEOS[s])

            s += 1

    return

def find_no_of_restarts_for_best_soln():
    s=0
    for no_of_cities in range(14,17):
        print("########### NO OF CITIES: " + str(no_of_cities) + "############")

        for problem_id in range(1,3):
            print("NO OF CITIES: {}, PROB_ID: {}".format(no_of_cities, problem_id))
            nodes_dict = get_problem(no_of_cities, problem_id)
            print(versionE(nodes_dict, NEOS_2[s]))
            s += 1
    return

def q5():
    s = 0
    for no_of_cities in range(16,17):
        print("########### NO OF CITIES: " + str(no_of_cities) + "############")

        for problem_id in range(1,3):
            print("NO OF CITIES: {}, PROB_ID: {}".format(no_of_cities, problem_id))
            nodes_dict = get_problem(no_of_cities, problem_id)
            num_restarts_test = [100, 500, 1000, 1500, 2000, 2500 ]
            for r in num_restarts_test:
                print("NUMBER OF RESTARTS: "+str(r))
                start_time = time.time()
                sum = 0
                for i in range(100):

                    best_path, cost, count = versionC(nodes_dict, r)

                    sum += cost

                C_ls = sum / 100


                # performance measuremenbts/avg solution quality
                quality = C_ls / NEOS_2[s]
                print(quality)

                #avg soln time
                print("time: "+str((time.time()-start_time)/100))

                if quality <= 1.01:
                    print("WOW quality is "+str(quality))


            s += 1


        return

def q7():
    import time
    s=0
    schedules=['linear', 'expo', 'log']
    s = 0
    for no_of_cities in range(14, 17):
        print("########### NO OF CITIES: " + str(no_of_cities) + "############")

        for problem_id in range(1, 3):
            for schedule in schedules:
                sum_quality=0
                sum_time=0
                print("No cities: {} Prob ID: {} Schedule {}".format(no_of_cities, problem_id, schedule))
                for r in range(100):

                    start_time = time.time()

                    nodes_dict = get_problem(no_of_cities, problem_id)
                    best_path, cost= versionD(nodes_dict, schedule)
                    sum_quality+=cost/NEOS_2[s]
                    sum_time+=(time.time() - start_time)
                print("quality:"+str(sum_quality/100))
                print("time:"+str(sum_time/100))
            s += 1
def test():
    nodes_dict = get_problem(14, 1)
    versionA(nodes_dict)
    return
if __name__ == '__main__':
    print("Q2")
    #q2()
    print("Q5")
    #q5()
    #find_no_of_restarts_for_best_soln()
    print("Q7")
    q7()
    #test()
