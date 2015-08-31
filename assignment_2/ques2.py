from itertools import chain

class State:
    """Represents a state of the environment"""
    
    def __init__(self, l, n, parent):
        self.root = l
        self.n = n
        self.parent = parent

    def __repr__(self):
        return '%r' % self.root

    def __len__(self):
        return self.n

    def blank_pos(self):
        for i in range(self.n):
            for j in range(self.n):
                if int(self.root[i][j]) == -1:
                    return (i, j)
    def __iter__(self):
        return iter(self.root)

#    def __getitem__(self):
#        return self.root

    def __hash__(self):
        new = list(chain.from_iterable(self.root))
        return hash(tuple(new))

    def __eq__(self, other):
        return (self.__hash__(), self.n) == (other.__hash__(), other.n)

class Graph():
    """Represents the state graph"""

    def __init__(self, state):
        self.root = state

    def copy(self, node):
        copy = []
        for i in range(node.n):
            l = []
            for j in range(node.n):
                l.append(node.root[i][j])
            copy.append(l)
        #print 'copy ', copy
        return copy

    def neighbours(self, node):
        n_ = []
        count = 0
        for i in range(len(node)):
            for j in range(len(node)):
                if int(node.root[i][j]) == -1:
                    count += 1
                    if j > 0:
                        x = self.copy(node)
                        x[i][j], x[i][j-1] = x[i][j-1], x[i][j]
                        obj_state1 = State(x, node.n, node)
                        n_.append(obj_state1)
                    if i > 0:
                        x = self.copy(node)
                        x[i-1][j], x[i][j] = x[i][j], x[i-1][j]
                        obj_state2 = State(x, node.n, node)
                        n_.append(obj_state2)
                    if j < node.n - 1:
                        x = self.copy(node)
                        x[i][j], x[i][j+1] = x[i][j+1], x[i][j]
                        obj_state3 = State(x, node.n, node)
                       # print x == node.root
                       # print self.root.root == node.root
                        n_.append(obj_state3)
                       # print n_
                    if i < node.n - 1:
                        x = self.copy(node)
                        x[i][j], x[i+1][j] = x[i+1][j], x[i][j]
                        obj_state4 = State(x, node.n, node)
                        n_.append(obj_state4)
                       # print n_
        return n_

    def is_final(self, node, x, y):
        new = list(chain.from_iterable(node))
        copy = []
        for i in range(node.n * node.n -1):
            copy.append(new[i])
        copy = map(int, copy)
        index = x * 3 + y
        copy.pop(index)
        if sorted(copy) == copy:
            return True
        else:
            return False

    def is_final_blank_pos(self, node):
        (x, y) = node.blank_pos()
        n = node.n
        if (x, y) == (0, n-1) or (x, y) == (n-1, 0) or (x, y) == (n-1, n-1) or (x, y) == (0, 0):
            return ((x, y), True)
        else:
            return (None, False)

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
        visited = set()
        while queue:

            #dequeue from the queue
            node = queue.pop(0)
            X, Y = self.is_final_blank_pos(node)
            if Y == True:
                (x, y) = X
                if self.is_final(node, x, y):
                    return node

            #do what you want to do with the node
            #but, first check if it is not visited
            #if node not in visited:
            #    print node,

            #check for other nodes in the
            #neighbourhood
            n_ = self.neighbours(node)
            for vertex in n_:
#                print 'neighbours ', vertex
                if vertex not in visited:
                    queue.append(vertex)
                    #print 'queue'
                    #print queue

            #you visited the node earlier!
            visited.add(node)
            #print 'visited ', visited

def main():
    t = int(raw_input())
    n = int(raw_input())

    l = []
    for i in range(n):
        x = raw_input()
        x = x.split(' ')
        [int(j) for j in x]
        l.append(x)
    
    obj_state = State(l, n, None)
    g = Graph(obj_state)
    #print 'A'
    x = g.level_order_traversal()
    stack = []
    while x != None:
        stack.append(x.root)
        x = x.parent

    while stack:
        x = stack.pop()
        l = list(chain.from_iterable(x))
        for i in l:
            print i,
        print

main()
