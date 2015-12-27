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
        if self.__len__() == 0:
            return None
        e = self.A[self.start]
        self.start += 1
        if self.start > 5 and self.start > len(self.A)/2:
            self.A = self.A[self.start:]
            self.start = 0
        return e
    def clear(self):
        del self.A[:]
        self.start = 0


class Controller:
    "This class is a controller for a Bomberman game."

    def __init__(self, board, steps):
        """Initialize controller for given game board and number of steps.
        This method MUST terminate within the specified timeout."""
        t1 = time.time()
        self.board = board
        self.Policy = {}
        self.reward = 0
        self.BMx = None
        self.BMy = None
        self.InitBMx = None
        self.InitBMy = None
        self.Bombx = None
        self.Bomby = None
        self.InitBombx = None
        self.InitBomby = None
        self.Monsters = {}
        self.N = len(board)
        self.M = len(board[1])
        self.Steps = steps
        self.LastAction = 'W'
        self.MinDistance = None
        self.MinMonsterLoc = ()
        self.adj = {}
        self.costs = {}
        self.Fifo = FIFOQueue()
        self.UsePolicyLastMove = False
        self.CreatePolicy()
        t2 = time.time()
        if t2-t1 > 55:
            return
        self.BuildGraph()
        return

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
        # self.Bomb = []
        TempMonsters = {}
        i = 0
        for row in range(0,self.N):
            for col in range(0,self.M):
                cell = self.board[row][col]
                if cell in [10, 12, 18, 80, 88, 90]:
                    self.UpdateAdjcosts(row,col)
                    if cell in [18, 88]:
                        self.BMx, self.InitBMx = row, row
                        self.BMy, self.InitBMy = col, col
                        if cell == 88:
                            self.Bombx, self.InitBMx = row, row
                            self.Bomby, self.InitBMy = col, col
                    elif cell == 12:
                        TempMonsters[i] = [row,col]
                        i+=1

        for Location in TempMonsters.values():
            self.Monsters[(Location[0], Location[1])] = self.monsterBomberManhattannDistance(Location[0], Location[1])
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
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','U','L','B','R','D']
                               flag = False
                           elif self.in_bound(row-1,col+1) and (self.board[row-1][col+1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','U','R','B','L','D']
                               flag = False
                           elif self.in_bound(row-2,col) and (self.board[row-2][col] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','U','U','B','D','D']
                               flag = False
                       if self.in_bound(row+1,col) and (self.board[row+1][col] in [10, 12, 18, 80, 88]) and ((row+1 != location[0]) or (col != (location[1]))) and flag:
                           if self.in_bound(row+1,col-1) and (self.board[row+1][col-1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','D','L','B','R','U']
                               flag = False
                           elif self.in_bound(row+1,col+1) and (self.board[row+1][col+1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','D','R','B','L','U']
                               flag = False
                           elif self.in_bound(row+2,col) and (self.board[row+2][col] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','D','D','B','U','U']
                               flag = False
                       if self.in_bound(row,col-1) and (self.board[row][col-1] in [10, 12, 18, 80, 88]) and ((row != location[0]) or (col-1 != (location[1]))) and flag:
                           if self.in_bound(row,col-2) and (self.board[row][col-2] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','L','L','B','R','R']
                               flag = False
                           elif self.in_bound(row+1,col-1) and (self.board[row+1][col-1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','L','D','B','U','R']
                               flag = False
                           elif self.in_bound(row-1,col-1) and (self.board[row-1][col-1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','L','U','B','D','R']
                               flag = False
                       if self.in_bound(row,col+1) and (self.board[row][col+1] in [10, 12, 18, 80, 88]) and ((row != location[0]) or (col+1 != (location[1]))) and flag:
                           if self.in_bound(row,col+2) and (self.board[row][col+2] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','R','R','B','L','L']
                               flag = False
                           elif self.in_bound(row+1,col+1) and (self.board[row+1][col+1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','R','D','B','U','L']
                               flag = False
                           elif self.in_bound(row-1,col+1) and (self.board[row-1][col+1] in [10, 12, 18, 80, 88]):
                               self.costs[((row,col),(location[0],location[1]))] = [2,'S','R','U','B','D','L']
                               flag = False
                   if (row == location[0]) and (col+1 == (location[1])):
                       if flag:
                           self.costs[((row,col),(location[0],location[1]))] = [1,'R']
                       else:
                           self.costs[((row,col),(location[0],location[1]))].append('R')
                   elif (row+1 == location[0]) and (col == (location[1])):
                       if flag:
                           self.costs[((row,col),(location[0],location[1]))] = [1,'D']
                       else:
                           self.costs[((row,col),(location[0],location[1]))].append('D')
                   elif (row == location[0]) and (col-1 == (location[1])):
                       if flag:
                           self.costs[((row,col),(location[0],location[1]))] = [1,'L']
                       else:
                           self.costs[((row,col),(location[0],location[1]))].append('L')
                   elif (row-1 == location[0]) and (col == (location[1])):
                       if flag:
                           self.costs[((row,col),(location[0],location[1]))] = [1,'U']
                       else:
                           self.costs[((row,col),(location[0],location[1]))].append('U')
        if len(TempNeighboorsList):
            self.adj[(row,col)] = TempNeighboorsList


    def dijkstra(self, board):
        self.UpdateMonstersLocation(board)
        self.Fifo.clear()

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
            cost, parent, u = heapq.heappop(Q)
            if u not in visited_set:
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


    def choose_next_move(self, board, steps, reward):
        "Choose next action for Bomberman given the current state of the board."

        if steps == self.Steps - 1:
            self.BMx, self.BMy = self.InitBMx, self.InitBMy
            self.Bombx, self.Bomby = self.InitBombx, self.InitBomby
            self.LastAction ='W'
            self.UsePolicyLastMove = False
        if reward - self.reward <= -5:
            self.BMx, self.BMy = self.InitBMx, self.InitBMy
            self.Bombx, self.Bomby = self.InitBombx, self.InitBomby
            self.LastAction ='W'
            self.UsePolicyLastMove = False
        self.reward = reward
        # if self.LastAction == 'W':
        #     self.LastAction == 'W'
        if self.LastAction == 'S':
            self.LastAction == 'S'
        # if self.LastAction == 'B' and self.in_bound(self.Bombx, self.Bomby):
        if self.in_bound(self.Bombx, self.Bomby):
            if board[self.Bombx][self.Bomby] == 10:
                self.Bombx, self.Bomby = None, None
        if self.in_bound(self.BMx, self.BMy) and board[self.BMx][self.BMy] in [18,88]:
            if self.LastAction == 'S' and board[self.BMx][self.BMy] == 88:
                self.Bombx, self.Bomby = self.BMx, self.BMy
            self.GetNextMove(board)
            # if self.LastAction == 'WM':
            #    return 'W'
            # else:
            # if self.LastAction == 'W':
            #     return self.LastAction
            return self.LastAction
        else:
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                if self.in_bound(self.BMx + x, self.BMy + y) == True:
                    if board[self.BMx + x][self.BMy + y] in [18,88]:
                        self.BMx , self.BMy = self.BMx + x, self.BMy + y
                        if board[self.BMx][self.BMy] == 88:
                            self.Bombx, self.Bomby = self.BMx, self.BMy
                        self.LastAction = self.GetNextMove(board)
                        # if self.LastAction == None:
                        #     return self.LastAction
                        return self.LastAction
        self.LastAction ='W'
        self.UpdateBombermanLocation(board)
        return self.LastAction

    def GetNextMove(self, board):
        Boarders = self.BuildPlus()
        Bombs, NumMonsters, Monsters, Walls = self.FillPlus(board, Boarders)
        if NumMonsters == 0:
            if self.UsePolicyLastMove:
                # self.UpdateMonstersLocation(board)
                self.dijkstra(board)
                self.UsePolicyLastMove = False
            NextMove = self.Fifo.pop()
            if NextMove == None: #FIFO is empty
                # if self.LastAction == 'WM':
                #     self.dijkstra()
                #     self.LastAction = self.Fifo.pop()
                #     if not self.UpdateBombermanLocation(board):
                #         self.LastAction = 'W'
                #     # return self.LastAction
                # else:
                # self.UpdateMonstersLocation(board)
                self.dijkstra(board)
                NextMove = self.Fifo.pop()
                if NextMove == 'S' and self.Bombx is not None:
                    NextMove = self.Fifo.pop()
                if NextMove == None: #FIFO is empty
                    self.LastAction = 'W'
                    self.UpdateBombermanLocation(board)
                    #     self.LastAction = 'W'
                else:
                    self.LastAction = NextMove
                    while not self.UpdateBombermanLocation(board):
                        NextMove = self.Fifo.pop()
                        if NextMove == 'S' and self.Bombx is not None:
                            NextMove = self.Fifo.pop()
                        self.LastAction = NextMove

                    # if not self.UpdateBombermanLocation(board):
                    #     self.LastAction = 'W'
                    return self.LastAction
            else:
                if NextMove == 'S' and self.Bombx is not None:
                    NextMove = self.Fifo.pop()
                self.LastAction = NextMove
                while not self.UpdateBombermanLocation(board):
                    NextMove = self.Fifo.pop()
                    if NextMove == 'S' and self.Bombx is not None:
                        NextMove = self.Fifo.pop()
                    self.LastAction = NextMove

                # if not self.UpdateBombermanLocation(board):
                #     self.LastAction = 'W'
                return self.LastAction
        else:
            self.UsePolicyLastMove = True
            Bombs = tuple(Bombs)
            Monsters = tuple(Monsters)
            Walls = tuple(Walls)
            Boarders = tuple(Boarders)
            NextMove = self.GetPolicy((Bombs, NumMonsters, Monsters, Walls, Boarders))
            if NextMove in ('U', 'D', 'R', 'L', 'W', 'B'):
                self.LastAction = NextMove
                self.UpdateBombermanLocation(board)
                # return self.LastAction
            elif NextMove == 'S':
                self.LastAction = NextMove
                self.UpdateBombermanLocation(board)
                # return self.LastAction
            elif NextMove == None:
                if self.Bomby is not None:
                    if self.monsterBomberManhattannDistance(self.Bombx, self.Bomby) == 1:
                        self.LastAction = 'W'
                    else:
                        self.LastAction = 'B'
                else:
                    self.LastAction = 'W'
                    self.UpdateBombermanLocation(board)
                # return self.LastAction
            elif NextMove == 'Check234':
                return self.CheckThreeZones(list(board), list(Monsters),3, 'Check3',2, 'Check2',4, 'Check4', 1, 1)
            elif NextMove == 'Check134':
                return self.CheckThreeZones(list(board), list(Monsters),4, 'Check4',3, 'Check3',1, 'Check1', 0, 0)
            elif NextMove == 'Check124':
                return self.CheckThreeZones(list(board), list(Monsters),1, 'Check1',2, 'Check2',4, 'Check4', -1, 1)
            elif NextMove == 'Check123':
                return self.CheckThreeZones(list(board), list(Monsters),2, 'Check2',3, 'Check3',1, 'Check1', 0, 0)
            elif NextMove == 'CheckS':
                self.LastAction = self.CheckS(board,list(Monsters))
                self.UpdateBombermanLocation(board)
                # return self.LastAction
            else:
                self.Check(NextMove, board)
                self.UpdateBombermanLocation(board)
                # return self.LastAction

    def CheckS(self, board, Monsters):
            # def UpdateCell (self, board, x, y, Bombs, ChangeBomb):
        CellZone1 = 0
        CellZone2 = 0
        CellZone3 = 0
        CellZone4 = 0
        for CellZone, x,y in [(1, -1,0), (2,0,-1), (3, 1,0), (4, 0,1)]:
            if self.in_bound(self.BMx + x, self.BMy + y) == True:
                if CellZone == 1:
                    CellZone1 = board[self.BMx + x][self.BMy + y]
                    continue
                if CellZone == 2:
                    CellZone2 = board[self.BMx + x][self.BMy + y]
                    continue
                if CellZone == 3:
                    CellZone3 = board[self.BMx + x][self.BMy + y]
                    continue
                if CellZone == 4:
                    CellZone4 = board[self.BMx + x][self.BMy + y]
                    continue

        if Monsters[0] == 1 and CellZone1 in [12,90]:
            return 'S'
        elif Monsters[1] == 1 and CellZone2 in [12,90]:
            return 'S'
        elif Monsters[2] == 1 and CellZone3 in [12,90]:
            return 'S'
        elif Monsters[3] == 1 and CellZone4 in [12,90]:
            return 'S'
        else:
            for zone in xrange(0,4):
                if Monsters[zone] == 0:
                    if zone == 0 and CellZone1 == 10:
                        if self.LastAction in [None, 'U', 'W','B', 'S']:
                            return 'U'
                    if zone == 1 and CellZone2 == 10:
                        if self.LastAction in [None, 'L', 'W','B', 'S']:
                            return 'L'
                    if zone == 2 and CellZone3 == 10:
                        if self.LastAction in [None, 'D', 'W','B', 'S']:
                            return 'D'
                    if zone == 3 and CellZone4 == 10:
                        if self.LastAction in [None, 'R', 'W','B', 'S']:
                            return 'R'

            for zone in xrange(0,4):
                if Monsters[zone] == 0:
                    if zone == 0 and CellZone1 == 10:
                        return 'U'
                    if zone == 1 and CellZone2 == 10:
                        return 'L'
                    if zone == 2 and CellZone3 == 10:
                        return 'D'
                    if zone == 3 and CellZone4 == 10:
                        return 'R'

        self.LastAction = 'S'
        return 'S'

    def CheckThreeZones(self, board, Monsters,Zone1, MoveZone1,Zone2, MoveZone2,Zone3, MoveZone3, x, y ):
        if Monsters[Zone1-1] == 0:
            self.Check(MoveZone1, board)
            if self.LastAction == 'W':
                return self.CheckTwoZones(board, Monsters,Zone2, MoveZone2,Zone3, MoveZone3, x, y)
            else:
                self.UpdateBombermanLocation(board)
                return self.LastAction
        else:
            FirstOption = self.CheckTwoZones(board, Monsters,Zone2, MoveZone2,Zone3, MoveZone3, x, y) #if there are monsters in zone1 and zone1 in (1,3) --> check the two sides of the move to 2 or 4
            if FirstOption not in ['W','B'] and Zone1 in [1,3]: #if we need to move to zone 2 or zone 4 --> check if there is a monster in the side that you didn't check
                SecondOption = self.CheckTwoZones(board, Monsters,Zone2, MoveZone2,Zone3, MoveZone3, -x, y)
                if FirstOption == SecondOption: #if they are the same --> you can go there, if not --> blow the bomb
                    return self.LastAction
                else:
                    self.LastAction = 'B'
                    self.UpdateBombermanLocation(board)
                    return self.LastAction
            else:
                return self.LastAction #if it told mw to Blow to Wait, or I don't need to check (zone1 in (2,4)) --> return what it said in the first time



    def CheckTwoZones(self, board, Monsters, Zone1, MoveZone1,Zone2, MoveZone2, x, y):
        if Monsters[Zone1-1] == 0:
            if self.in_bound(self.BMx -x,self.BMy -y):
                if board[self.BMx -x][self.BMy -y] != 12:
                    self.Check(MoveZone1, board)
                    if self.LastAction == 'W':
                        if Monsters[Zone2-1] == 0:
                            if self.in_bound(self.BMx -x,self.BMy +y):
                                if board[self.BMx - x][self.BMy + y] != 12:
                                    self.Check(MoveZone2, board)
                                    if self.LastAction == 'W':
                                        self.LastAction = 'B'
                                        self.UpdateBombermanLocation(board)
                                        return self.LastAction
                                    else:
                                        self.UpdateBombermanLocation(board)
                                        return self.LastAction
                                else:
                                    self.LastAction ='B'
                                    self.UpdateBombermanLocation(board)
                                    return self.LastAction
                            else:
                                self.LastAction ='B'
                                self.UpdateBombermanLocation(board)
                                return self.LastAction
                        else:
                            self.LastAction = 'B'
                            self.UpdateBombermanLocation(board)
                            return self.LastAction
                    else:
                        self.UpdateBombermanLocation(board)
                        return self.LastAction
        if Monsters[Zone2-1] == 0:
            if self.in_bound(self.BMx -x,self.BMy +y):
                if board[self.BMx - x][self.BMy + y] != 12:
                    self.Check(MoveZone2, board)
                    if self.LastAction == 'W':
                        self.LastAction = 'B'
                        self.UpdateBombermanLocation(board)
                        return self.LastAction
                    else:
                        self.UpdateBombermanLocation(board)
                        return self.LastAction
        self.LastAction = 'B'
        self.UpdateBombermanLocation(board)
        return self.LastAction

    def UpdateBombermanLocation(self, board):
        Actions = ('L', 'D', 'R', 'U', 'W', 'S', 'B', None)
        ActionDict = dict(zip(Actions,((0,-1),(1,0),(0,1),(-1,0), (0,0), (0,0), (0,0), (0,0))))
        MoveCheck = ActionDict[self.LastAction][0] + self.BMx,  ActionDict[self.LastAction][1] + self.BMy

        if not self.in_bound(MoveCheck[0], MoveCheck[1]):
            self.LastAction = 'W'
            return False

        Square = board[MoveCheck[0]][MoveCheck[1]]

        if Square not in (10, 18, 88): #this is illegal action
            self.LastAction = 'W'
            return False

        if self.LastAction == None:
            self.LastAction = 'W'
            return False

        else:
            self.BMx, self.BMy = MoveCheck[0],MoveCheck[1]
            return True

    def UpdateMonstersLocation(self, board):
        self.Monsters.clear()
        for row in range(0,self.N):
            for col in range(0,self.M):
                cell = board[row][col]
                if cell == 12:
                    self.Monsters[(row, col)] = self.monsterBomberManhattannDistance(row,col)
        self.MinMonster()

    def BuildPlus(self):
        Boarders = []
        for x,y in [(-1,0), (0,-1), (1,0), (0,1)]:
            if self.in_bound(self.BMx + x, self.BMy + y) == True:
                Boarders.append(0)
            else:
                Boarders.append(1)

        return Boarders

    def FillPlus(self, board, Boarders):
        Bombs =[0,0,0]
        ChangeBomb = False # will be False of didn't change Bomb for this area
        NumMonsters = 0
        Monsters = [0,0,0,0]
        Walls = [0,0,0,0]
        #check zone 1:
        if Boarders[0] == 0:
            ChangeMonsters = False # will be False of didn't change NumMonster and Monsters for this area
            ChangeWallsFlag = False# will be False of didn't change Walls for this area
            ChangeBombZone = False# will be False of didn't change Bomb for this area
            for x,y in [(-2,0), (-1,-1), (-1,0), (-1,1)]:
                ChangeBombZone, Bombs, ChangeBomb, WallInCell, MonsterInCell = self.UpdateCell (board, x, y, Bombs, ChangeBomb, ChangeBombZone)
                if MonsterInCell and not ChangeMonsters:
                    if NumMonsters in [0,1,2,3]:
                        NumMonsters =+ 1
                    Monsters[0] = 1
                    ChangeMonsters = True
                if WallInCell and not ChangeWallsFlag:
                    Walls[0] = 1
                    ChangeWallsFlag = True
                if ChangeWallsFlag and ChangeMonsters and ChangeBombZone:
                    break
        #check zone 2:
        if Boarders[1] == 0:
            ChangeMonsters = False # will be False of didn't change NumMonster and Monsters for this area
            ChangeWallsFlag = False # will be False of didn't change Walls for this area
            ChangeBombZone = False# will be False of didn't change Bomb for this area
            for x,y in [(0,-2), (0,-1)]:
                ChangeBombZone, Bombs, ChangeBomb, WallInCell, MonsterInCell = self.UpdateCell (board, x, y, Bombs, ChangeBomb, ChangeBombZone)
                if MonsterInCell and not ChangeMonsters:
                    if NumMonsters in [0,1,2,3]:
                        NumMonsters =+ 1
                    Monsters[1] = 1
                    ChangeMonsters = True
                if WallInCell and not ChangeWallsFlag:
                    Walls[1] = 1
                    ChangeWallsFlag = True
                if ChangeWallsFlag and ChangeMonsters and ChangeBombZone:
                    break
        #check zone 3:
        if Boarders[2] == 0:
            ChangeMonsters = False # will be False of didn't change NumMonster and Monsters for this area
            ChangeWallsFlag = False # will be False of didn't change Walls for this area
            ChangeBombZone = False# will be False of didn't change Bomb for this area
            for x,y in [(2,0), (1,-1), (1,0), (1,1)]:
                ChangeBombZone, Bombs, ChangeBomb, WallInCell, MonsterInCell = self.UpdateCell (board, x, y, Bombs, ChangeBomb, ChangeBombZone)
                if MonsterInCell and not ChangeMonsters:
                    if NumMonsters in [0,1,2,3]:
                        NumMonsters =+ 1
                    Monsters[2] = 1
                    ChangeMonsters = True
                if WallInCell and not ChangeWallsFlag:
                    Walls[2] = 1
                    ChangeWallsFlag = True
                if ChangeWallsFlag and ChangeMonsters and ChangeBombZone:
                    break
            # ChangeMonsters,ChangeWallsFlag, Bombs, ChangeBomb, NumMonsters, Monsters, Walls = self.UpateZone(3, ChangeMonsters,ChangeWallsFlag, board, Bombs,NumMonsters, Monsters, Walls, ChangeBomb, x, y)
        #check zone 4:
        if Boarders[3] == 0:
            ChangeMonsters = False # will be False of didn't change NumMonster and Monsters for this area
            ChangeWallsFlag = False # will be False of didn't change Walls for this area
            ChangeBombZone = False# will be False of didn't change Bomb for this area
            for x,y in [(0,1), (0,2)]:
                ChangeBombZone, Bombs, ChangeBomb, WallInCell, MonsterInCell = self.UpdateCell (board, x, y, Bombs, ChangeBomb,ChangeBombZone)
                if MonsterInCell and not ChangeMonsters:
                    if NumMonsters in [0,1,2,3]:
                        NumMonsters =+ 1
                    Monsters[3] = 1
                    ChangeMonsters = True
                if WallInCell and not ChangeWallsFlag:
                    Walls[3] = 1
                    ChangeWallsFlag = True
                if ChangeWallsFlag and ChangeMonsters and ChangeBombZone:
                    break
        if not ChangeBomb:
            if board[self.BMx][self.BMy] == 88:
                Bombs[0], Bombs[1], Bombs[2] = 1 , 0, 0
            else:
                Bombs[1], Bombs[2] = None, None
        return Bombs, NumMonsters, Monsters, Walls

    # def UpateZone(self, Zone, ChangeMonsters,ChangeWallsFlag, board, Bombs,NumMonsters, Monsters, Walls, ChangeBomb, x, y):
    #     Bombs, ChangeBomb,NumMonsters, Monsters, ChangeMonsters, ChangeWallsFlag, Walls = self.UpdateDict(board,4, x, y, Bombs, ChangeBomb,NumMonsters, Monsters, ChangeMonsters, ChangeWallsFlag, Walls)
    #     if not ChangeMonsters and Monsters[Zone-1] == 1:
    #         ChangeMonsters = True
    #     if not ChangeWallsFlag and Walls [Zone-1] == 1:
    #         ChangeWallsFlag = True
    #     return ChangeMonsters,ChangeWallsFlag, Bombs, ChangeBomb, NumMonsters, Monsters, Walls

    def UpdateCell (self, board, x, y, Bombs, ChangeBomb, ChangeBombZone):
        MonsterInCell = False
        WallInCell = False
        if self.in_bound(self.BMx + x, self.BMy + y) == True:
            if board[self.BMx + x][self.BMy + y] == 12:
                MonsterInCell = True
                return ChangeBombZone, Bombs, ChangeBomb, WallInCell, MonsterInCell
            if not ChangeBomb:
                if board[self.BMx + x][self.BMy + y] in [80,88]:
                    Bombs[0], Bombs[1], Bombs[2] = 1, x, y
                    ChangeBomb = True
                    ChangeBombZone = True
                    return ChangeBombZone, Bombs, ChangeBomb, WallInCell, MonsterInCell
            if board[self.BMx + x][self.BMy + y] in [90,99]:
                WallInCell = True
                return ChangeBombZone, Bombs, ChangeBomb, WallInCell, MonsterInCell
        return ChangeBombZone, Bombs, ChangeBomb, WallInCell, MonsterInCell

    # def UpdateDict (self, board, zone, x, y, Bombs, ChangeBomb,NumMonsters, Monsters, ChangeMonsters, ChangeWallsFlag, Walls):
    #     if not ChangeMonsters:
    #         if self.in_bound(self.BMx + x, self.BMy + y) == True:
    #             if board[self.BMx + x][self.BMy + y] == 12:
    #                 if NumMonsters in [0,1,2,3]:
    #                     NumMonsters +=1
    #                 Monsters.append(1)
    #                 ChangeMonsters = True
    #             else:
    #                 Monsters.append(0)
    #     if not ChangeBomb:
    #         if self.in_bound(self.BMx + x, self.BMy + y) == True:
    #             if board[self.BMx + x][self.BMy + y] in [80,88]:
    #                 Bombs[0], Bombs[1], Bombs[2] = 1, x, y
    #                 ChangeBomb = True
    #             else:
    #                 Bombs[0], Bombs[1], Bombs[2] = 0, None, None
    #     if not ChangeWallsFlag:
    #         if self.in_bound(self.BMx + x, self.BMy + y) == True:
    #             if board[self.BMx + x][self.BMy + y] in [90,99]:
    #                 Walls.append(1)
    #             else:
    #                 Walls.append(0)
    #     return Bombs, ChangeBomb, NumMonsters, Monsters, ChangeMonsters, ChangeWallsFlag, Walls

    def monsterBomberManhattannDistance (self, row, col):
        #claculate manhattan distance between a monster and bomberman
        return (abs(row - self.BMx)+ abs(col - self.BMy))
        
    def Check(self, NextMove, board):
        if NextMove in ['Check1', 'Check12', 'Check13', 'Check14','CheckAll']:
            return self.CheckAction('U', board)
        elif NextMove in ['Check2', 'Check12', 'Check23', 'Check24', 'CheckAll']:
            return self.CheckAction('L', board)
        elif NextMove in ['Check3', 'Check13', 'Check23', 'Check34', 'CheckAll']:
            return self.CheckAction('D', board)
        elif NextMove in ['Check4', 'Check14', 'Check24', 'Check34', 'CheckAll']:
            return self.CheckAction('R', board)
        else:
            self.LastAction = 'W'

    def CheckAction(self, action, board):
        CellZone1 = 0
        CellZone2 = 0
        CellZone3 = 0
        CellZone4 = 0
        Actions = ('L', 'D', 'R', 'U')
        ActionDict = dict(zip(Actions,((0,-1),(1,0),(0,1),(-1,0))))
        MoveCheck = ActionDict[action][0] + self.BMx,  ActionDict[action][1] + self.BMy
        if self.in_bound(MoveCheck[0], MoveCheck[1]) == True:
            if board[MoveCheck[0]][MoveCheck[1]] == 10:
                if self.in_bound(self.BMx, self.BMy) == True and board[self.BMx][self.BMy] == 88:
                    for CellZone, x,y in [(1, -1,0), (2,0,-1), (3, 1,0), (4, 0,1)]:
                        if self.in_bound(MoveCheck[0] + x, MoveCheck[1] + y) == True:
                            if CellZone == 1:
                                CellZone1 = board[MoveCheck[0] + x][MoveCheck[1] + y]
                                continue
                            if CellZone == 2:
                                CellZone2 = board[MoveCheck[0] + x][MoveCheck[1] + y]
                                continue
                            if CellZone == 3:
                                CellZone3 = board[MoveCheck[0] + x][MoveCheck[1] + y]
                                continue
                            if CellZone == 4:
                                CellZone4 = board[MoveCheck[0] + x][MoveCheck[1] + y]
                                continue
                self.LastAction = action
        else:
            self.LastAction = 'W'

    def CreatePolicy(self):
        #create the self.Policy[((1,x,y),NumMonster,monster,walls,boarders)]--> look on the + around Bomberman and define the following:
        #[0:[IsBomb, BombX, BombY], 1:number of ares with monsters(1: 1,2-3:2, 4 and up:4), 2:monsters:{1:_, 2:_, 3:_, 4:_}, 3:walls:{1:_, 2:_, 3:_, 4:_},
        # 4:boarders:{1:_, 2:_, 3:_, 4:_},]

        for IsBomb in (0,1): #if there is no bomb in the +, but there is monsters --> set a bomb
            if IsBomb == 0:
                for NumMonster in (1, 2,3, 4):
                    for monster in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1),(1,1,1,0),(1,0,1,1),(1,1,0,1),(0,1,1,1),(1,1,1,1)]:
                            for walls in [(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1),(1,1,1,0),(1,0,1,1),(1,1,0,1),(0,1,1,1),(1,1,1,1),(0,0,0,0)]:
                                for boarders in [(1,1,0,0),(1,0,0,1),(0,0,1,1), (0,1,1,0),(1,0,0,0),(0,1,0,0),(0,0,1,0),(0,0,0,1),(0,0,0,0)]:
                                    self.Policy[((0,None,None),NumMonster,monster,walls,boarders)] = 'CheckS'
            else:
                for NumMonster in [4]:#if there 4  monsters on the board --> blow the bomb
                    for monster in [(1,1,1,1)]:
                        for x,y in [(0,0),(-2,0),(0,-2),(2,0),(0,2),(-1,1),(-1,-1),(1,1),(1,-1),(-1,0),(0,-1),(1,0),(0,1)]:
                            for walls in [(1,0,0,0),(0,1,0,0),(0,1,0,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1),(1,1,1,0),(1,0,1,1),(1,1,0,1),(0,1,1,1),(1,1,1,1),(0,0,0,0)]:
                                for boarders in [(1,1,0,0), (1,0,0,1), (0,0,1,1),(0,1,1,0), (1,0,0,0), (0,1,0,0),(0,1,0,0), (0,0,0,1), (0,0,0,0)]:
                                    self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B'

                for x,y in [(0,0)]: #when there is a bomb with bomberman in the same cell --> escape to the area you can go, if there no such area --> bomb or wait
                   for NumMonster in (1, 2):
                        if NumMonster == 1:#if there is one monster on the board --> and you can't escape --> bomb, if there are 3 monsters- check if there are more that close to you than far from you
                            for monster in [(1,0,0,0)]: #noster in zone 1:
                                for boarders in [(0,1,0,0), (0,0,0,0), (0,1,0,1), (0,1,0,0)]: #there is no boarder in 3:
                                    for walls in [(1,0,0,0),(0,1,0,0), (0,0,0,1),(1,1,0,0), (1,0,0,1), (0,1,0,1),(1,1,0,1), (0,0,0,0)]:#there are no wall in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [(0,0,0,1), (0,0,0,0)]: #there is no boarder in 3 and in 2:
                                    for walls in [(0,1,0,0), (1,0,1,0),(0,0,1,1),(1,0,1,1)]:#there are walls in 3 but not in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                    for walls in [(0,1,1,1), (1,1,1,1)]: #there are walls in 2,3,4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckAll'
                                    for walls in [(0,1,1,0),(1,1,1,0)]: #there are walls in 2,3 but not in 4:
                                        if boarders == (0,0,0,1): #there is boarder in 4:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check23'
                                        elif boarders == (0,0,0,0): #there is no boarder in 4:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [(1,1,0,0),(0,1,0,0)]:#there is no boarder in 3 but there is in 2:
                                    for walls in [(0,1,0,0), (1,0,1,0)]: #there are walls in 3 but not in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                    for walls in [(0,0,1,1), (1,0,1,1)]: #there are walls in 3 and 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check34'
                                for boarders in [(0,1,1,0)]: #there is boarder in 2 and 3:
                                    for walls in [(0,0,0,1), (1,0,0,1)]:  #there are walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B'
                                    for walls in [(1,0,0,0), (0,0,0,0)]:#there are no walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [(0,1,0,0)]: #there is no boarder in 4,2 but there is boarder in 3:
                                    for walls in [(0,1,0,1),(1,1,0,1)]: #there is wall in 4,2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check42'
                                    for walls in [(0,1,0,0), (1,1,0,0)]:#there is no wall in 4 but there is wall in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [(0,0,1,1), (0,1,0,0)]: #there is no boarder in 2 but there is boarder in 3:
                                    for walls in [(1,0,0,0), (0,0,0,1),(1,0,0,1),(0,0,0,0)]: #there is no walls in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                for boarders in [(0,0,1,1)]: #there is no boarder in 2 but there is boarder in 3,4:
                                    for walls in [(1,1,0,0),(0,1,0,0)]: #there is walls in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check2'


                            for monster in [(0,1,0,0)]: #noster in zone 2:
                                for boarders in [(1,0,1,0), (0,0,0,0), (1,0,0,0), (0,1,0,0)]: #there is no boarder in 4:
                                    for walls in [(1,0,0,0),(0,1,0,0), (0,1,0,0), (1,1,0,0), (1,0,1,0),(0,1,1,0),(1,1,1,0),(0,0,0,0)]:#there are no wall in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [(1,0,0,0), (0,0,0,0)]: #there is no boarder in 3 and in 4:
                                    for walls in [(0,0,0,1),(1,0,0,1),(0,1,0,1), (1,1,0,1)]:#there are walls in 4 but not in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                    for walls in [(1,0,1,1),(1,1,1,1)]: #there are walls in 1,3,4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckAll'
                                    for walls in [(0,0,1,1),(0,1,1,1)]: #there are walls in 3,4 but not in 1:
                                        if boarders == (1,0,0,0): #there is boarder in 1:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check34'
                                        elif boarders == (0,0,0,0): #there is no boarder in 1:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [(0,1,1,0), (0,1,0,0)]:#there is no boarder in 4 but there is in 3:
                                    for walls in [(0,0,0,1),(0,1,0,1)]: #there are walls in 4 but not in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                    for walls in [(1,0,0,1),(1,1,0,1)]: #there are walls in 1 and 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check14'
                                for boarders in [(0,0,1,1)]: #there is boarder in 4 and 3:
                                    for walls in [(1,0,0,0), (1,1,0,0)]:  #there are walls in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check1'
                                    for walls in [(0,1,0,0), (0,0,0,0)]:#there are no walls in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [(0,0,0,1)]: #there is no boarder in 1,3 but there is boarder in 4:
                                    for walls in [(0,1,1,0),(1,1,1,0)]: #there is wall in 1,3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check13'
                                    for walls in [(0,1,1,0), (0,1,0,0)]:#there is no wall in 1 but there is wall in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [(0,0,0,1), (1,0,0,1)]: #there is no boarder in 3 but there is boarder in 4:
                                    for walls in [(1,0,0,0), (0,0,0,0),(1,1,0,0),(0,1,0,0)]: #there is no walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [(1,0,0,1)]: #there is no boarder in 3 but there is boarder in 1,4:
                                    for walls in [(0,1,0,0),(0,1,1,0)]: #there is walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check3'

                            for monster in [(0,1,0,0)]: #noster in zone 3:
                                for boarders in [(0,1,0,0), (0,0,0,0), (0,1,0,1), (0,1,0,0)]: #there is no boarder in 1:
                                    for walls in [(0,1,0,0), (0,1,0,0), (0,0,0,1),(0,1,1,0), (0,1,0,1), (0,0,1,1),(0,1,1,1), (0,0,0,0)]:#there are no wall in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [(0,1,0,0), (0,0,0,0)]: #there is no boarder in 4 and in 1:
                                    for walls in [(1,0,0,0), (1,1,0,0), (1,0,1,0),(1,1,1,0)]:#there are walls in 1 but not in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                    for walls in [(1,1,1,1),(1,1,0,1)]: #there are walls in 1,2,4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckAll'
                                    for walls in [(1,0,1,1),(1,0,0,1)]: #there are walls in 1,4 but not in 2:
                                        if boarders == (0,1,0,0): #there is boarder in 2:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check14'
                                        elif boarders == (0,0,0,0): #there is no boarder in 3:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [(0,1,0,1), (0,0,0,1)]:#there is no boarder in 1 but there is in 4:
                                    for walls in [(1,0,0,0),(1,0,1,0)]: #there are walls in 1 but not in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                    for walls in [(1,1,0,0),(1,1,1,0)]: #there are walls in 1 and 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check12'
                                for boarders in [(1,0,0,1)]: #there is boarder in 1 and 4:
                                    for walls in [(0,1,0,0),(0,1,1,0)]:  #there are walls in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B'
                                    for walls in [(0,0,0,0), (0,1,0,0)]:#there are no walls in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                for boarders in [(1,0,0,0)]: #there is no boarder in 4,2 but there is boarder in 1:
                                    for walls in [(0,1,1,1),(0,1,0,1)]: #there is wall in 4,2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check24'
                                    for walls in [(0,0,1,1), (0,0,1,1)]:#there is no wall in 2 but there is wall in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                for boarders in [(0,0,0,1), (1,0,0,1)]: #there is no boarder in 4 but there is boarder in 1:
                                    for walls in [(0,0,0,0), (0,1,0,0),(0,1,1,0),(0,1,0,0)]: #there is no walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [(1,0,0,1)]: #there is no boarder in 4 but there is boarder in 1,2:
                                    for walls in [(0,0,1,1),(0,0,0,1)]: #there is walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check4'

                            for monster in [(0,0,0,1)]: #noster in zone 4:
                                for boarders in [(1,0,1,0), (0,0,0,0), (1,0,0,0), (0,1,0,0)]: #there is no boarder in 2:
                                    for walls in [(1,0,0,0), (0,1,0,0), (0,0,0,1),(1,0,1,0), (1,0,0,1), (0,0,1,1),(1,0,1,1),(0,0,0,0)]:#there are no wall in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                for boarders in [(0,1,0,0), (0,0,0,0)]: #there is no boarder in 1,2:
                                    for walls in [(0,1,0,0),(0,1,1,0), (0,1,0,1),(0,1,1,1)]:#there are walls in 2 but not in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                    for walls in [(1,1,1,1),(1,1,1,0)]: #there are walls in 1,2,3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckAll'
                                    for walls in [(1,1,0,1),(1,1,0,0)]: #there are walls in 1,2 but not in 3:
                                        if boarders == (0,1,0,0): #there is boarder in 3:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check12'
                                        elif boarders == (0,0,0,0): #there is no boarder in 3:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [(1,0,0,0), (1,0,1,0)]:#there is no boarder in 2 but there is in 1:
                                    for walls in [(0,1,0,0),(0,1,0,1)]: #there are walls in 2 but not in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                    for walls in [(0,1,1,0),(0,1,1,1)]: #there are walls in 2 and 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check23'
                                for boarders in [(1,1,0,0)]: #there is boarder in 1,2:
                                    for walls in [(0,1,0,0), (0,0,1,1)]:  #there are walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check3'
                                    for walls in [(0,0,0,0), (0,0,0,1)]:#there are no walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [(0,1,0,0)]: #there is no boarder in 1,3 but there is boarder in 2:
                                    for walls in [(1,0,1,1),(1,0,1,0)]: #there is wall in 1,3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check13'
                                    for walls in [(1,0,0,0), (1,0,0,1)]:#there is no wall in 3 but there is wall in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [(0,1,0,0),(0,1,1,0)]: #there is no boarder in 1 but there is boarder in 2:
                                    for walls in [(0,0,0,0), (0,1,0,0),(0,0,1,1),(0,0,0,1)]: #there are no walls in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [(0,1,1,0)]: #there is no boarder in 1 but there is boarder in 2,3:
                                    for walls in [(1,0,0,0),(1,0,0,1)]: #there are walls in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check1'


                        if NumMonster == 2:#if there are 2 monsters in the board
                            for monster in [(1,1,0,0)]: #there are monsters in 1,2
                                for boarders in [(0,0,1,1)]: #there is boarder in 3,4
                                    for walls in [(0,0,0,0), (1,0,0,0), (0,1,0,0),(1,1,0,0)]: #there is no walls in 3,4 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(0,1,0,0)]: #there is boarder in 3 but not in 4
                                    for walls in [(0,0,0,1), (1,0,0,1), (0,1,0,1),(1,1,0,1)]: #there are walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [(0,0,0,0), (1,0,0,0), (0,1,0,0),(1,1,0,0)]: #there are no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(3)
                                for boarders in [(0,0,0,0)]: #there are no boarders in 3,4
                                    for walls in [(0,0,1,1), (1,0,1,1),(0,1,1,1),(1,1,1,1)]: #there are walls in 3,4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [(0,1,0,0), (1,0,1,0),(0,1,1,0),(1,1,1,0)]: #there are walls in 3 but not in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(5)
                                    for walls in [(1,0,0,0),(0,1,0,0), (0,0,0,1), (1,1,0,0), (1,0,0,1), (0,1,0,1),(1,1,0,1),(0,0,0,0)]: #there are walls no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(6)
                                for boarders in [(0,0,0,1)]: #there are no boarders in 3 but there are in 4
                                    for walls in [(1,0,0,0),(0,1,0,0), (1,1,0,0),(0,0,0,0)]: #there are walls no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(7)
                                    for walls in [(0,1,0,0), (1,0,1,0),(0,1,1,0),(1,1,1,0)]: #there are walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [(1,0,0,1)]: #there are monsters in 1,4
                                for boarders in [(0,1,1,0)]: #there are boarders in 3,2
                                    for walls in [(0,0,0,0), (1,0,0,0), (0,0,0,1),(1,0,0,1)]: #there is no walls in 3,2 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(0,1,0,0)]: #there is boarder in 3 but not in 2
                                    for walls in [(0,1,0,0), (1,1,0,0), (0,1,0,1),(1,1,0,1)]: #there are walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [(0,0,0,0), (1,0,0,0), (0,0,0,1),(1,0,0,1)]: #there are no walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(3)
                                for boarders in [(0,0,0,0)]: #there are no boarders in 3,2
                                    for walls in [(0,1,1,0),(1,1,1,0),(0,1,1,1),(1,1,1,1)]: #there are walls in 3,2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [(0,1,0,0), (1,0,1,0), (0,0,1,1),(1,0,1,1)]: #there are walls in 3 but not in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(5)
                                    for walls in [(1,0,0,0),(0,1,0,0), (0,0,0,1), (1,1,0,0), (1,0,0,1), (0,1,0,1),(1,1,0,1),(0,0,0,0)]: #there are walls no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(6)
                                for boarders in [(0,1,0,0)]: #there are no boarders in 3 but there are in 2
                                    for walls in [(1,0,0,0), (0,0,0,1),  (1,0,0,1), (0,0,0,0)]: #there are walls no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(7)
                                    for walls in [(0,1,0,0), (1,0,1,0), (0,0,1,1),(1,0,1,1)]: #there are walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [(0,1,1,0)]: #there are monsters in 2,3
                                for boarders in [(1,0,0,1)]: #there is boarder in 1,4
                                    for walls in [(0,0,0,0), (0,1,0,0), (0,1,0,0),(0,1,1,0)]: #there is no walls in 1,4 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(1,0,0,0)]: #there is boarder in 1 but not in 4
                                    for walls in [(0,0,0,1), (0,0,1,1), (0,1,0,1),(0,1,1,1)]: #there are walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [(0,0,0,0), (0,1,0,0), (0,1,0,0),(0,1,1,0)]: #there are no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(3)
                                for boarders in [(0,0,0,0)]: #there are no boarders in 1,4
                                    for walls in [(1,0,0,1), (1,0,1,1), (1,1,0,1),(1,1,1,1)]: #there are walls in 1,4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [(1,0,0,0), (1,0,1,0), (1,1,0,0),(1,1,1,0)]: #there are walls in 1 but not in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(5)
                                    for walls in [(0,1,0,0),(0,1,0,0), (0,0,0,1),(0,1,1,0), (0,0,1,1), (0,1,0,1),(0,1,1,1),(0,0,0,0)]: #there are walls no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                for boarders in [(0,0,0,1)]: #there are no boarders in 1 but there are in 4
                                    for walls in [(0,1,0,0),(0,1,0,0),(0,1,1,0),(0,0,0,0)]: #there are walls no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                    for walls in [(1,0,0,0), (1,0,1,0), (1,1,0,0),(1,1,1,0)]: #there are walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [(0,0,1,1)]: #there are monsters in 3,4
                                for boarders in [(1,1,0,0)]: #there is boarder in 1,2
                                    for walls in [(0,0,0,0), (0,1,0,0), (0,0,0,1),(0,0,1,1)]: #there is no walls in 1,2 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(1,0,0,0)]: #there is boarder in 1 but not in 2
                                    for walls in [(0,1,0,1),(0,1,1,1), (0,1,0,0),(0,1,1,0)]: #there are walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [(0,0,0,0), (0,1,0,0), (0,0,0,1),(0,0,1,1)]: #there are no walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(3)
                                for boarders in [(0,0,0,0)]: #there are no boarders in 1,2
                                    for walls in [(1,1,0,0),(1,1,1,0), (1,1,0,1),(1,1,1,1)]: #there are walls in 1,2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [(1,0,0,0), (1,0,1,0), (1,0,0,1),(1,0,1,1)]: #there are walls in 1 but not in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(5)
                                    for walls in [(0,1,0,0),(0,1,0,0), (0,0,0,1),(0,1,1,0), (0,0,1,1), (0,1,0,1),(0,1,1,1),(0,0,0,0)]: #there are walls no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                for boarders in [(0,1,0,0)]: #there are no boarders in 1 but there are in 2
                                    for walls in [(0,1,0,0), (0,0,0,1),  (0,0,1,1),(0,0,0,0)]: #there are no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                    for walls in [(1,0,1,1), (1,0,0,1), (1,0,0,0),(1,0,1,0)]: #there are walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [(0,1,0,1)]: #there are monsters in 2,4
                                for boarders in [(1,0,1,0)]: #there is boarder in 1,3
                                    for walls in [(0,0,0,0), (0,1,0,0), (0,0,0,1),(0,1,0,1)]: #there is no walls in 1,3 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(1,0,0,0)]: #there is boarder in 1 but not in 3
                                    for walls in [(0,0,1,1),(0,1,1,1), (0,1,0,0),(0,1,1,0)]: #there are walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [(0,0,0,0), (0,1,0,0), (0,0,0,1),(0,1,0,1)]: #there are no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(3)
                                for boarders in [(0,0,0,0)]: #there are no boarders in 1,3
                                    for walls in [(1,0,1,0),(1,1,1,0), (1,0,1,1),(1,1,1,1)]: #there are walls in 1,3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [(1,0,0,0), (1,1,0,0), (1,0,0,1),(1,1,0,1)]: #there are walls in 1 but not in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(5)
                                    for walls in [(0,1,0,0),(0,1,0,0), (0,0,0,1),(0,1,1,0), (0,0,1,1), (0,1,0,1),(0,1,1,1),(0,0,0,0)]: #there are walls no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                for boarders in [(0,1,0,0)]: #there are no boarders in 1 but there are in 3
                                    for walls in [(0,1,0,0), (0,0,0,1),  (0,1,0,1),(0,0,0,0)]: #there are no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                    for walls in [(1,0,0,0), (1,1,0,0), (1,0,0,1),(1,1,0,1)]: #there are walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [(0,0,1,1)]: #there are monsters in 1,3
                                for boarders in [(0,1,0,1)]: #there is boarder in 4,2
                                    for walls in [(0,0,0,0), (0,1,0,0), (1,0,0,0),(1,0,1,0)]: #there is no walls in 4,2 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(0,0,0,1)]: #there is boarder in 4 but not in 2
                                    for walls in [(1,1,0,0),(1,1,1,0), (0,1,0,0),(0,1,1,0)]: #there are walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [(0,0,0,0), (0,1,0,0), (1,0,0,0),(1,0,1,0)]: #there are no walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(3)
                                for boarders in [(0,0,0,0)]: #there are no boarders in 1,2
                                    for walls in [(0,1,0,1),(0,1,1,1), (1,1,0,1),(1,1,1,1)]: #there are walls in 2,4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [(0,0,0,1), (0,0,1,1), (1,0,0,1),(1,0,1,1)]: #there are walls in 4 but not in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(5)
                                    for walls in [(0,1,0,0),(0,1,0,0), (1,0,0,0),(0,1,1,0), (1,0,1,0), (1,1,0,0),(0,1,1,1),(0,0,0,0)]: #there are walls no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(6)
                                for boarders in [(0,1,0,0)]: #there are no boarders in 1 but there are in 2
                                    for walls in [(0,1,0,0), (1,0,0,0),  (1,0,1,0),(0,0,0,0)]: #there are no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(6)
                                    for walls in [(0,0,0,1), (0,0,1,1), (1,0,0,1),(1,0,1,1)]: #there are walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                        if NumMonster == 3:#if there are 3 monsters in the board
                            for monster in [(1,1,1,0)]: #there are monsters in 1,2,3
                                for boarders in [(0,0,0,1)]: #there is boarder in 4
                                    for walls in [(1,0,0,0),(0,1,0,0), (0,1,0,0),(1,1,0,0), (1,0,1,0),(0,1,1,0),(1,1,1,0), (0,0,0,0)]: #there can't be walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(0,0,0,0)]: #there is no boarder in 4
                                    for walls in [(1,0,0,0),(0,1,0,0), (0,1,0,0),(1,1,0,0), (1,0,1,0),(0,1,1,0),(1,1,1,0), (0,0,0,0)]:#there are no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(2)
                                    for walls in [(0,0,0,1),(1,0,0,1), (0,1,0,1), (0,0,1,1),(1,0,1,1), (1,1,0,1),(0,1,1,1),(1,1,1,1)]:#there are walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(3)

                            for monster in [(1,1,0,1)]: #there are monsters in 1,2,4
                                for boarders in [(0,1,0,0)]: #there is boarder in 3
                                    for walls in [(1,0,0,0),(0,1,0,0), (0,0,0,1),(1,1,0,0),(1,0,0,1), (0,1,0,1), (1,1,0,1), (0,0,0,0)]: #there can't be walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(0,0,0,0)]: #there is no boarder in 3
                                    for walls in [(1,0,0,0),(0,1,0,0), (0,0,0,1),(1,1,0,0),(1,0,0,1), (0,1,0,1), (1,1,0,1), (0,0,0,0)]: #there are no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(2)
                                    for walls in [(0,1,0,0), (1,0,1,0),(0,1,1,0), (0,0,1,1),(1,1,1,0), (1,0,1,1), (0,1,1,1),(1,1,1,1)]:#there are walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(3)

                            for monster in [(0,1,1,1)]: #there are monsters in 2,3,4
                                for boarders in [(1,0,0,0)]: #there is boarder in 1
                                    for walls in [(0,1,0,0),(0,1,0,0), (0,0,0,1),(0,1,1,0),(0,0,1,1), (0,1,0,1),(0,1,1,1), (0,0,0,0)]: #there can't be walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(0,0,0,0)]: #there is no boarder in 1
                                    for walls in [(0,1,0,0),(0,1,0,0), (0,0,0,1),(0,1,1,0),(0,0,1,1), (0,1,0,1),(0,1,1,1), (0,0,0,0)]: #there are no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(2)
                                    for walls in [(1,0,0,0), (1,0,1,0),(1,1,0,0), (1,0,0,1),(1,1,1,0), (1,0,1,1), (1,1,0,1),(1,1,1,1)]:#there are walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(3)

                            for monster in [(1,0,1,1)]: #there are monsters in 1,3,4
                                for boarders in [(0,1,0,0)]: #there is boarder in 2
                                    for walls in [(0,1,0,0),(1,0,0,0), (0,0,0,1),(1,0,1,0),(0,0,1,1), (1,0,0,1), (1,0,1,1), (0,0,0,0)]: #there can't be walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [(0,0,0,0)]: #there is no boarder in 2
                                    for walls in [(0,1,0,0),(1,0,0,0), (0,0,0,1),(1,0,1,0),(0,0,1,1), (1,0,0,1), (1,0,1,1), (0,0,0,0)]: #there are no walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(2)
                                    for walls in [(0,1,0,0),(0,1,1,0),(1,1,0,0), (0,1,0,1),(1,1,1,0),(0,1,1,1), (1,1,0,1),(1,1,1,1)]:#there are walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(3)

                for x,y in [(-2,0),(0,-2),(2,0),(0,2),(-1,1),(-1,-1),(1,1),(1,-1)]: #the bomb is 2 steps from bomberman--> blow it
                    for NumMonster in [1,2,3,4]: #no mattar how many monsters are in the +
                        for monster in [(1,0,0,0),(0,1,0,0),(0,1,0,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1),(1,1,1,0),(1,0,1,1),(1,1,0,1),(0,1,1,1)]:
                            for walls in [(1,0,0,0),(0,1,0,0),(0,1,0,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1),(1,1,1,0),(1,0,1,1),(1,1,0,1),(0,1,1,1),(1,1,1,1),(0,0,0,0)]:
                                for boarders in [(1,1,0,0),(1,0,0,1),(0,0,1,1),(0,1,1,0),(1,0,0,0),(0,1,0,0),(0,1,0,0),(0,0,0,1),(0,0,0,0)]:
                                    self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B'


                for x,y in [(-1,0),(0,-1),(1,0),(0,1)]: #the bomb is 1 step from bomberman--> go away from it if you can --> blow it if you can't escape
                    for NumMonster in [1,2,3]: # there is 1,2,3 monster
                        for monster in [(1,0,0,0),(0,1,0,0),(0,1,0,0),(0,0,0,1),(1,1,0,0),(1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1),(1,1,1,0),(1,0,1,1),(1,1,0,1),(0,1,1,1)]:
                            for walls in [(1,0,0,0),(0,1,0,0),(0,1,0,0),(0,0,0,1),(1,1,0,0), (1,0,1,0),(1,0,0,1),(0,1,1,0),(0,1,0,1),(0,0,1,1),(1,1,1,0),(1,0,1,1),(1,1,0,1),(0,1,1,1),(1,1,1,1),(0,0,0,0)]:
                                for boarders in [(1,1,0,0),(1,0,0,1),(0,0,1,1),(0,1,1,0),(1,0,0,0),(0,1,0,0),(0,1,0,0),(0,0,0,1),(0,0,0,0)]:
                                    if (x,y) == (-1,0):
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check234'
                                    if (x,y) == (0,-1):
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check134'
                                    if (x,y) == (1,0):
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check124'
                                    if (x,y) == (0,1):
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check123'

    def GetPolicy(self,key):
        return self.Policy.get(key)

