from random import randint, choice
import random
import kociemba
import pygame



class RubiksCube(): #Creates the 3x3 cube class
    #Contructor method to create the new object.
    def __init__(self, n = 3,colours = ['w', 'o', 'g', 'r', 'b', 'y'], 
                 state = "wwwwwwwwwooooooooogggggggggrrrrrrrrrbbbbbbbbbyyyyyyyyy"):
        self.colours = colours
        self.cube = [[[]]]
        self.n = n
        for i, s in enumerate(state):
            self.cube[-1][-1].append(s) # Adds the colour to the correct location of the 3D array
            if len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) < self.n:
                self.cube[-1].append([]) # Creates a new column in the 3D array
            elif len(self.cube[-1][-1]) == self.n and len(self.cube[-1]) == self.n and i < len(state) - 1:
                self.cube.append([[]]) # Creates a new row in the current column
    

        self.hitboxes = [[],[],[],[],[],[]] 
        self.coords_3 = [[160,70], [40, 190], [160,190], [280,190], [400, 190], [160, 310]]
        self.coords_2 = [[140, 40], [20, 160], [140, 160], [260,160], [380, 160], [140, 280]]
        self.scrambleString = ""
       
    def createHitboxes(self): #Creates the hitboxes for each cubie
        for i in range (6): # Iterates through each face
            for j in range (len(self.cube[0])): #Iterates through each row
                for z in range(len(self.cube[0])): #Ietrates through the pieces in a row
                    if len(self.cube[0]) == 3: #Checks if 3x3 cube
                        x = self.coords_3[i][0] + ((z+1)*40) #Generates X coordinate of piece
                        y = self.coords_3[i][1] + ((j+1)*40) #Generates Y coordinate of piece
                        rect = pygame.Rect(x, y, 40,40) #Creates a hitbox (rectangle) usingthe X and Y coordinates
                        self.hitboxes[i].append(rect)
                    
                    elif len(self.cube[0]) == 2 : #Checks if 2x2 cube
                        x = self.coords_2[i][0] + ((z+1)*60)
                        y = self.coords_2[i][1] + ((j+1)*60)
                        rect = pygame.Rect(x, y, 60,60)   
                        self.hitboxes[i].append(rect) 

    def scramble(self):
        moves = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'"] #List of possible moves
        #self.scrambleString  = "" #Resets scrambleString before every scramble so that it is accurate
        for i in range(20):
            m = choice(moves) # Chooses a random move from moves list 
            match m: #Applies the move (m) to the cube
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
         
    def clear(self): #Clears the cube
        for i in range(6): #Iterates through sided
            for j in range(len(self.cube[0])): #Iterates through rows
                for z in range(len(self.cube[0])): #Iterates through pieces
                    self.cube[i][j][z] = "w" 
        
    def displayCube(self):
        spacing = " " * (len(str(self.cube[0][0])) + 2)  #Calculates the spacing required in order to display the cube in a readable way
        topFace = '\n'.join(spacing + str(w) for w in self.cube[0]) #Stores the white face as a string
        middleFaces = '\n'.join('  '.join(str(self.cube[i][j]) for i in range(1,5)) for j in range(len(self.cube[0]))) #Stores the green, blue , red and orange faces
        bottomFace = '\n'.join(spacing + str(y) for y in self.cube[5]) #Stores the yellow face
        print(f'{topFace}\n\n{middleFaces}\n\n{bottomFace}') #Combines all faces in one output
    
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
    
    def cubeString(self): #Iterates through each piece in the cube and joinds it to the return string
        return ''.join([i for r in self.cube for s in r for i in s]) 
    
    def cubeStringKociemba(self): 
        cubeStringKociembaOrder = ""
        order = [0, 3, 2, 5, 1, 4] #Establishes order in which the cube faces are added to the cubeStringKociembaOrder string
        for i in range (6): #Iterates through the faces in cube
            for j in range(3): # Iterates through the rows in face (i)
                for z in range (3): #Iterates through the pieces in the row (j)
                    cubeStringKociembaOrder = cubeStringKociembaOrder + self.cube[order[i]][j][z] #Adds the value stored in that index to the string
        
        cubeStateKociemba = ""
        for i in range(54): #Iterates through all pieces
            match cubeStringKociembaOrder[i]:
                case "r": #Converts cube states to Kocimeba format
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

class miniRubiksCube(RubiksCube):
    def __init__(self, miniState ):
          super().__init__(n = 2, state = miniState)
          self.n = 2

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
                    self.cube[0][0][0], self.cube[0][0][1], self.cube[0][1][0], self.cube[0][1][1] = self.cube[0][1][0], self.cube[0][0][0], self.cube[0][1][1], self.cube[0][0][1]
                    
                elif row == len(self.cube[0]) - 1: # Rotates yellow face anticlockwise
                    self.cube[5][0][0], self.cube[5][0][1],self.cube[5][1][0],self.cube[5][1][1] = self.cube[5][0][1], self.cube[5][1][1], self.cube[5][0][0], self.cube[5][1][0]
                    
            
            elif direction == 1: #Twist right
                if row == 0: # Rotates white face anticlockwise
                    self.cube[0][0][0], self.cube[0][0][1],self.cube[0][1][0],self.cube[0][1][1] = self.cube[0][0][1], self.cube[0][1][1], self.cube[0][0][0], self.cube[0][1][0]
                    
                elif row == len(self.cube[0]) - 1: # Rotates yellow face clockwise
                    self.cube[5][0][0], self.cube[5][0][1], self.cube[5][1][0], self.cube[5][1][1] = self.cube[5][1][0], self.cube[5][0][0], self.cube[5][1][1], self.cube[5][0][1]
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
                    self.cube[1][0][0], self.cube[1][0][1],self.cube[1][1][0],self.cube[1][1][1] = self.cube[1][1][0], self.cube[1][0][0], self.cube[1][1][1], self.cube[1][0][1]
                   
                elif column == len(self.cube[0]) - 1: #Rotates blue face anticlockwise
                    self.cube[3][0][0], self.cube[3][0][1],self.cube[3][1][0],self.cube[3][1][1] = self.cube[3][0][1], self.cube[3][1][1], self.cube[3][0][0], self.cube[3][1][0]
                   
            elif direction == 1: #Twist up
                if column == 0: #Rotates green face anticlockwise
                    self.cube[1][0][0], self.cube[1][0][1],self.cube[1][1][0],self.cube[1][1][1] = self.cube[1][0][1], self.cube[1][1][1], self.cube[1][0][0], self.cube[1][1][0]
                
                elif column == len(self.cube[0]) - 1: # Rotates blue face clockwise
                    self.cube[3][0][0], self.cube[3][0][1],self.cube[3][1][0],self.cube[3][1][1] = self.cube[3][1][0], self.cube[3][0][0], self.cube[3][1][1], self.cube[3][0][1]
                    
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
                   self.cube[4][0][0], self.cube[4][0][1],self.cube[4][1][0],self.cube[4][1][1] = self.cube[4][0][1], self.cube[4][1][1], self.cube[4][0][0], self.cube[4][1][0]
                    
                elif column == len(self.cube[0]) - 1: #Moves green clockwise
                    self.cube[2][0][0], self.cube[2][0][1],self.cube[2][1][0],self.cube[2][1][1] = self.cube[2][1][0], self.cube[2][0][0], self.cube[2][1][1], self.cube[2][0][1]
                    
            elif direction == 0: #Twist up
                if column == 0: # Moves blue face clockwise
                    self.cube[4][0][0], self.cube[4][0][1],self.cube[4][1][0],self.cube[4][1][1] = self.cube[4][1][0], self.cube[4][0][0], self.cube[4][1][1], self.cube[4][0][1]
                   
                elif column == len(self.cube[0]) - 1: # Moves green face anticlockwise
                    self.cube[2][0][0], self.cube[2][0][1],self.cube[2][1][0],self.cube[2][1][1] = self.cube[2][0][1], self.cube[2][1][1], self.cube[2][0][0], self.cube[2][1][0]            
        else:
            print('Invalid column number')
            return
    
    def R(self):
        self.moveV(1,1)
        return
    
    def L(self):
        self.moveV(0,0)
        return
    
    def U(self):
        self.moveH(0, 0)
        return

    def D(self):
        self.moveH(1, 1)
        return

    def F(self):
        self.moveS(1,1)
        return

    def B(self):
        self.moveS(0,0)
        return

    def xR(self):
        self.moveV(1,0)
        return

    def xL(self):
        self.moveV(0,1)
        return

    def xU(self):
        self.moveH(0, 1)
        return

    def xD(self):
        self.moveH(1, 0)
        return
    
    def xF(self):
        self.moveS(1,0)
        return

    def xB(self):
        self.moveS(0,1)
        return
    
    def scramble(self):
        moves = ["R", "L", "U", "D", "F", "B", "R'", "L'", "U'", "D'", "F'", "B'"] #List of possible moves
        self.scrambleString  = "" #Resets scrambleString before every scramble so that it is accurate
        for i in range(4):
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

# cube = RubiksCube()
# cube.scramble()
# cube.displayCube()
# print(kociemba.solve(cube.cubeStringKociemba()))

