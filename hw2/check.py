import bomberman
import random
import ex2
import time

def evaluate(board ,steps):    
    """Run solver function on given problem and evaluate it's effectiveness."""
    run_bomberman = bomberman.Game(steps, board) 

    t1 = time.time()
    controller = ex2.Controller(board, steps)
    t2 = time.time()
    
    print "Controller initialization took: ", t2 - t1, " seconds."
    print "The average score for the problem is:", 
    print run_bomberman.evaluate_policy(controller, 3000, visualize = False)

def main():
    """Print students id's and run evaluation on a given game"""
    print ex2.ids
    
    game0 = ((12,10,10,99,10),
             (10,10,10,90,10),
             (10,10,10,99,10),
             (10,10,10,99,10),
             (10,12,10,99,18))
    
    evaluate(game0, 1000)    


if __name__ == '__main__':
    main()
    
