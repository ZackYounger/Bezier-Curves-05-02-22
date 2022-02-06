### Zack Younger

import pygame
from copy import deepcopy
import random


pygame.init()


clock = pygame.time.Clock()
fps_limit = 30
points = [[]]
path = []
circle_colour = (255,0,255)
background_colour = (0,0,0)
colours = [(255,0,0),(255, 165, 0),(255,255,0),(0,255,0),(0,255,255),(0,0,255),(255,0,255)]
maroon = (128,0,0)
width, height = 800 , 800
screen = pygame.display.set_mode([width, height])   
screen.fill(background_colour)
pygame.display.flip()
steps = 100
 

def animate():
    for line in range(len(points[0]) - 1):
        copiedlist = deepcopy(points[line])
        copiedlist.pop(len(points[line]) - 1)
        points.append(copiedlist)
        
    for step in range(steps + 1):
        clock.tick(fps_limit)
        percent = step/steps
        screen.fill(background_colour)
        for line in range(1,len(points[0])):
            for point in range(len(points[line])):
                points[line][point] = (points[line - 1][point][0] + (points[line - 1][point + 1][0] - points[line - 1][point][0]) * percent , points[line - 1][point][1] + (points[line - 1][point + 1][1] - points[line - 1][point][1]) * percent)
                pygame.draw.circle(screen,(colours[line] if line<len(colours) else maroon),points[line][point],10)
                pygame.draw.circle(screen,(background_colour),points[line][point],7)
                if len(points[line]) == 1:
                    path.append(points[line][point])
        for connect in range(len(points[0])):
            pygame.draw.circle(screen,(colours[0]),points[0][connect],10)
            pygame.draw.circle(screen,(background_colour),points[0][connect],7)
        
        for line,lines in enumerate(points):
            for point in range(len(lines) - 1):
                pygame.draw.line(screen,(colours[line] if line<len(colours) else maroon),points[line][point], points[line][point + 1])
        
        if step != 0:
            for i in range(1,len(path)):
                pygame.draw.line(screen,(255,255,255),path[i],path[i - 1])
                
        pygame.display.flip()


running = True
while running:
    clock.tick(fps_limit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen,(colours[0]),pos,10)
            pygame.draw.circle(screen,(background_colour),pos,7)
            points[0].append(pos)
            if len(points[0]) > 1:
                index = len(points[0]) - 1
                pygame.draw.line(screen,(colours[0]),points[0][index - 1], points[0][index])
            print(points)
            pygame.display.flip()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                animate()
                
            if event.key == pygame.K_g:
                points = [[]]
                path = []
                screen.fill(background_colour)
                pygame.display.flip()
                print("g")
                no_points = 200
                width_gap = width / no_points
                for point in range(no_points+1):
                    pos = (point*width_gap,random.randint(0,height))
                    points[0].append(pos)
                    pygame.draw.circle(screen,(colours[0]),pos,10)
                    pygame.draw.circle(screen,(background_colour),pos,7)
                    if len(points[0]) > 1:
                        index = len(points[0]) - 1
                        pygame.draw.line(screen,(colours[0]),points[0][index - 1], points[0][index])
                pygame.display.flip()
                animate()
                
            if event.key == pygame.K_r:
                    points = [[]]
                    path = []
                    screen.fill(background_colour)
                    pygame.display.flip()


pygame.quit()
