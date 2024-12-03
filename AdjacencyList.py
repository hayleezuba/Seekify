# This is the adjacency List class that we will use to hold the dataset
class AdjacencyList:

    def __init__(self):
        # Create an empty dictionary to store graph
        self.graph = {}

    def addvertex(self, vertex):
        # Add vertex to graph if it does not exist already
        if vertex not in self.graph:
            self.graph[vertex] = {}

    def addedge(self, fromv, tov, weight):
        # Add an edge with weight to the graph
        self.addVertex(fromv)
        self.addVertex(tov)
        self.graph[fromv][tov] = weight

    def getneighbors(self, vertex):
        # Return the neighbors of a vertex using dictionary .get function
        return self.graph.get(vertex, {})
