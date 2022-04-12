
import pygame

from const import *
from player import *
from ball import BALL
from team import *
from state import *

pygame.init()

class AwayTeam(Team):
    def __init__(self):
        super().__init__()

        self.players = [
        AwayPlayer(400, 420, PG),
        AwayPlayer(500, 500, SG),
        AwayPlayer(300, 420, SF),
        AwayPlayer(400, 500, PF),
        AwayPlayer(500, 420, C),
        ]

        for player in self.players:
            self.add(player)

        for i,player in enumerate(self.players):
            player.atkpos = AWAY_ATTACK_POSITIONS[i]
            player.defpos = HOME_ATTACK_POSITIONS[i]
        
        self.index = 0
        self.player = self.players[self.index]
        self.cursor = None

    def handle(self):
        if BALL.owner == self.player:
            self.player.state = State.COMPUTER
        elif BALL.owner == None:
            self.attack()
            self.player = self.getClosestComputer()
            self.player.state = State.FIND_BALL
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

    def performAction(self, player):
        if player.state == State.ATTACK:
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
