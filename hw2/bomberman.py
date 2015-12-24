import random
import time

class Game:    
    """Game class --- presents a Bomberman game played for given number of steps."""
    
    def __init__(self, steps, board):
        """Initialize the Game class.       
        steps - represents the number of steps the game is run 
        board - the initial state of the board

        Magic numbers for monsters and Bomberman are: 
        2 - Moster, 8 - Bomberman;
        Other stuff:
        90 - removable wall, 99 - solid wall, 80 - bomb, 10 - empty cell. 
        """

        self.steps = steps
        self.init = list(list(row) for row in board)
        
        self.actions = ('L', 'D', 'R', 'U', 'W', 'S', 'B') 
        self.apl_dict = dict(zip(self.actions,((-1, 0), (0, 1), (1, 0), (0, -1), (0, 0))))
        
        
    def set_locations(self):
        self.locations = dict.fromkeys((8, 80))
        self.locations[2] = set()
        for j, row in enumerate(self.init):
            for i, square in enumerate(row):
                what_is, who_is = divmod(square, 10)
                if who_is == 2:
                    self.locations[who_is].add((i, j))
                elif who_is == 8:
                    self.locations[who_is] = i, j
                if what_is == 8:
                    self.locations[80] = i, j
           
        if not self.locations[8]:
            print "Where is the Bbomberman?"
            self.done = True
           
    def reset(self):
        """Resets the board and monster locations to the initial state."""
        self.done = False
        self.board = [row[:] for row in self.init]
        self.set_locations()

    def there_is_cell(self, move):
        if 0 <= move[0] < len(self.init[0]) and 0 <= move[1] < len(self.init):
            return True
        return False
    

    def move_bomberman(self, act):
        if act not in self.actions:
            return False
        
        if act == 'S':
            return self.set_bomb()
        elif act == 'B':
            return self.blowup()

        move_check = self.apl_dict[act][0] + self.locations[8][0],  self.apl_dict[act][1] + self.locations[8][1]
        
        if not self.there_is_cell(move_check):
            return False
        
        what_in_square  = self.board[move_check[1]][move_check[0]]
        
        if what_in_square not in (10, 18, 88):
            if what_in_square == 12:
                self.reward -= 10
                self.done = True
                print "Suicide by monster"
                return True
            return False

        self.board[self.locations[8][1]][self.locations[8][0]] -= 8       
        self.board[move_check[1]][move_check[0]] += 8
        self.locations[8] = move_check[0], move_check[1]
        
        return True

    def set_bomb(self):
        if self.locations[80]:
            self.print_state()
            print self.locations
            return False
        
        self.board[self.locations[8][1]][self.locations[8][0]] = 88
        self.locations[80] = self.locations[8][0], self.locations[8][1]
        self.reward -= 1
        return True

    def blowup(self):
        if not self.locations[80]:
            return False
        for x, y in [(-1, 0), (0, 1), (1, 0), (0, -1), (0, 0)]:
            blowup_cell = self.locations[80][0] + x, self.locations[80][1] + y
            
            if not self.there_is_cell(blowup_cell):
                continue
            
            cell = self.board[blowup_cell[1]][blowup_cell[0]]

            if cell == 99:
                continue
            elif cell == 12:
                self.locations[2].discard(blowup_cell)
                self.reward += 5
            elif cell in (18, 88):
                self.reward -= 10
                self.done = True

            self.board[blowup_cell[1]][blowup_cell[0]] = 10

        self.locations[80] = None
        return True

    def choose_monster_move(self, monster_location):
        min_dist = len(self.init) + len(self.init[0]) + 1
        move_g = 0, 0
        
        for x, y in sorted([(1, 0), (0, 1), (-1, 0), (0, -1)], key=lambda k: random.random()):
            move_check = monster_location[0] + x, monster_location[1] + y       
            if not self.there_is_cell(move_check):
                continue
            
            if self.board[move_check[1]][move_check[0]] in (10, 18):
                dist = (abs(move_check[0] - self.locations[8][0]) 
                        + abs(move_check[1] - self.locations[8][1]))
                if dist < min_dist:
                    min_dist = dist
                    move_g = x, y
                 
        return move_g
    
    def move_monster(self, monster_location):
        x, y = self.choose_monster_move(monster_location)

        new_monster_loc = monster_location[0] + x, monster_location[1] + y

        if self.board[new_monster_loc[1]][new_monster_loc[0]] == 18:
            self.reward -= 10
            self.done = True
        
        self.locations[2].discard(monster_location)
        self.locations[2].add(new_monster_loc)

        self.board[monster_location[1]][monster_location[0]] = 10
        self.board[new_monster_loc[1]][new_monster_loc[0]] = 12
        
        

    def move_all_monsters(self):
        for monster_location in sorted(self.locations[2], key=lambda k: random.random()):
            self.move_monster(monster_location)

    def print_state(self):
        for row in self.board:
            for c in row:
                print c,
            print
    
    def update_board(self, move):
        """Move the the Bomberman and than the monsters, in this order."""
        
        if not self.move_bomberman(move):
            self.reward -= 1

        if self.done:
            return
        elif not self.locations[2]:
            self.reward += 50
            self.done = True
        else:
            self.move_all_monsters()


    def play_game(self, policy, visualize = True):
        """Execute given policy, for a given number of steps.
        if Visualize = True, prints all states along execution.
        Returns the reward"""
        self.reward = 0
        self.done = True
        
        for i in xrange(self.steps):
            if self.done:
                self.reset()
                
            t1 = time.time()
            move = policy.choose_next_move(tuple(tuple(row) for row in self.board), self.steps - i - 1, self.reward)
            t2 = time.time()
            
            if move not in self.actions:
                print "This is wrong!"
            
            self.update_board(move)
            
            if visualize:
                print "Chosen action is", move
                print "The choice of the action took: ", t2 - t1, " seconds."
                print "Action results in state:"
                for row in self.board:
                    for c in row:
                        print c,
                    print
                               
        return self.reward

    def evaluate_policy(self, policy, times, visualize = True):
        return sum([self.play_game(policy, visualize) for i in xrange(times) ]) / (1.0 * times)
