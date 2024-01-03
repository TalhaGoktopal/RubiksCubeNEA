from random import choice
from tqdm import tqdm
from Cube import RubiksCube
from collections import deque


class IDA_star(object):
    def __init__(self, heuristic, maxDepth = 20):
        self.maxDepth = maxDepth #The maximum amount of moves that can be serached
        self.threshold = maxDepth 
        self.minThreshold = None
        self.heuristic = heuristic #The heuristic database used to determine the best moves
        self.moves = [] #The moves to solve the cube
    
    def run(self, state):
        while True:
            status = self.search(state, 1)
            if status: return self.moves  #It checks if status retruns true - A solution is found, and returns the moves for solution
            self.moves = [] # If soluition is not found moves is empty
            self.threshold = self.minThreshold
        return []

    def search(self, state, gScore):
        #State - Represents current state of cube
        #gScore  - Represents the current distance from the start state
        cube = RubiksCube(state=state)
        
        #Checks if the cube is already solved
        if cube.solved():
            return True
        #If the number of moves applied has passed the threshold amount it returns False
        elif len(self.moves) >= self.threshold:
            return False
        
        #Used to keep track of the best moves found during the search.
        minVal = float('inf')
        bestAction = None
        
        #Goes through all the possiblee moves that can be applied to the cube and apllies one
        for a in [(r, n, d) for r in ['h', 'v', 's'] for d in [0, 1] for n in range(0,3,2)]:
            cube = RubiksCube(state=state)
            if a[0] == 'h':
                cube.moveH(a[1], a[2])
            elif a[0] == 'v':
                cube.moveV(a[1], a[2])
            elif a[0] == 's':
                cube.moveS(a[1], a[2])
           #Checks if cube is solved
            if cube.solved():
                #If the cube is now solved it appens the move to self.moves
                self.moves.append(a)
                return True
            
            cubeStr = cube.cubeString()
            #If the cube string is in the heuristic dictionary if it is it retrieves the 
            # correpondigng heuristic value else it passes self.maxdepth as default
            hScore = self.heuristic[cubeStr] if cubeStr in self.heuristic else self.maxDepth
            #Calculates fScore - the fotal cost to reach solved state from current one
            fScore = gScore + hScore
            
            if fScore < minVal:
                # If the fScore is less then min_val that means the current move has a lower cost 
                # then the previously predicted best move
                minVal = fScore
                bestAction = [(cubeStr, a)]
            elif fScore == minVal:
                #There are multiple best acitons
                if bestAction is None:
                    bestAction = [(cubeStr, a)]
                else:
                    bestAction.append((cubeStr, a))
        if bestAction is not None:
            if self.minThreshold is None or minVal < self.minThreshold:
                self.minThreshold = minVal
           
            #Chooses a random move to make from the best aciton array
            next_action = choice(bestAction)
           
            #Appends this move to self.moves
            self.moves.append(next_action[1])
            
            #Calls the search function with the new state (after move is applied) , and the new gScore (previous gScor + min_val)
            status = self.search(next_action[0], gScore + minVal)
            #If the solution has been found after the recursive function that the function retruns True
            if status: return status
        #If no solution is found the function return False
        return False
    
    

def buildHeuristic(state, actions, maxMoves=20, heuristic=None):
    #state - initial state of cube (solved cube)
    #actions - list of possible actions
    #maxMoves - maximum number of moves that can be carried of to find solution
    #heuristic - dictionary holding heuristic values for cube state
        
    #Checks if a heuristic dictionary is given
    if heuristic is None:
        heuristic = {state: 0}
    
    #que constains state and current distance
    que = [(state, 0)]
    
    #Calculates the toatl number of cube states
    nodeCount = sum([len(actions) ** (x + 1) for x in range(maxMoves + 1)])

    with tqdm(total=nodeCount, desc = 'Heuristic') as progressBar:
        while True:
            if not que:
                break
            s, d = que.pop()
            #Checks if the distance is greater then max moves to prevent excessive exploration
            if d > maxMoves:
                continue
        
            #Applies all the posssible moves to the current state of the cube
            for m in actions:
                cube = RubiksCube(state=s)
                if m[0] == 'h':
                    cube.moveH(m[1], m[2])
                elif m[0] == 'v':
                    cube.moveV(m[1], m[2])
                elif m[0] == 's':
                    cube.moveS(m[1], m[2])

                #Stores new state in mStr 
                mStr = cube.cubeString()
                #If the new state has not been visited or the new distance if less then the origianl distance for that state
                if mStr not in heuristic or heuristic[mStr] > d + 1:
                    #Sets new distance
                    heuristic[mStr] = d + 1
                #Adds the new state and new distance to the que
                que.append((mStr, d + 1))
                progressBar.update(1)
    
    return heuristic


# Pruning or avoiding parts of the search space that are unlikely to lead to a solution.
def prune_states(heuristic, pattern_database):
    #Iterates through the states and corresponding distance values in heuristic dictionary
    for state, distance in list(heuristic.items()):
        #Compares the value of the state in the pattern database and the heuristic dictionary if the 
        if state in pattern_database and pattern_database[state] < distance:
            del heuristic[state]
