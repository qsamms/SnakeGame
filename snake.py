import pygame
import time
import random
import pickle

#reading the highscore from the highscore file
try:
    with open('highscore.dat','rb') as file:
        highscore = pickle.load(file)
except:
    highscore = 0

#some constants we'll need
display_width = 800
display_height = 600
light = (208,208,208)
dark = (190,190,190)
blue = (0,0,255)
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)
speed = 12
snakesize = 20

#initializing 
pygame.init()
pygame.mixer.init()
display = pygame.display.set_mode((display_width,display_height))
pygame.display.update()
pygame.display.set_caption("Snake Game!")
font_style = pygame.font.SysFont(None,50)
score_style = pygame.font.SysFont(None,25)
clock = pygame.time.Clock()
display.fill(white)

#functions
def checkFood(snakeList,foodx,foody):
    for x in snakeList:
        if([foodx,foody] == x):
            return False
    return True

def displayHighscore():
    highscoremess = "Highscore: " + str(highscore)
    highscoredisplay = score_style.render(highscoremess,True,white)
    display.blit(highscoredisplay,[670,10])

def displayScore(score):
    scoremessage = "Score: " + str(score)
    message = score_style.render(scoremessage,True,white)
    display.blit(message,[10,10])

def displayMessage(message,color,width,height):
    mess = font_style.render(message,True,color)
    display.blit(mess,[width,height])

def displayChart():
    display.fill(light)

    for x in range(0,40,2):
        for y in range(0,30,2):
            pygame.draw.rect(display,dark,[x*snakesize,y*snakesize,snakesize,snakesize])

    for x in range(1,40,2):
        for y in range(1,30,2):
            pygame.draw.rect(display,dark,[x*snakesize,y*snakesize,snakesize,snakesize])
    
    pygame.draw.rect(display,black,[0,0,800,40])

def displaySnake(snakeList):
    for x in snakeList:
        pygame.draw.rect(display,black,[x[0],x[1],snakesize,snakesize])

#our main function
def gameloop():
    high = highscore
    scorecount = 1
    quit = False
    lost = False
    x1 = 400
    y1 = 300
    x1diff = 0
    y1diff = 0
    snakelength = 1
    snakeList = []
    movedfromlastpress = True
    crunch = pygame.mixer.Sound('./sound/crunch.mp3')
    losesound = pygame.mixer.Sound('./sound/losingsound.mp3')

    #generating the random number for the food
    #food has to be a multiple of 20 or else its position can't 
    #fully equal that of the snake
    foodx = random.randint(0,39) * 20
    foody = random.randint(2,29) * 20
    check = checkFood([x1,y1],foodx,foody)
    while not check:
        foodx = random.randint(0,39) * 20
        foody = random.randint(2,29) * 20
        check = checkFood([x1,y1],foodx,foody)

    while not quit:
        #if user loses, ask them whether they want to play again or not
        while lost:
            displayMessage("You Lost :( Play again?",(51,153,255),display_width/4+10,display_height/3)
            displayMessage("(Y)es    (N)o",(51,153,255),display_width/4+90,display_height/3+70)
            pygame.display.update()
            for event in pygame.event.get():
                if(event.type == pygame.KEYDOWN):
                    if(event.key == pygame.QUIT):
                        quit = True
                        lost = False
                    if(event.key == pygame.K_y):
                        gameloop()
                    if(event.key == pygame.K_n):
                        lost = False
                        quit = True
            
        #just checks events for keypresses and adjusts movement of snake accordingly
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                quit = True
            if(event.type == pygame.KEYDOWN and movedfromlastpress):
                movedfromlastpress = False
                #the if and else statements in this section make sure if the snake
                #is going right you can't just immediately go left(or any opposite direction 
                #to the current one) and cross over the snake body and suddenly lose
                #because that would be a dumb and annoying mechanic, so if that happens i just keep 
                #the snake going in whatever direction it was
                if(event.key == pygame.K_LEFT or event.key == pygame.K_a):
                    if(x1diff == snakesize):
                        x1diff = snakesize
                        y1diff = 0
                    else:    
                        x1diff = -snakesize
                        y1diff = 0
                if(event.key == pygame.K_RIGHT or event.key == pygame.K_d):
                    if(x1diff == -snakesize):
                        x1diff = -snakesize
                        y1diff = 0
                    else:
                        x1diff = snakesize
                        y1diff = 0
                if(event.key == pygame.K_UP or event.key == pygame.K_w):
                    if(y1diff == snakesize):
                        x1diff = 0
                        y1diff = snakesize
                    else:
                        x1diff = 0
                        y1diff = -snakesize
                if(event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    if(y1diff == -snakesize):
                        x1diff = 0
                        y1diff = -snakesize
                    else:
                        x1diff = 0
                        y1diff = snakesize

        #we just pressed a key so we don't want any other keypresses to mess 
        #with x1 and y1 until the snake has fully been moved, so we'll set 
        #movedfromlastpress to False so no other keypresses will be read
        movedfromlastpress = False
        #if snake goes off screen player loses
        if(x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 40):
            lost = True
            pygame.mixer.Sound.play(losesound)

        x1 += x1diff
        y1 += y1diff
        displayChart()
        pygame.draw.rect(display,red,[foodx,foody,snakesize,snakesize])

        #list to store x and y coordinates for the head
        snakeHead = []
        snakeHead.append(x1)
        snakeHead.append(y1)
        #we add this to the larger snake 
        snakeList.append(snakeHead)

        #to make the snake maintain its current length while moving, 
        #we have to delete a section from the back of the snake if the length
        #gets too long
        if(len(snakeList) > snakelength):
            del snakeList[0]

        #check all of the snake sections(besides the head) and if one of 
        #them is on the same grid as the head then player loses
        for x in snakeList[:-1]:
            if x == snakeHead:
                lost = True
                pygame.mixer.Sound.play(losesound)
        
        #since we displayed the chart again above^ we have to display everything again
        #snake has finally fully moved and updated so we set movedfromlastpress true
        displayHighscore()
        displayScore(scorecount)
        displaySnake(snakeList)
        pygame.display.update()
        movedfromlastpress = True

        #checking for collision with the food
        if(x1 == foodx and y1 == foody):
            foodx = random.randint(0,39) * 20
            foody = random.randint(2,29) * 20
            check = checkFood(snakeList,foodx,foody)
            while not check:
                foodx = random.randint(0,39) * 20
                foody = random.randint(2,29) * 20
                check = checkFood(snakeList,foodx,foody)
            snakelength += 1
            scorecount += 1
            pygame.mixer.Sound.play(crunch)
        
        clock.tick(speed)

    #resets the highscore if needed and writes it to the file
    if(scorecount > high):
        high = scorecount

    with open('highscore.dat','wb') as file:
        pickle.dump(high,file)
    
    pygame.quit()
    quit()

gameloop()