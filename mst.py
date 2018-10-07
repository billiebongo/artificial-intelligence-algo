
class MinimumSpanningTree:
    # matrix of roads
    road = [[]]

    # if not exists road
    infinit = 88

    # number of nodes
    nodes = -1

    #new addn attempt to fix out of range issue
    input = []

    # to store the visited nodes
    S = []

    # to store the father of node
    T = []

    # cost
    cost = 0

    # output
    output = []

    # constructor of the class
    def __init__(self):

        # do smth about this
        self.cost = 0

    # public method that gets the minimum cost spanning tree
    def getCost(self):

        return self.cost

    def solution(self, n):

        self.draw(n)
        f = open('minspantree.out', 'w')
        out = "Minimum cost = " + str(self.cost) + "\n"
        out += "Minimum Spanning Tree from 1 to {} => {}".format(n, str(self.output))
        f.write(out)
        f.close()
        return self.output

    def draw(self, node):

        if self.T[node] is not 0:
            self.draw(self.T[node])

        self.output.append(node)

        # this algorithm solves the problem with time running O(N^2)

    def solve(self):

        # define an array with n nodes
        print(self.nodes)
        self.S = [0] * (self.nodes + 1)

        # define an array with n nodes
        self.T = [0] * (self.nodes + 1)

        # start with the first node, if we start with second node, possibly we can get another spanning tree
        r = 1

        # step 1 => I mean the start node is selected and the rest of the nodes is r
        print(self.S)
        self.S[r] = 0

        for i in range(1, self.nodes + 1):

            if i is not r:
                self.S[i] = r

        # step 2

        self.cost = 0

        # execute of n-1 nodes
        for i in range(1, self.nodes):

            min = self.infinit

            for j in range(1, self.nodes + 1):

                if self.S[j] is not 0:

                    if self.road[self.S[j]][j] < min:
                        min = self.road[self.S[j]][j]

                        pos = j

            self.cost += self.road[self.S[pos]][pos]

            self.T[pos] = self.S[pos]

            self.S[pos] = 0

            for k in range(1, self.nodes + 1):

                if self.S[k] is not 0:

                    if self.road[self.S[k]][k] > self.road[pos][k]:
                        self.S[k] = pos

    # public method that reads the graph from an input file
    def buildGraph(self, input): #should pass in a list called input

        counter = 0

        #input = []
        #input = [['1', '2', 7], ['1', '3', 9], ['1', '6', 14], ['2', '3', 10], ['2', '4', 15]
        #    , ['3', '4', 11], ['3', '6', 2], ['4', '5', 6], ['5', '6', 9]]


            #for a_line in file:
                #counter += 1
                #if counter == 1:
                    #number_of_nodes = int(a_line.rstrip())
                #else:
                    #input.append(a_line.rstrip())

        size = len(input)

        self.road = [[0 for i in range(0, self.nodes + 1)] for j in range(0, self.nodes + 1)]

        for i in range(0, self.nodes + 1):

            for j in range(0, self.nodes + 1):

                if i == j:

                    self.road[i][j] = 0

                else:

                    self.road[i][j] = self.infinit

        for i in range(0, size):
            component = input[i]

            node1 = int(component[0])

            node2 = int(component[1])

            cost = int(component[2])
            print(self.road)
            print(self.nodes)
            self.road[node1][node2], self.road[node2][node1] = cost, cost

if __name__ == '__main__':
    ob = MinimumSpanningTree()
    print("$$$$$$ COST $$$$$$$")

    ob.nodes =6

    #input = [['1', '2', 7], ['1', '3', 9], ['1', '6', 14], ['2', '3', 10], ['2', '4', 15]
                 , ['3', '4', 11], ['3', '6', 2], ['4', '5', 6], ['5', '6', 9]]
    input=[['1', '2', 1448], ['1', '3', 4409], ['1', '4', 1252], ['1', '5', 2080], ['2', '3', 9109], ['2', '4', 4580], ['2', '5', 1544], ['3', '4', 6125],
     ['3', '5', 4913], ['4', '5', 6516], ['5','6', 10]]

    ob.buildGraph(input) # input is the
    print("WOW")
    ob.solve()
    print(ob.getCost())
    print(ob.getCost())
#ob = MinimumSpanningTree()

#ob.solve()

#print("Minimum Cost = ", ob.getCost())

#n = 1

#print("Give me from 1 to the node {} is {}".format(n, ob.solution(n)))