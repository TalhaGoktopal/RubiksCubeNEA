import json
import os.path

from Cube import RubiksCube
from cubeSolver import IDA_star, buildHeuristic

SOLVER_MAX_MOVES = 20
NEW_HEURISTICS = False
HEURISTIC_DATABASE_FILE = 'heuristic.json'

cube = RubiksCube(n=3) # Creates a cube object
cube.displayCube() #Displays current cube state

print("----------------------------------------------------")
if os.path.exists(HEURISTIC_DATABASE_FILE): #Checks if the heuristic file exists
    with open(HEURISTIC_DATABASE_FILE) as databaseFile:
        heuristicDatabase = json.load(databaseFile) #Loads the file as heurisit Databse
else:
    heuristicDatabase = None

if heuristicDatabase is None or NEW_HEURISTICS is True:
    moves = [(r, n, d) for r in ['h', 'v', 's'] for d in [0, 1] for n in range(0,3,2)]
    heuristicDatabase = buildHeuristic(cube.cubeString(), moves, maxMoves = SOLVER_MAX_MOVES, heuristic = heuristicDatabase)
    #Creates heurisitc databse if it does not exist
    with open(HEURISTIC_DATABASE_FILE, 'w', encoding='utf-8') as file:
        json.dump( heuristicDatabase , databaseFile , ensure_ascii=False , indent=4)

cube.scramble() #Scrambles cube
cube.displayCube() 

print("----------------------------------------------------")

solver = IDA_star(heuristicDatabase) # Creates a solver object that is going to be used to solve the cube
movesForSolve = solver.run(cube.cubeString())

solution = ""
for m in movesForSolve: # Converts the moves in moves into the R,L,U,D,F,B format
    match m[0], m[1], m[2]:
        case "v", 2, 1: #R
            solution = solution + " R "
        case "v", 0, 0: #L
            solution = solution + " L "
        case "h", 0, 0: #U
            solution = solution +" U "
        case "h", 2, 1: #D
            solution = solution + " D "
        case "s", 2, 1: #F
            solution = solution + " F "
        case "s", 0, 0: #B
            solution = solution +" B "
        case "v", 2, 0: #R'
            solution = solution +" R' "
        case "v", 0, 1: #L'
            solution = solution +" L' "
        case "h", 0, 1: #U'
            solution = solution +" U' "
        case "h", 2, 0: #D'
            solution = solution +" D' "
        case "s", 2, 0: #F'
            solution = solution + " F' "
        case "s", 0, 1: #B'
            solution = solution + " B' "

print("Solution is: " + solution)

for m in movesForSolve: #Aples the moveForSolve to the cube
    if m[0] == 'h':
        cube.moveH(m[1], m[2])
    elif m[0] == 'v':
        cube.moveV(m[1], m[2])
    elif m[0] == 's':
        cube.moveS(m[1], m[2])
        
cube.displayCube()

