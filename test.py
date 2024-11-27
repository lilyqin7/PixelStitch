#could also make it so the slider only works to preserve the original aspect ratio of the image
    #keep aspect ratio button????

#also need to move grid over a bit


from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image
import copy

def loadPilImage(url):
    image = Image.open(urlopen(url))
    return image.convert('RGB')

def onAppStart(app):
    #for both diy and image screens
    app.cellBorderWidth = 1
    #screen dimensions 
    app.width = 800
    app.height = 500    

    #color dropper and color wheel tool
    app.selectColorDropper = False
    app.selectColorWheel = False
    app.colorDropperColor = None
    #image from clipartmax
    wheel = Image.open('clipart835798.png')
    app.colorWheel = wheel.resize((100, 100))
    app.selectedFromColorWheel = False
    app.selectedColorFromWheel = (0, 0, 0)

    #####variables for image####

    # url = 'https://www.w3schools.com/images/picture.jpg'
    url = 'https://tinyurl.com/great-pitch-gif'
    #loadPilImage only loads some images???

    #turns url into PIL image
    app.pilImage = loadPilImage(url)
    
    # app.pilImage = Image.open('tree-736885_1280 (1).jpg').convert('RGB')

    app.imageWidth, app.imageHeight = app.pilImage.size

    #sets necessary variables for controlling size/pixels of image
    app.imagePixelsWide = app.imagePixelsTall = 20
    app.imageWidthSlider = app.imageHeightSlider = 100

    #changes size of image so the pixels are square
    changeImageDimensions(app)
    
    #changes PIL image to CMU image
    app.cmuImage = CMUImage(pixelate(app.pilImage, app.imagePixelsWide, 
                                     app.imagePixelsTall, app.imageWidth, app.imageHeight))

    #create dictionary to store all the hex codes and the frequency they appear
    app.hexCodeToFrequency = calculateHexCodes(app, app.pilImage)
    app.mostFrequentHex = calculateMostFrequentHex(app)

    #variables for drawing board
    app.imageBoard = [([None] * app.imagePixelsWide) for row in range(app.imagePixelsTall)]
    app.imageBoardLeft = app.width/2 + 47 - app.imagePixelsWide * 5
    app.imageBoardTop = app.height/2 - app.imagePixelsTall * 5
    
    pilImage = pixelate(app.pilImage, app.imagePixelsWide, 
                        app.imagePixelsTall, app.imageWidth, app.imageHeight)
    #update app.imageBoard with the appropriate colors
    for row in range(app.imagePixelsTall):
        for col in range(app.imagePixelsWide):
            color = pilImage.getpixel((col * 10 + 5, row * 10 + 5))
            rgbColor = rgb(color[0], color[1], color[2])
            app.imageBoard[row][col] = rgbColor

    #variables for color select
    app.imageColorSelect = None
    app.imageMouseX = 0
    app.imageMouseY = 0

    ####variables for diy####

    #sets necessary variables for controlling size/pixels of diy
    app.diyPixelsWide = app.diyPixelsTall = 20
    app.diyWidthSlider = app.diyHeightSlider = 100

    #variables for drawing board
    app.diyBoard = [([None] * app.diyPixelsWide) for row in range(app.diyPixelsTall)]
    app.diyBoardLeft = app.width/2 + 47 - app.diyPixelsWide * 5 
    app.diyBoardTop = app.height/2 - app.diyPixelsTall * 5

    #variables for color select
    app.colorSelect = None
    app.diyColorSelect = None
    app.diyMouseX = 0
    app.diyMouseY = 0

    #colors on screen
    app.diyColors = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'white', 'black', 'brown']

    app.prevScreen = 'start'

####USED ON IMAGE SCREEN
def calculateMostFrequentHex(app):
    frequent = []
    hexFrequency = app.hexCodeToFrequency.copy()
    #app.mostFrequentHex can hold UP TO 10 values
    #if there aren't 10 vastly unique colors, loop will still terminate
    while len(frequent) < 10 and len(hexFrequency) > 0:
        num = 0
        code = None
        #searches through app.hexCodeToFrequency for most frequent hex code
        for val in hexFrequency:
            if hexFrequency[val] > num:
                num = hexFrequency[val]
                code = val
        frequent.append(code)
        hexFrequency.pop(code)
        #search through app.mostFrequentHex and pop too similar colors
        j = 0
        while j < len(frequent):
            rgbVal = frequent[j]
            r = rgbVal[0]
            g = rgbVal[1]
            b = rgbVal[2]
            k = j + 1
            while k < len(frequent):
                nextVal = frequent[k]
                #if all 3 rgb values are less than 50, colors are too similar
                if abs(nextVal[0] - r) < 50 and abs(nextVal[1] - g) < 50 and abs(nextVal[2] - b) < 50:
                    frequent.pop()
                k += 1
            j += 1
    return frequent
   

#goes through all x and y computer pixels and calculates the frequncy of each color
def calculateHexCodes(app, pilImage):
    d = {}
    for x in range(pilImage.width):
        for y in range(pilImage.height):
            rgb = pilImage.getpixel((x, y))
            d[rgb] = d.get(rgb, 0) + 1
    return d

def pixelate(image, pixelsWide, pixelsTall, width, height):
    image = image.resize((pixelsWide, pixelsTall), Image.NEAREST)
    return image.resize((width, height), Image.NEAREST)

#changes image size based on pixels (they should be square)
def changeImageDimensions(app):
    app.pixelWidth = app.pixelHeight = 10
    app.imageWidth = app.pixelWidth * app.imagePixelsWide
    app.imageHeight = app.pixelHeight * app.imagePixelsTall

##ADJUSTS GRIDS##
def image_change(app):
    (app.imageWidthSlider, app.imageHeightSlider, app.imagePixelsWide, 
     app.imagePixelsTall) = calculateGridDimensions(app.imageWidthSlider, 
                                                     app.imageHeightSlider,
                                                     app.imagePixelsWide, app.imagePixelsTall)
    changeImageDimensions(app)
    app.imageBoard = resizingBoard(app, app.imageBoard, app.imagePixelsWide, app.imagePixelsTall)
    app.imageBoardLeft = app.width/2 + 47 - app.imagePixelsWide * 5
    app.imageBoardTop = app.height/2 - app.imagePixelsTall * 5

    pilImage = pixelate(app.pilImage, app.imagePixelsWide, 
                        app.imagePixelsTall, app.imageWidth, app.imageHeight)
    
    #currently cannot "save" drawings made prior to resizing
    for row in range(app.imagePixelsTall):
        for col in range(app.imagePixelsWide):
            color = pilImage.getpixel((col * 10 + 5, row * 10 + 5))
            rgbColor = rgb(color[0], color[1], color[2])
            app.imageBoard[row][col] = rgbColor

def diy_change(app):
    (app.diyWidthSlider, app.diyHeightSlider, app.diyPixelsWide, 
    app.diyPixelsTall) = calculateGridDimensions(app.diyWidthSlider, 
                                                   app.diyHeightSlider, 
                                                   app.diyPixelsWide, app.diyPixelsTall)
    
    app.diyBoard = resizingBoard(app, app.diyBoard, app.diyPixelsWide, app.diyPixelsTall)
    app.diyBoardLeft = app.width/2 + 47 - app.diyPixelsWide * 5
    app.diyBoardTop = app.height/2 - app.diyPixelsTall * 5

####NECESSARY FOR BOTH####
def resizingBoard(app, board, pixelsWide, pixelsTall):
    oldBoard = board
    #create new board of the updated size
    newBoard = [([None] * pixelsWide) for row in range(pixelsTall)]
    #copy existing values into new board
    #may need to change logic later
    #need to find way to center it
    for row in range(min(len(oldBoard), len(newBoard))):
        for col in range(min(len(oldBoard[0]), len(newBoard[0]))):
            newBoard[row][col] = oldBoard[row][col]
    return newBoard

def mousePress(app, mouseX, mouseY, widthSlider, heightSlider):
    #changes width
    if 130 <= mouseY <= 160 and 25 <= mouseX <= 175:
        widthSlider = mouseX
    #changes height
    elif 210 <= mouseY <= 240 and 25 <= mouseX <= 175:
        heightSlider = mouseX
    return widthSlider, heightSlider

#checks if mouse is hovering over valid color grid option
def mouseMove(app, mouseX, mouseY, colorList):
    row, col = 0, 0
    #calculate row based on mouseX position
    if 650 <= mouseX <= 668:
        col = 1
    elif 668 <= mouseX <= 686:
        col = 2
    elif 686 <= mouseX <= 704:
        col = 3
    
    #calculate col based on mouseY position
    if 100 <= mouseY <= 118:
        row = 1
    elif 118 <= mouseY <= 136:
        row = 2
    elif 136 <= mouseY <= 154:
        row = 3
    elif 154 <= mouseY <= 172:
        row = 4

    #calculates the index in colorList
    if row > 0 and col > 0:
        index = (row - 1) * 3 + (col - 1)
        if index < len(colorList):
            app.colorSelect = colorList[index]
        else:
            app.colorSelect = None
    else:
        app.colorSelect = None

def updateColor(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
    if isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
        row, col = findSquare(app, mouseX, mouseY, board, boardLeft, boardTop)
        board[row][col] = app.diyColorSelect
    return board

def isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
    if (boardLeft <= mouseX <= boardLeft + pixelsWide * 10 and boardTop <= mouseY <= boardTop + pixelsTall * 10):
            return True
    return False

def findSquare(app, mouseX, mouseY, board, boardLeft, boardTop):
    for row in range(len(board)):
        for col in range(len(board[0])):
            cellLeft, cellTop = getCellLeftTop(app, row, col, boardLeft, boardTop)
            if cellLeft <= mouseX <= cellLeft + 10 and cellTop <= mouseY <= cellTop + 10:
                return row, col

def distance(x0, y0, x1, y1):
    return ((x0 - x1)**2 + (y0 - y1)**2)**0.5

#with assistance from chatGPT
def getGradientColor(app, mouseX, x0, x1, startColor, middleColor, endColor):
    midX = (x0 + x1) / 2
    if mouseX <= midX:
        r1, g1, b1 = startColor
        r2, g2, b2 = middleColor
        factor = (mouseX - x0) / (midX - x0)
    else:
        r1, g1, b1 = middleColor
        r2, g2, b2 = endColor
        factor = (mouseX - midX) / (x1 - midX)
    factor = max(0, min(1, factor))

    r = r1 + (r2 - r1) * factor
    g = g1 + (g2 - g1) * factor
    b = b1 + (b2 - b1) * factor

    return (int(r), int(g), int(b))

#changes pixelsWide and pixelsTall when bar is slid in increments of 5 pixels
def calculateGridDimensions(widthSlider, heightSlider, pixelsWide, pixelsTall):
    #changes width display
    if 25 <= widthSlider < 30:
        pixelsWide = 5
    elif 30 <= widthSlider < 35:
        pixelsWide = 6
    elif 35 <= widthSlider < 40:
        pixelsWide = 7
    elif 40 <= widthSlider < 45:
        pixelsWide = 8
    elif 45 <= widthSlider < 50:
        pixelsWide = 9
    elif 50 <= widthSlider < 55:
        pixelsWide = 10
    elif 55 <= widthSlider < 60:
        pixelsWide = 11
    elif 60 <= widthSlider < 65:
        pixelsWide = 12
    elif 65 <= widthSlider < 70:
        pixelsWide = 13
    elif 70 <= widthSlider < 75:
        pixelsWide = 14
    elif 75 <= widthSlider < 80:
        pixelsWide = 15
    elif 80 <= widthSlider < 85:
        pixelsWide = 16
    elif 85 <= widthSlider < 90:
        pixelsWide = 17
    elif 90 <= widthSlider < 95:
        pixelsWide = 18
    elif 95 <= widthSlider < 100:
        pixelsWide = 19
    elif 100 <= widthSlider < 105:
        pixelsWide = 20
    elif 105 <= widthSlider < 110:
        pixelsWide = 21
    elif 110 <= widthSlider < 115:
        pixelsWide = 22
    elif 115 <= widthSlider < 120:
        pixelsWide = 23
    elif 120 <= widthSlider < 125:
        pixelsWide = 24
    elif 125 <= widthSlider < 130:
        pixelsWide = 25
    elif 130 <= widthSlider < 135:
        pixelsWide = 26
    elif 135 <= widthSlider < 140:
        pixelsWide = 27
    elif 140 <= widthSlider < 145:
        pixelsWide = 28
    elif 145 <= widthSlider < 150:
        pixelsWide = 29
    elif 150 <= widthSlider < 155:
        pixelsWide = 30
    elif 155 <= widthSlider < 160:
        pixelsWide = 31
    elif 160 <= widthSlider < 165:
        pixelsWide = 32
    elif 165 <= widthSlider < 170:
        pixelsWide = 33
    elif 170 <= widthSlider <= 175:
        pixelsWide = 34
    #changes height display
    if 25 <= heightSlider < 30:
        pixelsTall = 5
    elif 30 <= heightSlider < 35:
        pixelsTall = 6
    elif 35 <= heightSlider < 40:
        pixelsTall = 7
    elif 40 <= heightSlider < 45:
        pixelsTall = 8
    elif 45 <= heightSlider < 50:
        pixelsTall = 9
    elif 50 <= heightSlider < 55:
        pixelsTall = 10
    elif 55 <= heightSlider < 60:
        pixelsTall = 11
    elif 60 <= heightSlider < 65:
        pixelsTall = 12
    elif 65 <= heightSlider < 70:
        pixelsTall = 13
    elif 70 <= heightSlider < 75:
        pixelsTall = 14
    elif 75 <= heightSlider < 80:
        pixelsTall = 15
    elif 80 <= heightSlider < 85:
        pixelsTall = 16
    elif 85 <= heightSlider < 90:
        pixelsTall = 17
    elif 90 <= heightSlider < 95:
        pixelsTall = 18
    elif 95 <= heightSlider < 100:
        pixelsTall = 19
    elif 100 <= heightSlider < 105:
        pixelsTall = 20
    elif 105 <= heightSlider < 110:
        pixelsTall = 21
    elif 110 <= heightSlider < 115:
        pixelsTall = 22
    elif 115 <= heightSlider < 120:
        pixelsTall = 23
    elif 120 <= heightSlider < 125:
        pixelsTall = 24
    elif 125 <= heightSlider < 130:
        pixelsTall = 25
    elif 130 <= heightSlider < 135:
        pixelsTall = 26
    elif 135 <= heightSlider < 140:
        pixelsTall = 27
    elif 140 <= heightSlider < 145:
        pixelsTall = 28
    elif 145 <= heightSlider < 150:
        pixelsTall = 29
    elif 150 <= heightSlider < 155:
        pixelsTall = 30
    elif 155 <= heightSlider < 160:
        pixelsTall = 31
    elif 160 <= heightSlider < 165:
        pixelsTall = 32
    elif 165 <= heightSlider < 170:
        pixelsTall = 33
    elif 170 <= heightSlider <= 175:
        pixelsTall = 34
    return widthSlider, heightSlider, pixelsWide, pixelsTall

def drawControls(app, widthSlider, heightSlider, pixelsWide, pixelsTall):
    #label and rectangles below are hardcoded in place
    #may move later
    drawLabel('Adjust Size', 100, 90)

    #draws sliders
    #pixels wide
    drawLabel('Width', 100, 170)
    drawRect(100, 145, 150, 5, align = 'center')
    drawRect(225, 145, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{pixelsWide}', 225, 145)
    drawOval(widthSlider, 145, 5, 15, fill = 'blue')

    #pixels tall
    drawLabel('Height', 100, 250)
    drawRect(100, 225, 150, 5, align = 'center')
    drawRect(225, 225, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{pixelsTall}', 225, 225)
    drawOval(heightSlider, 225, 5, 15, fill = 'blue')

    #back button
    drawRect(50, 450, 100, 30, fill = 'pink')
    drawLabel('Back', 100, 465, size = 15)

    #generate pattern button
    drawRect(650, 450, 100, 30, fill = 'pink')
    drawLabel('Generate', 700, 465, size = 15)

#with assistance from chatGPT
def drawTeardrop(centerX, centerY, width, height, fillColor):
    # The widest part of the teardrop (the top)
    ovalWidth = width
    ovalHeight = height * 0.8  # Adjust to control the curve of the teardrop
    ovalTopY = centerY - ovalHeight / 2

    # The pointed part of the teardrop (the bottom)
    triangleBaseY = centerY + ovalHeight / 2
    triangleHeight = height * 0.4  # Adjust to control the length of the point

    # Draw the oval part
    drawOval(centerX, ovalTopY, ovalWidth, ovalHeight, align='center', fill=fillColor)

    # Draw the triangular part
    drawPolygon(
        centerX - ovalWidth / 2, triangleBaseY,  # Left corner of the base
        centerX + ovalWidth / 2, triangleBaseY,  # Right corner of the base
        centerX, triangleBaseY + triangleHeight,  # The tip of the teardrop
        fill=fillColor
    )

def drawColorPanel(app, colorList, mouseX, mouseY):
    drawLabel('Color Bank', 678, 80, align = 'center')

    #draws colors
    for i in range(len(colorList)):
        row, col = i % 3, i // 3
        if isinstance(colorList[i], str):
            drawRect(650 + (row) * 18, 100 + (col) * 18, 20, 20, fill = colorList[i], border = 'black')
        else:
            rgbVal = colorList[i]
            color = rgb(rgbVal[0], rgbVal[1], rgbVal[2])
            drawRect(650 + (row) * 18, 100 + (col) * 18, 20, 20, fill = color, border = 'black')
    
    #selected color
    if app.colorSelect != None:
        drawRect(738, 120, 30, 30, fill = app.colorSelect, border = 'black')
    elif app.prevScreen == 'diy':
        drawRect(738, 120, 30, 30, fill = app.diyColorSelect, border = 'black')
    elif app.prevScreen == 'image':
        drawRect(738, 120, 30, 30, fill = app.imageColorSelect, border = 'black')

    #color dropper
    #image from Icon Archive
    drawImage('Icons8-Ios7-Editing-Color-Dropper.512.png', 670.5, 156.5, width = 15, height = 15)
    drawRect(668, 154, 20, 20, fill = None, border = 'black')

    #color wheel
    #image from PNGWing
    drawImage('pngwing.com (1).png', 688.5, 156.5, width = 15, height = 15)
    drawRect(686, 154, 20, 20, fill = None, border = 'black')

    #draws color wheel
    if app.selectColorWheel == True:
        #image from clipartmax
        drawImage(CMUImage(app.colorWheel), 645, 230)
        drawRect(620, 205, 150, 200, fill = None, border = 'black')
        if distance(mouseX, mouseY, 695, 280) <= 50 and app.colorSelect != None:
            drawRect(635, 350, 120, 20, fill = gradient('white', app.colorSelect, 'black', start = 'left'), border = 'black')
        elif app.selectedFromColorWheel == True:
            color = rgb(app.selectedColorFromWheel[0], app.selectedColorFromWheel[1], app.selectedColorFromWheel[2])
            drawRect(635, 350, 120, 20, fill = gradient('white', color, 'black', start = 'left'), border = 'black')
        else:
            drawRect(635, 350, 120, 20, fill = gradient('white', 'black', start = 'left'), border = 'black')

def findColorDropperColor(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
    #checks if mouse is hovering over a square
    if app.colorSelect == None:
        if isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
            row, col = findSquare(app, mouseX, mouseY, board, boardLeft, boardTop)
            app.colorDropperColor = board[row][col]

def getColorWheelColor(app, mouseX, mouseY):
    #check if mouse is in color wheel or in color rectangle beneath
    if app.selectColorWheel == True:
        if distance(mouseX, mouseY, 695, 280) <= 50:
            color = app.colorWheel.getpixel((mouseX - 645, mouseY - 230))
            app.colorSelect = rgb(color[0], color[1], color[2])
        elif 635 <= mouseX <= 755 and 350 <= mouseY <= 370:
            app.colorSelect = getGradientColor(app, mouseX, 635, 755, (255, 255, 255), app.selectedColorFromWheel[:3], (0, 0, 0))

    if app.colorSelect != None:
        if (isinstance(app.colorSelect, tuple) and len(app.colorSelect) == 3 and all(isinstance(c, int) for c in app.colorSelect)): #with assistance from chatGPT
            app.colorSelect = rgb(app.colorSelect[0], app.colorSelect[1], app.colorSelect[2])

def checkColorControls(app, mouseX, mouseY):
    #checks if pressing on color dropper
    if 668 <= mouseX <= 686 and 154 <= mouseY <= 172:
        app.selectColorDropper = not app.selectColorDropper

    #checks if pressing on color wheel icon
    if 686 <= mouseX <= 704 and 154 <= mouseY <= 172:
        app.selectColorWheel = not app.selectColorWheel
    
    #checks if selected color from color wheel
    if app.selectColorWheel == True and distance(mouseX, mouseY, 695, 280) <= 50:
        app.selectedFromColorWheel = True
        app.selectedColorFromWheel = app.colorWheel.getpixel((mouseX - 645, mouseY - 230))
    elif app.selectColorWheel == False:
        app.selectedFromColorWheel = False

def checkButtons(app, mouseX, mouseY):
    #if back button pressed
    if 50 <= mouseX <= 150 and 450 <= mouseY <= 480:
        setActiveScreen('start')
    #if generate button pressed
    elif 650 <= mouseX <= 750 and 450 <= mouseY <= 480:
        setActiveScreen('result')

def drawUserColorSelection(app, mouseX, mouseY):
    #if mouse hovering over valid color, draw teardrop so user can see color
    if app.colorSelect != None:
        drawTeardrop(mouseX, mouseY, 10, 10, app.colorSelect)

    #if user has selected color dropper, draw so can see
    if app.selectColorDropper == True:
        drawImage('Icons8-Ios7-Editing-Color-Dropper.512.png', mouseX, mouseY, width = 15, height = 15)

##DRAWS THE GRID##
#modified from Tetris creative task
def drawGrid(app, board, boardLeft, boardTop, center):
    drawBoard(app, board, boardLeft, boardTop)
    drawBoardBorder(app, board, center)
def drawBoard(app, board, boardLeft, boardTop):
    for row in range(len(board)):
        for col in range(len(board[row])):
            drawCell(app, row, col, board[row][col], boardLeft, boardTop)
def drawBoardBorder(app, board, leftEdge):
  #draw the board outline (with double-thickness)
  drawRect(leftEdge, app.height/2, len(board[0]) * 10, len(board) * 10,
           fill=None, border='black', borderWidth=2*app.cellBorderWidth, align = 'center')
def drawCell(app, row, col, color, boardLeft, boardTop):
    cellLeft, cellTop = getCellLeftTop(app, row, col, boardLeft, boardTop)
    cellWidth, cellHeight = 10, 10
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,fill=color, 
             border='black', borderWidth=app.cellBorderWidth)
def getCellLeftTop(app, row, col, boardLeft, boardTop):
    cellWidth, cellHeight = 10, 10
    cellLeft = boardLeft + col * cellWidth
    cellTop = boardTop + row * cellHeight
    return (cellLeft, cellTop)

####DIY SCREEN####
def diy_onMouseMove(app, mouseX, mouseY):
    app.diyMouseX, app.diyMouseY = mouseX, mouseY
    mouseMove(app, mouseX, mouseY, app.diyColors)

    if isSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall):
        row, col = findSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop)
        if app.diyBoard[row][col] != None:
            if app.selectColorDropper == True:
                findColorDropperColor(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyBoardLeft, app.diyPixelsTall)
        else:
            app.colorDropperColor = None
    
    getColorWheelColor(app, mouseX, mouseY)

def diy_onMouseDrag(app, mouseX, mouseY):
    app.diyBoard = updateColor(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)

def diy_onMousePress(app, mouseX, mouseY):
    app.selectColorDropper = False

    if app.colorSelect != None:
        app.diyColorSelect = app.colorSelect
        
    app.diyWidthSlider, app.diyHeightSlider = mousePress(app, mouseX, mouseY, app.diyWidthSlider, app.diyHeightSlider)
    checkButtons(app, mouseX, mouseY)
    diy_change(app)
    app.diyBoard = updateColor(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)
    checkColorControls(app, mouseX, mouseY)

def diy_redrawAll(app):
    drawGrid(app, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, 447)
    drawControls(app, app.diyWidthSlider, app.diyHeightSlider, app.diyPixelsWide, app.diyPixelsTall)
    drawColorPanel(app, app.diyColors, app.diyMouseX, app.diyMouseY)
    drawUserColorSelection(app, app.diyMouseX, app.diyMouseY)

####IMAGE SCREEN####
def image_onMousePress(app, mouseX, mouseY):
    app.selectColorDropper = False

    #if mouse hovering over valid color option and user presses, assigns "brush" as that color
    if app.colorSelect != None:
        app.imageColorSelect = app.colorSelect

    #adjusts the width sliders
    oldWidth, oldHeight = app.imageWidthSlider, app.imageHeightSlider
    app.imageWidthSlider, app.imageHeightSlider = mousePress(app, mouseX, mouseY, app.imageWidthSlider, app.imageHeightSlider)
    checkButtons(app, mouseX, mouseY)
    if oldWidth != app.imageWidthSlider or oldHeight != app.imageHeightSlider:
        image_change(app)

    #starts filling in squares
    if isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop)
        app.imageBoard[row][col] = app.imageColorSelect

    checkColorControls(app, mouseX, mouseY)

def image_onMouseDrag(app, mouseX, mouseY):
    #changes width
    if 130 <= mouseY and mouseY <= 160 and abs(mouseX - app.imageWidthSlider) <= 15:
        app.imageWidthSlider = max(25, min(mouseX, 175))     
        image_change(app)   
    #changes height
    elif 210 <= mouseY and mouseY <= 240 and abs(mouseX - app.imageHeightSlider) <= 15:
        app.imageHeightSlider = max(25, min(mouseX, 175))
        #change labels and pixelization image
        image_change(app)

    if isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop)
        app.imageBoard[row][col] = app.imageColorSelect

def image_onMouseMove(app, mouseX, mouseY):
    app.imageMouseX, app.imageMouseY = mouseX, mouseY
    mouseMove(app, mouseX, mouseY, app.mostFrequentHex)

    #checks if mouse is hovering over an image square
    if isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall):
        if app.selectColorDropper == True:
            findColorDropperColor(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall)
            row, col = findSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop)
            app.colorSelect = app.imageBoard[row][col]
        else:
            app.colorDropperColor = None

    getColorWheelColor(app, mouseX, mouseY)

def image_redrawAll(app):
    drawControls(app, app.imageWidthSlider, app.imageHeightSlider, app.imagePixelsWide, app.imagePixelsTall)
    drawGrid(app, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, 447)
    drawColorPanel(app, app.mostFrequentHex, app.imageMouseX, app.imageMouseY)
    drawUserColorSelection(app, app.imageMouseX, app.imageMouseY)

####RESULT SCREEN####
def result_onMousePress(app, mouseX, mouseY):
    #if back button pressed
    if 50 <= mouseX <= 150 and 450 <= mouseY <= 480:
        setActiveScreen(app.prevScreen)

def result_redrawAll(app):
    #back button
    drawRect(50, 450, 100, 30, fill = 'pink')
    drawLabel('Back', 100, 465, size = 15)

    drawLabel('Pattern', app.width/2, app.height/8, size = 20)

    #draws design
    if app.prevScreen == 'image':
        drawGrid(app, app.imageBoard, app.imageBoardLeft - 47, app.imageBoardTop, 400)
    elif app.prevScreen == 'diy':
        drawGrid(app, app.diyBoard, app.diyBoardLeft - 47, app.diyBoardTop, 400)

    #scrollbar
    drawRect(788, 0, 12, 500, fill = 'lightGray')
    drawRect(788, 0, 12, 50, fill = 'gray')

####START SCREEN####
def start_onMousePress(app, mouseX, mouseY):
    if app.width/12 <= mouseX <= app.width*5/12 and app.height*102/160 <= mouseY <= app.height*122/160:
        setActiveScreen('diy')
        app.prevScreen = 'diy'
    elif app.width*7/12 <= mouseX <= app.width*11/12 and app.height*102/160 <= mouseY <= app.height*122/160:
        setActiveScreen('image')
        app.prevScreen = 'image'

def start_redrawAll(app):
    # drawImage('tree-736885_1280 (1).jpg', 0, 0)
    # drawImage(app.cmuImage, 0, 0)
    drawLabel('DIY or image?', app.width/2, app.height/2, size = 40)
    drawRect(app.width/4, app.height * 7/10, app.width/3, app.height/8, fill = 'pink', align = 'center')
    drawLabel('DIY', app.width/4, app.height * 7/10, size = 25)
    drawRect(app.width*3/4, app.height * 7/10, app.width/3, app.height/8, fill = 'pink', align = 'center')
    drawLabel('Image', app.width*3/4, app.height * 7/10, size = 25)

def main():
    runAppWithScreens(initialScreen = 'start', width = app.width, height = app.height)

main()