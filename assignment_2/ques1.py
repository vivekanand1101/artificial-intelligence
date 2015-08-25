class State:
    """Represents a state of the environment"""
    
    def __init__(self, l):
        self.root = l

    def __repr__(self):
        for i in l.length:
            for j in i:
                s = s + str(j)
            s = s + '\n'
        return s

    def __hash__(self):
        return hash(self.root)

    def __eq__(self, other):
        return self.root == other.root

    def blank_pos(self):
        for i in l.legth:
            for j in i:
                if l[i][j] == -1:
                    return (i, j)


class Matrix:
    """Represents a graph, uses python dict
        data structure.
    """

    def __init__(self, graph_dict={}):
        """Initializes the graph, has
            a default value as an empty dict
        """
        self.graph_dict = graph_dict

    def vertices(self):
        """Returns all the vertices of the graph"""
        return list(self.graph_dict.keys())

    def edges(self):
        """Returns all the edges of the graph,
            uses the generate edge method
        """
        return self.generate_edges()

    def neighbours(self, node):
        """Returns all the adjacent nodes
            of a given node
        """
        return self.graph_dict[node]

    def add_vertex(self, vertex):
        """Adds a vertex to the graph"""

        #here if the vertex is not present,
        #then it is initialized with an empty list
        #and is added as a key to the graph dict
        #and thus gets added to the graph
        if vertex not in self.graph_dict:
            self.graph_dict[vertex] = []

    def add_edge(self, edge):
        """Add an edge to the graph"""

        edge = set(edge)
        (vertex1, vertex2) = tuple(edge)

        #if the edge has to be entered,
        #considering it is undirected graph,
        #the entry has to be done for both
        #the vertices as the key
        if vertex1 in self.graph_dict:
            self.graph_dict[vertex1].append(vertex2)
        else:
            self.graph_dict[vertex1] = [vertex2]

        if vertex2 in self.graph_dict:
            self.graph_dict[vertex2].append(vertex1)
        else:
            self.graph_dict[vertex2] = [vertex1]

    def generate_edges(self):
        """Generate all the edge of the graph,
            It is a helper function for edges()
        """

        #every pair of key and value in the
        #list of all the values for the keys
        #will make for the edge. Iterate over
        #all the keys and you have all the edges
        edges = []
        for key, values in self.graph_dict.iteritems():
            for value in values:
                if (value, key) not in edges:
                        edges.append((key, value))
        return edges

class Graph:
"""Represents the state graph"""

    def __init__(self, state):
        self.root = state

    def neighbours(self, node):
        n = []
        for i in range(node.length):
            for j in range(i):
                if node[i][j] == -1:
                    if j > 0:
                        node[i][j], node[i][j-1] = node[i][j-1], node[i][j]
                        obj_state = State(node)
                        n.extend(obj_state)
                        node[i][j], node[i][j-1] = node[i][j-1], node[i][j]
                    if i > 0:
                        node[i][j], node[i-1][j] = node[i-1][j], node[i][j]
                        obj_state = State(node)
                        n.extend(obj_state)
                        node[i][j], node[i-1][j] = node[i-1][j], node[i][j]
                    if j < n - 1:
                        node[i][j], node[i][j+1] = node[i][j+1], node[i][j]
                        obj_state = State(node)
                        n.extend(obj_state)
                        node[i][j], node[i][j+1] = node[i][j+1], node[i][j]
                    if i < n - 1:
                        node[i][j], node[i+1][j] = node[i+1][j], node[i][j]
                        obj_state = State(node)
                        n.extend(obj_state)
                        node[i][j], node[i+1][j] = node[i+1][j], node[i][j]
        return n

    def level_order_traversal(self):
        """Print the graph in breadth first manner"""

        #the idea is we first put
        #the elements in the queue
        #and then visit it. So, we
        #first take the root and enqueue
        #it and look for its neighbours
        #and visit them one by one
        queue = []
        queue.append(self.root)

        #to keep track that we
        #we don't loop forever
        visited = []
        while queue:

            #dequeue from the queue
            node = queue.pop(0)

            #do what you want to do with the node
            #but, first check if it is not visited
            if node not in visited:
                print node,

            #check for other nodes in the
            #neighbourhood
            for vertex in self.neighbours(node):
                if vertex not in visited:
                    queue.extend(vertex)

            #you visited the node earlier!
            visited.extend(node)


def main():
    t = int(raw_input())
    n = int(raw_input())

    l = []
    for i in range(n):
        x = raw_input()
        x = x.split(' ')
        [int(j) for j in x]
        l.append(x)

    g = {}
    for i in range(n):
        for j in range(n):
            e = l[i][j]
            l_ = []
            if j > 0:
                l_.extend(l[i][j-1])
            if j < n - 1:
                l_.extend(l[i][j+1])
            if i > 0:
                l_.extend(l[i-1][j])
            if i < n - 1:
                l_.extend(l[i+1][j])

            g[str(e)] = l_

    graph = Graph(g)
    graph.level_order_traversal(l[0][0])

main()
