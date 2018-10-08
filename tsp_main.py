from kruskal import Kruskal
import math
#using A* search to solve tsp.

def calc_squared_distance(p1, p2): #p1 and p2 are lists
    # sqaured distance to shave off computational time

    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

def convert_input_into_readable_form_by_graph(input):
    #print(input)
    unique_nodes = []
    unique_nodes_dict = {}

    #find all the unique nodes
    for edge in input:
        if edge[0] not in unique_nodes:
            unique_nodes.append(int(edge[0]))
        if edge[1] not in unique_nodes:
            unique_nodes.append(int(edge[1]))
    #print(unique_nodes)
    # make dict w (node, index)
    index = 0
    for unique_node in unique_nodes:
        unique_nodes_dict[unique_node]=index
        index += 1
    #print(unique_nodes_dict)

    for edge in input:
    #    print(edge)
        edge[0] =  unique_nodes_dict[int(edge[0])]
        edge[1] = unique_nodes_dict[int(edge[1])]
    input_converted=input
    #print(input_converted)
    return input_converted


def get_h(input, num_of_nodes):
    """
    Given unvisited nodes return the cost of MST
    """

    #print(input)
    ob=Kruskal(num_of_nodes)
    input_converted = convert_input_into_readable_form_by_graph(input)
    #print(input_converted)
    ob.add_edges(input_converted)
    #need to convert input into running numbers
    cost = ob.KruskalMST()

    return cost

def get_input(nodes_dict, MST_nodes): #given pairs return input

    input = []
    #generate all possible unique pairs amongst unvisited nodes
    # do not include the unvisitednode aka the possible next node path in the pairs generation
    #print("first")
    for i in range(len(MST_nodes)):
        j = i+1

        #print(len(MST_nodes))
        while j < len(MST_nodes):
        # generate list of pairs
            #print(i,j)
            pair = [MST_nodes[i], MST_nodes[j]]

            pair.append(calc_squared_distance(nodes_dict[MST_nodes[i]], nodes_dict[MST_nodes[j]]))
            input.append(pair)
            j +=1
    #print(input)

    return input




    #[['1', '2', 7], ['1', '3', 9], ['1', '6', 14], ['2', '3', 10], ['2', '4', 15]
    #    , ['3', '4', 11], ['3', '6', 2], ['4', '5', 6], ['5', '6', 9]]





def solve_problem(nodes_dict):
    path = [1]  # visited nodes in order
    unvisited_nodes = [ *nodes_dict ] #list of dictionary keys

    unvisited_nodes.remove(1) # does not count returning to A either
    current_node=1 # start node is A by default
    #decide next step
    #print("len of unv nodes is {}".format(str(len(unvisited_nodes))))
    g=0
    while len(unvisited_nodes) >0:

        #choose the next step by calculating f of each of next steps (unvisited nodes)
        f_dict = {}
        for unvisited_node in unvisited_nodes:
            MST_nodes = [x for x in unvisited_nodes if x != unvisited_node ]
            #print("MST notes:")
            #print(MST_nodes)
            #print(len(unvisited_nodes))

            input=get_input(nodes_dict, MST_nodes)
            #print(input)
            #print("len of inpt")
            #print(len(input))
            #print("len of unvisited nodes {}".format(str(len(unvisited_nodes)-1)))
            if len(input)>0:
                h = get_h(input, len(unvisited_nodes)-1) # h is sum of MST built using
            #    print("h value is ".format(str(h)))
            else:
                h = 0
            # question: does the mst include the next-node?
            g_next = g + calc_squared_distance(nodes_dict[current_node], nodes_dict[unvisited_node])
            f = g_next + h

            f_dict[unvisited_node] = f

        #pick the unvisited node with the lowest f value
        next_node = min(f_dict.items(), key=lambda x: x[1])
        #print(type(next_node[0]))
        #print(nodes_dict)
        #print(path[-1])
        g =  g+ calc_squared_distance(nodes_dict[next_node[0]], nodes_dict[path[-1]])
        current_node = next_node[0]

        #print("next node is {}".format(next_node))
        #print(unvisited_nodes)
        path.append(next_node[0])
        unvisited_nodes.remove(next_node[0]) # is this modified globally
    #print(path)
    return path


def get_problem(no_of_cities, instance):
    #just for instance 5 of input size 5

    file_dir = "data/tsp_problems/{}/instance_{}.txt".format(str(no_of_cities), instance)
    with open(file_dir) as f:
        content = f.readlines()

    # all the file input converted into a nodes dictionary
    nodes_dict = {}
    # change the city_id from alphabet to numerical immediately after reading the file
    index = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6', "G":'7', 'H': '8', "I":'9', "J":'10'}
    for line in content[1:]:
        parts = line.split()
        #print(parts)
        nodes_dict[int(index[parts[0]])] = [int(parts[1]), int(parts[2])]
    return nodes_dict

def main():
    #for no_of_cities in range(1,17):
    for no_of_cities in range(1,10):
        for problem_id in range(1,11):
            nodes_dict= get_problem(no_of_cities, problem_id)
            path_soln = solve_problem(nodes_dict)
            print("NO OF CITIES: {}, PROB_ID: {}".format(no_of_cities, problem_id))
            print(path_soln)


if __name__ == '__main__':

    #add here if want to programmatically get each prpoblm

    #nodes_dict = get_problem(10, 2)
    #nodes_dict is now the dictionary containing unvisited nodes

    #path_soln = solve_problem(nodes_dict)
    main()









#The A* algorithm should find the MST of the unvisited cities and use the cost
# of the minimum spanning tree in computing h(n)
#shown above. The cost of a spanning tree is the sum of the edge costs of the tree.


#• Assume that A is always the starting city.
# Generate the successors of any state in alphabetical order.