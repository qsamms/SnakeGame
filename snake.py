import pygame
import time
import random

display_width = 810
display_height = 600
blue = (0,0,255)
black = (0,0,0)
red = (255,0,0)
white = (255,255,255)

pygame.init()
display = pygame.display.set_mode((display_width,display_height))
pygame.display.update()
pygame.display.set_caption("Snake Game!")
font_style = pygame.font.SysFont(None,50)

clock = pygame.time.Clock()
speed = 15
snakesize = 15
display.fill(white)

def displayMessage(message,color,width,height):
    mess = font_style.render(message,True,color)
    display.blit(mess,[width,height])
    pygame.display.update()


def displaySnake(snakeList):
    for x in snakeList:
        pygame.draw.rect(display,black,[x[0],x[1],snakesize,snakesize])

def gameloop():
    display.fill(white)
    quit = False
    lost = False
    x1 = 390
    y1 = 300
    x1diff = 0
    y1diff = 0
    snakelength = 1
    snakeList = []

    foodx = random.randint(1,53) * 15
    foody = random.randint(1,39) * 15

    while not quit:

        while lost:
            displayMessage("You Lost! Play again?",red,display_width/4,display_height/4)
            displayMessage("Y for yes, N for no",red,display_width/4,display_height/4+70)
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
            
        for event in pygame.event.get():
            if(event.type==pygame.QUIT):
                quit = True
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_LEFT):
                    if(x1diff == snakesize):
                        x1diff = snakesize
                        y1diff = 0
                    else:
                        x1diff = -snakesize
                        y1diff = 0
                if(event.key == pygame.K_RIGHT):
                    if(x1diff == -snakesize):
                        x1diff = -snakesize
                        y1diff = 0
                    else:
                        x1diff = snakesize
                        y1diff = 0
                if(event.key == pygame.K_UP):
                    if(y1diff == snakesize):
                        x1diff = 0
                        y1diff = snakesize
                    else:
                        x1diff = 0
                        y1diff = -snakesize
                if(event.key == pygame.K_DOWN):
                    if(y1diff == -snakesize):
                        x1diff = 0
                        y1diff = -snakesize
                    else:
                        x1diff = 0
                        y1diff = snakesize

        if(x1 >= display_width or x1 < 0 or y1 >= display_height or y1 < 0):
            lost = True

        x1 += x1diff
        y1 += y1diff
        display.fill(white)
        pygame.draw.rect(display,red,[foodx,foody,snakesize,snakesize])
        snakeHead = []
        snakeHead.append(x1)
        snakeHead.append(y1)
        snakeList.append(snakeHead)

        if(len(snakeList) > snakelength):
            del snakeList[0]

        for x in snakeList[:-1]:
            if x == snakeHead:
                lost = True
        
        displaySnake(snakeList)
        pygame.display.update()

        if(x1 == foodx and y1 == foody):
            foodx = random.randint(1,53) * 15
            foody = random.randint(1,39) * 15
            snakelength += 1
        
        clock.tick(speed)

    pygame.quit()
    quit()

gameloop()

    