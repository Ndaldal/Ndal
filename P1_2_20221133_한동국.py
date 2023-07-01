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


def getRegularPolygon(N, radius=1):
    v = np.zeros((N, 2))
    for i in range(N):
        deg = i * 360. / N
        rad = deg * np.pi / 180.
        x = radius * np.cos(rad)
        y = radius * np.sin(rad)
        v[i] = [x, y]
    return v


def rectangleDraw(m, points, scr, color=0x000000, line=0, p0=None):
    r = m[0:2, 0:2]
    t = m[0:2, 2]

    points_transformed = (r @ points.T).T + t
    pygame.draw.polygon(scr, color, points_transformed, line)

    if p0 is not None:
        pygame.draw.line(screen, (0, 0, 0), p0, points_transformed[0])


def planetDraw(ang, planet, distance, scr, color=0xFF9F9F):
    c_planet = t_mat(CENTER[0], CENTER[1]) @ r_mat(ang) @ t_mat(distance, 0) @ r_mat(-ang) @ r_mat(ang)
    rectangleDraw(c_planet, planet, scr, color, p0=c_planet[:2, 2])


pygame.init()
pygame.display.set_caption("20221133 한동국")
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

Mercury = getRegularPolygon(100, 5)
Venus = getRegularPolygon(100, 7)
Earth = getRegularPolygon(100, 8)
Mars = getRegularPolygon(100, 6)
Jupiter = getRegularPolygon(100, 15)
Saturn = getRegularPolygon(100, 13)
Uranus = getRegularPolygon(100, 11)
Neptune = getRegularPolygon(100, 9)

moon = getRegularPolygon(50, 10)
moon_1 = getRegularPolygon(50, 5)

angle = 0.

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

    pygame.draw.circle(screen, 0xFF0000, CENTER, 100)  # Sun

    planetDraw(angle, Mercury, 150, screen)
    planetDraw(angle, Venus, 200, screen)
    planetDraw(angle, Earth, 250, screen)
    planetDraw(angle, Mars, 300, screen)
    planetDraw(angle, Jupiter, 350, screen)
    planetDraw(angle, Saturn, 400, screen)
    planetDraw(angle, Uranus, 450, screen)
    planetDraw(angle, Neptune, 500, screen)

    m_earth = t_mat(CENTER[0], CENTER[1]) @ r_mat(angle) @ t_mat(250, 0) @ r_mat(-angle) @ r_mat(angle)
    m_moon = m_earth @ r_mat(angle - 2) @ t_mat(100, 0) @ r_mat(angle - 2)
    rectangleDraw(m_moon, moon, screen, color=0x123456, p0=m_moon[:2, 2])

    m_jupiter = t_mat(CENTER[0], CENTER[1]) @ r_mat(angle) @ t_mat(350, 0) @ r_mat(-angle) @ r_mat(angle)
    m_moon = m_earth @ r_mat(angle - 2) @ t_mat(200, 0) @ r_mat(angle - 2)
    rectangleDraw(m_moon, moon_1, screen, color=0x123456, p0=m_moon[:2, 2])

    m_moon = m_earth @ r_mat(angle - 2) @ t_mat(150, 0) @ r_mat(angle - 2)
    rectangleDraw(m_moon, moon_1, screen, color=0x123456, p0=m_moon[:2, 2])

    planetDraw(angle, getRegularPolygon(5, 50), 600, screen, color=0xFFFFFF)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
