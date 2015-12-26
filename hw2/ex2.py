import time
import random
import heapq
ids = ["201316346", "201110376"]
# aTeam


class Queue:
    def __init__(self):
        abstract

    def extend(self, items):
        for item in items: self.append(item)


class FIFOQueue(Queue):
    """A First-In-First-Out Queue."""
    def __init__(self):
        self.A = []; self.start = 0
    def append(self, item):
        self.A.append(item)
    def __len__(self):
        return len(self.A) - self.start
    def extend(self, items):
        self.A.extend(items)
    def pop(self):
        e = self.A[self.start]
        self.start += 1
        if self.start > 5 and self.start > len(self.A)/2:
            self.A = self.A[self.start:]
            self.start = 0
        return e


class Controller:
    "This class is a controller for a Bomberman game."

    def __init__(self, board, steps):
        """Initialize controller for given game board and number of steps.
        This method MUST terminate within the specified timeout."""
        self.board = board
        self.Policy = {}
        self.BMx = None
        self.BMy = None
        self.Monsters = {}
        self.N = len(board)
        self.M = len(board[1])
        self.Steps = steps
        self.LastAction = None
        self.MinDistance = None
        self.MinMonsterLoc = ()
        self.adj = {}
        self.costs = {}
        self.Fifo = FIFOQueue()


    def MinMonster(self):
        del self.MinMonsterLoc
        minDist, monstLoc = min((v, k) for k, v in self.Monsters.items())
        self.MinDistance = minDist
        self.MinMonsterLoc = monstLoc


    def in_bound(self, x, y):
        if 0 <= x < self.N and 0 <= y < self.M:
            return True
        return False


    def BuildGraph(self):
        for row in range(0,self.N):
            for col in range(0,self.M):
                cell = self.board[row][col]
                if cell in [10, 12, 18, 80, 88, 90]:
                    self.UpdateAdjcosts(row,col)
                    if cell == 18:
                        self.BMx = row
                        self.BMy = col
                    elif cell == 12:
                        self.Monsters[(row, col)] = self.monsterBomberManhattannDistance(row,col)
        self.MinMonster()


    def UpdateAdjcosts(self, row, col):
        TempNeighboorsList = []
        for location in [[row+1, col], [row-1, col], [row, col+1], [row, col-1]]:
            if self.in_bound(location[0], location[1]):
                if self.board[location[0]][location[1]] in [10, 12, 18, 80, 88, 90]:
                   TempNeighboorsList.append((location[0],location[1]))
                   flag = True
                   if self.board[location[0]][location[1]] == 90:
                       if self.in_bound(row-1,col) and (self.board[row-1][col] in [10, 12, 18, 80, 88]) and ((row-1 != location[0]) or (col != (location[1]))) and flag:
                           if self.in_bound(row-1,col-1) and (self.board[row-1][col-1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','U','L','B','R','D']
                               flag = False
                           elif self.in_bound(row-1,col+1) and (self.board[row-1][col+1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','U','R','B','L','D']
                               flag = False
                           elif self.in_bound(row-2,col) and (self.board[row-2][col] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','U','U','B','D','D']
                               flag = False
                       if self.in_bound(row+1,col) and (self.board[row+1][col] in [10, 12, 18, 80, 88]) and ((row+1 != location[0]) or (col != (location[1]))) and flag:
                           if self.in_bound(row+1,col-1) and (self.board[row+1][col-1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','D','L','B','R','U']
                               flag = False
                           elif self.in_bound(row+1,col+1) and (self.board[row+1][col+1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','D','R','B','L','U']
                               flag = False
                           elif self.in_bound(row+2,col) and (self.board[row+2][col] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','D','D','B','U','U']
                               flag = False
                       if self.in_bound(row,col-1) and (self.board[row][col-1] in [10, 12, 18, 80, 88]) and ((row != location[0]) or (col-1 != (location[1]))) and flag:
                           if self.in_bound(row,col-2) and (self.board[row][col-2] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','L','L','B','R','R']
                               flag = False
                           elif self.in_bound(row+1,col-1) and (self.board[row+1][col-1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','L','D','B','U','R']
                               flag = False
                           elif self.in_bound(row-1,col-1) and (self.board[row-1][col-1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','L','U','B','D','R']
                               flag = False
                       if self.in_bound(row,col+1) and (self.board[row][col+1] in [10, 12, 18, 80, 88]) and ((row != location[0]) or (col+1 != (location[1]))) and flag:
                           if self.in_bound(row,col+2) and (self.board[row][col+2] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','R','R','B','L','L']
                               flag = False
                           elif self.in_bound(row+1,col+1) and (self.board[row+1][col+1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','R','D','B','U','L']
                               flag = False
                           elif self.in_bound(row-1,col+1) and (self.board[row-1][col+1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [1,'S','R','U','B','D','L']
                               flag = False
                   if (row == location[0]) and (col+1 == (location[1])):
                       if flag:
                           self.costs[((row,col),(location[0],location[1]))] = [0,'R']
                       else:
                           self.costs[((row,col),(location[0],location[1]))].append('R')
                   elif (row+1 == location[0]) and (col == (location[1])):
                       if flag:
                           self.costs[((row,col),(location[0],location[1]))] = [0,'D']
                       else:
                           self.costs[((row,col),(location[0],location[1]))].append('D')
                   elif (row == location[0]) and (col-1 == (location[1])):
                       if flag:
                           self.costs[((row,col),(location[0],location[1]))] = [0,'L']
                       else:
                           self.costs[((row,col),(location[0],location[1]))].append('L')
                   elif (row-1 == location[0]) and (col == (location[1])):
                       if flag:
                           self.costs[((row,col),(location[0],location[1]))] = [0,'U']
                       else:
                           self.costs[((row,col),(location[0],location[1]))].append('U')
        if len(TempNeighboorsList):
            self.adj[(row,col)] = TempNeighboorsList


    def dijkstra(self):
        Q = []     # priority queue of items; note item is mutable.
        d = {(self.BMx, self.BMy): 0} # vertex -> minimal distance
        Qd = {}    # vertex -> [d[v], parent_v, v]
        p = {}     # predecessor
        visited_set = set([(self.BMx, self.BMy)])
        pathMoves = []

        for v in self.adj.get((self.BMx, self.BMy), []):
            d[v] = self.costs[(self.BMx, self.BMy), v][0]
            item = [d[v], (self.BMx, self.BMy), v]
            heapq.heappush(Q, item)
            Qd[v] = item

        while Q:
            # print Q
            cost, parent, u = heapq.heappop(Q)
            if u not in visited_set:
                # print 'visit:', u
                p[u]= parent
                visited_set.add(u)
                if u == self.MinMonsterLoc:
                    t = self.MinMonsterLoc
                    c = t
                    path = [c]
                    while p.get(c):
                        path.insert(0, p[c])
                        c = p[c]
                    i = len(path)-1
                    for j in xrange(0,i):
                        tempList = self.costs[(path[j],path[j+1])]
                        k = len(tempList)
                        for l in xrange(1,k):
                            pathMoves.append(tempList[l])
                    for item in pathMoves:
                        self.Fifo.append(item)
                    return
                for v in self.adj.get(u, []):
                    if d.get(v):
                        if d[v] > self.costs[u, v][0] + d[u]:
                            d[v] =  self.costs[u, v][0] + d[u]
                            Qd[v][0] = d[v]    # decrease key
                            Qd[v][1] = u       # update predecessor
                            heapq._siftdown(Q, 0, Q.index(Qd[v]))
                    else:
                        d[v] = self.costs[u, v][0] + d[u]
                        item = [d[v], u, v]
                        heapq.heappush(Q, item)
                        Qd[v] = item
        return None


    def choose_next_move(self, board, n, reward):
        "Choose next action for Bomberman given the current state of the board."


    def monsterBomberManhattannDistance (self, row,col):
        #claculate manhattan distance between a monster and bomberman
        return (abs(row - self.BMx)+ abs(col - self.BMy))
        

    def CreatePolicy (self):
        #create the policy--> look on the + around Bomberman and define the following:
        #[0:[IsBomb, BombX, BombY], 1:number of monsters(1: 1,2-3:2, 4 and up:4), 2:monsters:{1:_, 2:_, 3:_, 4:_}, 3:walls:{1:_, 2:_, 3:_, 4:_},
        # 4:boarders:{1:_, 2:_, 3:_, 4:_},]

        for IsBomb in (0,1): #if there is no bomb in the +, but there is monsters --> set a bomb
            if IsBomb == 0:
                for NumMonster in (1, 2, 4):
                    for monster in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                    {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                    {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1}]:
                            for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                        {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                                 {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]:
                                    self.Policy[[0,None,None],NumMonster,monster,walls,boarders] = 'S'
            else:
                for x,y in [(0,0)]: #when there is a bomb with bomberman in the same cell --> escape to the area you can go, if there no such area --> bomb or wait
                   for NumMonster in (1, 2, 4):
                        if NumMonster == 1:#if there is one monster on the board --> and you can't escape --> bomb, if there are 3 monsters- check if there are more that close to you than far from you
                            for monster in [{1:1,2:0,3:0,4:0}]: #noster in zone 1:
                                for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                                 {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]: #there is no boarder in 3:
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:0,4:1},
                                                {1:1,2:1,3:0,4:1}, {1:0,2:0,3:0,4:0}]:#there are no wall in 3:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'D'
                                for boarders in [{1:1,2:0,3:0,4:1}, {1:1,2:0,3:0,4:0},{1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]: #there is no boarder in 3 and in 2:
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0},{1:0,2:0,3:1,4:1},{1:1,2:0,3:1,4:1}]:#there are walls in 3 but not in 2:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'L'
                                    for walls in [{1:0,2:1,3:1,4:1}, {1:1,2:1,3:1,4:1}]: #there are walls in 2,3,4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'B'
                                    for walls in [{1:0,2:1,3:1,4:0}, {1:1,2:1,3:1,4:0}]: #there are walls in 2,3 but not in 4:
                                        for boarders in [{1:1,2:0,3:0,4:1}, {1:0,2:0,3:0,4:1}]: #there is boarder in 4:
                                            self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'check'
                                        for boarders in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:0}]: #there is no boarder in 4:
                                            self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'R'
                                for boarders in [{1:1,2:1,3:0,4:0},{1:0,2:1,3:0,4:0}]:#there is no boarder in 3 but there is in 2:
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0}]: #there are walls in 3 but not in 4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'R'
                                    for walls in [{1:0,2:0,3:1,4:1}, {1:1,2:0,3:1,4:1}, {1:0,2:1,3:1,4:1}, {1:1,2:1,3:1,4:1}]: #there are walls in 3 and 4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'check'
                                for boarders in [{1:0,2:1,3:1,4:0}]: #there is boarder in 2 and 3:
                                    for walls in [{1:0,2:0,3:0,4:1}, {1:1,2:0,3:0,4:1}]:  #there are walls in 4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'B'
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:0,2:1,3:1,4:0},
                                                {1:1,2:1,3:1,4:0}, {1:0,2:0,3:0,4:0}]:#there are no walls in 4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'R'
                                for boarders in [{1:0,2:0,3:1,4:0}]: #there is no boarder in 4,2 but there is boarder in 3:
                                    for walls in [{1:0,2:1,3:0,4:1},{1:1,2:1,3:0,4:1}]: #there is wall in 4,2:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'check'
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:1,2:1,3:0,4:0}]:#there is no wall in 4 but there is wall in 2:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'R'
                                for boarders in [{1:0,2:0,3:1,4:1}]: #there is no boarder in 2 but there is boarder in 3,4:
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:1,2:0,3:0,4:1},{1:0,2:0,3:0,4:0}]: #there is no walls in 2:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'L'

                            for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                        {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                                 {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]:


                            for monster in [{1:0,2:1,3:0,4:0}]: #noster in zone 2:
                                for boarders in [{1:1,2:1,3:0,4:0}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                                 {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:0}]: #there is no boarder in 4:
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0},{1:0,2:1,3:1,4:0},
                                                 {1:1,2:1,3:1,4:0},{1:0,2:0,3:0,4:0}]:#there are no wall in 4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'R'
                                 for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},{1:0,2:0,3:0,4:0}]: #there is no boarder in 3 and in 4:
                                    for walls in [{1:0,2:0,3:0,4:1},{1:1,2:0,3:0,4:1},{1:0,2:1,3:0,4:1}, {1:1,2:1,3:0,4:1}]:#there are walls in 4 but not in 3:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'D'
                                    for walls in [{1:1,2:0,3:1,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 1,3,4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'B'
                                    for walls in [{1:0,2:0,3:1,4:1},{1:0,2:1,3:1,4:1}]: #there are walls in 3,4 but not in 1:
                                        for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:0}]: #there is boarder in 1:
                                            self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'check'
                                        for boarders in [{1:0,2:1,3:0,4:0},{1:0,2:0,3:0,4:0}]: #there is no boarder in 1:
                                            self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'U'
                                for boarders in [{1:0,2:1,3:1,4:0}, {1:0,2:0,3:1,4:0}]:#there is no boarder in 4 but there is in 3:
                                    for walls in [{1:0,2:0,3:0,4:1},{1:0,2:1,3:0,4:1}]: #there are walls in 4 but not in 1:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'U'
                                for walls in [{1:1,2:0,3:0,4:1},{1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 1 and 4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'check'
                                for boarders in [{1:0,2:1,3:1,4:0}]: #there is boarder in 2 and 3:
                                    for walls in [{1:0,2:0,3:0,4:1}, {1:1,2:0,3:0,4:1}]:  #there are walls in 4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'B'
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:0,2:1,3:1,4:0},
                                                {1:1,2:1,3:1,4:0}, {1:0,2:0,3:0,4:0}]:#there are no walls in 4:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'R'
                                for boarders in [{1:0,2:0,3:1,4:0}]: #there is no boarder in 4,2 but there is boarder in 3:
                                    for walls in [{1:0,2:1,3:0,4:1},{1:1,2:1,3:0,4:1}]: #there is wall in 4,2:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'check'
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:1,2:1,3:0,4:0}]:#there is no wall in 4 but there is wall in 2:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'R'
                                for boarders in [{1:0,2:0,3:1,4:1}]: #there is no boarder in 2 but there is boarder in 3,4:
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:1,2:0,3:0,4:1},{1:0,2:0,3:0,4:0}]: #there is no walls in 2:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'L'





                            for monster in [{1:1,2:0,3:0,4:0}]:
                                for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},
                                            {1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1},
                                            {1:1,2:1,3:1,4:0},  {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                            {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                    for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                                    {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'D'
                                 for walls in  [{1:0,2:0,3:1,4:0},{1:1,2:0,3:1,4:0},{1:0,2:0,3:1,4:1},{1:1,2:0,3:1,4:1}]:
                                    for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}]:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'D'
                            for monster in [{1:0,2:1,3:0,4:0}]:
                                for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0},{1:0,2:1,3:1,4:0},
                                            {1:1,2:1,3:1,4:0},{1:0,2:0,3:0,4:0}]:
                                    for boarders in [{1:1,2:1,3:0,4:0}, {1:0,2:1,3:1,4:0}]:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'R'
                            for monster in [{1:0,2:0,3:1,4:0}]:
                                for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                            {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                            {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                            {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                    for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}]:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'U'
                            for monster in [{1:0,2:0,3:0,4:1}]:
                                for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},{1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                            {1:0,2:1,3:1,4:1},{1:0,2:0,3:0,4:0}]:
                                    for boarders in [{1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}]:
                                        self.Policy[[1,x,y],NumMonster,monster,walls,boarders] = 'L'

                        if NumMonster == 2:





                for x, y in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0), (-2, 0), (-1, -1), (-1, 1), (0, -2),(0, 2), (1, -1), (1, 1), (2, 0)]:
                    for NumMonster in (1, 2, 4):
                        if NumMonster == 1:
                            for monster in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}]:
                                for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                            {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                            {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                            {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                    for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}]:

