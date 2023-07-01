import pygame
import numpy as np
from datetime import datetime


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


def clockLineDraw(angle, line, height, scr, color=0xFF9F9F):
    c_line = np.eye(3) @ t_mat(CENTER[0], CENTER[1]) @ r_mat(-90) @ r_mat(angle) @ t_mat(0, -height / 2)
    rectangleDraw(c_line, line, scr, color)


hour_width = 150.
hour_height = 20.
hour_angle = 0.
minute_width = 250.
minute_height = 15.
minute_angle = 0.
second_width = 300.
second_height = 5.
second_angle = 0.

hour_line = getRectangle(hour_width, hour_height)
minute_line = getRectangle(minute_width, minute_height)
second_line = getRectangle(second_width, second_height)

pygame.init()
pygame.display.set_caption("20221133 한동국")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

done = False
while not done:
    year = datetime.today().year
    month = datetime.today().month
    day = datetime.today().day
    hour = datetime.today().hour
    minute = datetime.today().minute
    second = datetime.today().second

    c_hour = hour
    if hour >= 12:
        c_hour = hour - 12
    hour_angle = (30. * c_hour) + (30 * (minute / 60.)) + (0.5 * (second / 60.))
    minute_angle = (6. * minute) + (0.1 * second)
    second_angle = (6. * second)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True

    screen.fill(0x999999)

    pygame.draw.circle(screen, 0xFF9F9F, CENTER, 400, width=8)  # clock's outline
    pygame.draw.circle(screen, 0xFF9F9F, CENTER, 10)  # clock's center

    clockLineDraw(hour_angle, hour_line, hour_height, screen)
    clockLineDraw(minute_angle, minute_line, minute_height, screen)
    clockLineDraw(second_angle, second_line, second_height, screen)

    bell = pygame.mixer.Sound("assets/24-piano-keys/key01.mp3")
    if minute == 0 and second == 0:
        bell.play(1)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
