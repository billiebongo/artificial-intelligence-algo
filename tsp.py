
#using A* search to solve tsp.

def calc_squared_distance(p1, p2): #p1 and p2 are lists
    # sqaured distance to shave off computational time
    return (p1[0]-p2[0])**2 + (p1[1]-p2[2])**2

def build_MST(remaining_cities): # remaining_cities is a dict

    # numner of cities on map
    # implement TSP as a search algo

    #    sort the edges of G in increasing order of cost

    #keep a subgraph of G and calc all edges. for each edge in sorted order, if not connected to graph, add edge tp graph.



return S

file_dir = "/data/tsp_problems/{}".format(str(no_of_cities))

    # generate all posible edges given points

    # add edges to the graph
    g = Graph()
    for key, value in remaining_cities.items(): #value is a list of x,y
        g.add_vertex(key)

        #add an edge for vertex to the other vertex
        for key2, value2 in remaining_cities.items():
            if (key != key2):
                distance = calc_squared_distance(value, value2)
                g.add_edge(key, key2, distance)



    return h #total weight of MST

def select_next_city(remaining_cities):

    f = calc_f(g, h)

    for k, v in remaining_cities.items():
        # find g
        #find h
        #find f

    select the smallest f

    # choose the lowest f






if __name__ == '__main__':
    # start at A.
    # all nodes
    # Add a to the path
    # if there are stll unvisited nodes
    # find next point to go to by puttinf in unvisited nodes
    # delete thatchosen node from unvisited nodes.






#The A* algorithm should find the MST of the unvisited cities and use the cost
# of the minimum spanning tree in computing h(n)
#shown above. The cost of a spanning tree is the sum of the edge costs of the tree.


#• Assume that A is always the starting city.
# Generate the successors of any state in alphabetical order.