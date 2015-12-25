import time
import random

ids = ["201316346", "201110376"]
# aTeam
class Controller:
    "This class is a controller for a Bomberman game."
    
    def __init__(self, board, steps):
        """Initialize controller for given game board and number of steps.
        This method MUST terminate within the specified timeout."""
        self.Policy = {}
        self.BMx = None
        self.BMy = None
        self.Monsters = {}
        self.N = len(board)
        self.M = len(board[1])
        self.steps = steps
        self.LastAction = None
        for row in range(0,self.N):
            for col in range(0,self.M):
                cell = board[row][col]
                if cell == 18:
                    self.BMx = row
                    self.BMy = col
                elif cell == 12:
                    self.Monsters.update({self.monsterBomberManhattannDistance(row,col): [row, col]})
        # change mosters so you can use the key --> run number
        self.DistanceMonsterBomberman = set(sorted(self.Monsters.keys()))




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

