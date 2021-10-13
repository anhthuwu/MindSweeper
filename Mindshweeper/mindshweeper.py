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

boardBlock = (boardX,boardY,boardW,boardH)

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

# blanks = (list(pyautogui.locateAllOnScreen('blank.png', confidence=.95, region=boardBlock)),7)
# winsound.Beep(2000,333)

# val = {'1️⃣ ':1, '2️⃣ ':2, '3️⃣ ':3, '4️⃣ ':4, '5️⃣ ':5}

# ones += list(pyautogui.locateAllOnScreen('oneD.png', confidence=.8))
#print(f"Number of one(s): {len(ones)}")
# for pos in ones:
#     print(pos)
#     pyautogui.moveTo(pyautogui.center(pos))
#     winsound.Beep(2000, 333)
hardDim = (20,24)

cellW = boardW/hardDim[1]
cellH = boardH/hardDim[0]
grid = [ [-1]*24 for i in range(20)]
print(f"Cell width: {cellW}; Cell Height: {cellH}")
def boardToGridCoordinate(x, y): #center coor
    c = round((x-(cellW/2)+cellW-boardX)/cellW-1)
    r = round((y-(cellH/2)+cellH-boardY)/cellH-1)
    return (r,c)

def fillNum():
    for n in num:
        for pos in n[0]:
            (x,y) = pyautogui.center(pos)
            (r,c) = boardToGridCoordinate(x,y)
            grid[r][c] = n[1]



# for pos in ones:
#     bCoor = pyautogui.center(pos)
#     gCoor = boardToGridCoordinate(bCoor[0], bCoor[1])
#     grid[gCoor[0]][gCoor[1]] = 1

# pprint(grid)


safeL = (232,196,156)
safeD = (216,188,156)

def gridToBoardCoor(r,c):
    x = (c*cellW)+(cellW/2)
    y = (r*cellH)+(cellH/2)
    return (x,y)

def clickOnBoard(s):
    for cell in s:
        (r,c) = cell
        (x,y) = gridToBoardCoor(r,c)
        pyautogui.click(x+boardX,y+boardY)

def rightClickOnBoard(l):
    for cell in l:
        (r,c) = cell
        (x,y) = gridToBoardCoor(r,c)
        pyautogui.rightClick(x+boardX,y+boardY)

def potentialMine(r,c): #can this coordinate be a mine?
    numN = getNumNeighbor(r,c)
    for n in numN:
        (nr,nc) = n
        nVal = grid[nr][nc]
        mineN = getMineNeighbor(nr,nc)
        if nVal-len(mineN) <= 0:
            return False
    return True

def getNextAssignedNum(): 
    toret = []
    for r in range(hardDim[0]):
        for c in range(hardDim[1]):
            b = grid[r][c]
            if b == -1: #also click on nonpotential Mine if unassigned
                if not potentialMine(r,c):
                    toClick.add((r,c))
            elif b != 0 and b != 69:
                un = getUnassignedNeighbor(r,c)
                if len(un) > 0:
                    toret.append((r,c))
    return toret

def getUnassignedVar():
    toret = []
    for r in range(hardDim[0]):
        for c in range(hardDim[1]):
            b = grid[r][c]
            if b == -1:
                toret.append((r,c))
    return toret

def getUnassignedNeighbor(r,c):
    n = []
    for i in range(3):
        for j in range(3):
            nr = r+i-1
            nc = c+j-1
            if (nr in range(20) and nc in range(24)):
                if grid[nr][nc] == -1 and not (i == 1 and j == 1): #if only passing assigned, delete second cond
                    n.append((r+i-1,c+j-1))
    return n

def getNumNeighbor(r,c):
    n = []
    for i in range(3):
        for j in range(3):
            nr = r+i-1
            nc = c+j-1
            if (nr in range(20) and nc in range(24)):
                if grid[nr][nc] != -1 and grid[nr][nc] != 0 and grid[nr][nc] != 69 and not (i == 1 and j == 1): #if only passing assigned, delete second cond
                    n.append((nr,nc))
    return n

def getMineNeighbor(r,c):
    m = []
    for i in range(3):
        for j in range(3):
            nr = r+i-1
            nc = c+j-1
            if (nr in range(20) and nc in range(24)):
                if grid[nr][nc] == 69:# and not (i == 1 and j == 1): #if only passing assigned, delete second cond
                    m.append((nr,nc))
    return m

def getCommonPotentialMineNeighbor(r1,c1,r2,c2):
    pmn1 = set()
    pmn2 = set()
    un1 = getUnassignedNeighbor(r1,c1)
    for u in un1:
        (ur,uc) = u
        if potentialMine(ur,uc):
            pmn1.add(u)
    un2 = getUnassignedNeighbor(r2,c2)
    for u in un2:
        (ur,uc) = u
        if potentialMine(ur,uc):
            pmn2.add(u)
    return list(pmn1&pmn2)

def fillMine():
    av = getNextAssignedNum()
    for v in av:
        (r,c) = v
        vVal = grid[r][c]
        un = getUnassignedNeighbor(r,c)
        mn = getMineNeighbor(r,c)
        if (len(un)+len(mn)) == vVal:
            for n in un:
                (i,j) = n
                grid[i][j] = 69
                # toRightClick.append(n)

def explore():
    av = getNextAssignedNum()
    for v in av:
        (r,c) = v
        vVal = grid[r][c]
        if vVal != 0:
            un = getUnassignedNeighbor(r,c)
            mn = getMineNeighbor(r,c)
            if len(un) != 0 and len(mn) == vVal:
                for u in un:
                    toClick.add(u)
            elif len(un) != 0:
                nn = getNumNeighbor(r,c)
                for n in nn: #check each number neighbor
                    (i,j) = n
                    nVal = grid[i][j]
                    n_mn = getMineNeighbor(i,j)
                    n_un = getUnassignedNeighbor(i,j)
                    cpmn = getCommonPotentialMineNeighbor(r,c,i,j) #get common potential mine between it and its num neighbor
                    n_noncommon = list(set(n_un)-set(cpmn))
                    v_noncommon = list(set(un)-set(cpmn))
            
                    n_minspill = nVal-len(n_mn)-len(n_noncommon)
                    v_minspill = vVal-len(mn)-len(v_noncommon)
                    n_maxspill = min(nVal-len(n_mn),len(cpmn))
                    v_maxspill = min(vVal-len(mn),len(cpmn))
                    spill = min(n_minspill,v_minspill) #ADD functionality to consider 2 non neighbor sharing mine neighbor as well; only update unassigned for new board
                    if n_minspill > 0:
                        if (vVal-len(mn)) == n_minspill:
                            for vn in v_noncommon:
                                toClick.add(vn)
                    if v_minspill > 0:
                        if (nVal-len(n_mn)) == v_minspill:
                            for nn in n_noncommon:
                                toClick.add(nn)
                    if spill > 0: #guarantee exact spill <= why can't DELETE??
                        if v_maxspill-n_minspill >= len(v_noncommon) and v_maxspill > n_maxspill:
                            # either make sure to open nums first or check that mine 
                            #won't violate
                            #deleted: vVal-len(mn) > len(v_noncommon) and vVal-len(mn)-spill == len(v_noncommon) and 
                            for vn in v_noncommon:
                                (vnr,vnc) = vn
                                # check = getNumNeighbor(vnr,vnc)
                                # guess = True
                                # for cell in check:
                                #     (cr,cc) = cell
                                #     if grid[cr][cc] <= len(getMineNeighbor(cr,cc)):
                                #         guess = False
                                # if guess:
                                print(f"spill = {v_maxspill}-{n_minspill}\nv-n: {v}-{n} \nvn: {vn}")#\nv_noncom-n_noncommon: {v_noncommon}-{n_noncommon}")
                                grid[vnr][vnc] = 69
                                # toRightClick.append(vn)
                        if n_maxspill-v_minspill >= len(n_noncommon) and n_maxspill > v_maxspill:
                            for nn in n_noncommon:
                                (nnr,nnc) = nn
                                print(f"spill = {v_maxspill}-{n_minspill}\nv-n: {v}-{n} \nnn: {nn}")#\nv_noncom-n_noncommon: {v_noncommon}-{n_noncommon}")
                                grid[nnr][nnc] = 69
                                # toRightClick.append(nn)

def closeTo(a,b):
    toret = (b[0]-a[0])**2+(b[1]-a[1])**2+(b[2]-a[2])**2
    return toret<500

def fillSafe():
    for r in range(hardDim[0]):
        for c in range(hardDim[1]):
            (x,y) = gridToBoardCoor(r,c)
            if grid[r][c] == -1:
                if (closeTo(board.getpixel((x,y)), safeL) or closeTo(board.getpixel((x,y)), safeD)):
                    grid[r][c] = 0

butt = {-1:'⬜', 0:'🟦', 1:'1️⃣ ', 2:'2️⃣ ', 3:'3️⃣ ', 4:'4️⃣ ', 5:'5️⃣ ', 6:'6️⃣ ', 7:'7️⃣ ', 69:'💣', 96:'▪ '}
def print_grid(grid):
    colstr = "  "
    for i in range(24):
        colstr += str(i)
        if i < 10:
            colstr += " "
    print(colstr)
    j = 0
    for row in grid:
        if j < 10:
            print(" ",end='')
        print(j,end='')
        j += 1
        for ock in row:  
            print(butt[ock],end='')
        print()

(sX,sY) = gridToBoardCoor(10,12)
pyautogui.click(sX+boardX,sY+boardY)

while(len(getUnassignedVar()) > 0):
    pyautogui.moveTo(fullBoardX+100,fullBoardY+30)
    board = pyautogui.screenshot('board.png',region=(boardX,boardY, boardW, boardH))
    toClick = set()
    # toRightClick = []
    winsound.Beep(5000,333)
    ones = (list(pyautogui.locateAllOnScreen('one.png', confidence=.8, region=boardBlock)), 1)
    winsound.Beep(2000,333)
    twos = (list(pyautogui.locateAllOnScreen('two.png', confidence=.8, region=boardBlock)), 2)
    winsound.Beep(2000,333)
    threes = (list(pyautogui.locateAllOnScreen('three.png', confidence=.8, region=boardBlock)), 3)
    winsound.Beep(2000,333)
    fours = (list(pyautogui.locateAllOnScreen('four.png', confidence=.8, region=boardBlock)), 4)
    winsound.Beep(2000,333)
    fives = (list(pyautogui.locateAllOnScreen('five.png', confidence=.8, region=boardBlock)), 5)
    winsound.Beep(2000,333)
    sixes = (list(pyautogui.locateAllOnScreen('six.png', confidence=.8, region=boardBlock)), 6)
    winsound.Beep(2000,333)
    sevens = (list(pyautogui.locateAllOnScreen('seven.png', confidence=.8, region=boardBlock)), 7)
    winsound.Beep(2000,333)
    num = [ones, twos, threes, fours, fives, sixes, sevens]
    fillSafe()
    fillNum()
    fillMine()
    explore()
    clickOnBoard(toClick)
    # rightClickOnBoard(list(set(toRightClick)))
    time.sleep(.5)
    print_grid(grid)
    print("\n______________________\n")