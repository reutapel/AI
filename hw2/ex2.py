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
        self.Bombx = None
        self.Bomby = None
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


    def choose_next_move(self, board, steps, reward):
        "Choose next action for Bomberman given the current state of the board."


    def monsterBomberManhattannDistance (self, row,col):
        #claculate manhattan distance between a monster and bomberman
        return (abs(row - self.BMx)+ abs(col - self.BMy))
        

    def CreatePolicy(self):
        #create the self.Policy[((1,x,y),NumMonster,monster,walls,boarders)]--> look on the + around Bomberman and define the following:
        #[0:[IsBomb, BombX, BombY], 1:number of ares with monsters(1: 1,2-3:2, 4 and up:4), 2:monsters:{1:_, 2:_, 3:_, 4:_}, 3:walls:{1:_, 2:_, 3:_, 4:_},
        # 4:boarders:{1:_, 2:_, 3:_, 4:_},]

        for IsBomb in (0,1): #if there is no bomb in the +, but there is monsters --> set a bomb
            if IsBomb == 0:
                for NumMonster in (1, 2, 4):
                    for monster in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                    {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                    {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},{1:1,2:1,3:1,4:1}]:
                            for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                        {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                                 {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]:
                                    self.Policy[((1,None,None),NumMonster,monster,walls,boarders)] = 'S'
            else:
                for NumMonster in [4]:#if there 4  monsters on the board --> blow the bomb
                    for monster in [{1:1,2:1,3:1,4:1}]:
                        for x,y in [(0,0),(-2,0),(0,-2),(2,0),(0,2),(-1,1),(-1,-1),(1,1),(1,-1),(-1,0),(0,-1),(1,0),(0,1)]:
                            for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                      {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                      {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                      {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                              {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]:
                                    self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B'

                for x,y in [(0,0)]: #when there is a bomb with bomberman in the same cell --> escape to the area you can go, if there no such area --> bomb or wait
                   for NumMonster in (1, 2):
                        if NumMonster == 1:#if there is one monster on the board --> and you can't escape --> bomb, if there are 3 monsters- check if there are more that close to you than far from you
                            for monster in [{1:1,2:0,3:0,4:0}]: #noster in zone 1:
                                for boarders in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:1,3:0,4:0}]: #there is no boarder in 3:
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:0,4:1},
                                                {1:1,2:1,3:0,4:1}, {1:0,2:0,3:0,4:0}]:#there are no wall in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [{1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]: #there is no boarder in 3 and in 2:
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0},{1:0,2:0,3:1,4:1},{1:1,2:0,3:1,4:1}]:#there are walls in 3 but not in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                    for walls in [{1:0,2:1,3:1,4:1}, {1:1,2:1,3:1,4:1}]: #there are walls in 2,3,4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckAll'
                                    for walls in [{1:0,2:1,3:1,4:0}, {1:1,2:1,3:1,4:0}]: #there are walls in 2,3 but not in 4:
                                        if boarders == {1:0,2:0,3:0,4:1}: #there is boarder in 4:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check23'
                                        elif boarders == {1:0,2:0,3:0,4:0}: #there is no boarder in 4:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [{1:1,2:1,3:0,4:0},{1:0,2:1,3:0,4:0}]:#there is no boarder in 3 but there is in 2:
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0}]: #there are walls in 3 but not in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                    for walls in [{1:0,2:0,3:1,4:1}, {1:1,2:0,3:1,4:1}]: #there are walls in 3 and 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check34'
                                for boarders in [{1:0,2:1,3:1,4:0}]: #there is boarder in 2 and 3:
                                    for walls in [{1:0,2:0,3:0,4:1}, {1:1,2:0,3:0,4:1}]:  #there are walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B'
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:0}]:#there are no walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [{1:0,2:0,3:1,4:0}]: #there is no boarder in 4,2 but there is boarder in 3:
                                    for walls in [{1:0,2:1,3:0,4:1},{1:1,2:1,3:0,4:1}]: #there is wall in 4,2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check42'
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:1,2:1,3:0,4:0}]:#there is no wall in 4 but there is wall in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [{1:0,2:0,3:1,4:1}, {1:0,2:0,3:1,4:0}]: #there is no boarder in 2 but there is boarder in 3:
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:1,2:0,3:0,4:1},{1:0,2:0,3:0,4:0}]: #there is no walls in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                for boarders in [{1:0,2:0,3:1,4:1}]: #there is no boarder in 2 but there is boarder in 3,4:
                                    for walls in [{1:1,2:1,3:0,4:0},{1:0,2:1,3:0,4:0}]: #there is walls in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check2'


                            for monster in [{1:0,2:1,3:0,4:0}]: #noster in zone 2:
                                for boarders in [{1:1,2:0,3:1,4:0}, {1:0,2:0,3:0,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}]: #there is no boarder in 4:
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0},{1:0,2:1,3:1,4:0},
                                                 {1:1,2:1,3:1,4:0},{1:0,2:0,3:0,4:0}]:#there are no wall in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:0}]: #there is no boarder in 3 and in 4:
                                    for walls in [{1:0,2:0,3:0,4:1},{1:1,2:0,3:0,4:1},{1:0,2:1,3:0,4:1}, {1:1,2:1,3:0,4:1}]:#there are walls in 4 but not in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                    for walls in [{1:1,2:0,3:1,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 1,3,4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckAll'
                                    for walls in [{1:0,2:0,3:1,4:1},{1:0,2:1,3:1,4:1}]: #there are walls in 3,4 but not in 1:
                                        if boarders == {1:1,2:0,3:0,4:0}: #there is boarder in 1:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check34'
                                        elif boarders == {1:0,2:0,3:0,4:0}: #there is no boarder in 1:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [{1:0,2:1,3:1,4:0}, {1:0,2:0,3:1,4:0}]:#there is no boarder in 4 but there is in 3:
                                    for walls in [{1:0,2:0,3:0,4:1},{1:0,2:1,3:0,4:1}]: #there are walls in 4 but not in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                    for walls in [{1:1,2:0,3:0,4:1},{1:1,2:1,3:0,4:1}]: #there are walls in 1 and 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check14'
                                for boarders in [{1:0,2:0,3:1,4:1}]: #there is boarder in 4 and 3:
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:1,3:0,4:0}]:  #there are walls in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check1'
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:0}]:#there are no walls in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [{1:0,2:0,3:0,4:1}]: #there is no boarder in 1,3 but there is boarder in 4:
                                    for walls in [{1:0,2:1,3:1,4:0},{1:1,2:1,3:1,4:0}]: #there is wall in 1,3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check13'
                                    for walls in [{1:0,2:1,3:1,4:0}, {1:0,2:0,3:1,4:0}]:#there is no wall in 1 but there is wall in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [{1:0,2:0,3:0,4:1}, {1:1,2:0,3:0,4:1}]: #there is no boarder in 3 but there is boarder in 4:
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:0},{1:1,2:1,3:0,4:0},{1:0,2:1,3:0,4:0}]: #there is no walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [{1:1,2:0,3:0,4:1}]: #there is no boarder in 3 but there is boarder in 1,4:
                                    for walls in [{1:0,2:0,3:1,4:0},{1:0,2:1,3:1,4:0}]: #there is walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check3'

                            for monster in [{1:0,2:0,3:1,4:0}]: #noster in zone 3:
                                for boarders in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:1,3:0,4:0}]: #there is no boarder in 1:
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},{1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                        {1:0,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:#there are no wall in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:0}]: #there is no boarder in 4 and in 1:
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:1,3:1,4:0}]:#there are walls in 1 but not in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                    for walls in [{1:1,2:1,3:1,4:1},{1:1,2:1,3:0,4:1}]: #there are walls in 1,2,4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckAll'
                                    for walls in [{1:1,2:0,3:1,4:1},{1:1,2:0,3:0,4:1}]: #there are walls in 1,4 but not in 2:
                                        if boarders == {1:0,2:1,3:0,4:0}: #there is boarder in 2:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check14'
                                        elif boarders == {1:0,2:0,3:0,4:0}: #there is no boarder in 3:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [{1:0,2:1,3:0,4:1}, {1:0,2:0,3:0,4:1}]:#there is no boarder in 1 but there is in 4:
                                    for walls in [{1:1,2:0,3:0,4:0},{1:1,2:0,3:1,4:0}]: #there are walls in 1 but not in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                    for walls in [{1:1,2:1,3:0,4:0},{1:1,2:1,3:1,4:0}]: #there are walls in 1 and 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check12'
                                for boarders in [{1:1,2:0,3:0,4:1}]: #there is boarder in 1 and 4:
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:1,3:1,4:0}]:  #there are walls in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B'
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}]:#there are no walls in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                for boarders in [{1:1,2:0,3:0,4:0}]: #there is no boarder in 4,2 but there is boarder in 1:
                                    for walls in [{1:0,2:1,3:1,4:1},{1:0,2:1,3:0,4:1}]: #there is wall in 4,2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check24'
                                    for walls in [{1:0,2:0,3:1,4:1}, {1:0,2:0,3:1,4:1}]:#there is no wall in 2 but there is wall in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                for boarders in [{1:0,2:0,3:0,4:1}, {1:1,2:0,3:0,4:1}]: #there is no boarder in 4 but there is boarder in 1:
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},{1:0,2:1,3:1,4:0},{1:0,2:0,3:1,4:0}]: #there is no walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                                for boarders in [{1:1,2:0,3:0,4:1}]: #there is no boarder in 4 but there is boarder in 1,2:
                                    for walls in [{1:0,2:0,3:1,4:1},{1:0,2:0,3:0,4:1}]: #there is walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check4'

                            for monster in [{1:0,2:0,3:0,4:1}]: #noster in zone 4:
                                for boarders in [{1:1,2:0,3:1,4:0}, {1:0,2:0,3:0,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}]: #there is no boarder in 2:
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},{1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                        {1:1,2:0,3:1,4:1},{1:0,2:0,3:0,4:0}]:#there are no wall in 2:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                                for boarders in [{1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:0}]: #there is no boarder in 1,2:
                                    for walls in [{1:0,2:1,3:0,4:0},{1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1},{1:0,2:1,3:1,4:1}]:#there are walls in 2 but not in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                    for walls in [{1:1,2:1,3:1,4:1},{1:1,2:1,3:1,4:0}]: #there are walls in 1,2,3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckAll'
                                    for walls in [{1:1,2:1,3:0,4:1},{1:1,2:1,3:0,4:0}]: #there are walls in 1,2 but not in 3:
                                        if boarders == {1:0,2:0,3:1,4:0}: #there is boarder in 3:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check12'
                                        elif boarders == {1:0,2:0,3:0,4:0}: #there is no boarder in 3:
                                            self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [{1:1,2:0,3:0,4:0}, {1:1,2:0,3:1,4:0}]:#there is no boarder in 2 but there is in 1:
                                    for walls in [{1:0,2:1,3:0,4:0},{1:0,2:1,3:0,4:1}]: #there are walls in 2 but not in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                    for walls in [{1:0,2:1,3:1,4:0},{1:0,2:1,3:1,4:1}]: #there are walls in 2 and 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check23'
                                for boarders in [{1:1,2:1,3:0,4:0}]: #there is boarder in 1,2:
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:0,2:0,3:1,4:1}]:  #there are walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check3'
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1}]:#there are no walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [{1:0,2:1,3:0,4:0}]: #there is no boarder in 1,3 but there is boarder in 2:
                                    for walls in [{1:1,2:0,3:1,4:1},{1:1,2:0,3:1,4:0}]: #there is wall in 1,3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check13'
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:0,3:0,4:1}]:#there is no wall in 3 but there is wall in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                                for boarders in [{1:0,2:1,3:0,4:0}, {1:0,2:1,3:1,4:0}]: #there is no boarder in 1 but there is boarder in 2:
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0},{1:0,2:0,3:1,4:1},{1:0,2:0,3:0,4:1}]: #there are no walls in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                                for boarders in [{1:0,2:1,3:1,4:0}]: #there is no boarder in 1 but there is boarder in 2,3:
                                    for walls in [{1:1,2:0,3:0,4:0},{1:1,2:0,3:0,4:1}]: #there are walls in 1:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'Check1'


                        if NumMonster == 2:#if there 4  monsters on the board --> blow the bomb
                            for monster in [{1:1,2:1,3:0,4:0}]: #there are monsters in 1,2
                                for boarders in [{1:0,2:0,3:1,4:1}]: #there is boarder in 3,4
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},{1:1,2:1,3:0,4:0}]: #there is no walls in 3,4 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:0,2:0,3:1,4:0}]: #there is boarder in 3 but not in 4
                                    for walls in [{1:0,2:0,3:0,4:1}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:0,4:1},{1:1,2:1,3:0,4:1}]: #there are walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},{1:1,2:1,3:0,4:0}]: #there are no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(3)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there are no boarders in 3,4
                                    for walls in [{1:0,2:0,3:1,4:1}, {1:1,2:0,3:1,4:1}, {1:0,2:1,3:1,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 3,4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0}, {1:0,2:1,3:1,4:0},{1:1,2:1,3:1,4:0}]: #there are walls in 3 but not in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(5)
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1}, {1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:0,4:1},
                                                    {1:1,2:1,3:0,4:1},{1:0,2:0,3:0,4:0}]: #there are walls no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(6)
                                for boarders in [{1:0,2:0,3:0,4:1}]: #there are no boarders in 3 but there are in 4
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:1,2:1,3:0,4:0},{1:0,2:0,3:0,4:0}]: #there are walls no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(7)
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0}, {1:0,2:1,3:1,4:0},{1:1,2:1,3:1,4:0}]: #there are walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [{1:1,2:0,3:0,4:1}]: #there are monsters in 1,4
                                for boarders in [{1:0,2:1,3:1,4:0}]: #there are boarders in 3,2
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:1,2:0,3:0,4:1}]: #there is no walls in 3,2 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:0,2:0,3:1,4:0}]: #there is boarder in 3 but not in 2
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:1,2:1,3:0,4:0}, {1:0,2:1,3:0,4:1},{1:1,2:1,3:0,4:1}]: #there are walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:1,2:0,3:0,4:1}]: #there are no walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(3)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there are no boarders in 3,2
                                    for walls in [{1:0,2:1,3:1,4:0}, {1:1,2:1,3:1,4:0}, {1:0,2:1,3:1,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 3,2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0}, {1:0,2:0,3:1,4:1},{1:1,2:0,3:1,4:1}]: #there are walls in 3 but not in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(5)
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1}, {1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:0,4:1},
                                                    {1:1,2:1,3:0,4:1},{1:0,2:0,3:0,4:0}]: #there are walls no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(6)
                                for boarders in [{1:0,2:1,3:0,4:0}]: #there are no boarders in 3 but there are in 2
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1},  {1:1,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]: #there are walls no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(7)
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0}, {1:0,2:0,3:1,4:1},{1:1,2:0,3:1,4:1}]: #there are walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [{1:0,2:1,3:1,4:0}]: #there are monsters in 2,3
                                for boarders in [{1:1,2:0,3:0,4:1}]: #there is boarder in 1,4
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:1,3:0,4:0},{1:0,2:1,3:1,4:0}]: #there is no walls in 1,4 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:1,2:0,3:0,4:0}]: #there is boarder in 1 but not in 4
                                    for walls in [{1:0,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:0,4:1},{1:0,2:1,3:1,4:1}]: #there are walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:1,3:0,4:0},{1:0,2:1,3:1,4:0}]: #there are no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(3)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there are no boarders in 1,4
                                    for walls in [{1:1,2:0,3:0,4:1}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 1,4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:1,3:0,4:0},{1:1,2:1,3:1,4:0}]: #there are walls in 1 but not in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(5)
                                    for walls in [{1:0,2:0,3:1,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:0,4:1},
                                                    {1:0,2:1,3:1,4:1},{1:0,2:0,3:0,4:0}]: #there are walls no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                for boarders in [{1:0,2:0,3:0,4:1}]: #there are no boarders in 1 but there are in 4
                                    for walls in [{1:0,2:0,3:1,4:0},{1:0,2:1,3:0,4:0},{1:0,2:1,3:1,4:0},{1:0,2:0,3:0,4:0}]: #there are walls no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:1,3:0,4:0},{1:1,2:1,3:1,4:0}]: #there are walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [{1:0,2:0,3:1,4:1}]: #there are monsters in 3,4
                                for boarders in [{1:1,2:1,3:0,4:0}]: #there is boarder in 1,2
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},{1:0,2:0,3:1,4:1}]: #there is no walls in 1,2 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:1,2:0,3:0,4:0}]: #there is boarder in 1 but not in 2
                                    for walls in [{1:0,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1}, {1:0,2:1,3:0,4:0},{1:0,2:1,3:1,4:0}]: #there are walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},{1:0,2:0,3:1,4:1}]: #there are no walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(3)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there are no boarders in 1,2
                                    for walls in [{1:1,2:1,3:0,4:0}, {1:1,2:1,3:1,4:0}, {1:1,2:1,3:0,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 1,2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1},{1:1,2:0,3:1,4:1}]: #there are walls in 1 but not in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(5)
                                    for walls in [{1:0,2:0,3:1,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:0,4:1},
                                                    {1:0,2:1,3:1,4:1},{1:0,2:0,3:0,4:0}]: #there are walls no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                for boarders in [{1:0,2:1,3:0,4:0}]: #there are no boarders in 1 but there are in 2
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},  {1:0,2:0,3:1,4:1},{1:0,2:0,3:0,4:0}]: #there are no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                    for walls in [{1:1,2:0,3:1,4:1}, {1:1,2:0,3:0,4:1}, {1:1,2:0,3:0,4:0},{1:1,2:0,3:1,4:0}]: #there are walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [{1:0,2:1,3:0,4:1}]: #there are monsters in 2,4
                                for boarders in [{1:1,2:0,3:1,4:0}]: #there is boarder in 1,3
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:0,2:1,3:0,4:1}]: #there is no walls in 1,3 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:1,2:0,3:0,4:0}]: #there is boarder in 1 but not in 3
                                    for walls in [{1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:1}, {1:0,2:0,3:1,4:0},{1:0,2:1,3:1,4:0}]: #there are walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},{1:0,2:1,3:0,4:1}]: #there are no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(3)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there are no boarders in 1,3
                                    for walls in [{1:1,2:0,3:1,4:0}, {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 1,3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1},{1:1,2:1,3:0,4:1}]: #there are walls in 1 but not in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(5)
                                    for walls in [{1:0,2:0,3:1,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:0,4:1},
                                                    {1:0,2:1,3:1,4:1},{1:0,2:0,3:0,4:0}]: #there are walls no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                for boarders in [{1:0,2:0,3:1,4:0}]: #there are no boarders in 1 but there are in 3
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},  {1:0,2:1,3:0,4:1},{1:0,2:0,3:0,4:0}]: #there are no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(6)
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1},{1:1,2:1,3:0,4:1}]: #there are walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [{1:0,2:0,3:1,4:1}]: #there are monsters in 1,3
                                for boarders in [{1:0,2:1,3:0,4:1}]: #there is boarder in 4,2
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:1,2:0,3:0,4:0},{1:1,2:0,3:1,4:0}]: #there is no walls in 4,2 because there are boasrders
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:0,2:0,3:0,4:1}]: #there is boarder in 4 but not in 2
                                    for walls in [{1:1,2:1,3:0,4:0}, {1:1,2:1,3:1,4:0}, {1:0,2:1,3:0,4:0},{1:0,2:1,3:1,4:0}]: #there are walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(2)
                                    for walls in [{1:0,2:0,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:1,2:0,3:0,4:0},{1:1,2:0,3:1,4:0}]: #there are no walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(3)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there are no boarders in 1,2
                                    for walls in [{1:0,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1}, {1:1,2:1,3:0,4:1},{1:1,2:1,3:1,4:1}]: #there are walls in 2,4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(4)
                                    for walls in [{1:0,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:1,2:0,3:0,4:1},{1:1,2:0,3:1,4:1}]: #there are walls in 4 but not in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(5)
                                    for walls in [{1:0,2:0,3:1,4:0},{1:0,2:1,3:0,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:1,3:0,4:0},
                                                    {1:0,2:1,3:1,4:1},{1:0,2:0,3:0,4:0}]: #there are walls no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(6)
                                for boarders in [{1:0,2:1,3:0,4:0}]: #there are no boarders in 1 but there are in 2
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:0,4:0},  {1:1,2:0,3:1,4:0},{1:0,2:0,3:0,4:0}]: #there are no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(6)
                                    for walls in [{1:0,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:1,2:0,3:0,4:1},{1:1,2:0,3:1,4:1}]: #there are walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(8)

                            for monster in [{1:1,2:1,3:1,4:0}]: #there are monsters in 1,2,3
                                for boarders in [{1:0,2:0,3:0,4:1}]: #there is boarder in 4
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:0,2:1,3:1,4:0},
                                                    {1:1,2:1,3:1,4:0}, {1:0,2:0,3:0,4:0}]: #there can't be walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there is no boarder in 4
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:0,2:1,3:1,4:0},
                                                    {1:1,2:1,3:1,4:0}, {1:0,2:0,3:0,4:0}]:#there are no walls in 4
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R' #(2)
                                    for walls in [{1:0,2:0,3:0,4:1},{1:1,2:0,3:0,4:1}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},{1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                                    {1:1,2:1,3:1,4:1}]:#there are walls in 4:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(3)

                            for monster in [{1:1,2:1,3:0,4:1}]: #there are monsters in 1,2,4
                                for boarders in [{1:0,2:0,3:1,4:0}]: #there is boarder in 3
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:1,2:1,3:0,4:0},{1:1,2:0,3:0,4:1}, {1:0,2:1,3:0,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:0,3:0,4:0}]: #there can't be walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there is no boarder in 3
                                    for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},
                                                    {1:1,2:1,3:0,4:0},{1:1,2:0,3:0,4:1}, {1:0,2:1,3:0,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:0,3:0,4:0}]: #there are no walls in 3
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D' #(2)
                                    for walls in [{1:0,2:0,3:1,4:0}, {1:1,2:0,3:1,4:0},{1:0,2:1,3:1,4:0}, {1:0,2:0,3:1,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1},  {1:0,2:1,3:1,4:1},{1:1,2:1,3:1,4:1}]:#there are walls in 3:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(3)

                            for monster in [{1:0,2:1,3:1,4:1}]: #there are monsters in 2,3,4
                                for boarders in [{1:1,2:0,3:0,4:0}]: #there is boarder in 1
                                    for walls in [{1:0,2:0,3:1,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:0,2:1,3:1,4:0},{1:0,2:0,3:1,4:1}, {1:0,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]: #there can't be walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there is no boarder in 1
                                    for walls in [{1:0,2:0,3:1,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},
                                                    {1:0,2:1,3:1,4:0},{1:0,2:0,3:1,4:1}, {1:0,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]: #there are no walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U' #(2)
                                    for walls in [{1:1,2:0,3:0,4:0}, {1:1,2:0,3:1,4:0},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1},{1:1,2:1,3:1,4:1}]:#there are walls in 1
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(3)

                            for monster in [{1:1,2:0,3:1,4:1}]: #there are monsters in 1,3,4
                                for boarders in [{1:0,2:1,3:0,4:0}]: #there is boarder in 2
                                    for walls in [{1:0,2:0,3:1,4:0},{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:1,2:0,3:1,4:0},{1:0,2:0,3:1,4:1}, {1:1,2:0,3:0,4:1}, {1:1,2:0,3:1,4:1}, {1:0,2:0,3:0,4:0}]: #there can't be walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(1)
                                for boarders in [{1:0,2:0,3:0,4:0}]: #there is no boarder in 2
                                    for walls in [{1:0,2:0,3:1,4:0},{1:1,2:0,3:0,4:0}, {1:0,2:0,3:0,4:1},
                                                    {1:1,2:0,3:1,4:0},{1:0,2:0,3:1,4:1}, {1:1,2:0,3:0,4:1}, {1:1,2:0,3:1,4:1}, {1:0,2:0,3:0,4:0}]: #there are no walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L' #(2)
                                    for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:1,3:1,4:0},{1:1,2:1,3:0,4:0}, {1:0,2:1,3:0,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:0,2:1,3:1,4:1}, {1:1,2:1,3:0,4:1},{1:1,2:1,3:1,4:1}]:#there are walls in 2
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B' #(3)

                for x,y in [(-2,0),(0,-2),(2,0),(0,2),(-1,1),(-1,-1),(1,1),(1,-1)]: #the bomb is 2 steps from bomberman--> blow it
                    for NumMonster in [1,2,4]: #no mattar how many monsters are in the +
                        for monster in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                    {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                    {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1}]:
                            for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                        {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                                 {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'B'


                for x,y in [(-1,0),(0,-1),(1,0),(0,1)]: #the bomb is 1 step from bomberman--> go away from it if you can --> blow it if you can't escape
                    for NumMonster in [1,2]: # there is one monster
                        for monster in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1}]:
                            for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                                        {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                                        {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                                        {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                                for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                                                 {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]:
                                        self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'CheckMonsterBomb'

    def GetPolicy(self,key):
        return self.Policy.get(key)



                #             for monster in [{1:1,2:0,3:0,4:0}]:
                #                 for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:0,4:1},
                #                             {1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1},
                #                             {1:1,2:1,3:1,4:0},  {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                #                             {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                #                     for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}, {1:1,2:0,3:0,4:0}, {1:0,2:1,3:0,4:0},
                #                                     {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}, {1:0,2:0,3:0,4:0}]:
                #                         self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                #                 for walls in  [{1:0,2:0,3:1,4:0},{1:1,2:0,3:1,4:0},{1:0,2:0,3:1,4:1},{1:1,2:0,3:1,4:1}]:
                #                     for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}]:
                #                         self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'D'
                #             for monster in [{1:0,2:1,3:0,4:0}]:
                #                 for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0},{1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0},{1:0,2:1,3:1,4:0},
                #                             {1:1,2:1,3:1,4:0},{1:0,2:0,3:0,4:0}]:
                #                     for boarders in [{1:1,2:1,3:0,4:0}, {1:0,2:1,3:1,4:0}]:
                #                         self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'R'
                #             for monster in [{1:0,2:0,3:1,4:0}]:
                #                 for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                #                             {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                #                             {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                #                             {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                #                     for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}]:
                #                         self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'U'
                #             for monster in [{1:0,2:0,3:0,4:1}]:
                #                 for walls in [{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},{1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                #                             {1:0,2:1,3:1,4:1},{1:0,2:0,3:0,4:0}]:
                #                     for boarders in [{1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}]:
                #                         self.Policy[((1,x,y),NumMonster,monster,walls,boarders)] = 'L'
                #
                #         if NumMonster == 2:
                #
                #
                #
                #
                #
                # for x, y in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0), (-2, 0), (-1, -1), (-1, 1), (0, -2),(0, 2), (1, -1), (1, 1), (2, 0)]:
                #     for NumMonster in (1, 2, 4):
                #         if NumMonster == 1:
                #             for monster in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1}]:
                #                 for walls in [{1:1,2:0,3:0,4:0},{1:0,2:1,3:0,4:0}, {1:0,2:0,3:1,4:0}, {1:0,2:0,3:0,4:1},
                #                             {1:1,2:1,3:0,4:0}, {1:1,2:0,3:1,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:1,3:1,4:0}, {1:0,2:1,3:0,4:1}, {1:0,2:0,3:1,4:1},
                #                             {1:1,2:1,3:1,4:0}, {1:1,2:0,3:1,4:1}, {1:1,2:1,3:0,4:1}, {1:0,2:1,3:1,4:1},
                #                             {1:1,2:1,3:1,4:1}, {1:0,2:0,3:0,4:0}]:
                #                     for boarders in [{1:1,2:1,3:0,4:0}, {1:1,2:0,3:0,4:1}, {1:0,2:0,3:1,4:1}, {1:0,2:1,3:1,4:0}]:

