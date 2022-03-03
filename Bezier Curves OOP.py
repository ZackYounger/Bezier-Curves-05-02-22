import pygame
from pygame import gfxdraw
from copy import deepcopy
import random
import colorsys, time, math
import ctypes
from PyProbs import Probability as pr

pygame.init()

transformations = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

clock = pygame.time.Clock()
fps_limit = 120
line_width = 6
points = [[]]
path = []
circle_colour = (255, 0, 255)
background_colour = (0, 0, 0)
width, height = 1900, 900
screen = pygame.display.set_mode([width, height])
screen.fill(background_colour)
pygame.display.flip()
steps = 200
drawing_colours = []
colour_seeds = []
death_list = []
lines = []
rotation_mode = False
max_lines = 12
manual_rotation = False


class Line:
    def __init__(self, first_curve=True, new_child=True, last_point=False, shared_point=False, original_parent=True,
                 line_width=5, decay=0.008):
        self.path = []
        self.points = [[]]
        self.drawing_colours = []
        self.colour_seeds = []
        self.line_width = line_width
        self.steps = steps
        self.step = 0
        self.decay = decay
        self.first_curve = first_curve
        self.shared_point = shared_point
        self.last_point = last_point
        self.new_child = new_child
        self.original_parent = original_parent
        self.schedule_death = False
        self.die = False
        self.new_curve()

    def new_curve(self):
        global rotation_mode, manual_rotation
        self.no_points = 5
        self.points = [[]]
        for point in range(self.no_points - 1):  # no of points in said curve
            pos = (random.randint(0, width), random.randint(0, height))

            n = random.randint(1, 4)

            if n == 1:
                pos = (random.randint(0, width / 4), random.randint(0, height))
            elif n == 2:
                pos = (random.randint(0, width), random.randint(0, height / 4))
            elif n == 3:
                pos = (random.randint(3 * width / 4, width), random.randint(0, height))
            elif n == 4:
                pos = (random.randint(0, width), random.randint(3 * height / 4, height))

            self.points[0].append(pos)

        if self.original_parent:
            self.points[0][0] = (
            (width + (width + 100) * random.randint(-1, 1)) / 2, (height + (height + 100) * random.randint(-1, 1)) / 2)

        self.points[0].append((random.randint(width / 4, width * 3 / 4), random.randint(height / 4, height * 3 / 4)))

        # rotationmode
        if rotation_mode and not self.original_parent:
            if self.new_child:
                id_list = [id(i) for i in lines]
                id_list.append(id(self))
            else:
                id_list = [id(i) for i in lines]
            theta = (2 * math.pi) / len(id_list)
            self.index = id_list.index(id(self))
            self.angle = theta * (self.index)
            for index, point in enumerate(lines[0].points[0]):
                self.points[0][index] = ((math.cos(self.angle) * (point[0] - width / 2) - math.sin(self.angle) * (
                            point[1] - height / 2)) + width / 2,
                                         (math.sin(self.angle) * (point[0] - width / 2) + math.cos(self.angle) * (
                                                     point[1] - height / 2)) + height / 2)
        # start rotation
        if (pr.Prob(1 / 4) and self.original_parent and not self.first_curve and len(lines) != 1) or manual_rotation:
            rotation_mode = not rotation_mode
            print("rotation")

        # smooth curves together
        if not self.first_curve:
            self.points[0][0] = self.last_point
            if (not self.new_child or self.original_parent):
                length = 65
                gradient = -(self.path[-1][1] - self.path[-2][1]) / (self.path[-1][0] - self.path[-2][0])
                dx = math.sqrt(length ** 2 / (gradient ** 2 + 1)) * (
                            (self.path[-1][0] - self.path[-2][0]) / abs(self.path[-1][0] - self.path[-2][0]))
                dy = math.sqrt(length ** 2 - dx ** 2) * (
                            (self.path[-1][1] - self.path[-2][1]) / abs(self.path[-1][1] - self.path[-2][1]))
                self.points[0][1] = (self.points[0][0][0] + (dx * abs(self.path[-2][0] - self.path[-1][0])),
                                     self.points[0][0][1] + (dy * abs(self.path[-2][1] - self.path[-1][1])))
            else:
                self.points[0][1] = self.shared_point

        # kill line
        if self.schedule_death:
            self.die = True
            death_list.remove(self.grave_line)

        # Raise and Nurture Child
        if len(lines) < max_lines and pr.Prob(
                (max_lines - len(lines)) / max_lines) and not self.first_curve and not self.new_child and id(
                self) not in death_list and not (self.schedule_death or self.die) and not rotation_mode:
            lines.append(Line(False, True, self.last_point, self.points[0][1], False))

        # Child tragically falls ill and will die soon
        if pr.Prob(len(lines) / max_lines) and not self.original_parent and not self.new_child and not (
                self.schedule_death or self.die) and id(self) not in death_list and not rotation_mode:
            id_list = [id(i) for i in lines]
            self.grave_line = id(self)
            attempts = 0
            close = False
            while self.grave_line == id(self) or lines[id_list.index(self.grave_line)].schedule_death or lines[
                id_list.index(self.grave_line)].die or self.grave_line in death_list:
                self.grave_line = id_list[random.randint(0, len(id_list) - 1)]
                attempts += 1
                if attempts > 5:
                    close = True
                    break
            if not close:
                self.points[0][-1] = lines[id_list.index(self.grave_line)].points[0][-1]
                self.points[0][-2] = lines[id_list.index(self.grave_line)].points[0][-2]
                death_list.append(self.grave_line)
                self.schedule_death = True

        self.last_point = self.points[0][-1]

        # child grows up and is no longer a child
        if self.first_curve:
            self.first_curve = False
        self.new_child = False

        for line in range(len(self.points[0]) - 1):
            copiedlist = deepcopy(self.points[line])
            copiedlist.pop(len(self.points[line]) - 1)
            self.points.append(copiedlist)

        manual_rotation = False

        return

    def advance_frame(self):

        # print("step")
        self.percent = self.step / self.steps
        for line in range(1, len(self.points[0])):
            for point in range(len(self.points[line])):
                self.points[line][point] = (self.points[line - 1][point][0] + (
                            self.points[line - 1][point + 1][0] - self.points[line - 1][point][0]) * self.percent,
                                            self.points[line - 1][point][1] + (self.points[line - 1][point + 1][1] -
                                                                               self.points[line - 1][point][
                                                                                   1]) * self.percent)
                if len(self.points[line]) == 1:
                    if not self.die:
                        self.path.append(self.points[line][point])

        # Setting Colours
        (r, g, b) = colorsys.hsv_to_rgb((1 / self.steps + 1) * self.step, 1, 1)
        self.colour_seeds.append(((1 / self.steps + 1) * self.step, 1))
        self.drawing_colours.append((int(255 * r), int(255 * g), int(255 * b)))

        # Updating Colours
        for index, colour in enumerate(self.colour_seeds):
            self.colour_seeds[index] = [colour[0], colour[1] - self.decay]
            (r, g, b) = colorsys.hsv_to_rgb(colour[0], 1, colour[1])
            self.drawing_colours[index] = ((int(255 * r), int(255 * g), int(255 * b)))
        if self.drawing_colours[0][1] <= 0:
            self.colour_seeds.pop(0)
            self.drawing_colours.pop(0)
            try:
                self.path.pop(0)
            except:
                pass

        if self.step != 0:
            for i in range(1, len(self.path)):
                self.mirror = False
                if self.mirror:
                    for transform in transformations:
                        pygame.draw.line(screen, self.drawing_colours[i - 1],
                                         (width / 2 - (self.path[i][0] - width / 2) * transform[0],
                                          width / 2 - (self.path[i][1] - width / 2) * transform[1]),
                                         (width / 2 - (self.path[i - 1][0] - width / 2) * transform[0],
                                          width / 2 - (self.path[i - 1][1] - width / 2) * transform[1]),
                                         self.line_width)

                        pygame.draw.line(screen, self.drawing_colours[i - 1],
                                         (width / 2 - (self.path[i][1] - width / 2) * transform[1],
                                          width / 2 - (self.path[i][0] - width / 2) * transform[0]),
                                         (width / 2 - (self.path[i - 1][1] - width / 2) * transform[1],
                                          width / 2 - (self.path[i - 1][0] - width / 2) * transform[0]),
                                         self.line_width)
                else:
                    pygame.draw.line(screen, self.drawing_colours[i - 1], self.path[i], self.path[i - 1],
                                     self.line_width)

        self.step += 1
        if self.step == self.steps:
            if self.die:
                id_list = [id(i) for i in lines]
                lines.pop(id_list.index(id(self)))
            else:
                self.step = 1
                self.new_curve()

        return


def update_screen():
    try:
        # print("a")
        for i in range(1, len(lines[0].path)):
            # print("b")
            for line in lines:
                # print("y")
                pygame.draw.line(screen, line.drawing_colours[i - 1], line.path[i], line.path[i - 1], line.line_width)
    except:
        pass


lines.append(Line())

running = True
while running:
    clock.tick(fps_limit)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = False
                while True:
                    clock.tick(fps_limit)
                    screen.fill(background_colour)
                    for x in lines:
                        x.advance_frame()

                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            quit()

                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                pause = True

                            if event.key == pygame.K_r:
                                manual_rotation = True
                    if pause:
                        break

pygame.quit()