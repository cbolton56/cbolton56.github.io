""" A Graph class implemented in python. 
A graph represented in Python by using dictionary objects.
Each instance of the graph has a member variable __graph_dict that
is a dictionary object. The keys of this object are nodes of the graph. 
Each key value pair has a value of list. The list can be filled with other nodes.
This class does not have functionality for digraphs.
Examples:
        Basic layout:  

        __graph_dict = {"key": ["edge"]}

        Empty graph: 

        __graph_dict = {}

        Graph object with multiple nodes that may have multiple edges: 

        __graph_dict = {"suzy": ["bob", "carol"], "bob":["suzy"], "carol": ["suzy"]}      """
class Graph(): 
    # Constructor
    def __init__(self, graph_dict = None):
        if graph_dict == None: 
            graph_dict = {}
        self.__graph_dict = graph_dict 

    #accessor function returns the nodes in a graph
    def nodes(self):
        #nodes are represented by keys in the dictionary object
        return list(self.__graph_dict.keys())

    def edges(self):
        return self.get_edges()

    def add_node(self, node): 
        #If the node isn't in the graph, this method adds the node.
        #Adds a key to the graph_dict object given by node paramter. 
        #Empty by default
        if node not in self.__graph_dict: 
            self.__graph_dict[node] = []
    
    #Takes a list of nodes and adds to the graph
    def add_nodes(self, nodes): 
        for node in nodes:
            self.add_node(node)
    
    def add_edge(self, edge): 
        #Assumes edge is of type tuple, i.e.: (node, node)
        if edge[0] not in self.__graph_dict: 
            self.__graph_dict[edge[0]] = []
        if edge[1] not in self.__graph_dict: 
            self.__graph_dict[edge[1]] = []
        self.__graph_dict[edge[0]].append(edge[1])
        self.__graph_dict[edge[1]].append(edge[0])

    def add_edges(self, edges): 
        #method for adding multiple edges at one time
        #takes a list of tuples
        for edge in edges:
            self.add_edge(edge)
    
    def get_edges(self): 
        #Return all edge pairs as a list of tuples
        edges = []
        for node in self.__graph_dict: 
            for neighbor in self.__graph_dict[node]: 
                if (neighbor, node) not in edges: 
                    edges.append((node, neighbor))
        return edges
    
    #Returns the direct neighbors of the node being passed in (one level out)
    def get_neighbors(self, node):
        neighbors = self.__graph_dict[node]
        return neighbors
    
    #Calculates degree of the node passed in 
    def get_degree(self, node): 
        degree = len(self.__graph_dict[node])
        return degree 

    #Overloaded __str__() method returns string representation of object
    def __str__(self):
        label = "vertices: "
        for k in self.__graph_dict:
            label += str(k) + " , "
        label += "\nedges: "
        for edge in self.get_edges():
            label += str(edge) + " "
        return label

