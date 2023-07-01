import pygame
import numpy as np


WINDOW_WIDTH = 800.
WINDOW_HEIGHT = 800.

GREEN = (100, 200, 100)
angle1 = 0.
angle2 = 0.
angle3 = 0.

center1 = [100., 600.]



def getRectangle(width, height):
    points = np.array([[0, 0], [width, 0], [width, height], [0, height]], dtype=float)
    return points


def r_mat(degree):
    radian = np.deg2rad(degree)
    c = np.cos(radian)
    s = np.sin(radian)
    r = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return r


def t_mat(tx, ty):
    t = np.array([[1, 0, tx], [0, 1, ty], [0, 0, 1]], dtype=float)
    return t


def draw(m, points):
    r = m[0:2, 0:2]
    t = m[0:2, 2]

    points_transformed = (r @ points.T).T + t
    pygame.draw.polygon(screen, (0, 0, 0), points_transformed, 2)


width1 = 300.
height1 = 100.
rect1 = getRectangle(width1, height1)

width2 = 200.
height2 = 100.
rect2 = getRectangle(width2, height2)

width3 = 100.
height3 = 100.
rect3 = getRectangle(width3, height3)

gap12 = 30
gap23 = 15

pygame.init()
pygame.display.set_caption("20221133 한동국")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse Button Pressed!")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                angle1 -= 5
            elif event.key == pygame.K_b:
                angle1 += 5
            elif event.key == pygame.K_c:
                angle2 -= 5
            elif event.key == pygame.K_d:
                angle2 += 5
            elif event.key == pygame.K_e:
                angle3 -= 5
            elif event.key == pygame.K_f:
                angle3 += 5
            elif event.key == pygame.K_ESCAPE:
                done = True

    screen.fill(GREEN)

    M1 = np.eye(3) @ t_mat(center1[0], center1[1]) @ r_mat(angle1) @ t_mat(0, -height1 / 2)
    draw(M1, rect1)

    M2 = M1 @ t_mat(width1, 0) @ t_mat(0, height1 / 2) @ t_mat(gap12, 0) @ r_mat(angle2) @ t_mat(0, -height2 / 2)
    draw(M2, rect2)

    M3 = M2 @ t_mat(width2, 0) @ t_mat(0, height2 / 2) @ t_mat(gap23, 0) @ r_mat(angle3) @ t_mat(0, -height3 / 2)
    draw(M3, rect3)

    pygame.draw.circle(screen, (0, 0, 0), center1, 4)

    c1 = M1 @ t_mat(width1, 0) @ t_mat(0, height1 / 2)
    center2 = c1[0:2, 2]
    pygame.draw.circle(screen, (0, 0, 0), center2, 4)

    c2 = c1 @ t_mat(gap12, 0)
    center3 = c2[0:2, 2]
    pygame.draw.circle(screen, (0, 0, 0), center3, 4)

    c3 = M2 @ t_mat(width2, 0) @ t_mat(0, height2 / 2)
    center4 = c3[0:2, 2]
    pygame.draw.circle(screen, (0, 0, 0), center4, 4)

    c4 = c3 @ t_mat(gap23, 0)
    center5 = c4[0:2, 2]
    pygame.draw.circle(screen, (0, 0, 0), center5, 4)

    pygame.draw.line(screen, (0, 0, 0), center2, center3, 3)
    pygame.draw.line(screen, (0, 0, 0), center4, center5, 3)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
