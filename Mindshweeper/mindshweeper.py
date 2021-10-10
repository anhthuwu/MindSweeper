import time
import winsound
import pyautogui
from pprint import pprint
time.sleep(2)
# tL = pyautogui.locateCenterOnScreen('topLeft.png', confidence=0.7)
tR = pyautogui.locateCenterOnScreen('topRight.png', confidence=0.9)
bL = pyautogui.locateCenterOnScreen('botLeft.png', confidence=0.9)
# bR = pyautogui.locateCenterOnScreen('botRight.png', confidence=0.7)
bar = pyautogui.locateOnScreen('dif.png', confidence=0.9)

fullBoardX = bL[0]
fullBoardY = tR[1]
fullBoardW = tR[0]-bL[0]
fullBoardH = bL[1]-tR[1]

boardX = bL[0]
boardY = tR[1]+bar[3]
boardW = tR[0]-bL[0]
boardH = bL[1]-(bar[1]+bar[3])


fullBoard = pyautogui.screenshot('fullBoard.png',region=(fullBoardX,fullBoardY, fullBoardW, fullBoardH))
board = pyautogui.screenshot('board.png',region=(boardX,boardY, boardW, boardH))
winsound.Beep(2000,333)

dLevel = None

if pyautogui.locate('hard.png', 'fullBoard.png', confidence=0.95):
    dLevel='h'
elif pyautogui.locate('medium.png', 'fullBoard.png', confidence=0.95):
    dLevel='m'
elif pyautogui.locate('easy.png', 'fullBoard.png', confidence=0.95):
    dLevel='e'
else:
    print("Can't determine difficulty level.")

print(f"Difficulty Level is: {dLevel}")

# ones = list(pyautogui.locateAllOnScreen('one.png', confidence=.8))
# winsound.Beep(2000,333)
# twos = list(pyautogui.locateAllOnScreen('two.png', confidence=.8))
# winsound.Beep(2000,333)
# threes = list(pyautogui.locateAllOnScreen('three.png', confidence=.8))
# winsound.Beep(2000,333)
# element = [ones, twos, threes]

ones = (list(pyautogui.locateAllOnScreen('one.png', confidence=.8)),1)
winsound.Beep(2000,333)
twos = (list(pyautogui.locateAllOnScreen('two.png', confidence=.8)),2)
winsound.Beep(2000,333)
threes = (list(pyautogui.locateAllOnScreen('three.png', confidence=.8)),3)
winsound.Beep(2000,333)
element = [ones, twos, threes]

# ones += list(pyautogui.locateAllOnScreen('oneD.png', confidence=.8))
#print(f"Number of one(s): {len(ones)}")
# for pos in ones:
#     print(pos)
#     pyautogui.moveTo(pyautogui.center(pos))
#     winsound.Beep(2000, 333)
hardDim = (20,24)

cellW = boardW/hardDim[1]
cellH = boardH/hardDim[0]
grid = [ [0]*24 for i in range(20)]
print(f"Cell width: {cellW}; Cell Height: {cellH}")
def boardToGridCoordinate(x, y): #center coor
    c = round((x-(cellW/2)+cellW-boardX)/cellW-1)
    r = round((y-(cellH/2)+cellH-boardY)/cellH-1)
    return (r,c)

def fill(element):
    for e in element:
        for pos in e[0]:
            bCoor = pyautogui.center(pos)
            gCoor = boardToGridCoordinate(bCoor[0], bCoor[1])
            grid[gCoor[0]][gCoor[1]] = e[1]

fill(element)

# for pos in ones:
#     bCoor = pyautogui.center(pos)
#     gCoor = boardToGridCoordinate(bCoor[0], bCoor[1])
#     grid[gCoor[0]][gCoor[1]] = 1

pprint(grid)
