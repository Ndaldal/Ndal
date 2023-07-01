import pygame
import numpy as np


WINDOW_WIDTH = 1600.
WINDOW_HEIGHT = 900.
CENTER = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)


def r_mat(degree):
    radian = np.deg2rad(degree)
    cos = np.cos(radian)
    sin = np.sin(radian)
    r = np.array([[cos, -sin, 0], [sin, cos, 0], [0, 0, 1]], dtype=float)
    return r


def t_mat(tx, ty):
    t = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype=float)
    return t


def getRectangle(width, height):
    points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=float)
    return points


def rectangleDraw(m, points, scr, color=0x000000, line=0):
    r = m[0:2, 0:2]
    t = m[0:2, 2]

    points_transformed = (r @ points.T).T + t
    pygame.draw.polygon(scr, color, points_transformed, line)


def LineDraw(first_angle, angle, line, height, scr, color=0xFF9F9F):
    c_line = np.eye(3) @ t_mat(CENTER[0], CENTER[1])\
             @ r_mat(first_angle) @ r_mat(-90) @ r_mat(angle) @ t_mat(0, -height / 2)
    rectangleDraw(c_line, line, scr, color)


width = 150.
height = 20.
angle = 0.

line = getRectangle(width, height)


pygame.init()
pygame.display.set_caption("20221133 한동국")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

done = False
while not done:
    angle += 3
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    screen.fill(0x999999)

    LineDraw(0, angle, line, height, screen, color=0x123456)
    LineDraw(90, angle, line, height, screen, color=0x789ABC)
    LineDraw(180, angle, line, height, screen, color=0x9FFF9F)
    LineDraw(270, angle, line, height, screen, color=0x9F9FFF)

    pygame.draw.circle(screen, 0xFFFFFF, CENTER, 10)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
