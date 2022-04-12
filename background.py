import pygame
import os
from const import *
from ball import BALL

BG_FOLDER = 'Assets'
BG_FILENAME = 'COURT.jpg'

pygame.init()

class Background(pygame.Surface):
    def __init__(self):
        super(Background, self).__init__((WIDTH, HEIGHT))
        
        img = pygame.image.load(os.path.join(BG_FOLDER, BG_FILENAME))
        COURT = pygame.transform.scale(img, (WIDTH, HEIGHT))
        self.blit(COURT, (0, 0))

        pygame.draw.line(self,BLACK,BOTTOM_LEFT,BOTTOM_RIGHT) #BOTTOM
        pygame.draw.line(self,BLACK,TOP_LEFT,TOP_RIGHT) #TOP
        pygame.draw.line(self,BLACK,BOTTOM_LEFT,TOP_LEFT) #LEFT
        pygame.draw.line(self,BLACK,BOTTOM_RIGHT,TOP_RIGHT) #RIGHT

        pygame.draw.rect(self, RED, RIGHT_GOAL_RECT, 2)
        pygame.draw.rect(self, RED, RIGHT_BASKET_RECT, 2)
        pygame.draw.rect(self, RED, LEFT_GOAL_RECT, 2)
        pygame.draw.rect(self, RED, LEFT_BASKET_RECT, 2)
        
        pygame.draw.rect(self, RED, AWAY_PG_ATTACK_POSITION, 2)
        pygame.draw.rect(self, RED, AWAY_SG_ATTACK_POSITION, 2)
        pygame.draw.rect(self, RED, AWAY_SF_ATTACK_POSITION, 2)
        pygame.draw.rect(self, RED, AWAY_PF_ATTACK_POSITION, 2)
        pygame.draw.rect(self, RED, AWAY_C_ATTACK_POSITION, 2)

        pygame.draw.rect(self, RED, HOME_PG_ATTACK_POSITION, 2)
        pygame.draw.rect(self, RED, HOME_SG_ATTACK_POSITION, 2)
        pygame.draw.rect(self, RED, HOME_SF_ATTACK_POSITION, 2)
        pygame.draw.rect(self, RED, HOME_PF_ATTACK_POSITION, 2)
        pygame.draw.rect(self, RED, HOME_C_ATTACK_POSITION, 2)

        pygame.draw.rect(self, RED, RECT_GAME, 2)
