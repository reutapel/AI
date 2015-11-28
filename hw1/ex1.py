import search
import math

ids = ["201316346", "201110376"]  # Feel your IDs


class BombermanProblem(search.Problem):
    """This class implements a Bomberman problem"""


    def __init__(self, initial):
        """ Constructor only needs the initial state.
        Don't forget to set the goal or implement the goal test"""
        search.Problem.__init__(self, initial)
        self.N = len(initial)
        self.M = len(initial[1])
        self.Monsters = {}
        self.Walls = set()
        self.Bomb = [False, [None, None]]
        self.BMx = None
        self.BMy = None
        # for row in range(0,self.N):
        #     for col in range(0,self.M):
        #         cell = initial[row][col]
        #         if cell == 90:
        #             self.Walls.add((row, col))
        #         elif cell == 18:
        #             self.BMx = row
        #             self.BMy = col
        #         elif cell in range(12,16):
        #             self.Monsters.update({cell: [row, col]})

    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        suc_list = []
        for act in ['U', 'D', 'R', 'L', 'W', 'B', 'S']: #for each action, check what will be the state after we bomberman will do it/
            suc_state = self.suc_successor(act, state)
            if suc_state is not None: #if the action is legal --> insert the action+ new successor state to the successors list
                suc_list.append((act, suc_state))
        return suc_list

    def suc_successor(self, act, state):
        mut_state = [list(a) for a in state] #change the given state to mutable state

        if act == 'U':
            bmx = self.BMx
            bmy = self.BMy
            nx = (bmx-1)
            ny = bmy
            checked_state = self.do_checks(mut_state, bmx, bmy, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'D':
            bmx = self.BMx
            bmy = self.BMy
            nx = (bmx+1)
            ny = bmy
            checked_state = self.do_checks(mut_state, bmx, bmy, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'R':
            bmx = self.BMx
            bmy = self.BMy
            nx = bmx
            ny = (bmy+1)
            checked_state = self.do_checks(mut_state, bmx, bmy, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'L':
            bmx = self.BMx
            bmy = self.BMy
            nx = bmx
            ny = (bmy-1)
            checked_state = self.do_checks(mut_state, bmx, bmy, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'W':
            if not self.move_mons(mut_state,self.BMx, self.BMy):
                return None
            imut_state = tuple(tuple(b) for b in mut_state)
            return imut_state

        elif act == 'S':
            if self.Bomb[0]:
                return None
            else:
                mut_state[self.BMx][self.BMy] = 88
                if not self.move_mons(mut_state, self.BMx, self.BMy):
                    return None
                imut_state = tuple(tuple(b) for b in mut_state)
                return imut_state

        elif act == 'B':
            if not self.Bomb[0]:
                return None
            if self.blow_bomber():
                return None
            self.blow_walls(mut_state)
            self.blow_mons(mut_state)
            if not self.move_mons(mut_state,self.BMx, self.BMy):
                return None
            mut_state[self.Bomb[1][0]][self.Bomb[1][1]] = 10
            imut_state = tuple(tuple(b) for b in mut_state)
            return imut_state

    def in_bound(self, x, y):
        if 0 <= x < self.N and 0 <= y < self.M:
            return True
        return False
    #
    # def is_wall(self, x, y):
    #     if (x,y) in self.Walls:
    #         return True
    #     return False

    # def is_mons(self, x, y):
    #     if [x, y] in self.Monsters.values():
    #         return True
    #     return False
    #
    # def is_hwall(self, mut_state, x, y):
    #     if mut_state[x][y] == 99:
    #         return True
    #     return False
    #
    # def is_bomb(self, x, y):
    #     if self.Bomb[0]:
    #         if self.Bomb[1] == [x, y]:
    #             return True
    #     return False

    def is_empty(self, mut_state, x, y):
        if mut_state[x][y] == 10:
            return True
        return False

    def move_mons(self, mut_state, bmx, bmy):  # Q- return true in all functions that there is an if condition waiting for false?
        for key in sorted(self.Monsters.iterkeys()):
            monsterx = self.Monsters[key][0]
            monstery = self.Monsters[key][1]
            minx = monsterx
            miny = monstery
            move_to = self.man_dis(minx, miny, bmx, bmy,  mut_state)
            if not move_to:
                return False
            # self.Monsters[key][0] = move_to[0]
            # self.Monsters[key][1] = move_to[1]
            mut_state[move_to[0]][move_to[1]] = key
            mut_state[monsterx][monstery] = 10
        return True

    def do_checks(self, mut_state, bmx, bmy, nx, ny):  # Q: can I save mut_state and just use self.
        if not self.in_bound(nx, ny):
            return False
        if self.is_empty(mut_state, nx, ny):
            mut_state[nx][ny] = 18
 #           self.BMx = nx
 #           self.BMy = ny
            if mut_state[bmx][bmy] == 18:
                mut_state[bmx][bmy] = 10
            else:
                mut_state[bmx][bmy] = 80
            if not self.move_mons(mut_state, nx, ny):
                return False
            imut_state = tuple(tuple(b) for b in mut_state )
            return imut_state
        # else:
        #     if not self.move_mons(mut_state, bmx, bmy):
        #         return False
        #     imut_state = tuple(tuple(b) for b in mut_state )
        #     return imut_state

    def blow_bomber(self):
        if (self.BMx == self.Bomb[1][0]) and (self.BMy == self.Bomb[1][1]):
            return True
        elif (self.BMx == self.Bomb[1][0]+1) and (self.BMy == self.Bomb[1][1]):
            return True
        elif (self.BMx == self.Bomb[1][0]-1) and (self.BMy == self.Bomb[1][1]):
            return True
        elif (self.BMx == self.Bomb[1][0]) and (self.BMy == self.Bomb[1][1]+1):
            return True
        elif (self.BMx == self.Bomb[1][0]) and (self.BMy == self.Bomb[1][1]-1):
            return True
        else:
            return False

    def blow_walls(self, mut_state):
        bombx = self.Bomb[1][0]
        bomby = self.Bomb[1][1]
        if (bombx+1, bomby) in self.Walls:
            mut_state[bombx+1][bomby] = 10
  #          self.Walls.remove(x+1, y)
        if (bombx-1, bomby) in self.Walls:
            mut_state[bombx-1][bomby] = 10
 #           self.Walls.remove(x-1, y)
        if (bombx, bomby+1) in self.Walls:
            mut_state[bombx][bomby+1] = 10
  #          self.Walls.remove(x, y+1)
        if (bombx, bomby-1) in self.Walls:
            mut_state[bombx][bomby-1] = 10
 #           self.Walls.remove(x, y-1)
        return

    def blow_mons(self, mut_state):
        bombx = self.Bomb[1][0]
        bomby = self.Bomb[1][1]
        for key, item in self.Monsters.items():
            if item in ([bombx+1, bomby],[bombx+1, bomby], [bombx, bomby+1],[bombx, bomby-1]):
                mut_state[item[0]][item[1]] = 10
                del self.Monsters[key]
        return
                # del self.Monsters[key]
            # if item == [bombx+1, bomby]:
            #     mut_state[bombx+1][bomby] = 10
#                del self.Monsters[key]
#             elif item == [bombx-1, bomby]:
#                 mut_state[bombx-1][bomby] = 10
#               del self.Monsters[key]
#             elif item == [bombx, bomby+1]:
#                 mut_state[bombx][bomby+1] = 10
 #               del self.Monsters[key]
 #            elif item == [bombx, bomby-1]:
 #                mut_state[bombx][bomby-1] = 10
 #               del self.Monsters[key]

    def man_dis(self,minx, miny, bmx, bmy , mut_state):
        U = [minx-1,miny]
        L = [minx,miny-1]
        D = [minx+1,miny]
        R = [minx,miny+1]
        minDis= self.M + self.N
        for move in (U, L , D, R):
            if not self.in_bound(move[0],move[1]):
                continue
            destination = mut_state[move[0]][move[1]]
            if destination == 18:
                return False
            elif destination == 10:
                tempDis = (abs(bmx- move[0]) + abs(bmy - move[1]))
                if tempDis <= minDis:
                    minx = move[0]
                    miny = move[1]
                    minDis = tempDis
        return [minx, miny]

    # def man_dis(self, x, y, minx, miny,  mut_state):
    #     dis = 0
    #     dest = mut_state[x-1][y]
    #     if dest == 18:
    #         return False
    #     elif dest == 10:
    #         dis = abs(self.BMx - (x-1)) + abs(self.BMy - y)
    #         minx = x-1
    #         miny = y
    #     dest = mut_state[x][y-1]
    #     if dest == 18:
    #         return False
    #     elif dest == 10:
    #         if abs(self.BMx - x) + abs(self.BMy - y-1) <= dis:
    #             minx = x
    #             miny = y-1
    #     dest = mut_state[x+1][y]
    #     if dest == 18:
    #         return False
    #     elif dest == 10:
    #         if abs(self.BMx - x+1) + abs(self.BMy - y) <= dis:
    #             minx = x+1
    #             miny = y
    #     dest = mut_state[x][y+1]
    #     if dest == 18:
    #         return False
    #     elif dest == 10:
    #         if abs(self.BMx - x) + abs(self.BMy - y+1) <= dis:
    #             minx = x
    #             miny = y+1
    #     return [minx, miny]

    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        state = node.state
        return 0
        # manhattanDistanceList = []
        # for monsterNum in self.Monsters.keys():
        #     manhattanDistanceList.append(self.monsterBomberManhattannDistance(monsterNum))
        # minMonsterBombermanDistance = min(manhattanDistanceList) #the minimum manhattan Bomberman-monster distance
        # if self.Bomb[0]:
        #     if self.BombBomberManhattanDistance() >= 2:
        #         manhattanBombDistanceList = []
        #         for monsterNum in self.Monsters.keys():
        #             manhattanBombDistanceList.append(self.monsterBombManhattanDistance(monsterNum))
        #         minMonsterBombDistance = min(manhattanBombDistanceList)  #the minimum manhattan Bomb-monster distance
        #         return (minMonsterBombDistance+2)*len(self.Monsters) #return the (minimun manhattan Bomb-Monster distance+2)*number of monsters
        #     else:
        #         BombValue = self.DecisionBomb(state) #the return value of the decisionBomb function
        #     if BombValue in (1,2,3):
        #         return BombValue
        #     elif math.isinf(BombValue):
        #         return float("infinity")
        # else:
        #     return minMonsterBombermanDistance*4 #if there is no bomb, return the (minimun manhattan Bombberman-Monster distance)*number of monsters

    def goal_test(self, state):
        """Return True if the state is a goal.
        State will be a goal only if Bomberman lives and all the monsters die"""
        self.Bomb = [False, [None, None]]
        self.Walls.clear()
        self.Monsters.clear()
        for row in range(0,self.N):
            for col in range(0,self.M):
                cell = state[row][col]
                if cell == 90:
                    self.Walls.add((row, col))
                elif cell == 18:
                    self.BMx = row
                    self.BMy = col
                elif cell in range(12,16):
                    self.Monsters.update({cell: [row, col]})
                elif cell == 80:
                    self.Bomb = [True, [row, col]]
                elif cell == 88:
                    self.Bomb = [True, [row, col]]
                    self.BMx = row
                    self.BMy = col
        # if self.BMx is not None and not bool(self.Monsters):
        if len(self.Monsters) == 0:
            return True
        else:
            return False

    def monsterBomberManhattannDistance (self, mosterNum):
        #claculate manhattan distance between a monster and bomberman
        return (abs(self.Monsters.get(mosterNum)[0] - self.BMx)+ abs(self.Monsters.get(mosterNum)[1] - self.BMy))

    def monsterBombManhattanDistance(self, monsterNum):
        #claculate manhattan distance between a monster and bomb
        return (abs(self.Bomb[1][0] - self.Monsters.get(monsterNum)[0])+ abs(self.Bomb[1][1] - self.Monsters.get(monsterNum)[1]))

    def BombBomberManhattanDistance(self):
        #claculate manhattan distance between a bomb and bomberman
        return (abs(self.Bomb[1][0] - self.BMx)+ abs(self.Bomb[1][1] - self.BMy))

    def DecisionBomb (self, state):
        #check if there is a goal state or dead end in the next steps when you already set a bomb
        if self.initial[self.Bomb[1][0]][self.Bomb[1][1]] == 88:
            successorListGen1 = self.successor(state) #list of the first generation of successors
            for successorGen1 in successorListGen1:
                successorListGen2 = self.successor(successorGen1) #list of the second generation of successors
                for successorGen2 in successorListGen2:
                    successorListGen3 = self.successor(successorGen2) #list of the third generation of successors
                    if not successorListGen3: #list is empty --> no successor
                        return float("infinity")
                    else:
                        for successorGen3 in successorListGen3: #check if one of the successor is a goal state
                            if self.goal_test(successorGen3):
                                return 3
        elif self.initial[self.Bomb[1][0]][self.Bomb[1][1]] == 80:
            if (abs(self.Bomb[1][0] - self.BMx)+ abs(self.Bomb[1][1] - self.BMy)) == 1:
                successorListGen1 = self.successor(state) #list of the first generation of successors
                for successorGen1 in successorListGen1:
                    if not successorListGen1: #list is empty --> no successor
                        return float("infinity")
                    elif self.goal_test(successorGen1): #check if one of the successor is a goal state
                        return 1
            elif (abs(self.Bomb[1][0] - self.BMx)+ abs(self.Bomb[1][1] - self.BMy)) == 2:
                successorListGen1 = self.successor(state) #list of the first generation of successors
                for successorGen1 in successorListGen1:
                    successorListGen2 = self.successor(successorGen1) #list of the second generation of successors
                    for successorGen2 in successorListGen2:
                        if not successorListGen2: #list is empty --> no successor
                            return float("infinity")
                        elif self.goal_test(successorGen2):#check if one of the successor is a goal state
                            return 2



def create_bomberman_problem(game):
    print "<<create_bomberman_problem"
    """ Create a bomberman problem, based on the description.
    game - matrix as it was described in the pdf file"""
    print "PROBLEM: "
    for row in game:
        for c in row:
            print c,
        print
    return BombermanProblem(game)