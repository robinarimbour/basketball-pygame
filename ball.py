
import pygame
import os

from const import *
from functions import *

BALL_FOLDER = 'Assets/Ball'
BALL_FILENAME = 'ball1.png'
GRAVITY = 1

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.owner = None
        self.isRolling = False
        self.isShooting = False
        self.outOfBounds = False
        self.isBouncing = True
        self.bounceCount = -5
        self.currBounce = 5
        self.isTipOff = True
        self.tipOffBounceCount = 10
        self.tipOffBounce = 10

        ball_image = pygame.image.load(os.path.join(BALL_FOLDER, BALL_FILENAME))
        self.image = pygame.transform.scale(ball_image, (BALL_SIZE, BALL_SIZE))

        self.rect = self.image.get_rect()
        self.rect.centerx = CENTER_X
        self.rect.centery = CENTER_Y

        self.velocity = pygame.math.Vector2(0,0)
        self.friction = 0.97
        self.fieldSize = pygame.Rect(TOP_LEFT[0], TOP_LEFT[1], TOP_RIGHT[0]-TOP_LEFT[0], PLAY_AREA_HEIGHT)

    def tipOff(self):
        if self.tipOffBounce > 0:
            if self.tipOffBounceCount >= -self.tipOffBounce:
                    neg = 1
                    if self.tipOffBounceCount < 0:
                        neg = -1
                    self.rect = self.rect.move(0, -(self.tipOffBounceCount ** 2) * 0.4 * neg)
                    self.tipOffBounceCount -= 1
            else:
                self.tipOffBounce -= 1
                self.tipOffBounceCount = self.tipOffBounce
        else:
            self.isTipOff = False

    def bounce(self):
        if self.bounceCount < self.currBounce:
            self.rect.y -= self.bounceCount
            self.bounceCount += 1
        elif self.currBounce < 1:
            self.currBounce = 5
            self.bounceCount = -5
            self.isBouncing = False
        else:
            self.currBounce -= 1
            self.bounceCount = -self.currBounce

    def update(self):
        if self.outOfBounds:
            self.outOfBounds = False
        elif self.owner != None:
            self.velocity = pygame.math.Vector2(0, 0)
            self.isTipOff = False
            if self.owner.isJump:
                return
            if self.bounceCount <= 5:
                self.rect.y -= self.bounceCount
                self.bounceCount += 1
            else:
                self.bounceCount = -5
        elif self.isShooting:
            if WINDOW_RECT.contains(self.rect):
                self.rect.x -= self.velocity.x
                self.rect.y -= self.velocity.y
                self.velocity.y -= GRAVITY
            else:
                self.ballAfterGoal()
        elif self.velocity == (0, 0):
            if self.isTipOff:
                self.tipOff()
            if self.isBouncing:
                pass
            else:
                self.isRolling = False
        else:

            if self.isBouncing or self.isTipOff:
                pass

            self.rect.x += self.velocity.x
            self.rect.y += self.velocity.y
            self.velocity *= self.friction  #FRICTION
            
            if abs(self.velocity.x) < 1:
                self.velocity.x = 0
            if abs(self.velocity.y) < 1:
                self.velocity.y = 0

            #bound collision response
            if self.rect.left < self.fieldSize.left:
                if not checkBoundaries(self.rect, self.velocity.x, LEFT):
                    self.outOfBounds = True
                    
            if self.rect.right > self.fieldSize.right:
                if not checkBoundaries(self.rect, self.velocity.x, RIGHT):
                    self.outOfBounds = True

            if self.rect.top < self.fieldSize.top:
                if self.rect.left < TOP_LEFT[0] or self.rect.right > TOP_RIGHT[0]:
                    if not checkBoundaries(self.rect, self.velocity.y, UP):
                        self.outOfBounds = True
                else:
                    self.outOfBounds = True
            
            if self.rect.bottom > self.fieldSize.bottom:
                self.outOfBounds = True

    def passBall(self, vec):
        self.isRolling = True
        self.owner = None
        self.velocity = vec

    def shoot(self, basketRect, isJump):
        self.isRolling = True
        self.owner = None
        self.isShooting = True
        shotDistanceX = self.rect.centerx - basketRect.centerx
        shotDistanceY = self.rect.centery - basketRect.centery
        self.velocity.x = shotDistanceX // 35
        if isJump:
            self.velocity.y = shotDistanceY // 6
        else:
            self.velocity.y = shotDistanceY // 10

    def ballAfterGoal(self):
        self.rect.centerx = (TOP_RIGHT[0] + TOP_LEFT[0]) // 2
        self.rect.centery = (BOTTOM_LEFT[1] + TOP_LEFT[1]) // 2
        self.velocity = pygame.math.Vector2(0, 0)
        self.isShooting = False
        self.isBouncing = True
        self.bounceCount = -5
        self.currBounce = 5

BALL = Ball()
