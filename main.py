from Cube import *
from cubeSolver import *
import pygame, sys, random
from pygame.locals import *
from kociemba import *
import random
import json
import os.path
from Cube import RubiksCube
from cubeSolver import IDA_star


#Creates Window
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

font = pygame.font.SysFont("Arial", 25)
font1 = pygame.font.SysFont("Arial", 16)
font2 = pygame.font.SysFont("Arial", 100)
RED =  (255, 0, 0)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
WHITE = (255,255,255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)	

MAX_MOVES = 6
NEW_HEURISTICS = False
HEURISTIC_FILE = 'heuristic.json'

# This function controls the main menu
click = False
mx, my = pygame.mouse.get_pos()

def main():
  running = True
  click = False
  scramble = 0
  while running:
    WINDOW.fill((255,255,255))
    pygame.display.set_caption('Main Menu')
    font = pygame.font.SysFont("Arial", 40)

    mx, my = pygame.mouse.get_pos()

    solver_button = pygame.Rect(300, 450, 200, 50)
    timer_button = pygame.Rect(300, 600, 200, 50)
    
    
  
    if solver_button.collidepoint((mx, my)):
      if click == True:
        solver()
    if timer_button.collidepoint((mx, my)):
      if click == True:
        timer()
   
   
    
    menuScreen = pygame.image.load(r"C:\Users\mtgok\.vscode\My Solver\static\menuScreen.png").convert_alpha()
    menuScreen = pygame.transform.scale(menuScreen, (800, 800))
    WINDOW.blit(menuScreen, (0,0))
    pygame.draw.rect(WINDOW, WHITE, solver_button)
    pygame.draw.rect(WINDOW,  WHITE, timer_button)

    text_solver = font.render("SOLVER", True, BLACK)
    WINDOW.blit(text_solver, (300, 450))
    
    text_timer = font.render("TIMER", True, BLACK)
    WINDOW.blit(text_timer, (300,600))

    click = False
    for event in pygame.event.get():
      if event.type == QUIT:
        pygame.quit()
        sys.exit()
      if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
          click = True
   
    pygame.display.update()
    fpsClock.tick(FPS)

# This function controls the solver
def solver() :
  click = False
  colourSelected = 0
  solution = ""
  solutionGenerated = False
  scrambleGenerated = False
  solutionApplied = False
  running = True
  cube = RubiksCube()

  while running :
    
    mx, my = pygame.mouse.get_pos()

    WINDOW.fill((255,255,255))
    pygame.display.set_caption('Solver')

    #Set images
    redCubie = pygame.image.load(r"C:\Users\mtgok\.vscode\My Solver\static\redCubie.png").convert_alpha()
    redCubie = pygame.transform.scale(redCubie, (40, 40))
    
    whiteCubie = pygame.image.load(r"C:\Users\mtgok\.vscode\My Solver\static\whiteCubie.png").convert_alpha()
    whiteCubie = pygame.transform.scale(whiteCubie, (40, 40))
    
    blueCubie = pygame.image.load(r"C:\Users\mtgok\.vscode\My Solver\static\blueCubie.png").convert_alpha()
    blueCubie = pygame.transform.scale(blueCubie, (40, 40))
    
    greenCubie = pygame.image.load(r"C:\Users\mtgok\.vscode\My Solver\static\greenCubie.png").convert_alpha()
    greenCubie = pygame.transform.scale(greenCubie, (40, 40))
    
    yellowCubie = pygame.image.load(r"C:\Users\mtgok\.vscode\My Solver\static\yellowCubie.png").convert_alpha()
    yellowCubie = pygame.transform.scale(yellowCubie, (40, 40))

    orangeCubie = pygame.image.load(r"C:\Users\mtgok\.vscode\My Solver\static\orangeCubie.png").convert_alpha()
    orangeCubie = pygame.transform.scale(orangeCubie, (40, 40))
    
    textMoves= font.render("Moves:", True, BLACK) 
    WINDOW.blit(textMoves, (650,260))
    
    textColours= font.render("Colours:", True, BLACK) 
    WINDOW.blit(textColours, (650,70))

    textScramble = font.render("Scramble : " + cube.scrambleString, True, BLACK)
    WINDOW.blit(textScramble, (40, 600))
    
    textSolution = font.render("Solution : " + str(solution), True, BLACK)
    WINDOW.blit(textSolution, (40, 650))
    
   

    #Draw White Face
    for i in range(0, 3):
      for j in range (0,3):
        x = 160 + ((j+1)*40)
        y = 70 + ((i+1)*40)
        match cube.whiteFace[i][j]:
          case "r":
            WINDOW.blit(redCubie,(x,y))
          case "w":
            WINDOW.blit(whiteCubie,(x,y))
          case "b" :
            WINDOW.blit(blueCubie,(x,y))
          case "g" :
            WINDOW.blit(greenCubie,(x,y))
          case "y" :
            WINDOW.blit(yellowCubie,(x,y))
          case "o" :
            WINDOW.blit(orangeCubie,(x,y))
  
    #Draw Green Face
    for i in range(0, 3):
      for j in range (0,3):
        x = 160 + ((j+1)*40)
        y = 190+ ((i+1)*40)
        match cube.greenFace[i][j]:
          case "r":
            WINDOW.blit(redCubie,(x,y))
          case "w":
            WINDOW.blit(whiteCubie,(x,y))
          case "b" :
            WINDOW.blit(blueCubie,(x,y))
          case "g" :
            WINDOW.blit(greenCubie,(x,y))
          case "y" :
            WINDOW.blit(yellowCubie,(x,y))
          case "o" :
            WINDOW.blit(orangeCubie,(x,y))
  
    #Draw Yellow Face
    for i in range(0, 3):
      for j in range (0,3):
        x = 160 + ((j+1)*40)
        y = 310 + ((i+1)*40)
        match cube.yellowFace[i][j]:
          case "r":
            WINDOW.blit(redCubie,(x,y))
          case "w":
            WINDOW.blit(whiteCubie,(x,y))
          case "b" :
            WINDOW.blit(blueCubie,(x,y))
          case "g" :
            WINDOW.blit(greenCubie,(x,y))
          case "y" :
            WINDOW.blit(yellowCubie,(x,y))
          case "o" :
            WINDOW.blit(orangeCubie,(x,y))

    #Draw Orange Face
    for i in range(0, 3):
      for j in range (0,3):
        x = 40 + ((j+1)*40)
        y = 190 + ((i+1)*40)
        match cube.orangeFace[i][j]:
          case "r":
            WINDOW.blit(redCubie,(x,y))
          case "w":
            WINDOW.blit(whiteCubie,(x,y))
          case "b" :
            WINDOW.blit(blueCubie,(x,y))
          case "g" :
            WINDOW.blit(greenCubie,(x,y))
          case "y" :
            WINDOW.blit(yellowCubie,(x,y))
          case "o" :
            WINDOW.blit(orangeCubie,(x,y))
  
    #Draw Red Face
    for i in range(0, 3):
      for j in range (0,3):
        x = 280 + ((j+1)*40)
        y = 190 + ((i+1)*40)
        match cube.redFace[i][j]:
          case "r":
            WINDOW.blit(redCubie,(x,y))
          case "w":
            WINDOW.blit(whiteCubie,(x,y))
          case "b" :
            WINDOW.blit(blueCubie,(x,y))
          case "g" :
            WINDOW.blit(greenCubie,(x,y))
          case "y" :
            WINDOW.blit(yellowCubie,(x,y))
          case "o" :
            WINDOW.blit(orangeCubie,(x,y))
  
    #Draw Blue Face
    for i in range(0, 3):
      for j in range (0,3):
        x = 400 + ((j+1)*40)
        y = 190 + ((i+1)*40)
        match cube.blueFace[i][j]:
          case "r":
            WINDOW.blit(redCubie,(x,y))
          case "w":
            WINDOW.blit(whiteCubie,(x,y))
          case "b" :
            WINDOW.blit(blueCubie,(x,y))
          case "g" :
            WINDOW.blit(greenCubie,(x,y))
          case "y" :
            WINDOW.blit(yellowCubie,(x,y))
          case "o" :
            WINDOW.blit(orangeCubie,(x,y))
    
    #Changes coulours of faces

    #Edit White Face
    for i in range(0, 9):
      if cube.hitboxWhite[i].collidepoint((mx, my)) and click and colourSelected:
          #Finds the x and y coordinate of the hitbox
          cubiePosY = cube.hitboxWhite[i].top
          cubiePosX = cube.hitboxWhite[i].left
          #Locates which element in the face is goign to be changed
          cubieI = int(((cubiePosY - 70) / 40) - 1) 
          cubieJ = int(((cubiePosX- 160) / 40) - 1) 
          cube.whiteFace[cubieI][cubieJ] = colourSelected
    
    #Edit Green Face
    for i in range(0, 9):
      if cube.hitboxGreen[i].collidepoint((mx, my)) and click and colourSelected:
          cubiePosY = cube.hitboxGreen[i].top
          cubiePosX = cube.hitboxGreen[i].left
          cubieI = int(((cubiePosY - 190) / 40) - 1)
          cubieJ = int(((cubiePosX - 160) / 40) - 1)
          cube.greenFace[cubieI][cubieJ] = colourSelected
    
    # Edit Yellow face
    for i in range(0,9):
      if cube.hitboxYellow[i].collidepoint((mx, my)) and click and colourSelected:
          cubiePosY = cube.hitboxYellow[i].top
          cubiePosX = cube.hitboxYellow[i].left
          cubieI = int(((cubiePosY - 310) / 40) - 1)
          cubieJ = int(((cubiePosX- 160) / 40) - 1)
          cube.yellowFace[cubieI][cubieJ] = colourSelected             
    
    #Edit Red face
    for i in range(0, 9):
      if cube.hitboxRed[i].collidepoint((mx, my)) and click and colourSelected:
          cubiePosY =  cube.hitboxRed[i].top
          cubiePosX = cube.hitboxRed[i].left
          cubieI = int(((cubiePosY - 190) / 40) - 1)
          cubieJ = int(((cubiePosX-280) / 40) - 1)
          cube.redFace[cubieI][cubieJ] = colourSelected
    
    #Edit Orange face
    for i in range(0, 9):
      if cube.hitboxOrange[i].collidepoint((mx, my)) and click and colourSelected:
          cubiePosY =  cube.hitboxOrange[i].top
          cubiePosX = cube.hitboxOrange[i].left
          cubieI = int(((cubiePosY - 190) / 40) - 1)
          cubieJ = int(((cubiePosX-40) / 40) - 1)
          cube.orangeFace[cubieI][cubieJ] = colourSelected
    
    #Edit Blue face
    for i in range(0, 9):
      if cube.hitboxBlue[i].collidepoint((mx, my)) and click and colourSelected:
          cubiePosY =  cube.hitboxBlue[i].top
          cubiePosX = cube.hitboxBlue[i].left
          cubieI = int(((cubiePosY - 190) / 40) - 1)
          cubieJ = int(((cubiePosX - 400) / 40) - 1)
          cube.blueFace[cubieI][cubieJ] = colourSelected
    

    # #Displays buttons
    solverButton = pygame.Rect(20, 20, 100, 40)
    pygame.draw.rect(WINDOW, BLACK, solverButton,  2)
    textSolver = font.render("SOLVER", True, BLACK)
    WINDOW.blit(textSolver, (25, 25)) 
    
    timerButton = pygame.Rect(140, 20, 100, 40)
    pygame.draw.rect(WINDOW, BLACK, timerButton,  2)
    textTimer = font.render("TIMER", True, BLACK)
    WINDOW.blit(textTimer, (155, 25)) 

    helpButton = pygame.Rect(700, 700, 70, 40)
    pygame.draw.rect(WINDOW, BLACK, helpButton,  2)
    textHelp = font.render("HELP", True, BLACK)
    WINDOW.blit(textHelp, (710, 705))
    
    scrambleButton = pygame.Rect(40, 500, 100, 30)
    pygame.draw.rect(WINDOW, BLACK, scrambleButton, 2)
    textScramble = font.render("Scramble", True, BLACK)
    WINDOW.blit(textScramble, (46,498))
    
    solveButton = pygame.Rect(150, 500, 100, 30)
    pygame.draw.rect(WINDOW, BLACK, solveButton, 2)
    textSolve = font.render("Solve", True, BLACK)
    WINDOW.blit(textSolve, (156,498))
    
    applyButton = pygame.Rect(260, 500, 100, 30)
    pygame.draw.rect(WINDOW, BLACK, applyButton, 2)
    textApply = font.render("Apply", True, BLACK)
    WINDOW.blit(textApply, (266,498))

    resetButton = pygame.Rect(370, 500, 100, 30)
    pygame.draw.rect(WINDOW, BLACK, resetButton, 2)
    textReset = font.render("Reset", True, BLACK)
    WINDOW.blit(textReset, (376, 498))
    
    clearButton = pygame.Rect(480, 500, 100, 30)
    pygame.draw.rect(WINDOW, BLACK, clearButton, 2)
    textClear = font.render("Clear", True, BLACK)
    WINDOW.blit(textClear, (486,498))
    whiteButton = pygame.Rect(650, 160, 40 ,40)
    WINDOW.blit(whiteCubie, (650,160))

    yellowButton = pygame.Rect(700, 160, 40 ,40)
    WINDOW.blit(yellowCubie, (700,160))

    blueButton = pygame.Rect(650, 210, 40 ,40)
    WINDOW.blit(blueCubie, (650,210))

    greenButton = pygame.Rect(700, 210, 40 ,40)
    WINDOW.blit(greenCubie, (700,210))

    redButton = pygame.Rect(650, 110, 40 ,40)
    WINDOW.blit(redCubie, (650,110))

    orangeButton = pygame.Rect(700, 110, 40 ,40)
    WINDOW.blit(orangeCubie, (700,110))

    Rbutton = pygame.Rect(650, 290, 40,40)
    pygame.draw.rect(WINDOW, BLACK, Rbutton, 2)
    textR = font.render("R", True, BLACK)
    WINDOW.blit(textR, (657,292))

    Lbutton = pygame.Rect(700, 290, 40,40)
    pygame.draw.rect(WINDOW, BLACK, Lbutton, 2)
    textL = font.render("L", True, BLACK)
    WINDOW.blit(textL, (709,292))

    Ubutton = pygame.Rect(650, 340, 40, 40)
    pygame.draw.rect(WINDOW, BLACK, Ubutton, 2)
    textU = font.render("U", True, BLACK)
    WINDOW.blit(textU, (657,342))

    Dbutton = pygame.Rect(700, 340, 40,40)
    pygame.draw.rect(WINDOW, BLACK, Dbutton, 2)
    textD = font.render("D", True, BLACK) 
    WINDOW.blit(textD, (709,342))

    Fbutton = pygame.Rect(650, 390, 40,40)
    pygame.draw.rect(WINDOW, BLACK, Fbutton, 2)
    textF = font.render("F", True, BLACK) 
    WINDOW.blit(textF, (667,393))

    Bbutton = pygame.Rect(700, 390, 40,40)
    pygame.draw.rect(WINDOW, BLACK, Bbutton, 2)
    textB = font.render("B", True, BLACK) 
    WINDOW.blit(textB, (709,393))
    
    xRbutton = pygame.Rect(650, 440,40,40)
    pygame.draw.rect(WINDOW, BLACK, xRbutton, 2)
    textxR = font.render("R'", True, BLACK)
    WINDOW.blit(textxR, (657,443))

    xLbutton = pygame.Rect(700, 440, 40,40)
    pygame.draw.rect(WINDOW, BLACK, xLbutton, 2)
    textxL = font.render("L'", True, BLACK)
    WINDOW.blit(textxL, (709,443))

    xUbutton = pygame.Rect(650, 490, 40, 40)
    pygame.draw.rect(WINDOW, BLACK, xUbutton, 2)
    textxU = font.render("U'", True, BLACK)
    WINDOW.blit(textxU, (657,493))

    xDbutton = pygame.Rect(700, 490, 40,40)
    pygame.draw.rect(WINDOW, BLACK, xDbutton, 2)
    textxD = font.render("D'", True, BLACK) 
    WINDOW.blit(textxD, (709,493))

    xFbutton = pygame.Rect(650, 540, 40,40)
    pygame.draw.rect(WINDOW, BLACK, xFbutton, 2)
    textxF = font.render("F'", True, BLACK)
    WINDOW.blit(textxF, (657,543))

    xBbutton = pygame.Rect(700, 540, 40,40)
    pygame.draw.rect(WINDOW, BLACK, xBbutton, 2)
    textxB = font.render("B'", True, BLACK) 
    WINDOW.blit(textxB, (709,543))

    # #Checks collisions with bottons
  
    #Help Button
    if helpButton.collidepoint((mx, my)) and click:
      helpScreen()
     

    #Scramble Button
    if scrambleButton.collidepoint((mx, my)) and click:
      #Resets cube each time to esnure scrambleString is accurate
      cube = RubiksCube(state = "wwwwwwwwwooooooooogggggggggrrrrrrrrrbbbbbbbbbyyyyyyyyy")
      cube.scramble()
      scrambleGenerated = True
      solutionGenerated= False
    
    currentState = cube.cubeStringKociemba()
    #Solve Button
    if solveButton.collidepoint((mx, my)) and click:
      if scrambleGenerated == True or currentState != "UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB":
        try: #Tests this code
          solution = solve(currentState)
        except ValueError: #If there is a ValueError cube is invalid
          solution = "Please enter a valid cube"
        else: #If no errors
          solution = solve(currentState)
          solutionGenerated = True
      else:
        solution = "Cube already solved"
      
    #Apply Button  
    if applyButton.collidepoint((mx, my)) and click:
      if solutionGenerated == True:
        solution = applySolution()
        
      else:
        solution = "Generate solution first"
    
    #Reset ButtonA
    if resetButton.collidepoint((mx, my)) and click:
      cube = RubiksCube(state = "wwwwwwwwwooooooooogggggggggrrrrrrrrrbbbbbbbbbyyyyyyyyy")
      cube.scrambleString = ""
      solution = ""
      scrambleGenerated = False
      solutionGenerated = False

    #Clear Button
    if clearButton.collidepoint((mx, my)) and click:
      cube.clear()
    
    #Timer Button
    if timerButton.collidepoint((mx, my)) and click:
      timer()
   
    #R button
    if Rbutton.collidepoint((mx, my)) and click:
      cube.R()

    #L button
    if Lbutton.collidepoint((mx, my)) and click:
      cube.L()

    #U button
    if Ubutton.collidepoint((mx, my)) and click:
      cube.U()

    #F button
    if Fbutton.collidepoint((mx, my)) and click:
      cube.F()

    #D button
    if Dbutton.collidepoint((mx, my)) and click:
      cube.D()

    #Bbutton
    if Bbutton.collidepoint((mx, my)) and click:
      cube.B()

    #xRbutton
    if xRbutton.collidepoint((mx, my)) and click:
      cube.xR()

    #xLbutton
    if xLbutton.collidepoint((mx, my)) and click:
      cube.xL()

    #xUbutton
    if xUbutton.collidepoint((mx, my)) and click:
     cube.xU()

    #xFbutton
    if xFbutton.collidepoint((mx, my)) and click:
      cube.xF()

    #xDbutton
    if xDbutton.collidepoint((mx, my)) and click:
      cube.xD()

    #xBbutton
    if xBbutton.collidepoint((mx, my)) and click:
      cube.xB()
    
    #White Button
    if whiteButton.collidepoint((mx,my)) and click :
      colourSelected = "w"
      print("w")
      
    #Yellow Button
    if yellowButton.collidepoint((mx,my)) and click :
      colourSelected = "y"
      
    #Blue Button
    if blueButton.collidepoint((mx,my)) and click :
      colourSelected = "b"
      
    #Green Button
    if greenButton.collidepoint((mx,my)) and click :
      colourSelected = "g"
      
    #Orange Button
    if orangeButton.collidepoint((mx,my)) and click :
      colourSelected = "o"
      
    #Red Button
    if redButton.collidepoint((mx,my)) and click :
      colourSelected = "r"
      
    # #Checks if valid cube is entered
    # def cubeValid():
    #   valid = False
    #   redPieces = 0
    #   bluePieces = 0
    #   whitePieces = 0
    #   yellowPieces = 0
    #   greenPieces = 0
    #   orangePieces = 0
    
    #   #Checks Red Face
    #   for i in range(0, 3):
    #     for j in range (0,3):
    #       match cube.redFace[i][j]:
    #         case "r":
    #           redPieces = redPieces + 1
    #         case "w":
    #           whitePieces = whitePieces + 1
    #         case "b" :
    #           bluePieces = bluePieces + 1
    #         case "g" :
    #           greenPieces = greenPieces + 1
    #         case "y" :
    #           yellowPieces = yellowPieces + 1
    #         case "o" :
    #           orangePieces = orangePieces + 1
    
    #   #Checks White Face
    #   for i in range(0, 3):
    #     for j in range (0,3):
    #       match cube.whiteFace[i][j]:
    #         case "r":
    #           redPieces = redPieces + 1
    #         case "w":
    #           whitePieces = whitePieces + 1
    #         case "b" :
    #           bluePieces = bluePieces + 1
    #         case "g" :
    #           greenPieces = greenPieces + 1
    #         case "y" :
    #           yellowPieces = yellowPieces + 1
    #         case "o" :
    #           orangePieces = orangePieces + 1
    
    #   #Checks Green Face
    #   for i in range(0, 3):
    #     for j in range (0,3):
    #       match cube.greenFace[i][j]:
    #         case "r":
    #           redPieces = redPieces + 1
    #         case "w":
    #           whitePieces = whitePieces + 1
    #         case "b" :
    #           bluePieces = bluePieces + 1
    #         case "g" :
    #           greenPieces = greenPieces + 1
    #         case "y" :
    #           yellowPieces = yellowPieces + 1
    #         case "o" :
    #           orangePieces = orangePieces + 1    
    
    #   #Checks Blue Face
    #   for i in range(0, 3):
    #     for j in range (0,3):
    #       match cube.blueFace[i][j]:
    #         case "r":
    #           redPieces = redPieces + 1
    #         case "w":
    #           whitePieces = whitePieces + 1
    #         case "b" :
    #           bluePieces = bluePieces + 1
    #         case "g" :
    #           greenPieces = greenPieces + 1
    #         case "y" :
    #           yellowPieces = yellowPieces + 1
    #         case "o" :
    #           orangePieces = orangePieces + 1   
    
    #   #Checks Orange Face
    #   for i in range(0, 3):
    #     for j in range (0,3):
    #       match cube.orangeFace[i][j]:
    #         case "r":
    #           redPieces = redPieces + 1
    #         case "w":
    #           whitePieces = whitePieces + 1
    #         case "b" :
    #           bluePieces = bluePieces + 1
    #         case "g" :
    #           greenPieces = greenPieces + 1
    #         case "y" :
    #           yellowPieces = yellowPieces + 1
    #         case "o" :
    #           orangePieces = orangePieces + 1    
    
    #   #Checks Yellow Face
    #   for i in range(0, 3):
    #     for j in range (0,3):
    #       match cube.yellowFace[i][j]:
    #         case "r":
    #           redPieces = redPieces + 1
    #         case "w":
    #           whitePieces = whitePieces + 1
    #         case "b" :
    #           bluePieces = bluePieces + 1
    #         case "g" :
    #           greenPieces = greenPieces + 1
    #         case "y" :
    #           yellowPieces = yellowPieces + 1
    #         case "o" :
    #           orangePieces = orangePieces + 1   
    
    #   if redPieces == 9 and bluePieces == 9 and yellowPieces == 9 and whitePieces == 9 and orangePieces == 9 and greenPieces == 9 :
    #     valid = True
    #   else:
    #     valid = False
    #   return valid
         
    
  
   
    solutionArray = solution.split()
    cubeSolved = cube.solved()
    #Applies the solution to the cube one move at a time
    def applySolution():
      applySolutionCount = 0
      solution = ""
      if cubeSolved == False:
        if applySolutionCount < len(solutionArray):
          solutionMoveString = solutionArray[0]
          solutionArray.pop(0)
          applySolutionCount += 1
          
          #Removes the first move from the displayed solution
          for i in solutionArray:
            solution = solution + " " + str( i )
          
          #Checks if the move is followed by ' or 2
          if len(solutionMoveString) > 1:
            SolutionMove = solutionMoveString[0]
            SolutionMoveState = solutionMoveString[1]
            if SolutionMoveState == "'" :
              match SolutionMove:
                case "R":
                  cube.xR()
                case "L":
                  cube.xL()
                case "F":
                  cube.xF()
                case "B":
                  cube.xB()
                case "U":
                  cube.xU()
                case "D":
                  cube.xD()
            
            elif SolutionMoveState == "2":
              match SolutionMove:
                case "R":
                  for i in range(2):
                    cube.R()
                case "L":
                  for i in range(2):
                    cube.L()
                case "F":
                  for i in range(2):
                    cube.F()
                case "B":
                  for i in range(2):
                    cube.B()
                case "U":
                  for i in range(2):
                    cube.U()
                case "D":
                  for i in range(2):
                    cube.D()

          else :
            SolutionMove = solutionMoveString[0]
            match SolutionMove:
              case "R":
                cube.R()
              case "L":
                cube.L()
              case "F":
                cube.F()
              case "B":
                cube.B()
              case "U":
                cube.U()
              case "D":
                cube.D()
      
      else:
        solution = "Cube solved"
      return solution
 
    click = False
    #Events    
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()     
      if event.type == KEYDOWN:
        if event.key == pygame.key.key_code("escape"):
          running = False
      if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
          click = True

    pygame.display.update()
    fpsClock.tick(FPS)

#This function controls the timer
def timer():
  running = True
  timed = 0
  button_press_times = []
  click = False
  
  while running :
    
    WINDOW.fill((255, 255, 255))
    pygame.display.set_caption('Timer') 

    solverButton = pygame.Rect(20, 20, 100, 40)
    pygame.draw.rect(WINDOW, BLACK, solverButton,  2)
    textSolver = font.render("SOLVER", True, BLACK)
    WINDOW.blit(textSolver, (25, 25)) 
    
    timerButton = pygame.Rect(140, 20, 100, 40)
    pygame.draw.rect(WINDOW, BLACK, timerButton,  2)
    textTimer = font.render("TIMER", True, BLACK)
    WINDOW.blit(textTimer, (155, 25)) 
   
    mx, my = pygame.mouse.get_pos()

    stopwatchScreen = pygame.Rect(20, 80, 750, 400)
    pygame.draw.rect(WINDOW, RED, stopwatchScreen)

    textInstruction1 = font.render("Press the spacebar to start the timer, you will see the screen turn green.", True, BLACK)
    WINDOW.blit(textInstruction1, (20, 500))

    textInstruction2 = font.render("Press agin to stop, the screen will turn red again", True, BLACK)
    WINDOW.blit(textInstruction2, (20, 550))
    
    if solverButton.collidepoint((mx, my)) and click:
      running = False
    
    #Events
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()     
      
      if event.type == KEYDOWN:
        if event.key == pygame.key.key_code("escape"):
          running = False
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.key.key_code("space"):
          timed += 1
          button_press_times.append(pygame.time.get_ticks()) # Addds the current time to butoon press times
      
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.key.key_code("R"):
          timed = 0
          button_press_times = [] # Will be used to claculate the difference between the two recorded times
      
      if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
          click = True

    #Ouputs data based on the amount of times space bar is pressed 
    if timed == 1:
      pygame.draw.rect(WINDOW, GREEN, stopwatchScreen)
      timer = pygame.time.get_ticks() - button_press_times[0]
      timerMinutes = timer // 60000
      if timerMinutes < 10:
        timerMinutes = "0" + str(timerMinutes)
      timerSecounds = (timer % 60000) // 1000
      if timerSecounds < 10:
        timerSecounds = "0" + str(timerSecounds)
      timerMilli = (timer % 1000) 
      minuteTimer = str(timerMinutes) + ":" + str(timerSecounds) + ":" + str(timerMilli) + ""
      textTimer = font2.render(str(minuteTimer), True, (0,0,0))
      WINDOW.blit(textTimer, (210, 200))
  
    if timed == 2:
        timer = button_press_times[1] - button_press_times[0]
        timerMinutes = timer // 60000
        if timerMinutes < 10:
          timerMinutes = "0" + str(timerMinutes)
        timerSecounds = (timer % 60000) // 1000
        if timerSecounds < 10:
          timerSecounds = "0" + str(timerSecounds)
        timerMilli = (timer % 1000) 
        minuteTimer = str(timerMinutes) + ":" + str(timerSecounds) + ":" + str(timerMilli)
        textTimer = font2.render(str(minuteTimer), True, (0,0,0))
        textTimerReset = font.render("Please press R to reset the timer before pressing the space bar again", True, (0,0,0))
        pygame.draw.rect(WINDOW, RED, stopwatchScreen)
        WINDOW.blit(textTimer, (210, 200)) 
        WINDOW.blit(textTimerReset, (20, 600))
    
    pygame.display.update()
    fpsClock.tick(FPS)

#This function controls the help screen display
def helpScreen():
  running = True
  #Loads the image to solverHelpScreen variable
  solverHelpScreen = pygame.image.load(r"C:\Users\mtgok\.vscode\My Solver\static\solverHelpScreen.png").convert_alpha()
  solverHelpScreen = pygame.transform.scale(solverHelpScreen, (780, 750))
  while running :
    pygame.display.set_caption('Help') 
    WINDOW.fill((255,255,255))
    WINDOW.blit(solverHelpScreen, (0,0))
    
    #Events
    for event in pygame.event.get() :
      if event.type == QUIT :
        pygame.quit()
        sys.exit()     
      if event.type == KEYDOWN:
        if event.key == pygame.key.key_code("escape"):
          running = False
      
    pygame.display.update()
    fpsClock.tick(FPS)


solver()
