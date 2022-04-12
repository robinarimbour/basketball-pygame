
import pygame
import os

from bresenham import bresenham
from const import *
from functions import *
from state import *
from ball import BALL

PLAYER_FOLDER_NAME = "assets/images/"
DISTANCE_PER_FRAME = 11

class BBPlayer(pygame.sprite.Sprite):
    def __init__(self, centerx, centery, team, pos):
        super().__init__()
        self.defaultx = centerx
        self.defaulty = centery
        self.vel = 4
        self.index = 1
        self.state = State.FREE
        self.totalDistance = 0
        self.pos = pos
        self.atkpos = None
        self.defpos = None
        self.team = team
        self.marker = None
        self.defense = False

        self.isJump = False
        self.jumpCount = 10
        
        self.sprites = {
            UP: [],
            DOWN: [],
            RIGHT: [],
            LEFT: [],
            UP_LEFT: [],
            UP_RIGHT: [],
            DOWN_LEFT: [],
            DOWN_RIGHT: [],
        }

        loadImages(self.sprites[UP], PLAYER_FOLDER_NAME + team + '/' + pos + '/walk' + '/up/')
        loadImages(self.sprites[DOWN], PLAYER_FOLDER_NAME + team + '/' + pos + '/walk' + '/down/')
        loadImages(self.sprites[RIGHT], PLAYER_FOLDER_NAME + team + '/' + pos + '/walk' +'/right/')
        loadImages(self.sprites[LEFT], PLAYER_FOLDER_NAME + team + '/' + pos + '/walk' + '/left/')
        loadImages(self.sprites[UP_LEFT], PLAYER_FOLDER_NAME + team + '/' + pos + '/walk' + '/left/')
        loadImages(self.sprites[DOWN_LEFT], PLAYER_FOLDER_NAME + team + '/' + pos + '/walk' + '/left/')
        loadImages(self.sprites[UP_RIGHT], PLAYER_FOLDER_NAME + team + '/' + pos + '/walk' +'/right/')
        loadImages(self.sprites[DOWN_RIGHT], PLAYER_FOLDER_NAME + team + '/' + pos + '/walk' + '/right/')

        if team is HOME_TEAM:
            self.direction = LEFT
            
        else: 
            self.direction = RIGHT

        self.images = self.sprites[self.direction]
        self.image = self.images[0]

        self.rect = pygame.Rect(centerx - PLAYER_WIDTH//2, centery - PLAYER_HEIGHT//2, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.controlRect = getControlRect(self.rect.centerx, self.rect.centery)
        self.legRect = getLegRect(self.rect.x, self.rect.y)
        
    def update(self):
        self.controlRect = getControlRect(self.rect.centerx, self.rect.centery)
        self.legRect = getLegRect(self.rect.x, self.rect.y)
     
    def move(self, direction):
        
        if direction != JUMP:
            if self.defense:
                pass
            else:
                self.updateDirection(direction)

            if self.index >= len(self.images):
                self.index = 0

            # update new frame
            if self.totalDistance > DISTANCE_PER_FRAME:
                self.image = self.images[self.index]
                self.totalDistance = 0
                self.index += 1

            self.totalDistance += self.vel

        if direction is LEFT and ((RECT_GAME.contains(self.legRect.move(-self.vel, 0)) and checkBoundaries(self.legRect, self.vel, LEFT)) or self.isJump):
            self.rect = self.rect.move(-self.vel, 0)
        elif direction is RIGHT and RECT_GAME.contains(self.legRect.move(self.vel, 0)) and checkBoundaries(self.legRect, self.vel, RIGHT):
            self.rect = self.rect.move(self.vel, 0)
        elif not self.isJump:
            if direction is UP and RECT_GAME.contains(self.legRect.move(0, -self.vel)) and checkBoundaries(self.legRect, self.vel, UP):
                self.rect = self.rect.move(0, -self.vel)
            elif direction is DOWN and RECT_GAME.contains(self.legRect.move(0, self.vel)):
                self.rect = self.rect.move(0, self.vel)
            elif direction is UP_LEFT and RECT_GAME.contains(self.legRect.move(- self.vel / SQRT_2, - self.vel / SQRT_2)) and checkBoundaries(self.legRect, self.vel, UP):
                self.rect = self.rect.move(- self.vel / SQRT_2, - self.vel / SQRT_2)
            elif direction is UP_RIGHT and RECT_GAME.contains(self.legRect.move(self.vel / SQRT_2, - self.vel / SQRT_2)) and checkBoundaries(self.legRect, self.vel, UP):
                self.rect = self.rect.move(self.vel / SQRT_2, - self.vel / SQRT_2)
            elif direction is DOWN_LEFT and RECT_GAME.contains(self.legRect.move( - self.vel / SQRT_2, self.vel / SQRT_2)) and checkBoundaries(self.legRect, self.vel, LEFT):
                self.rect = self.rect.move( - self.vel / SQRT_2, self.vel / SQRT_2)
            elif direction is DOWN_RIGHT and RECT_GAME.contains(self.legRect.move( self.vel / SQRT_2, self.vel / SQRT_2)) and checkBoundaries(self.legRect, self.vel, RIGHT):
                self.rect = self.rect.move( self.vel / SQRT_2, self.vel / SQRT_2)
        if self.isJump:
            if self.jumpCount >= -10:
                neg = 1
                if self.jumpCount < 0:
                    neg = -1
                self.rect = self.rect.move(0, -(self.jumpCount ** 2) * 0.4 * neg)
                self.jumpCount -= 1
            else:
                self.isJump = False
                self.jumpCount = 10
    
        self.update()
        if BALL.owner == self:
            self.updateBallPosition()

    def updateDirection(self, direction):
        if self.direction is direction:
            return
        self.direction = direction
        self.images = self.sprites[self.direction]
        self.totalDistance = 0
        self.index = 1
        self.image = self.images[0]

    def runFindBall(self):
        if BALL.owner == self:
            return

        if BALL.owner == None and BALL.velocity.length() > 10:
            return

        distances = {
        UP: caculateDistance((self.controlRect.centerx, self.controlRect.centery - self.vel), BALL.rect),
        DOWN: caculateDistance((self.controlRect.centerx, self.controlRect.centery + self.vel), BALL.rect),
        RIGHT: caculateDistance((self.controlRect.centerx + self.vel, self.controlRect.centery), BALL.rect),
        LEFT: caculateDistance((self.controlRect.centerx - self.vel, self.controlRect.centery), BALL.rect),
        UP_LEFT: caculateDistance((self.controlRect.centerx - self.vel / SQRT_2, self.controlRect.centery  - self.vel / SQRT_2), BALL.rect),
        UP_RIGHT: caculateDistance((self.controlRect.centerx + self.vel / SQRT_2, self.controlRect.centery  - self.vel / SQRT_2), BALL.rect),
        DOWN_LEFT: caculateDistance((self.controlRect.centerx - self.vel / SQRT_2, self.controlRect.centery  + self.vel / SQRT_2), BALL.rect),
        DOWN_RIGHT: caculateDistance((self.controlRect.centerx + self.vel / SQRT_2, self.controlRect.centery  + self.vel / SQRT_2), BALL.rect),
        }

        direction = UP
        distance = distances[UP]

        for key, value in distances.items():
            if value < distance:
                distance = value
                direction = key
        
        if distance < 1:
            return

        self.move(direction)
        self.takeBall()

    def takeBall(self):
        if BALL.owner == self:
            return

        if self.controlRect.colliderect(BALL.rect):
            BALL.owner = self
    
    def updateBallPosition(self):
        if BALL.owner != self:
            return

        BALL.rect.centerx = self.controlRect.centerx
        BALL.rect.centery = self.legRect.centery

        if (self.direction is JUMP):
            BALL.rect.centerx = self.controlRect.centerx
            BALL.rect.centery = self.controlRect.centery
        elif (self.direction is LEFT):
            BALL.rect.centerx = self.controlRect.centerx - PLAYER_WIDTH / 5
        elif (self.direction is RIGHT):
            BALL.rect.centerx = self.controlRect.centerx + PLAYER_WIDTH / 5
        elif (self.direction is UP):
            BALL.rect.centerx = self.controlRect.centerx + PLAYER_WIDTH / 5
        elif (self.direction is DOWN):
            BALL.rect.centerx = self.controlRect.centerx + PLAYER_WIDTH / 5

    def attack(self):
        if self.atkpos.colliderect(self.legRect):
            return
        distances = {
            UP: caculateDistance((self.legRect.centerx, self.legRect.centery - self.vel), self.atkpos),
            DOWN: caculateDistance((self.legRect.centerx, self.legRect.centery + self.vel), self.atkpos),
            RIGHT: caculateDistance((self.legRect.centerx + self.vel, self.legRect.centery), self.atkpos),
            LEFT: caculateDistance((self.legRect.centerx - self.vel, self.legRect.centery), self.atkpos),
            UP_LEFT: caculateDistance((self.legRect.centerx - self.vel / SQRT_2, self.legRect.centery  - self.vel / SQRT_2), self.atkpos),
            UP_RIGHT: caculateDistance((self.legRect.centerx + self.vel / SQRT_2, self.legRect.centery  - self.vel / SQRT_2), self.atkpos),
            DOWN_LEFT: caculateDistance((self.legRect.centerx - self.vel / SQRT_2, self.legRect.centery  + self.vel / SQRT_2), self.atkpos),
            DOWN_RIGHT: caculateDistance((self.legRect.centerx + self.vel / SQRT_2, self.legRect.centery  + self.vel / SQRT_2), self.atkpos)
        }
            
        direction = UP
        distance = distances[UP]

        for key, value in distances.items():
            if value < distance:
                distance = value
                direction = key
            
        if distance < 1:
            return

        self.move(direction)

    def defPosition(self, oppRect, oppGoal, oppTeam):

        pointsList = list(bresenham(oppRect.centerx, oppRect.centery, oppGoal.centerx, oppGoal.centery))
        defPoint = pointsList[-round(len(pointsList)*0.75)]

        distances = {
        UP: caculateDistance((self.controlRect.centerx, self.controlRect.centery - self.vel), defPoint),
        DOWN: caculateDistance((self.controlRect.centerx, self.controlRect.centery + self.vel), defPoint),
        RIGHT: caculateDistance((self.controlRect.centerx + self.vel, self.controlRect.centery), defPoint),
        LEFT: caculateDistance((self.controlRect.centerx - self.vel, self.controlRect.centery), defPoint),
        UP_LEFT: caculateDistance((self.controlRect.centerx - self.vel / SQRT_2, self.controlRect.centery  - self.vel / SQRT_2), defPoint),
        UP_RIGHT: caculateDistance((self.controlRect.centerx + self.vel / SQRT_2, self.controlRect.centery  - self.vel / SQRT_2), defPoint),
        DOWN_LEFT: caculateDistance((self.controlRect.centerx - self.vel / SQRT_2, self.controlRect.centery  + self.vel / SQRT_2), defPoint),
        DOWN_RIGHT: caculateDistance((self.controlRect.centerx + self.vel / SQRT_2, self.controlRect.centery  + self.vel / SQRT_2), defPoint)
        }

        direction = UP
        distance = distances[UP]

        for key, value in distances.items():
            if value < distance:
                distance = value
                direction = key

        if distance < 10:
            return

        if oppTeam is HOME_TEAM and self.rect.centerx > oppRect.centerx:
                self.updateDirection(direction)
        elif oppTeam is AWAY_TEAM and self.rect.centerx < oppRect.centerx:
                self.updateDirection(direction)
        else:
            faceVec = pygame.math.Vector2(oppRect.centerx - oppGoal.centerx, oppRect.centery - oppGoal.centery).normalize()
            if faceVec != pygame.math.Vector2(0,0):
                faceDir = convertVec2Dir(faceVec)
                self.updateDirection(faceDir)
        self.move(direction)

def getControlRect(centerx, centery):
  return pygame.Rect(centerx - PLAYER_WIDTH // 4, centery, PLAYER_WIDTH // 2, PLAYER_HEIGHT // 2)

def getLegRect(x, y):
    return pygame.Rect(x + round(0.3*PLAYER_WIDTH), y + round(0.85*PLAYER_HEIGHT), round(0.4*PLAYER_WIDTH), 3)

def loadImages(list, path):
  for filename in os.listdir(path):
    image = pygame.image.load(path + filename)
    resizeImage = pygame.transform.scale(image, (PLAYER_WIDTH, PLAYER_HEIGHT))
    list.append(resizeImage)
