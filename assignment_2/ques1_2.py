from collections import deque
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
        index = self.root.index(str(-1))
        return (index / self.n, index % self.n)

    def __iter__(self):
        return iter(self.root)

#    def __getitem__(self):
#        return self.root

    def __hash__(self):
        return hash(tuple(self.root))

    def __eq__(self, other):
        return (self.__hash__(), self.n) == (other.__hash__(), other.n)

class Graph():
    """Represents the state graph"""

    def __init__(self, state):
        self.root = state

    def copy(self, node):
        copy = []
        for i in node.root:
            copy.append(i)
        #print 'copy ', copy
        return copy

    def neighbours(self, node):
        n_ = []
        count = 0
        n = node.n
        for k in range(len(node) * len(node)):
            if int(node.root[k]) == -1:
                i, j = k / n, k % n
                if j > 0:
                    x = self.copy(node)
                    x[k], x[k-1] = x[k-1], x[k]
                    obj_state1 = State(x, n, node)
                    n_.append(obj_state1)
                if i > 0:
                    x = self.copy(node)
                    x[k-n], x[k] = x[k], x[k-n]
                    obj_state2 = State(x, n, node)
                    n_.append(obj_state2)
                if j < n - 1:
                    x = self.copy(node)
                    x[k], x[k+1] = x[k+1], x[k]
                    obj_state3 = State(x, n, node)
                    n_.append(obj_state3)
                if i < n - 1:
                    x = self.copy(node)
                    x[k], x[k+n] = x[k+n], x[k]
                    obj_state4 = State(x, n, node)
                    n_.append(obj_state4)
        return n_

    def is_final(self, node):
        if sorted(node.root[:-1]) == node.root[:-1]:
            return True
        else:
            return False

    def level_order_traversal(self):
        """Print the graph in breadth first manner"""

        #the idea is we first put
        #the elements in the queue
        #and then visit it. So, we
        #first take the root and enqueue
        #it and look for its neighbours
        #and visit them one by one
        queue = deque([])
        queue.append(self.root)

        #to keep track that we
        #we don't loop forever
        visited = set()
        while queue:

            #dequeue from the queue
            node = queue.popleft()
            if node.blank_pos() == (node.n - 1, node.n - 1) and self.is_final(node):
                return node

            #do what you want to do with the node
            #but, first check if it is not visited
            #if node not in visited:
             #   print node,

            #check for other nodes in the
            #neighbourhood
            n_ = self.neighbours(node)
            for vertex in n_:
                #print 'neighbours ', vertex
                if vertex not in visited:
                    queue.append(vertex)

            #you visited the node earlier!
            visited.add(node)
            print 'visited ', visited

def main():
    t = int(raw_input())
    n = int(raw_input())

    l = []
    for i in range(n):
        x = raw_input()
        x = x.split(' ')
        [int(j) for j in x]
        l.append(x)

    l = list(chain.from_iterable(l))
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
        for i in x:
            print i,
        print
main()
