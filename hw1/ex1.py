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
        for row in range(0,self.N):
            for col in range(0,self.M):
                cell = initial[row][col]
                if cell == 90:
                    self.Walls.add((row, col))
                elif cell == 18:
                    self.BMx = row
                    self.BMy = col
                elif cell in range(12,16):
                    self.Monsters.update({cell: [row, col]})

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
            x = self.BMx
            y = self.BMy
            nx = (x-1)
            ny = y
            checked_state = self.do_checks(self,mut_state, x, y, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'D':
            x = self.BMx
            y = self.BMy
            nx = (x+1)
            ny = y
            checked_state = self.do_checks(self,mut_state, x, y, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'R':
            x = self.BMx
            y = self.BMy
            nx = x
            ny = (y+1)
            checked_state = self.do_checks(self,mut_state, x, y, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'L':
            x = self.BMx
            y = self.BMy
            nx = x
            ny = (y-1)
            checked_state = self.do_checks(self,mut_state, x, y, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'W':
            self.move_mons()
            imut_state = (tuple(b) for b in mut_state)
            return imut_state

        elif act == 'S':
            if self.Bomb[0]:
                return None
            else:
                self.Bomb[1] = [self.BMx, self. BMy]
                mut_state[self.BMx][self.BMy] = 88
                self.move_mons()
                imut_state = (tuple(b) for b in mut_state)
                return imut_state

        elif act == 'B':
            if not self.Bomb[0]:
                return None
            if self.blow_bomber():
                return None
            self.blow_walls(self, mut_state)
            self.blow_mons(self, mut_state)
            self.move_mons()
            imut_state = (tuple(b) for b in mut_state)
            return imut_state

    def in_bound(self, x, y):
        if 0 <= x < self.N and 0 <= y < self.M:
            return True
        return False

    def is_wall(self, x, y):
        if (x,y) in self.Walls:
            return True
        return False

    def is_mons(self, x, y):
        if [x, y] in self.Monsters.values():
            return True
        return False

    def is_hwall(self, mut_state, x, y):
        if mut_state[x][y] == 99:
            return True
        return False

    def is_bomb(self, x, y):
        if self.Bomb[0]:
            if self.Bomb[1] == [x, y]:
                return True
        return False

    def is_empty(self, mut_state, x, y):
        if mut_state[x][y] == 10:
            return True
        return False

    def move_mons(self):
        return

    def do_checks(self, mut_state, x, y, nx, ny): ## Q: can I save mut_state and just use self.
        if not self.in_bound(self, nx, ny):
            return False
        if self.is_empty(mut_state, nx, ny):
            mut_state[nx][ny] = 18
            self.BMx = nx
            self.BMy = ny
            if mut_state[x][y] == 18:
                mut_state[x][y] = 10
            else:
                mut_state[x][y] = 80
            self.move_mons()
            imut_state = (tuple(b) for b in mut_state )
            return imut_state
        else:
            self.move_mons()
            imut_state = (tuple(b) for b in mut_state )
            return imut_state

    def blow_bomber(self):
        if [self.BMx] == self.Bomb[1][0] and [self.BMy] == self.Bomb[1][1]:
            return True
        if [self.BMx] == self.Bomb[1][0]+1 and [self.BMy] == self.Bomb[1][1]:
            return True
        elif [self.BMx] == self.Bomb[1][0]-1 and [self.BMy] == self.Bomb[1][1]:
            return True
        elif [self.BMx] == self.Bomb[1][0] and [self.BMy] == self.Bomb[1][1]+1:
            return True
        elif [self.BMx] == self.Bomb[1][0] and [self.BMy] == self.Bomb[1][1]-1:
            return True
        else:
            return False

    def blow_walls(self, mut_state):
        x = self.Bomb[1][0]
        y = self.Bomb[1][1]
        if [x+1, y] in self.Walls:
            mut_state[x+1][y] = 10
            self.Walls.remove(x+1, y)
        if [x-1, y] in self.Walls:
            mut_state[x-1][y] = 10
            self.Walls.remove(x-1, y)
        if [x, y+1] in self.Walls:
            mut_state[x][y+1] = 10
            self.Walls.remove(x, y+1)
        if [x, y-1] in self.Walls:
            mut_state[x][y-1] = 10
            self.Walls.remove(x, y-1)
        return

    def blow_mons(self, mut_state):
        x = self.Bomb[1][0]
        y = self.Bomb[1][1]
        for key, item in self.Monsters.items():
            # if item in ([x+1, y],[x+1, y], [x, y+1],[x, y-1]):
            #     mut_state[item] = 10
            #     del self.Monsters[key]
            if item == [x+1, y]:
                mut_state[x+1][y] = 10
                del self.Monsters[key]
            elif item == [x+1, y]:
                mut_state[x-1][y] = 10
                del self.Monsters[key]
            elif item == [x, y+1]:
                mut_state[x][y+1] = 10
                del self.Monsters[key]
            elif item == [x, y-1]:
                mut_state[x][y-1] = 10
                del self.Monsters[key]
        return

    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        state = node.state
        manhattanDistanceList = []
        for monsterNum in self.Monsters.keys():
            manhattanDistanceList.append(self.monsterBomberManhattannDistance(monsterNum))
        minMonsterBombermanDistance = min(manhattanDistanceList) #the minimum manhattan Bomberman-monster distance
        if self.Bomb[0]:
            if self.BombBomberManhattanDistance() >= 2:
                manhattanBombDistanceList = []
                for monsterNum in self.Monsters.keys():
                    manhattanBombDistanceList.append(self.monsterBombManhattanDistance(monsterNum))
                minMonsterBombDistance = min(manhattanBombDistanceList)  #the minimum manhattan Bomb-monster distance
                return (minMonsterBombDistance+2)*len(self.Monsters) #return the (minimun manhattan Bomb-Monster distance+2)*number of monsters
            else:
                BombValue = self.DecisionBomb(state) #the return value of the decisionBomb function
            if BombValue in (1,2,3):
                return BombValue
            elif math.isinf(BombValue):
                return float("infinity")
        else:
            return minMonsterBombermanDistance*4 #if there is no bomb, return the (minimun manhattan Bombberman-Monster distance)*number of monsters

    def goal_test(self, state):
        """Return True if the state is a goal.
        State will be a goal only if Bomberman lives and all the monsters die"""
        if self.BMx is not None and not bool(self.Monsters):
            return True

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
            successorListGen1 = self.successor(self, state) #list of the first generation of successors
            for successorGen1 in successorListGen1:
                successorListGen2 = self.successor(self, successorGen1) #list of the second generation of successors
                for successorGen2 in successorListGen2:
                    successorListGen3 = self.successor(self, successorGen2) #list of the third generation of successors
                    if not successorListGen3: #list is empty --> no successor
                        return float("infinity")
                    else:
                        for successorGen3 in successorListGen3: #check if one of the successor is a goal state
                            if self.goal_test(successorGen3):
                                return 3
        elif self.initial[self.Bomb[1][0]][self.Bomb[1][1]] == 80:
            if (abs(self.Bomb[1][0] - self.BMx)+ abs(self.Bomb[1][1] - self.BMy)) == 1:
                successorListGen1 = self.successor(self, state) #list of the first generation of successors
                for successorGen1 in successorListGen1:
                    if not successorListGen1: #list is empty --> no successor
                        return float("infinity")
                    elif self.goal_test(successorGen1): #check if one of the successor is a goal state
                        return 1
            elif (abs(self.Bomb[1][0] - self.BMx)+ abs(self.Bomb[1][1] - self.BMy)) == 2:
                successorListGen1 = self.successor(self, state) #list of the first generation of successors
                for successorGen1 in successorListGen1:
                    successorListGen2 = self.successor(self, successorGen1) #list of the second generation of successors
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


