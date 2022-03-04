### Zack Younger

import pygame
from copy import deepcopy
import random

# change
pygame.init()

clock = pygame.time.Clock()
fps_limit = 30
points = [[]]
path = []
circle_colour = (255, 0, 255)
background_colour = (0, 0, 0)
colours = [(255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 255, 255), (0, 0, 255), (255, 0, 255)]
maroon = (128, 0, 0)
width, height = 800, 800
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
        percent = step / steps
        screen.fill(background_colour)
        for line in range(1, len(points[0])):
            for point in range(len(points[line])):
                points[line][point] = (
                round(points[line - 1][point][0] + (points[line - 1][point + 1][0] - points[line - 1][point][0]) * percent),
                round(points[line - 1][point][1] + (points[line - 1][point + 1][1] - points[line - 1][point][1]) * percent))
                if len(points[line]) == 1:
                    path.append(points[line][point])

    return path


running = True
while running:
    clock.tick(fps_limit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            pygame.draw.circle(screen, (colours[0]), pos, 10)
            pygame.draw.circle(screen, (background_colour), pos, 7)
            points[0].append(pos)
            if len(points[0]) > 1:
                index = len(points[0]) - 1
                pygame.draw.line(screen, (colours[0]), points[0][index - 1], points[0][index])
            pygame.display.flip()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                path = animate()

            if event.key == pygame.K_r:
                points = [[]]
                path = []
                screen.fill(background_colour)
                pygame.display.flip()

    for i in range(1, len(path)):
        pygame.draw.line(screen, (255, 255, 255), path[i], path[i - 1])

    pygame.display.flip()

pygame.quit()
