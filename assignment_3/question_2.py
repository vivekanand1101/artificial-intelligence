from math import sqrt
import heapq

class PriorityQueue:

    def __init__(self):
        self.queue = []
        self.index = 0

    def push(self, item):
        heapq.heappush(self.queue, (item.total_cost, self.index, item))
        self.index += 1

    def pop(self):
        return heapq.heappop(self.queue)[-1]

    def __repr__(self):
        return '%r' % self.queue

    #def __iter__(self):
     #   for x in self.queue:
      #      yield x

class Node:
    
    def __init__(self, i, j, cost):
        self.i = i
        self.j = j
        self.cost = cost
        self.total_cost = cost

    def __repr__(self):
        return '%r cost: %r total cost: %r' % ((self.i, self.j), self.cost, self.total_cost)
'''
    def __hash__(self):
        return hash((self.i, self.j))

    def __eq__(self, other):
        return self.i, self.j == other.i, other.j
'''

class Environment:

    def __init__(self, matrix, m , n):
        self.matrix = matrix
        self.m = m
        self.n = n

    def sensor_is_navigable(self, i, j):
        if int(self.matrix[(i * self.n) + j]) == 0:
            return True
        else:
            return False

class Agent:

    def __init__(self, work, e):
        (self.source_i, self.source_j) = work[0]
        (self.dest_i, self.dest_j) = work[1]
        self.environ = e

    def new_fringes(self, fringe):
        """Returns all the navigable
            neighbours of the given fringe
        """
        (i, j) = (fringe.i, fringe.j)
        fringe_cost = fringe.cost
        fringes = []
        #print self.environ.n, j, self.environ.sensor_is_navigable(i, j+1)
        if j < self.environ.n - 1 and self.environ.sensor_is_navigable(i, j+1):
            fringes.append(Node(i, j+1, fringe_cost+self.get_cost((i, j), (i, j+1))))
            fringes[-1].total_cost += self.get_cost((fringes[-1].i, fringes[-1].j), (self.dest_i, self.dest_j))
        if j < self.environ.n - 1 and i < self.environ.m - 1 and self.environ.sensor_is_navigable(i+1, j+1):
            fringes.append(Node(i+1, j+1, fringe_cost+self.get_cost((i, j), (i+1, j+1))))           
            fringes[-1].total_cost += self.get_cost((fringes[-1].i, fringes[-1].j), (self.dest_i, self.dest_j))
        if i < self.environ.m - 1 and self.environ.sensor_is_navigable(i+1, j):
            fringes.append(Node(i+1, j, fringe_cost+self.get_cost((i, j), (i+1, j))))            
            fringes[-1].total_cost += self.get_cost((fringes[-1].i, fringes[-1].j), (self.dest_i, self.dest_j))
        if j > 0 and i < self.environ.m - 1 and self.environ.sensor_is_navigable(i+1, j-1):
            fringes.append(Node(i+1, j-1, fringe_cost+self.get_cost((i, j), (i+1, j-1))))
            fringes[-1].total_cost += self.get_cost((fringes[-1].i, fringes[-1].j), (self.dest_i, self.dest_j))       
        if j > 0 and self.environ.sensor_is_navigable(i, j-1):
            fringes.append(Node(i, j-1, fringe_cost+self.get_cost((i, j), (i, j-1))))
            fringes[-1].total_cost += self.get_cost((fringes[-1].i, fringes[-1].j), (self.dest_i, self.dest_j)) 
        if j > 0 and i > 0 and self.environ.sensor_is_navigable(i-1, j-1):
            fringes.append(Node(i-1, j-1, fringe_cost+self.get_cost((i, j), (i-1, j-1))))
            fringes[-1].total_cost += self.get_cost((fringes[-1].i, fringes[-1].j), (self.dest_i, self.dest_j))       
        if i > 0 and self.environ.sensor_is_navigable(i-1, j):
            fringes.append(Node(i-1, j, fringe_cost+self.get_cost((i, j), (i-1, j))))
            fringes[-1].total_cost += self.get_cost((fringes[-1].i, fringes[-1].j), (self.dest_i, self.dest_j))
        if i > 0 and j < self.environ.n - 1 and self.environ.sensor_is_navigable(i-1, j+1):
            fringes.append(Node(i-1, j+1, fringe_cost+self.get_cost((i, j), (i-1, j+1))))
            fringes[-1].total_cost += self.get_cost((fringes[-1].i, fringes[-1].j), (self.dest_i, self.dest_j))
#        print 'fringes ', fringes
        return fringes

    def prioritize_new_fringes(self, fringes):
        """Returns the fringes in
            a priority - least cost first
        """
        fringes.sort(key=lambda x: x.total_cost)
        return fringes

    def get_cost(self, source, dest):
        """Returns the path cost
            arguments are tuples (i, j)
        """
        (source_i, source_j) = source
        (dest_i, dest_j) = dest

        i_diff = abs(source_i - dest_i)
        j_diff = abs(source_j - dest_j)
        return sqrt(pow(i_diff, 2) + pow(j_diff, 2))

    def work(self):
        root = Node(self.source_i, self.source_j, 0)
        #queue = [root]
        queue = PriorityQueue()
        queue.push(root)
        visited = set()
        #cost = 0
        count = 0

        while queue.queue != []:
            #print queue.queue
            fringe = queue.pop()
            count += 1
            print count
            #if count != 1:
                #print 'queue ', queue
                #print 'visited ', visited
                #print 'adding ', visited[-1], 'and ', fringe
                #cost += self.get_cost(visited[-1], fringe)
                #print 'cost2 ', cost

            #print 'fringe ', fringe
            if (fringe.i, fringe.j) == (self.dest_i, self.dest_j):
                return fringe.cost

            fringes = self.new_fringes(fringe)
            #prioritized_fringes = self.prioritize_new_fringes(fringes)
            for x in fringes:
#                print 'x: ', x, 'visited: ', visited
#                print 'queue.queue ', queue.queue
                if (x not in visited) and (x not in queue.queue):
                    queue.push(x)
            #if prioritized_fringes[0] not in visited:
             #   queue.append(prioritized_fringes[0])
            visited.add(fringe)
#            print 'visited ', visited
            #queue.sort(key=lambda i: i.cost)
#            print 'queue ', queue

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
