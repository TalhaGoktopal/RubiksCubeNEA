from random import randint, choice
import random
import pygame


class RubiksCube():
    def __init__(self, n = 3,colours = ['w', 'o', 'g', 'r', 'b', 'y'], state = "wwwwwwwwwooooooooogggggggggrrrrrrrrrbbbbbbbbbyyyyyyyyy"):
        self.colours = colours
        self.cube = [[[]]]
        self.n = 3
        for i, s in enumerate(state):
            self.cube[-1][-1].append(s) # Adds the colour to the correct location of the 3D array
            if len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) < self.n:
                self.cube[-1].append([]) # Creates a new column in the 3D array
            elif len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) == self.n and i < len(state) - 1:
                self.cube.append([[]]) # Creates a new row in the current column
    
        self.whiteFace = self.cube[0]
        self.orangeFace = self.cube[1]
        self.greenFace = self.cube[2]
        self.redFace = self.cube[3]
        self.blueFace = self.cube[4]
        self.yellowFace = self.cube[5]
        self.hitboxWhite = []
        self.hitboxOrange = []
        self.hitboxGreen = []
        self.hitboxRed = []
        self.hitboxBlue= []
        self.hitboxYellow = []

        self.scrambleString = ""
       
        #Adds white hitboxes to hitboxWhite array
        for i in range (0,3):
            for j in range (0,3):
                x = 160 + ((j+1)*40)
                y = 70 + ((i+1)*40)
                rect = pygame.Rect(x, y, 40,40)   
                self.hitboxWhite.append(rect)
        #Adds green hitboxes to hitboxGreen array
        for i in range (0,3):
            for j in range (0,3):
                x = 160 + ((j+1)*40)
                y = 190 + ((i+1)*40)
                rect = pygame.Rect(x, y, 40,40)   
                self.hitboxGreen.append(rect)
        #Adds blue hitboxes to hitboxBlue array
        for i in range (0,3):
            for j in range (0,3):
                x = 400 + ((j+1)*40)
                y = 190 + ((i+1)*40)
                rect = pygame.Rect(x, y, 40,40)   
                self.hitboxBlue.append(rect)
        #Adds orange hitboxes to hitboxOrange array
        for i in range (0,3):
            for j in range (0,3):
                x = 40 + ((j+1)*40)
                y = 190 + ((i+1)*40)
                rect = pygame.Rect(x, y, 40,40)   
                self.hitboxOrange.append(rect)
        #Adds red hitboxes to hitboxRed array
        for i in range (0,3):
            for j in range (0,3):
                x = 280 + ((j+1)*40)
                y = 190 + ((i+1)*40)
                rect = pygame.Rect(x, y, 40,40)   
                self.hitboxRed.append(rect)
        #Adds yellow hitboxes to hitboxYellow array
        for i in range (0,3):
            for j in range (0,3):
                x = 160 + ((j+1)*40)
                y = 310 + ((i+1)*40)
                rect = pygame.Rect(x, y, 40,40)   
                self.hitboxYellow.append(rect)

    def scramble(self):
        moves = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'"] #List of possible moves
        self.scrambleString  = "" #Resets scrambleString before every scramble so that it is accurate
        for i in range(20):
            m = choice(moves) # Chooses a random move from moves lsit
            match m:
                case "R":
                    self.R()
                    self.scrambleString  = self.scrambleString + " R "
                case "L":
                    self.L()
                    self.scrambleString  = self.scrambleString + " L "
                case "U":
                    self.U()
                    self.scrambleString  = self.scrambleString + " U "
                case "D":
                    self.D()
                    self.scrambleString  = self.scrambleString + " D "
                case "F":
                    self.F()
                    self.scrambleString  = self.scrambleString + " F "
                case "B":
                    self.B()
                    self.scrambleString  = self.scrambleString + " B "
                case "R'":
                    self.xR()
                    self.scrambleString  = self.scrambleString + " R'"
                case "L'":
                    self.xL()
                    self.scrambleString  = self.scrambleString + " L' "
                case "U'":
                    self.xU()
                    self.scrambleString  = self.scrambleString + " U' "
                case "D'":
                    self.xD()
                    self.scrambleString  = self.scrambleString + " D' "
                case "F'":
                    self.xF()
                    self.scrambleString  = self.scrambleString + " F' "
                case "B'":
                    self.xB()
                    self.scrambleString  = self.scrambleString + " B' "

    def clear(self):
        self.whiteFace = [["w","w","w"],["w","w","w"],["w","w","w"]]
        self.orangeFace = [["w","w","w"],["w","w","w"],["w","w","w"]]
        self.greenFace = [["w","w","w"],["w","w","w"],["w","w","w"]]
        self.redFace = [["w","w","w"],["w","w","w"],["w","w","w"]]
        self.blueFace = [["w","w","w"],["w","w","w"],["w","w","w"]]
        self.yellowFace = [["w","w","w"],["w","w","w"],["w","w","w"]] 
        return
    
    def displayCube(self):
        spacing = f'{" " * (len(str(self.cube[0][0])) + 2)}'
        l1 = '\n'.join(spacing + str(c) for c in self.cube[0])
        l2 = '\n'.join('  '.join(str(self.cube[i][j]) for i in range(1,5)) for j in range(len(self.cube[0])))
        l3 = '\n'.join(spacing + str(c) for c in self.cube[5])
        print(f'{l1}\n\n{l2}\n\n{l3}')
    
    def solved(self):
        for side in self.cube: #Iterates through all sides in the cube
            cache = [] # Used to temporarily hold colours
            cubeSolved = True 
            for row in side: # Iterates through all the rows in one side
                if len(set(row)) == 1: # Set produces all unique values, so if the row contains more than one colour 
                                        #the size would be greater than one.
                    cache.append(row[0]) # Appends the colour in that row to cache to compare it with other rows
                else:
                    cubeSolved = False # Cube is not solved as there are multipiple colours in single row.
                    break
            if cubeSolved == False:
                break
            if len(set(cache)) > 1: # If there are diffrently coloured rows on one side then cube not solved.
                cubeSolved = False
                break
        return cubeSolved # Retrurns True if cube solved, False if cube not solved

    def cubeArray(self):
        cubeArray = []
        #Reads White Face
        for i in self.whiteFace:
            for j in i:
                cubeArray.append(j)
        #Reads Orange Face
        for i in self.orangeFace:
            for j in i:
                cubeArray.append(j)
        #Reads Green Face
        for i in self.greenFace:
            for j in i:
                cubeArray.append(j)
        #Reads Red Face
        for i in self.redFace:
            for j in i:
                cubeArray.append(j)
        #Reads Blue Face
        for i in self.blueFace:
            for j in i:
                cubeArray.append(j)
        #Reads Yellow Face
        for i in self.yellowFace:
            for j in i:
                cubeArray.append(j)
 
        return cubeArray
    
    def cubeString(self):    
        return ''.join([i for r in self.cube for s in r for i in s])

    def cubeStringKociemba(self):
        stateKociemba = ""
        for i in range(3): # White Face
            for j in range(3):
                stateKociemba  = stateKociemba + str(self.whiteFace[i][j])

        for i in range(3): # Red Face
            for j in range(3):
                stateKociemba  = stateKociemba + str(self.redFace[i][j])

        for i in range(3): # Green Face
            for j in range(3):
                stateKociemba  = stateKociemba + str(self.greenFace[i][j])

        for i in range(3): # Yellow Face
            for j in range(3):
                stateKociemba  = stateKociemba + str(self.yellowFace[i][j])

        for i in range(3): # Orange Face
            for j in range(3):
                stateKociemba  = stateKociemba + str(self.orangeFace[i][j])

        for i in range(3): # Blue Face
            for j in range(3):
                stateKociemba  = stateKociemba + str(self.blueFace[i][j])
        
        cubeStateKociemba = ""
        for i in range(54): #Converts the cube string to kociemba format
            match stateKociemba[i]:
                case "r":
                    cubeStateKociemba =  cubeStateKociemba + "R"
                case "w":
                    cubeStateKociemba = cubeStateKociemba + "U"
                case "b" :
                     cubeStateKociemba = cubeStateKociemba + "B"
                case "g" :
                    cubeStateKociemba = cubeStateKociemba + "F"
                case "y" :
                    cubeStateKociemba = cubeStateKociemba + "D"
                case "o" :
                    cubeStateKociemba = cubeStateKociemba + "L"

        return cubeStateKociemba

    def moveH(self, row, direction):
        if row < len(self.cube[0]):
            if direction == 0: #Twist left
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[2][row],self.cube[3][row],self.cube[4][row],self.cube[1][row])

            elif direction == 1: #Twist right
                self.cube[1][row], self.cube[2][row], self.cube[3][row], self.cube[4][row] = (self.cube[4][row],self.cube[1][row],self.cube[2][row],self.cube[3][row])
            else:
                print('Please enter a valid direction')
                return
            #Rotates connected faces
            if direction == 0: #Twist left
                if row == 0: # Rotates white face clockwise
                    self.cube[0][0][0], self.cube[0][0][1], self.cube[0][0][2], self.cube[0][1][0],self.cube[0][1][2], self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2] = self.cube[0][2][0], self.cube[0][1][0], self.cube[0][0][0], self.cube[0][2][1], self.cube[0][0][1], self.cube[0][2][2], self.cube[0][1][2],self.cube[0][0][2]
                    
                elif row == len(self.cube[0]) - 1: # Rotates yellow face anticlockwise
                    self.cube[5][0][0], self.cube[5][0][1], self.cube[5][0][2], self.cube[5][1][0],self.cube[5][1][2], self.cube[5][2][0], self.cube[5][2][1], self.cube[5][2][2] = self.cube[5][0][2], self.cube[5][1][2], self.cube[5][2][2], self.cube[5][0][1], self.cube[5][2][1], self.cube[5][0][0], self.cube[5][1][0],self.cube[5][2][0]
                    
            
            elif direction == 1: #Twist right
                if row == 0: # Rotates white face anticlockwise
                    self.cube[0][0][0], self.cube[0][0][1], self.cube[0][0][2], self.cube[0][1][0],self.cube[0][1][2], self.cube[0][2][0], self.cube[0][2][1], self.cube[0][2][2] = self.cube[0][0][2], self.cube[0][1][2], self.cube[0][2][2], self.cube[0][0][1], self.cube[0][2][1], self.cube[0][0][0], self.cube[0][1][0],self.cube[0][2][0]
                   
                elif row == len(self.cube[0]) - 1: # Rotates yellow face clockwise
                    self.cube[5][0][0], self.cube[5][0][1], self.cube[5][0][2], self.cube[5][1][0],self.cube[5][1][2], self.cube[5][2][0], self.cube[5][2][1], self.cube[5][2][2] = self.cube[5][2][0], self.cube[5][1][0], self.cube[5][0][0], self.cube[5][2][1], self.cube[5][0][1], self.cube[5][2][2], self.cube[5][1][2],self.cube[5][0][2]
        else:       
            print('Ivalid row number')
            return

    def moveV(self, column, direction):
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0: #Twist down
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i-1][-column-1], self.cube[5][i][column] = (self.cube[4][-i-1][-column-1],self.cube[0][i][column],self.cube[5][i][column],self.cube[2][i][column])
                elif direction == 1: #Twist up
                    self.cube[0][i][column], self.cube[2][i][column], self.cube[4][-i-1][-column-1], self.cube[5][i][column] = (self.cube[2][i][column], self.cube[5][i][column], self.cube[0][i][column],self.cube[4][-i-1][-column-1])
                else:
                    print('Invalid direction number')
                    return
            
            #Rotating connected face
            if direction == 0: #Twist down
                if column == 0: #Rotates green face clockwise
                    self.cube[1][0][0], self.cube[1][0][1], self.cube[1][0][2], self.cube[1][1][0],self.cube[1][1][2], self.cube[1][2][0], self.cube[1][2][1], self.cube[1][2][2] = self.cube[1][2][0], self.cube[1][1][0], self.cube[1][0][0], self.cube[1][2][1], self.cube[1][0][1], self.cube[1][2][2], self.cube[1][1][2],self.cube[1][0][2]
                   
                elif column == len(self.cube[0]) - 1: #Rotates blue face anticlockwise
                    self.cube[3][0][0], self.cube[3][0][1], self.cube[3][0][2], self.cube[3][1][0],self.cube[3][1][2], self.cube[3][2][0], self.cube[3][2][1], self.cube[3][2][2] = self.cube[3][0][2], self.cube[3][1][2], self.cube[3][2][2], self.cube[3][0][1], self.cube[3][2][1], self.cube[3][0][0], self.cube[3][1][0],self.cube[3][2][0]
                   
            elif direction == 1: #Twist up
                if column == 0: #Rotates green face anticlockwise
                    self.cube[1][0][0], self.cube[1][0][1], self.cube[1][0][2], self.cube[1][1][0],self.cube[1][1][2], self.cube[1][2][0], self.cube[1][2][1], self.cube[1][2][2] = self.cube[1][0][2],self.cube[1][1][2], self.cube[1][2][2], self.cube[1][0][1], self.cube[1][2][1], self.cube[1][0][0], self.cube[1][1][0],self.cube[1][2][0]
                  
                elif column == len(self.cube[0]) - 1: # Rotates blue face clockwise
                    self.cube[3][0][0], self.cube[3][0][1], self.cube[3][0][2], self.cube[3][1][0],self.cube[3][1][2], self.cube[3][2][0], self.cube[3][2][1], self.cube[3][2][2] = self.cube[3][2][0], self.cube[3][1][0], self.cube[3][0][0], self.cube[3][2][1], self.cube[3][0][1], self.cube[3][2][2], self.cube[3][1][2],self.cube[3][0][2]
                    
        else:
            print('Invalid column number')
            return

    def moveS(self, column, direction):
        if column < len(self.cube[0]):
            for i in range(len(self.cube[0])):
                if direction == 0: #Twist down
                    self.cube[0][column][i], self.cube[1][-i-1][column], self.cube[3][i][-column-1], self.cube[5][-column-1][-1-i] = (self.cube[3][i][-column-1],self.cube[0][column][i],self.cube[5][-column-1][-1-i],self.cube[1][-i-1][column])
                elif direction == 1: #Twist up
                    self.cube[0][column][i], self.cube[1][-i-1][column], self.cube[3][i][-column-1], self.cube[5][-column-1][-1-i] = (self.cube[1][-i-1][column],self.cube[5][-column-1][-1-i],self.cube[0][column][i],self.cube[3][i][-column-1])
                else:
                    print('Invalid direction number')
                    return
            
            #Rotating connected faces
            if direction == 1: #Twist down
                if column == 0: #Moves blue face anticlockwise
                   self.cube[4][0][0], self.cube[4][0][1], self.cube[4][0][2], self.cube[4][1][0],self.cube[4][1][2], self.cube[4][2][0], self.cube[4][2][1], self.cube[4][2][2] = self.cube[4][0][2], self.cube[4][1][2], self.cube[4][2][2], self.cube[4][0][1], self.cube[4][2][1], self.cube[4][0][0], self.cube[4][1][0],self.cube[4][2][0]
                    
                
                elif column == len(self.cube[0]) - 1: #Moves  green clockwise
                    self.cube[2][0][0], self.cube[2][0][1], self.cube[2][0][2], self.cube[2][1][0],self.cube[2][1][2], self.cube[2][2][0], self.cube[2][2][1], self.cube[2][2][2] = self.cube[2][2][0], self.cube[2][1][0], self.cube[2][0][0], self.cube[2][2][1], self.cube[2][0][1], self.cube[2][2][2], self.cube[2][1][2],self.cube[2][0][2]
                    
            elif direction == 0: #Twist up
                if column == 0: # Moves blue face clockwise
                    self.cube[4][0][0], self.cube[4][0][1], self.cube[4][0][2], self.cube[4][1][0],self.cube[4][1][2], self.cube[4][2][0], self.cube[4][2][1], self.cube[4][2][2] = self.cube[4][2][0], self.cube[4][1][0], self.cube[4][0][0], self.cube[4][2][1], self.cube[4][0][1], self.cube[4][2][2], self.cube[4][1][2],self.cube[4][0][2]
                   
                elif column == len(self.cube[0]) - 1: # Moves green face anticlockwise
                    self.cube[2][0][0], self.cube[2][0][1], self.cube[2][0][2], self.cube[2][1][0],self.cube[2][1][2], self.cube[2][2][0], self.cube[2][2][1], self.cube[2][2][2] = self.cube[2][0][2], self.cube[2][1][2], self.cube[2][2][2], self.cube[2][0][1], self.cube[2][2][1], self.cube[2][0][0], self.cube[2][1][0],self.cube[2][2][0]
                    
        else:
            print('Invalid column number')
            return

    def R(self):
        self.moveV(2,1)
        return
    
    def L(self):
        self.moveV(0,0)
        return
    
    def U(self):
        self.moveH(0, 0)
        return

    def D(self):
        self.moveH(2, 1)
        return

    def F(self):
        self.moveS(2,1)
        return

    def B(self):
        self.moveS(0,0)
        return

    def xR(self):
        self.moveV(2,0)
        return

    def xL(self):
        self.moveV(0,1)
        return

    def xU(self):
        self.moveH(0, 1)
        return

    def xD(self):
        self.moveH(2, 0)
        return
    
    def xF(self):
        self.moveS(2,0)
        return

    def xB(self):
        self.moveS(0,1)
        return

