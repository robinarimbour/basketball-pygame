
import pygame
from const import *
from background import Background
from ball import *
from game import *
from functions import *
from mainmenu import *
from math import sqrt

pygame.init()

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basketball")

bg = Background()
spriteBall = pygame.sprite.Group(BALL)

def main():

    GAME = GameInfo()
    homeTeam, awayTeam = GAME.initGame()

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
        
        GAME.GamePlay(homeTeam, awayTeam)
        BALL.update()

        draw_window(WIN, bg, homeTeam, awayTeam, spriteBall)

    main()

if __name__ == "__main__":
    main()
