from math import sqrt
import heapq

class Fringe:

    def __init__(self):
        self.queue = []
        self.index = 0

    def push(self, item):
        heapq.heappush(self.queue, (item.cost, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self.queue)[-1]

    def __repr__(self):
        return '%r' % self.queue

class Node:

    def __init__(self, i, j, cost):
        self.i = i
        self.j = j
        self.cost = cost

    def __repr__(self):
        return '(%r, %r)' % (self.i, self.j)

    def __eq__(self, other):
        return (self.i, self.j) == (other.i, other.j)

class Environment:

    def __init__(self, matrix, m , n):
        self.matrix = matrix
        self.m = m
        self.n = n

    def get_cost(self, source, dest):
        """Returns the path cost
            arguments are tuples (i, j)
        """
        (source_i, source_j) = source
        (dest_i, dest_j) = dest

        i_diff = abs(source_i - dest_i)
        j_diff = abs(source_j - dest_j)
        return sqrt(pow(i_diff, 2) + pow(j_diff, 2))

class Agent:

    def __init__(self, work, e):
        (self.source_i, self.source_j) = work[0]
        (self.dest_i, self.dest_j) = work[1]
        self.environ = e

    def sensor_is_navigable(self, i, j):
        if int(self.environ.matrix[(i * self.environ.n) + j]) == 0:
            return True
        else:
            return False

    def new_fringes(self, current_fringe):
        """Returns all the navigable
            neighbours of the given fringe
        """
        (i, j) = (current_fringe.i, current_fringe.j)
        fringe_cost = current_fringe.cost
        fringes = []
        if j < self.environ.n - 1 and self.sensor_is_navigable(i, j+1):
            fringes.append(Node(i, j+1, fringe_cost+self.environ.get_cost((i, j), (i, j+1))))
        if j < self.environ.n - 1 and i < self.environ.m - 1 and self.sensor_is_navigable(i+1, j+1):
            fringes.append(Node(i+1, j+1, fringe_cost+self.environ.get_cost((i, j), (i+1, j+1))))
        if i < self.environ.m - 1 and self.sensor_is_navigable(i+1, j):
            fringes.append(Node(i+1, j, fringe_cost+self.environ.get_cost((i, j), (i+1, j))))
        if j > 0 and i < self.environ.m - 1 and self.sensor_is_navigable(i+1, j-1):
            fringes.append(Node(i+1, j-1, fringe_cost+self.environ.get_cost((i, j), (i+1, j-1))))
        if j > 0 and self.sensor_is_navigable(i, j-1):
            fringes.append(Node(i, j-1, fringe_cost+self.environ.get_cost((i, j), (i, j-1))))
        if j > 0 and i > 0 and self.sensor_is_navigable(i-1, j-1):
            fringes.append(Node(i-1, j-1, fringe_cost+self.environ.get_cost((i, j), (i-1, j-1))))
        if i > 0 and self.sensor_is_navigable(i-1, j):
            fringes.append(Node(i-1, j, fringe_cost+self.environ.get_cost((i, j), (i-1, j))))
        if i > 0 and j < self.environ.n - 1 and self.sensor_is_navigable(i-1, j+1):
            fringes.append(Node(i-1, j+1, fringe_cost+self.environ.get_cost((i, j), (i-1, j+1))))
        return fringes

    def work(self):
        root = Node(self.source_i, self.source_j, 0)
        fringe = Fringe()
        fringe.push(root)
        visited = []
        #cost = 0
        count = 0

        while fringe.queue != []:
            node = fringe.pop()
            #print 'fringe ', fringe
            count += 1
            #print count
            if (node.i, node.j) == (self.dest_i, self.dest_j):
                return node.cost

            nodes = self.new_fringes(node)
            for i in nodes:
                if i not in visited:
                    flag = 0
                    if fringe.queue:
                        for k in fringe.queue:
                            if k[-1] == i:
                                flag = 1
                                break
                    if flag == 0:
                        fringe.push(i)
            visited.append(node)
            #print 'visited ', visited
            #print 'queue ', queue

def main():
    x = raw_input()
    x = x.split(' ')
    m = int(x[0])
    n = int(x[1])

    matrix = []
    for i in range(m):
        row = raw_input()
        row = row.split(' ')
        matrix.extend(row)

    queries = int(raw_input())
    aim = []
    for i in range(queries):
        x = raw_input()
        x = x.split(' ')
        (source_i, source_j) = (int(x[0]), int(x[1]))
        (dest_i, dest_j) = (int(x[2]), int(x[3]))
        aim.append([(source_i, source_j), (dest_i, dest_j)])

    [int(i) for i in matrix]
    e = Environment(matrix, m, n)
    for i in range(queries):
        work = aim[i]
        agent = Agent(work, e)
        cost = agent.work()
        print int(cost + 0.5)

main()
