import pygame
import time

display_width = 800
display_height = 600
blue = (0,0,255)
red = (255,0,0)
white = (255,255,255)
x1 = 400
y1 = 300
lost = False

pygame.init()
display = pygame.display.set_mode((display_width,display_height))
pygame.display.update()
pygame.display.set_caption("Snake Game!")
font_style = pygame.font.SysFont(None,50)
lostmessage = font_style.render("You Lost!",True,red)



x1 = 400
y1 = 300
x1diff = 0
y1diff = 0

clock = pygame.time.Clock()
speed = 30
display.fill(white)

while not lost:
    for event in pygame.event.get():
        if(event.type==pygame.QUIT):
            lost = True
        if(event.type == pygame.KEYDOWN):
            if(event.key == pygame.K_LEFT):
                x1diff = -10
                y1diff = 0
            if(event.key == pygame.K_RIGHT):
                x1diff = 10
                y1diff = 0
            if(event.key == pygame.K_UP):
                x1diff = 0
                y1diff = -10
            if(event.key == pygame.K_DOWN):
                x1diff = 0
                y1diff = 10
    
    if(x1 >= display_width or x1 < 0 or y1 >= display_height or y1 <= 0):
        lost = True

    x1 += x1diff
    y1 += y1diff
    pygame.draw.rect(display,blue,[x1,y1,10,10])
    pygame.display.update()
    clock.tick(speed)

display.blit(lostmessage,[display_width/2,display_height/2])
pygame.display.update()
time.sleep(2)
pygame.quit()
quit()     
    