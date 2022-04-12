
import pygame

from const import *
from player import *
from ball import BALL
from team import *
from state import *

pygame.init()

class HomeTeam(Team):
    def __init__(self):
        super().__init__()
        self.players = [
            HomePlayer(1000, 420, PG),
            HomePlayer(1000, 500, SG),
            HomePlayer(800, 500, SF),
            HomePlayer(900, 500, PF),
            HomePlayer(900, 420, C)
        ]

        for player in self.players:
            self.add(player)

        for i,player in enumerate(self.players):
            player.atkpos = HOME_ATTACK_POSITIONS[i]
            player.defpos = AWAY_ATTACK_POSITIONS[i]
        
        self.index = 0
        self.cursor = 0
        self.player = self.players[self.index]

    def handle(self):
        if BALL.owner == self.player:
            self.player.state = State.COMPUTER
        elif BALL.owner == None:
            self.attack()
            self.player = self.getClosestComputer()
            self.player.state = State.FIND_BALL
        self.players[self.cursor].state = State.GAMER
        for player in self.players:
            self.performAction(player)

    def getClosestComputer(self):
        minDistance = caculateDistance(self.players[0].controlRect.center, BALL.rect.center)

        minComputer = self.players[0]

        for player in self.players:
            distance = caculateDistance(player.rect, BALL.rect)

            if distance < minDistance:
                minDistance = distance
                minComputer = player
        
        return minComputer

    def control(self, player):
        keys = pygame.key.get_pressed()  # take pressed keys
        # update direction
        if keys[pygame.K_k]:
            self.passBall()
        elif keys[pygame.K_l]:
            player.shoot()
        if player.isJump:
            if keys[pygame.K_a]:
                player.move(LEFT)
            elif keys[pygame.K_d]:
                player.move(RIGHT)
            else:
                player.move(JUMP)
        elif keys[pygame.K_SPACE]:
            player.isJump = True
            player.move(JUMP)
        if not player.isJump:
            if keys[pygame.K_w] and keys[pygame.K_a]:
                player.move(UP_LEFT)
            elif keys[pygame.K_w] and keys[pygame.K_d]:
                player.move(UP_RIGHT)
            elif keys[pygame.K_s] and keys[pygame.K_a]:
                player.move(DOWN_LEFT)
            elif keys[pygame.K_s] and keys[pygame.K_d]:
                player.move(DOWN_RIGHT)
            elif keys[pygame.K_a]:
                player.move(LEFT)
            elif keys[pygame.K_d]:
                player.move(RIGHT)  
            elif keys[pygame.K_w]:
                player.move(UP)
            elif keys[pygame.K_s]:
                player.move(DOWN)

    def switchPosCheck(self):
        gamer = self.players[self.cursor]
        for player in self.players:
            if player != gamer:
                if gamer.legRect.colliderect(player.atkpos):
                    thirdAtkPos = player.atkpos
                    player.atkpos = gamer.atkpos
                    gamer.atkpos = thirdAtkPos

    def performAction(self, player):
        if player.state == State.GAMER:
            player.takeBall()
            self.control(player)
        elif player.state == State.ATTACK:
            self.switchPosCheck()
            player.attack()
        elif player.state == State.FIND_BALL:
            player.runFindBall()
        elif player.state == State.COMPUTER:
            num = random.randint(1,100)
            if player.atkpos.colliderect(player.legRect):
                if num < 90:
                    return
                elif num < 95:
                    self.passBall()
                elif num < 99:
                    player.leadToGoal()
                else:
                    player.shoot()
            else:
                if num < 98:
                    player.attack()
                else:
                    self.passBall()
