from random import choice
from tqdm import tqdm
from Cube import *
from collections import deque
import json


class IDA_star(object):
    def __init__(self, heuristic, maxDepth = 5, IDA_mode = None):
        self.maxDepth = maxDepth #The maximum amount of moves that can be serached
        self.threshold = maxDepth 
        self.minThreshold = None
        self.heuristic = heuristic #The heuristic database used to determine the best moves
        self.moves = [] #The moves to solve the cube
        self.mode = IDA_mode
    
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
        
        #Selects cube based on mode
        if self.mode == "2x2":
            cube = miniRubiksCube(miniState = state)
        else :
            cube = RubiksCube(state = state)
        
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
        for a in ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'"]:
           #Selects cube based on mode
            if self.mode == "2x2":
                cube = miniRubiksCube(miniState = state)
            else :
                cube = RubiksCube(state = state)
            
            match a:
                case "R":
                    cube.R()
                case "L":
                    cube.L()
                case "U":
                    cube.U()
                case "D":
                    cube.D()
                case "F":
                    cube.F()
                case "B":
                    cube.B()
                case "R'":
                    cube.xR()
                case "L'":
                    cube.xL()
                case "U'":
                    cube.xU()
                case "D'":
                    cube.xD()
                case "F'":
                    cube.xF()
                case "B'":
                    cube.xB()
           
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
    
    

def buildHeuristic(state, actions, maxMoves= None, heuristic=None, Heuristic_Mode = None):
    #state - initial state of cube (solved cube)
    #actions - list of possible actions
    #maxMoves - maximum number of moves that can be carried of to find solution
    #heuristic - dictionary holding heuristic values for cube state
        
    #Checks if a heuristic dictionary is given
    if heuristic is None:
        heuristic = {state: 0}
    
    #que constains state and current distance
    que = [(state, 0)]
    visited = set()
    visited.add(state)
    
    #Calculates the toatl number of cube states
    nodeCount = sum([len(actions) ** (x + 1) for x in range(maxMoves + 1)])

    with tqdm(total=nodeCount, desc = 'Heuristic') as progressBar:
        while True:
            if not que:
                break
            currentState, distance = que.pop()
            #Checks if the distance is greater then max moves to prevent excessive exploration
            if distance > maxMoves:
                continue
        
            #Applies all the posssible moves to the current state of the cube
            for m in actions:
                
            #Selects cube based on mode
                if Heuristic_Mode == "2x2":
                    cube = miniRubiksCube(miniState = currentState)
                else:
                    cube = RubiksCube(state = currentState)
                
                match m:
                    case "R":
                        cube.R()
                    case "L":
                        cube.L()
                    case "U":
                        cube.U()
                    case "D":
                        cube.D()
                    case "F":
                        cube.F()
                    case "B":
                        cube.B()
                    case "R'":
                        cube.xR()
                    case "L'":
                        cube.xL()
                    case "U'":
                        cube.xU()
                    case "D'":
                        cube.xD()
                    case "F'":
                        cube.xF()
                    case "B'":
                        cube.xB()

                #Stores new state as mStr 
                mStr = cube.cubeString()
                #If the new state has not been visited or the new distance if less then the origianl distance for that state
                if mStr not in heuristic or heuristic[mStr] > distance + 1:
                    #Sets new distance
                    heuristic[mStr] = distance + 1
                #Adds the new state and new distance to the que
                que.append((mStr, distance + 1))
                progressBar.update(1)
    
    return heuristic

# cube = miniRubiksCube(miniState ="wwwwooooggggrrrrbbbbyyyy")
# moves = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'"]
# heuristicDatabase = buildHeuristic(cube.cubeString(), moves, maxMoves = 6, heuristic = None, Heuristic_Mode="2x2")
# with open("2x2_Heuristic.json", 'w', encoding='utf-8') as file:
#     json.dump( heuristicDatabase , file , ensure_ascii=False , indent=4)

cube = RubiksCube()
actions = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'"]

heuristicDatabase = buildHeuristic(cube.cubeString(), actions, maxMoves = 20, heuristic = None)
#Creates heurisitc databse if it does not exist
with open("3x3Heuristic.json", 'w', encoding='utf-8') as file:
    json.dump( heuristicDatabase , file , ensure_ascii = False , indent = 4)

cube.scramble()

solver = IDA_star(heuristicDatabase) # Creates a solver object that is going to be used to solve the cube
movesForSolve = solver.run(cube.cubeString())
print(movesForSolve)
