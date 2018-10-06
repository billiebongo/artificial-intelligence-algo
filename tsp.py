import mst.MinimumSpanningTree
#using A* search to solve tsp.

def calc_squared_distance(p1, p2): #p1 and p2 are lists
    # sqaured distance to shave off computational time
    return (p1[0]-p2[0])**2 + (p1[1]-p2[2])**2

def get_h(input):
    ob = MinimumSpanningTree()
    ob.buildGraph(input)
    ob.solve()
    return ob.getCost()

def get_input(nodes_dict, unvisited_nodes): #given pairs return input

    input = []
    #generate unique pairs of unvisited nodes
    for i in range(len(unvisited_nodes)):
        j = i +1
        while j < len(unvisited_nodes):
        # generate list of pairs
            pair = [unvisited_nodes[i], [j]]
            pair.append(calc_squared_distance(nodes_dict[unvisited_nodes[i]], nodes_dict[unvisited_nodes[j]]))
            input.append(pair)
    print(input)

    return input




    #[['1', '2', 7], ['1', '3', 9], ['1', '6', 14], ['2', '3', 10], ['2', '4', 15]
    #    , ['3', '4', 11], ['3', '6', 2], ['4', '5', 6], ['5', '6', 9]]



if __name__ == '__main__':

    #just for instance 5 of input size 5

    file_dir = "/data/tsp_problems/5/instance_{}.txt".format(str(no_of_cities))
    with open(fname) as f:
        content = f.readlines()

    # all the file input converted into a nodes dictionary
    nodes_dict = {}
    # change the city_id from alphabet to numerical immediately after reading the file
    index = {'A': '1', 'B': '2', 'C': '3', 'D': '4', 'E': '5', 'F': '6'}
    for line in content:
        parts = line.split()
        print(parts)
        nodes_dict[index[parts[0]]] = [parts[1], parts[2]]

    print(nodes_dict) # all the lines read from the file
    #nodes_dict is now the dictionary containing unvisited nodes
    path = ['1'] #visited nodes in order

    unvisted_nodes = [ *nodes_dict ]
    unvisted_nodes.remove('1') # does not count returning to A either
    current_node="1" # start node is A by default
    #decide next step
    while unvisited nodes is not empty:

        #choose the next step by calculating f of each of next steps (unvisited nodes)
        f_dict = {}
        for unvisited_node in unvisited_nodes:
            h = get_h(get_input(unvisted_nodes))
            # question: does the mst include the next-node?
            new_distance = calc_squared_distance()
            g = g + calc_squared_distance(nodes_dict[current_node], nodes_dict[unvisted_node])
            f = g + h

        #pick the unvisited node with the lowest f value
        next_node = min(d.items(), key=lambda x: x[1])
        path.append(next_node)

        unvisted_nodes.pop(next_node)

    print(path)










#The A* algorithm should find the MST of the unvisited cities and use the cost
# of the minimum spanning tree in computing h(n)
#shown above. The cost of a spanning tree is the sum of the edge costs of the tree.


#• Assume that A is always the starting city.
# Generate the successors of any state in alphabetical order.