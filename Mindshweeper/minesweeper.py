import time
import pyautogui

first = True
# Locate the top right corner, bottom left corner of game board
tR = pyautogui.locateCenterOnScreen('topRightnew.png', confidence=0.9)
bL = pyautogui.locateCenterOnScreen('botLeft.png', confidence=0.9)

# board's starting x and y-coordinate in pixel
boardX = bL[0] 
boardY = tR[1] 
# board's width and height in pixel
boardW = tR[0]-boardX  
boardH = bL[1]-boardY 

# tuple of board's x-coordinate ,y-coordinate, width, and height
boardBlock = (boardX,boardY,boardW,boardH)

# screenshot board and save to file called 'board.png'
board = pyautogui.screenshot('board.png',region=boardBlock)

# row and column dimension of hard level board game
hardDim = (20,24)

# cell width and height in pixel
cellW = boardW/hardDim[1]
cellH = boardH/hardDim[0]

def boardToGridCoordinate(x, y): #center coor
    c = round((x-(cellW/2)+cellW-boardX)/cellW-1)
    r = round((y-(cellH/2)+cellH-boardY)/cellH-1)
    return (r,c)

def gridToBoardCoor(r,c):
    x = (c*cellW)+(cellW/2)
    y = (r*cellH)+(cellH/2)
    return (x,y)

def fillNum():
    for n in num:
        for pos in n[0]:
            (x,y) = pyautogui.center(pos)
            (r,c) = boardToGridCoordinate(x,y)
            grid[r][c] = n[1]

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
                toRightClick.append(n)

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
                        if (vVal-len(mn)) <= n_minspill: 
                            for vn in v_noncommon:
                                toClick.add(vn)
                    if v_minspill > 0:
                        if (nVal-len(n_mn)) <= v_minspill:  
                            for nn in n_noncommon:
                                toClick.add(nn)
                    if spill > 0: 
                        if v_maxspill-n_maxspill >= len(v_noncommon) and v_maxspill > n_maxspill: 
                            for vn in v_noncommon:
                                (vnr,vnc) = vn
                                grid[vnr][vnc] = 69
                                toRightClick.append(vn)
                        if n_maxspill-v_maxspill >= len(n_noncommon) and n_maxspill > v_maxspill: 
                            for nn in n_noncommon:
                                (nnr,nnc) = nn
                                grid[nnr][nnc] = 69
                                toRightClick.append(nn)

# make the guesss an unassigned variable with the most number of number neighbor
def crossYourFinger():
    print("????"*10)
    uac = getUnassignedVar()
    theGuess = uac[0]
    for i in range(1,len(uac)):
        (r,c) = theGuess
        (r2,c2) = uac[i]
        if len(getNumNeighbor(r2,c2)) > len(getNumNeighbor(r,c)):
            theGuess = uac[i]
    toClick.add(theGuess)

def closeTo(a,b):
    toret = (b[0]-a[0])**2+(b[1]-a[1])**2+(b[2]-a[2])**2
    return toret<500

safeL = (232,196,156)
safeD = (216,188,156)
def fillSafe():
    for r in range(hardDim[0]):
        for c in range(hardDim[1]):
            (x,y) = gridToBoardCoor(r,c)
            if grid[r][c] == -1:
                if (closeTo(board.getpixel((x,y)), safeL) or closeTo(board.getpixel((x,y)), safeD)):
                    grid[r][c] = 0

# game element domain: -1 is empty, 0 is safe, 1 through 7 is number, 69 is mine
butt = {-1:'???', 0:'????', 1:'1?????? ', 2:'2?????? ', 3:'3?????? ', 4:'4?????? ', 5:'5?????? ', 6:'6?????? ', 7:'7?????? ', 69:'????'}

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

# set up the 20x24 2D-array
grid = [ [-1]*24 for i in range(20)]

# start the game by clicking on the middle cell of the board
(sX,sY) = gridToBoardCoor(10,12)
pyautogui.click(sX+boardX,sY+boardY)

while(len(getUnassignedVar()) > 0):
    pyautogui.moveTo(boardX-130,boardY-35)
    time.sleep(.25)
    board = pyautogui.screenshot('board.png',region=(boardX,boardY, boardW, boardH))
    toClick = set()
    toRightClick = []
    ones = (list(pyautogui.locateAllOnScreen('one.png', confidence=.8, region=boardBlock)), 1)
    twos = (list(pyautogui.locateAllOnScreen('two.png', confidence=.8, region=boardBlock)), 2)
    threes = (list(pyautogui.locateAllOnScreen('three.png', confidence=.8, region=boardBlock)), 3)
    fours = (list(pyautogui.locateAllOnScreen('four.png', confidence=.8, region=boardBlock)), 4)
    fives = (list(pyautogui.locateAllOnScreen('five.png', confidence=.8, region=boardBlock)), 5)
    sixes = (list(pyautogui.locateAllOnScreen('six.png', confidence=.8, region=boardBlock)), 6)
    sevens = (list(pyautogui.locateAllOnScreen('seven.png', confidence=.8, region=boardBlock)), 7)
    num = [ones, twos, threes, fours, fives, sixes, sevens]
    fillSafe() # update grid with safe cells
    fillNum() # update grid with number cells
    fillMine() # determine mines using independent constraints 
    explore() # determine mines using interactions between constraints 
    if len(toClick) == 0 and not first:
        crossYourFinger()
    first = False
    clickOnBoard(toClick)
    rightClickOnBoard(list(set(toRightClick))) # optional
    print_grid(grid)
    print("\n______________________\n")