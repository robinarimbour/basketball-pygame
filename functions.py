import pygame
from const import *

pygame.init()

def caculateDistance(position1, position2):
    x = abs(position2[0] - position1[0])
    y = abs(position2[1] - position1[1])
    return x * x + y * y

def convertDirectVector(direction):
    if direction is LEFT:
        return pygame.math.Vector2(-1, 0).normalize()
    elif direction is RIGHT:
        return pygame.math.Vector2(1, 0).normalize()
    elif direction is UP:
        return pygame.math.Vector2(0, -1).normalize()
    elif direction is DOWN:
        return pygame.math.Vector2(0, 1).normalize()
    elif direction is UP_LEFT:
        return pygame.math.Vector2(-1, -1).normalize()
    elif direction is UP_RIGHT:
        return pygame.math.Vector2(1, -1).normalize()
    elif direction is DOWN_LEFT:
        return pygame.math.Vector2(-1, 1).normalize()
    elif direction is DOWN_RIGHT:
        return pygame.math.Vector2(1, 1).normalize()

def convertVec2Dir(vec):
    if vec.x < 0 and abs(vec.x) >= abs(vec.y):
        return LEFT
    elif vec.x > 0 and abs(vec.x) >= abs(vec.y):
        return RIGHT
    elif vec.y < 0 and abs(vec.x) < abs(vec.y):
        return UP
    elif vec.y > 0 and abs(vec.x) < abs(vec.y):
        return DOWN

def findLineEq(x1, y1, x2, y2):
    m = (y2-y1)/(x2-x1)
    b = y2 - (m*x2)
    return m,b

def checkBoundaries(rect, vel, direction):
    if direction == LEFT:       #LEFT
        if rect.left - vel < TOP_LEFT[0]:
            m,b = findLineEq(BOTTOM_LEFT[0], BOTTOM_LEFT[1], TOP_LEFT[0], TOP_LEFT[1])
            if rect.top > m*(rect.left) + b:
                return True
            else:
                return False
        else:
            return True

    elif direction == RIGHT:       #RIGHT
        if rect.right + vel > TOP_RIGHT[0]:
            m,b = findLineEq(BOTTOM_RIGHT[0],BOTTOM_RIGHT[1],TOP_RIGHT[0],TOP_RIGHT[1])
            if rect.top > m*(rect.right) + b:
                return True
            else:
                return False
        else:
            return True
    
    elif direction == UP:     #UP
        if rect.left  < TOP_LEFT[0]:
            m,b = findLineEq(BOTTOM_LEFT[0],BOTTOM_LEFT[1],TOP_LEFT[0],TOP_LEFT[1])
            if rect.top - vel > m*(rect.left) + b:
                return True
            else:
                return False
        elif rect.right > TOP_RIGHT[0]:
            m,b = findLineEq(BOTTOM_RIGHT[0],BOTTOM_RIGHT[1],TOP_RIGHT[0],TOP_RIGHT[1])
            if rect.top - vel > m*(rect.right) + b:
                return True
            else:
                return False
        else:
            return True
