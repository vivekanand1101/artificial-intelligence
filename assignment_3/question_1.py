from math import sqrt

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
        (i, j) = fringe
        fringes = []
        #print self.environ.n, j, self.environ.sensor_is_navigable(i, j+1)
        if j < self.environ.n - 1 and self.environ.sensor_is_navigable(i, j+1): 
            fringes.append((i, j+1))
        if j < self.environ.n - 1 and i < self.environ.m - 1 and self.environ.sensor_is_navigable(i+1, j+1):
            fringes.append((i+1, j+1))
        if i < self.environ.m - 1 and self.environ.sensor_is_navigable(i+1, j):
            fringes.append((i+1, j))
        if j > 0 and i < self.environ.m - 1 and self.environ.sensor_is_navigable(i+1, j-1):
            fringes.append((i+1, j-1))
        if j > 0 and self.environ.sensor_is_navigable(i, j-1):
            fringes.append((i, j-1))
        if j > 0 and i > 0 and self.environ.sensor_is_navigable(i-1, j-1):
            fringes.append((i-1, j-1))
        if i > 0 and self.environ.sensor_is_navigable(i-1, j):
            fringes.append((i-1, j))
        if i > 0 and j < self.environ.n - 1 and self.environ.sensor_is_navigable(i-1, j+1):
            fringes.append((i-1, j+1))
        return fringes

    def prioritize_new_fringes(self, fringe, fringes):
        """Returns the fringes in
            a priority - least cost first
        """
        fringes.sort(key=lambda x: self.get_cost(fringe, x))
        return fringes

    def get_cost(self, source, dest):
        """Returns the path cost
            arguments are tuples (i, j)
        """
        (source_i, source_j) = source
        (dest_i, dest_j) = dest
        if (abs(source_i - dest_i) == 1 and abs(source_j - dest_j) == 0) \
            or (abs(source_j - dest_j) == 1 and abs(source_i - dest_i) == 0):
                return 1.0
        else:
            return sqrt(2)

    def work(self):
        queue = [(self.source_i, self.source_j)]
        visited = []
        cost = 0
        count = 0

        while queue:
            fringe = queue.pop(0)
            count += 1
            if count != 1:
                #print 'queue ', queue
                #print 'visited ', visited
                print 'adding ', visited[-1], 'and ', fringe
                cost += self.get_cost(visited[-1], fringe)
                print 'cost2 ', cost

            if fringe == (self.dest_i, self.dest_j):
                print 're'
                return cost

            fringes = self.new_fringes(fringe)
            prioritized_fringes = self.prioritize_new_fringes(fringe, fringes)
            for i in prioritized_fringes:
                if i not in visited:
                    queue.append(i)
            #if prioritized_fringes[0] not in visited:
             #   queue.append(prioritized_fringes[0])
            print 'queue ', queue
            visited.append(fringe)
            print 'visited ', visited

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
        print cost

main()
