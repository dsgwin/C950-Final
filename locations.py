import csv

# Vertex Class
# from zyBooks section 6.6.1
class Vertex:
    def __init__(self, label):
        self.label = label

# Graph class
# From zyBooks section 6.6.2
class Graph:
    def __init__(self):
        self.adjacency_list = {}    # adjacency list tracks what edges are connected
        self.edge_weights = {}      # edge_weights tracks the distance or 'weight' between vertices

    # adds an adjacency to the list
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    # adds directed edge to the graph and updates edge weight and adjacency list
    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    # adds an undirected edge, which is technically two directed edges from the two supplied vertices
    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)

    # this function checks the edge_weight between two verticies and returns the value
    def compare_distance(self, start_vertex, end_vertex):
        weight = self.edge_weights[start_vertex, end_vertex]
        return weight

# A method to take in the CSV data file and return it in a list of lists format
# which will simplify iterating to create the graph
def get_distance_data(filename):
    distanceCSV = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            distanceCSV.append(row)
    return distanceCSV

# This method takes in the CSV file as a positional argument and calls the get_distance_data function
# The data is then used to create the graph used to lookup edge weights
def create_graph(filename):
    distance_table = get_distance_data(filename)    # Call to get_distance_data returns list of lists of CSV data
    distance_graph = Graph()                # Creates instance of the graph object
    for row in distance_table:              # for each row in the distance_table
        distance_graph.add_vertex(row[1])   # the second column containing street address is added as vertex

    for row in distance_table:                      # for each row in the distance_table
        for i in range(3,len(distance_table)+3):    # iterate through each row's column through the end of the row
            if row[i] != '':                        # if the distance cell in the row is not empty
                                                    # the undirected edge of the two verticies is added
                distance_graph.add_undirected_edge(row[1],distance_table[i-3][1], float(row[i]))

    return distance_graph
