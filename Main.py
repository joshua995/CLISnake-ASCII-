"""
Joshua Liu
April 3rd, 2024
Console Snake
"""

import os
import time

from pynput import keyboard
from random import randint

from SevenSegment import multi7SegmentLogic


gridSize = [30, 60]  # y, x
grid = []  # Game board

emptyC = "█"  # Alt + 219
appleC = "◙"  # Alt + 10
heartC = "♥"  # Alt + 3
homeC = "⌂"  # Alt + 127
timeBoostC = "+"

spikeC = "▲"  # Alt 30
waterC = "~"


snakeCs = [
    "S",
    "N",
    "A",
    "K",
    "E",
    "E",
    "K",
    "A",
    "N",
    "S",
]  # Characters to represent the snake
snakeCIndex = 0

snake, snakePos = [], []  # y, x
snakeDir = 0  # 1 - 2 - 3 - 4 | UP - DOWN - LEFT - RIGHT

applePos, heartPos, homePos, timeBoostPos = [-1, -1], [-1, -1], [-1, -1], [-1, -1]

spikePos, waterPos = [-1, -1], [-1, -1]

timeMultiplier = 15
score, lives, timeRemainingSec = 0, 1, 120 * timeMultiplier  # timer in seconds

isGameOver = False
hasMoved = False
isStarted = False


def on_press(key):
    global snakeDir, hasMoved, isStarted
    try:
        if key == keyboard.Key.up and snakeDir != 2 and not hasMoved:
            isStarted = True
            snakeDir = 1
            hasMoved = True
        elif key == keyboard.Key.down and snakeDir != 1 and not hasMoved:
            isStarted = True
            snakeDir = 2
            hasMoved = True
        elif key == keyboard.Key.left and snakeDir != 4 and not hasMoved:
            isStarted = True
            snakeDir = 3
            hasMoved = True
        elif key == keyboard.Key.right and snakeDir != 3 and not hasMoved:
            isStarted = True
            snakeDir = 4
            hasMoved = True
    except AttributeError:
        print("special key {0} pressed".format(key))


def on_release(key):
    if key == keyboard.Key.esc:
        return False


def placeObjectOnGrid(objPos, obj):
    grid[objPos[0]][objPos[1]] = emptyC
    objPos[0], objPos[1] = randint(0, gridSize[0] - 1), randint(0, gridSize[1] - 1)
    while grid[objPos[0]][objPos[1]] != emptyC:
        objPos[0], objPos[1] = randint(0, gridSize[0] - 1), randint(0, gridSize[1] - 1)
    grid[objPos[0]][objPos[1]] = obj


def addSectionToSnake(isInit):
    global snakeCIndex
    snake.append(snakeCs[snakeCIndex])
    snakeCIndex += 1
    snakeCIndex %= len(snakeCs)
    if isInit:
        snakePos.append([randint(0, gridSize[0] - 1), randint(0, gridSize[1] - 1)])
    else:
        snakePos.append(
            [
                snakePos[len(snakePos) - 1][0],
                snakePos[len(snakePos) - 1][1],
            ]
        )


def initGrid():
    # Initialize an empty grid
    for y in range(gridSize[0]):
        grid.append([])
        [grid[len(grid) - 1].append(emptyC) for x in range(gridSize[1])]

    # Place snake on board
    addSectionToSnake(True)

    # Place heart on board
    placeObjectOnGrid(heartPos, heartC)

    # Place apple on board
    placeObjectOnGrid(applePos, appleC)

    # Place spike on board
    placeObjectOnGrid(spikePos, spikeC)

    # Place water on board
    placeObjectOnGrid(waterPos, waterC)


def moveSnake():
    global hasMoved
    grid[snakePos[len(snakePos) - 1][0]][snakePos[len(snakePos) - 1][1]] = emptyC
    i = len(snakePos) - 1
    while i > 0:
        if i - 1 >= 0:
            snakePos[i][0] = snakePos[i - 1][0]
            snakePos[i][1] = snakePos[i - 1][1]
        i -= 1
    if snakeDir == 1 and snakePos[0][0] > 0:
        snakePos[0][0] -= 1
    elif snakeDir == 2 and snakePos[0][0] < gridSize[0] - 1:
        snakePos[0][0] += 1
    elif snakeDir == 3 and snakePos[0][1] > 0:
        snakePos[0][1] -= 1
    elif snakeDir == 4 and snakePos[0][1] < gridSize[1] - 1:
        snakePos[0][1] += 1
    for i, s in enumerate(snakePos):
        grid[s[0]][s[1]] = snake[i]
    hasMoved = False


def onCollision():
    global score, snakeCIndex, isGameOver, lives, timeRemainingSec
    for i, s in enumerate(snakePos):
        if s[0] == heartPos[0] and s[1] == heartPos[1]:
            # Place heart on board
            placeObjectOnGrid(heartPos, heartC)

            # Place spike on board
            placeObjectOnGrid(spikePos, spikeC)

            if randint(0, 5) == 0:
                # Place time booster on board
                placeObjectOnGrid(timeBoostPos, timeBoostC)

            lives += 1
            return
        elif s[0] == applePos[0] and s[1] == applePos[1]:
            # Place apple on board
            placeObjectOnGrid(applePos, appleC)

            # Place spike on board
            placeObjectOnGrid(spikePos, spikeC)

            addSectionToSnake(False)

            if randint(0, 5) == 0:
                # Place home on board
                placeObjectOnGrid(homePos, homeC)

            score += 1
            return
        elif s[0] == homePos[0] and s[1] == homePos[1]:
            homePos[0], homePos[1] = -1, -1

            addSectionToSnake(False)

            score += 1
            lives += 1
            return
        elif s[0] == timeBoostPos[0] and s[1] == timeBoostPos[1]:
            timeBoostPos[0], timeBoostPos[1] = -1, -1

            timeRemainingSec += 5 * timeMultiplier
            return
        elif s[0] == spikePos[0] and s[1] == spikePos[1]:
            # Place spike on board
            placeObjectOnGrid(spikePos, spikeC)
            lives -= 1
            if lives <= 0:
                isGameOver = True
            return
        elif s[0] == waterPos[0] and s[1] == waterPos[1]:
            # Place water on board
            placeObjectOnGrid(waterPos, waterC)

            score -= 1
            if len(snake) == 1:
                isGameOver = True
                return
            temp = len(snake) - 1
            grid[snakePos[temp][0]][snakePos[temp][1]] = emptyC
            snake.pop(temp)
            snakePos.pop(temp)
            snakeCIndex -= 1
            return
        elif s[0] == snakePos[0][0] and s[1] == snakePos[0][1] and i > 0:
            # Snake hit itself
            lives -= 1
            if lives <= 0:
                isGameOver = True
            return


def gameLoop(isClear):
    global timeRemainingSec, isGameOver
    for i, g in enumerate(grid):
        for gg in g:
            print("\033[38;2;100;100;100m", end="")
            if gg == heartC:
                print("\033[38;2;255;0;0m", end="")
            elif gg == appleC:
                print("\033[38;2;0;100;0m", end="")
            elif gg == spikeC:
                print("\033[38;2;100;100;100m", end="")
            elif gg == homeC:
                print("\033[38;2;0;255;0m", end="")
            elif gg == timeBoostC:
                print("\033[38;2;255;255;0m", end="")
            elif gg == waterC:
                print("\033[38;2;0;0;255m", end="")
            elif gg != emptyC:
                print("\033[38;2;0;255;0m", end="")
            print(gg, end="")
        if i == gridSize[0] // 3:
            print(f"\033[38;2;100;100;100m {spikeC}: -1 life")
        elif i == gridSize[0] // 3 + 1:
            print(f"\033[38;2;0;100;0m {appleC}: +1 score & length")
        elif i == gridSize[0] // 3 + 2:
            print(f"\033[38;2;255;0;0m {heartC}: +1 life")
        elif i == gridSize[0] // 3 + 3:
            print(f"\033[38;2;255;255;0m {timeBoostC}: +5 seconds")
        elif i == gridSize[0] // 3 + 4:
            print(f"\033[38;2;0;255;0m {homeC}: +1 life & score & length")
        elif i == gridSize[0] // 3 + 5:
            print(f"\033[38;2;0;0;255m {waterC}: -1 score & length")
        else:
            print()
    moveSnake()
    onCollision()
    print(f"\033[38;2;0;255;0mScore: {score}\t", end="")
    print(f"\033[38;2;255;0;0mLives: {lives}\t", end="\n")
    multi7SegmentLogic(timeRemainingSec // timeMultiplier, [255, 255, 0], 0)
    time.sleep(1 / timeMultiplier)
    if isStarted:
        timeRemainingSec -= 1
    if timeRemainingSec == 0:
        isGameOver = True
    os.system("cls") if isClear else ""


if __name__ == "__main__":
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()
    initGrid()
    while not isGameOver:
        gameLoop(True)
    gameLoop(False)
    print("Final Score:")
    multi7SegmentLogic(
        (score + lives + (timeRemainingSec // timeMultiplier)) * len(snake),
        [255, 255, 0],
        0,
    )
