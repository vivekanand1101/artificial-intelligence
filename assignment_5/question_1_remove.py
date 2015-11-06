class pointRobot():
    def __init__(self, rMax, cMax, Ra, R):
        self.Ra = Ra            # reward in non-terminal states (used to initialise r[[0 for x in xrange(cMax)] for x in xrange(rMax)] )
        self.gamma = 1          # discount factor
        self.pGood = 0.8        # probability of taking intended action
        self.pBad = (1 - self.pGood) / 2 # 2 bad actions, split prob between them
        self.N = 10000000             # max number of iterations of Value Iteration
        self.deltaMin = 1e-9    # convergence criterion for iteration
        self.R = R
        self.U = [0 for i in xrange(len(R))]
        self.Up = [0 for i in xrange(len(R))]
        self.Pi = [0 for i in xrange(len(R))]
        self.rMax = rMax
        self.cMax = cMax

        x = set(self.R)
        if 0 in list(set(self.R)):
            x.remove(0)
        if -100 in list(set(self.R)):
            x.remove(-100)

        self.terminating_nums = list(x)
        self.sink = self.sink_()
        self.obstacle_index = self.obstacle()

    def start(self):
        for i in xrange(len(self.R)):
            if (i not in self.sink) and (i not in self.obstacle_index):
                self.R[i] = self.Ra     
        #print 'R ', self.R
        n = 1
        delta = 0
        for r in xrange(self.rMax):
            for c in xrange(self.cMax):
                self.updateUPrime(r, c)
                diff = abs(self.Up[r * self.cMax + c] - self.U[r * self.cMax + c])
                if diff > delta:
                    delta = diff

        while (delta > self.deltaMin):  # Simultaneous updates: set U = Up, then compute changes in Up using prev value of U.
            self.duplicate()
            # if n >= self.N:
            #     raise IndexError
            n += 1
            delta = 0
            for r in xrange(self.rMax):
                for c in xrange(self.cMax):
                    self.updateUPrime(r, c)
                    diff = abs(self.Up[r * self.cMax + c] - self.U[r * self.cMax + c])
                    #print diff
                    if diff > delta:
                        delta = diff
         
        for r in xrange(self.rMax):
            for c in xrange(self.cMax):
                if (r * self.cMax + c) in self.obstacle_index:
                    print '%0.2f' % -100.00,
                else:
                    print '%0.2f' % self.U[r * self.cMax + c],
            print

        for i in xrange(len(self.R)):
            if (i in self.sink) or (i in self.obstacle_index):
                self.Pi[i] = '-'

        #print "Best policy:"
        for r in xrange(self.rMax):
            for c in xrange(self.cMax):
                print self.Pi[r * self.cMax + c],
            print

     
    def updateUPrime(self, r, c):
        # IMPORTANT: this modifies the value of Up, using values in U.
        a = [0 for x in xrange(4)]
        if ((r * self.cMax + c) in (self.sink)) \
                      or ((r * self.cMax + c) in (self.obstacle_index)):
            self.Up[r * self.cMax + c] = self.R[r * self.cMax + c]
        else:
            a[0] = self.aNorth(r, c) * self.pGood + self.aWest(r, c) * self.pBad + self.aEast(r, c) * self.pBad
            a[1] = self.aSouth(r, c) * self.pGood + self.aWest(r, c) * self.pBad + self.aEast(r, c) * self.pBad
            a[2] = self.aWest(r, c) * self.pGood + self.aSouth(r, c) * self.pBad + self.aNorth(r, c) * self.pBad
            a[3] = self.aEast(r, c) * self.pGood + self.aSouth(r, c) * self.pBad + self.aNorth(r, c) * self.pBad
            #print a
            best = self.maxindex(a)
            self.Up[r * self.cMax + c] = self.R[r * self.cMax + c] + self.gamma * a[best]

            if best == 0:
                self.Pi[r * self.cMax + c] = 'u'
            elif best == 1:
                self.Pi[r * self.cMax + c] = 'd'
            elif best == 2:
                self.Pi[r * self.cMax + c] = 'l'
            else:
                self.Pi[r * self.cMax + c] = 'r'

    def maxindex(self, a): 
        b = 1
        m = a[1]
        if a[0] - m > 0.00000001:
            m = a[0]
            b = 0
        if a[3] - m > 0.00000001:
            m = a[3]
            b = 3
        if a[2] - m > 0.00000001:
            m = a[2]
            b = 2
        return b
     
    def aNorth(self, r, c):
        # can't go north if at row 0 or if in cell (2,1)
        if (r == 0) or ((r * self.cMax + c - self.cMax) in self.obstacle_index):
            return self.U[(r * self.cMax) + c]
        return self.U[(r - 1) * self.cMax + c]

    def aSouth(self, r, c):
        # can't go south if at row 2 or if in cell (0,1)
        if (r == self.rMax - 1) or ((r * self.cMax + c + self.cMax) in self.obstacle_index):
            return self.U[(r * self.cMax) + c]
        return self.U[(r + 1) * self.cMax + c]

    def aWest(self, r, c):
        # can't go west if at col 0 or if in cell (1,2)
        if (c == 0) or ((r * self.cMax + c - 1) in self.obstacle_index):
            return self.U[r * self.cMax + c]
        return self.U[(r * self.cMax) + (c - 1)]

    def aEast(self, r, c):
        # can't go east if at col 3 or if in cell (1,0)
        if (c == self.cMax - 1) or ((r * self.cMax + c + 1) in self.obstacle_index):
            return self.U[r * self.cMax + c]
        return self.U[(r * self.cMax) + (c + 1)]
     
    def duplicate(self):
        for r in xrange(len(self.Up)):
            self.U[r] = self.Up[r]

    def sink_(self):
        neg = []
        for i in xrange(len(self.R)):
            if self.R[i] in self.terminating_nums:
                neg.append(i)
        return neg

    def obstacle(self):
        obs = []
        for i in xrange(len(self.R)):
            if self.R[i] == -100:
                obs.append(i)
        return obs

def main():
    t = int(raw_input())
    while t:
        x = raw_input().split(' ')
        n = int(x[0])
        m = int(x[1])
        Ra = float(x[2])
        R = []
        for i in xrange(n):
            r_ = raw_input().split(' ')
            r_ = map(int, r_)
            R.extend(r_)

        robot = pointRobot(n, m, Ra, R)
        robot.start()
        t -= 1

main()
