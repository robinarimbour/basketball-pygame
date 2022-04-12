
import pygame
import random

from const import *
from player import *
from ball import BALL
from state import *

pygame.init()

class HomePlayer(BBPlayer):
    def __init__(self, centerx, centery, pos):
        super().__init__(centerx, centery, HOME_TEAM, pos)
        self.goalRect = LEFT_GOAL_RECT
        self.basketRect = LEFT_BASKET_RECT

    def shoot(self):
        if BALL.owner == self:
            BALL.shoot(self.basketRect, self.isJump)
            self.state = State.FREE
        else:
            pass

    def leadToGoal(self):

        distances = {
        UP: caculateDistance((self.controlRect.centerx, self.controlRect.centery - self.vel), self.goalRect.center),
        DOWN: caculateDistance((self.controlRect.centerx, self.controlRect.centery + self.vel), self.goalRect.center),
        RIGHT: caculateDistance((self.controlRect.centerx + self.vel, self.controlRect.centery), self.goalRect.center),
        LEFT: caculateDistance((self.controlRect.centerx - self.vel, self.controlRect.centery), self.goalRect.center),
        UP_LEFT: caculateDistance((self.controlRect.centerx - self.vel / SQRT_2, self.controlRect.centery  - self.vel / SQRT_2), self.goalRect.center),
        UP_RIGHT: caculateDistance((self.controlRect.centerx + self.vel / SQRT_2, self.controlRect.centery  - self.vel / SQRT_2), self.goalRect.center),
        DOWN_LEFT: caculateDistance((self.controlRect.centerx - self.vel / SQRT_2, self.controlRect.centery  + self.vel / SQRT_2), self.goalRect.center),
        DOWN_RIGHT: caculateDistance((self.controlRect.centerx + self.vel / SQRT_2, self.controlRect.centery  + self.vel / SQRT_2), self.goalRect.center),
        }

        direction = LEFT
        distance = distances[LEFT]

        for key, value in distances.items():
            if value < distance:
                distance = value
                direction = key
        
        if distance < 1:
            return

        self.move(direction)

class AwayPlayer(BBPlayer):
    def __init__(self, centerx, centery, pos):
        super().__init__(centerx, centery, AWAY_TEAM, pos)
        self.goalRect = RIGHT_GOAL_RECT
        self.basketRect = RIGHT_BASKET_RECT

    def shoot(self):
        if BALL.owner == self:
            BALL.shoot(self.basketRect, self.isJump)
            self.state = State.FREE
        else:
            pass

    def leadToGoal(self):

        distances = {
        UP: caculateDistance((self.controlRect.centerx, self.controlRect.centery - self.vel), self.goalRect.center),
        DOWN: caculateDistance((self.controlRect.centerx, self.controlRect.centery + self.vel), self.goalRect.center),
        RIGHT: caculateDistance((self.controlRect.centerx + self.vel, self.controlRect.centery), self.goalRect.center),
        LEFT: caculateDistance((self.controlRect.centerx - self.vel, self.controlRect.centery), self.goalRect.center),
        UP_LEFT: caculateDistance((self.controlRect.centerx - self.vel / SQRT_2, self.controlRect.centery  - self.vel / SQRT_2), self.goalRect.center),
        UP_RIGHT: caculateDistance((self.controlRect.centerx + self.vel / SQRT_2, self.controlRect.centery  - self.vel / SQRT_2), self.goalRect.center),
        DOWN_LEFT: caculateDistance((self.controlRect.centerx - self.vel / SQRT_2, self.controlRect.centery  + self.vel / SQRT_2), self.goalRect.center),
        DOWN_RIGHT: caculateDistance((self.controlRect.centerx + self.vel / SQRT_2, self.controlRect.centery  + self.vel / SQRT_2), self.goalRect.center),
        }

        direction = LEFT
        distance = distances[LEFT]

        for key, value in distances.items():
            if value < distance:
                distance = value
                direction = key
        
        if distance < 1:
            return

        self.move(direction)

class Team(pygame.sprite.Group):
    def __init__(self):
        super(Team, self).__init__()

        self.players = []

        self.index = -1
        self.player = None
        self.possession = False

    def passBall(self):
        """pass ball to team member"""
        curPlayer = self.player
        desPlayer = None
        angle = 90

        directVector = convertDirectVector(self.player.direction)
        #caculate vector and calculate angle
        for player in self.players:
            if player != curPlayer:
                tempVector = pygame.math.Vector2(player.rect.x - curPlayer.rect.x, player.rect.y - curPlayer.rect.y)
                tempAngle = abs( directVector.angle_to( tempVector ) )
                if tempAngle > 180:
                    tempAngle = 360 - tempAngle

                if tempAngle < angle :
                    angle = tempAngle
                    desPlayer = player

        if desPlayer != None:
            passVector = pygame.math.Vector2( desPlayer.rect.x - curPlayer.rect.x, desPlayer.rect.y - curPlayer.rect.y)
            self.player = desPlayer

            length = passVector.length()
            if length < 50:
                BALL.passBall( passVector.normalize() * 6 )
            elif length < 100 :
                BALL.passBall( passVector.normalize() * 8 )
            elif length < 200 :
                BALL.passBall( passVector.normalize() * 10 )
            elif length < 300 :
                BALL.passBall( passVector.normalize() * 12 )
            elif length < 400 :
                BALL.passBall( passVector.normalize() * 15 )
            elif length < 500 :
                BALL.passBall( passVector.normalize() *  17)
            else:
                BALL.passBall( passVector.normalize() * 20 )
                BALL.isBouncing = True
        else:
            self.player.leadToGoal()

        curPlayer.state = State.ATTACK
        self.player.state = State.FREE

    def attack(self):
        for player in self.players:
            player.state = State.ATTACK
