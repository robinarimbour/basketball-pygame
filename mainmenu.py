
import pygame
from const import *
from ball import *

def draw_window(win, bg, h1, a1, ball):

    win.blit(bg, (0, 0))

    h1.draw(win)
    a1.draw(win)
    ball.draw(win)

    pygame.draw.rect(win, RED, BALL.rect, 2)
    pygame.draw.rect(win, RED, h1.player.controlRect, 2)
    
    pygame.display.update()
