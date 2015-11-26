import search
import math

ids = ["201316346", "201110376"]  # Feel your IDs worksss


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
    self.Bomb = [False, [None, None] ]
    for row in range (0,self.N):
        for col in range (0,self.M):
            cell= initial[row][col]
            if cell == 90:
                self.Walls.add((row, col))
            elif cell == 18:
                self.BMx = row
                self.BMy = col
            elif cell in range (12,16):
                self.Monsters.update({cell:[row, col]})

    def successor(self, state):
        """Given a state, return a sequence of (action, state) pairs reachable
        from this state. If there are many successors, consider an iterator
        that yields the successors one at a time, rather than building them
        all at once. Iterators will work fine within the framework."""
        suc_list = []
        for act in ['U', 'D', 'R', 'L', 'W', 'B', 'S']: #for each action, check what will be the state after we bomberman will do it/
            suc_state = suc_successor(act, state)
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
            checked_state = do_checks(self,mut_state, x, y, nx, ny)
            if not checked_state:
                return None
            return checked_state


        elif act == 'D':
            x = self.BMx
            y = self.BMy
            nx = (x+1)
            ny = y
            checked_state = do_checks(self,mut_state, x, y, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'R':
            x = self.BMx
            y = self.BMy
            nx = x
            ny = (y+1)
            checked_state = do_checks(self,mut_state, x, y, nx, ny)
            if not checked_state:
                return None
            return checked_state


        elif act == 'L':
            x = self.BMx
            y = self.BMy
            nx = x
            ny = (y-1)
            checked_state = do_checks(self,mut_state, x, y, nx, ny)
            if not checked_state:
                return None
            return checked_state

        elif act == 'W':


        elif act == 'S':


        elif act == 'B':



        imut_state = (tuple(b) for b in mut_state ) #return the changed state into hashable mode
        return imut_state


    def in_bound(self, x, y): # checks if the wanted direction will end in boundaries
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

    def is_hwall(mut_state, x, y):
        if mut_state[x][y] == 99:
            return True
        return False

    def is_bomb(self, x, y):
        if self.Bomb[0] == True:
            if self.Bomb[1] == [x, y]:
                return True
        return False

    def is_empty(mut_state, x, y):
        if mut_state[x][y] == 10:
            return True
        return False

    def move_mons():
        return

    def do_checks(self, mut_state, x, y, nx, ny): ## Q: can I save mut_state and just use self.
        if not in_bound(self, nx, ny):
            return False
        if is_empty(mut_state, nx, ny):
            mut_state[nx][ny] = 18
            self.BMx = nx
            self.BMy = ny
            if mut_state[x][y] == 18:
                mut_state[x][y] = 10
            else:
                mut_state[x][y] = 80
                move_mons()
                return mut_state
        if is_mons(self, nx,ny):
            return False
##        if is_wall(self, nx,ny):
##            return False
##        if is_hwall(mut_state,nx, ny):
##            return False
##        if is_bomb(self, nx, ny):
##            return False
        else:
            move_mons()
            return mut_state






    def h(self, node):
        """ This is the heuristic. It get a node (not a state)
        and returns a goal distance estimate"""
        state = node.state
        return None

    def goal_test(self, state):
        """Return True if the state is a goal.
        State will be a goal only if Bomberman lives and all the monsters die"""
        if self.BMx is not None and not bool(self.Monsters):
            return True


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


