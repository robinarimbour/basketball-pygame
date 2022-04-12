
from ball import *
from const import *
from hometeam import *
from awayteam import *

class GameInfo():
    def __init__(self):
        self.homeTeamScore = 0
        self.awayTeamScore = 0
        self.homeGoal =  LEFT_BASKET_RECT
        self.awayGoal = RIGHT_BASKET_RECT
        
    def isGoal(self):
        if self.homeGoal.colliderect(BALL.rect):
            if BALL.velocity.y < 0:
                self.homeTeamScore += 1
                return True
        if self.awayGoal.colliderect(BALL.rect):
            if BALL.velocity.y < 0:
                self.awayTeamScore += 1
                return True
            
        return False

    def GamePlay(self, homeTeam, awayTeam):
        
        self.gameTransition(homeTeam, awayTeam)

        if awayTeam.possession:
            self.findCloseAwayOpp(awayTeam, homeTeam, homeTeam.players[homeTeam.cursor])
        else:
            homeTeam.handle()

        if homeTeam.possession:
            self.findCloseHomeOpp(homeTeam, awayTeam)
        else:
            awayTeam.handle()

        if self.isGoal():
            self.gameAfterGoal(homeTeam, awayTeam)

        if BALL.outOfBounds:
            self.gameAfterGoal(homeTeam, awayTeam)

        BALL.update()

    def gameTransition(self, homeTeam, awayTeam):
        if not homeTeam.possession and not awayTeam.possession:
            if BALL.owner in homeTeam.players:
                homeTeam.possession = True
            elif BALL.owner in awayTeam.players:
                awayTeam.possession = True
        elif homeTeam.possession and BALL.owner in awayTeam.players:
            homeTeam.possession = False
            awayTeam.possession = True
        elif awayTeam.possession and BALL.owner in homeTeam.players:
            awayTeam.possession = False
            homeTeam.possession = True

    def findCloseHomeOpp(self, atkTeam, defTeam):
        attackTeam = []
        defendTeam = []
        for player in atkTeam.players:
            player.defense = False
            attackTeam.append(player)
        for player in defTeam.players:
            player.defense = True
            defendTeam.append(player)
        for oppPlayer in attackTeam:
            minDistance = caculateDistance(defendTeam[0].rect.center, oppPlayer.rect.center)
            minComputer = defendTeam[0]
            for player in defendTeam:
                distance = caculateDistance(player.rect, oppPlayer.rect)
                if distance < minDistance:
                    minDistance = distance
                    minComputer = player
            
            oppPlayer.marker = minComputer
            minComputer.marker = oppPlayer
            minComputer.defPosition(oppPlayer.controlRect, oppPlayer.goalRect, oppPlayer.team)
            defendTeam.pop(defendTeam.index(minComputer))

    def findCloseAwayOpp(self, atkTeam, defTeam, gamer):
        
        attackTeam = []
        defendTeam = []
        for player in atkTeam.players:
            player.defense = False
            attackTeam.append(player)
        for player in defTeam.players:
            if player != gamer:
                player.defense = True
                defendTeam.append(player)
        for oppPlayer in attackTeam[1:]:
            minDistance = caculateDistance(defendTeam[0].rect.center, oppPlayer.rect.center)
            minComputer = defendTeam[0]
            for player in defendTeam:
                distance = caculateDistance(player.rect, oppPlayer.rect)
                if distance < minDistance:
                    minDistance = distance
                    minComputer = player
            
            oppPlayer.marker = minComputer
            minComputer.marker = oppPlayer
            minComputer.defPosition(oppPlayer.controlRect, oppPlayer.goalRect, oppPlayer.team)
            i = defendTeam.index(minComputer)
            defendTeam.pop(i)
        defTeam.control(gamer)

    @staticmethod
    def initGame():
        homeTeam = HomeTeam()
        awayteam = AwayTeam() 
        return (homeTeam, awayteam)

    def gameAfterGoal(self, homeTeam, awayTeam):
        BALL.ballAfterGoal()
        homeTeam.possession = False
        awayTeam.possession = False
