import ex1
import search
import time

def timeout_exec(func, targs=(), kwargs={}, timeout_duration=10, default=None):
    """This function will spawn a thread and run the given function
    using the args, kwargs and return the given default value if the
    timeout_duration is exceeded.
    """ 
    import threading, ctypes
    class InterruptableThread(threading.Thread):
        def __init__(self):
            threading.Thread.__init__(self)
            self.result = default
        def run(self):
            try:
                self.result = func(*targs, **kwargs)
            except Exception as e:    
                self.result = [-3, -3, e]
        def _async_raise(cls, tid, excobj):
            res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(excobj))
            if res == 0:
                raise ValueError("nonexistent thread id")
            elif res > 1:
                ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, 0)
                raise SystemError("PyThreadState_SetAsyncExc failed")

        def raise_exc(self, excobj):
            assert self.isAlive(), "thread must be started"
            for tid, tobj in threading._active.items():
                if tobj is self:
                    self._async_raise(tid, excobj)
                    return
        def terminate(self):
            self.raise_exc(SystemExit)  
            
    it = InterruptableThread()
    t1 = time.time()
    it.start()
    it.join(timeout_duration)

    print "Start Thread execution"
    try:
        while  time.time() - t1 <= timeout_duration:
            if not it.isAlive():
                return it.result
        it.terminate()
        print "Thread killed by timeout"
        return default
    except Exception as e:
        print "Thread killed by exeption"
        return it.result
    print "End Thread execution"

def check_problem(p, search_method, timeout):    
    """ Constructs a problem using ex1.create_bomberman_problem, 
    and solves it using the given search_method with the given timeout.
    Returns a list of [solution length, solution time, solution]
    (-2, -2, None) means there was a timeout
    (-3, -3, ERR) means there was some error ERR during search"""        
    
    
    t1 = time.time()
    s = timeout_exec(search_method, targs=[p], timeout_duration=timeout)
    t2 = time.time()
    
    if isinstance(s, search.Node):
        solve = s
        solution = map(lambda n: n.action, solve.path()[::-1])[1:]
        return [len(solution), t2 - t1, solution]
    elif s is None:
        return [-2, -2, None]
    else:        
        return s
    

def solve_problem(problem):
    solved = 0
         
    try:
        t_delta = time.time()
        p = ex1.create_bomberman_problem(problem)
        t_delta = time.time() - t_delta
        print "Initialization took %s seconds." %t_delta
    except Exception as e:
        print "Error creating problem: ", e
        return None
    timeout = 60 - t_delta
    result = check_problem(p, (lambda p: search.best_first_graph_search(p, p.h)), timeout)
    if type(result) == 'list' and result[1] > 0:
        result[1] += t_delta
    print "GBFS", result

    if result[2] != None:
        solved = solved + 1
    #result = check_problem(p, search.astar_search, timeout)
    #print "A*   ", result
    #result = check_problem(p, search.breadth_first_graph_search, timeout)
    #print "BFSg ", result
    #result = check_problem(p, search.breadth_first_tree_search, timeout)
    #print "BFSt ", result
    #result = check_problem(p, search.depth_first_graph_search, timeout)
    #print "DFSg ", result
    #result = check_problem(p, search.depth_first_tree_search, timeout)
    #print "DFSt ", result
    #result = check_problem(p, search.iterative_deepening_search, timeout)
    
    print "GBFS Solved ", solved

    
def main():
    print ex1.ids
    game0 = (
             (12,99,18),
             (10,99,10),
             (10,90,10),
            )
    
    game1 = (
             (12,10,10,10,15),
             (10,10,99,99,99),
             (10,10,90,10,10),
             (13,10,90,10,18)
            )
    
    game2 = (
             (18,10,90,90,14),
             (10,99,90,99,90),
             (90,90,90,90,90),
             (90,99,90,99,90),
             (90,90,90,90,13)
            )
    
    game3 = (
             (12,10,10,10,10,10,10,10,10,10,15),
             (10,99,99,99,99,99,99,99,99,99,10),
             (10,99,10,90,10,10,10,10,90,90,10),
             (10,99,90,10,90,10,10,10,10,99,10),
             (10,99,10,90,10,90,10,10,10,99,10),
             (10,99,10,10,90,10,90,10,10,99,10),
             (10,99,10,10,10,90,10,90,10,99,10),
             (10,99,10,10,10,10,90,10,90,99,10),
             (10,99,10,10,10,10,10,90,10,99,10),
             (10,99,18,10,10,10,10,10,90,99,10),
             (10,99,99,99,99,99,99,99,99,99,10),
             (13,10,10,10,10,10,10,10,10,10,14),
            )
    solve_problem(game0)
    
if __name__ == '__main__':
    main()
