####FEATURES I STILL NEED TO DO####
###################################
# "move" selection on diy screen
# select all instances of a color to change on diy screen
# drag in specific shapes on diy screen
# scroll bar
# maybe "AI" image chooser based on categories user selects


#tree image from Pixabay via Pexel

from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image
import copy
import os

# def loadPilImage(url):
#     image = Image.open(urlopen(url))
#     return image.convert('RGB')

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
    wheel = Image.open('colorwheel.png')
    app.colorWheel = wheel.resize((100, 100))
    app.selectedFromColorWheel = False
    app.selectedColorFromWheel = (0, 0, 0)

    #editing tools
    app.dragSelection = False
    app.dragStart = 0, 0
    app.dragEnd = 0, 0
    app.drawingDrag = False

    app.fillSelection = False

    app.ovalTool = False
    app.ovalToolStart = 0, 0
    app.ovalToolEnd = 0, 0
    app.drawingOval = False

    app.rectTool = False
    app.rectToolStart = 0, 0
    app.rectToolEnd = 0, 0
    app.drawingRect = False

    app.drawShape = False
    
    app.boardSelected = set()

    #####variables for image####

    # url = 'https://www.w3schools.com/images/picture.jpg'
    #image from PIL demos
    # url = 'https://tinyurl.com/great-pitch-gif'
    #loadPilImage only loads some images???

    #turns url into PIL image
    # app.pilImage = loadPilImage(url)
    
    app.pilImage = Image.open(os.path.join('images', 'tree.png')).convert('RGB')

    app.originalImageWidth, app.originalImageHeight = app.pilImage.size
    app.imageWidth, app.imageHeight = app.pilImage.size

    #sets necessary variables for controlling size/pixels of image
    app.imagePixelsWide, app.imagePixelsTall = 20, 30
    app.imageWidthSlider = app.imageHeightSlider = 100

    #changes size of image so the pixels are square
    changeImageDimensions(app)
    
    #changes PIL image to CMU image
    # app.cmuImage = CMUImage(pixelate(app.pilImage, app.imagePixelsWide, 
                                    #  app.imagePixelsTall, app.imageWidth, app.imageHeight))

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
    app.imageMouseX = app.imageMouseY = 0

    app.preserveAspectRatio = False

    ####variables for diy####

    #sets necessary variables for controlling size/pixels of diy
    app.diyPixelsWide, app.diyPixelsTall = 20, 30
    app.diyWidthSlider = app.diyHeightSlider = 100

    #variables for drawing board
    app.diyBoard = [([None] * app.diyPixelsWide) for row in range(app.diyPixelsTall)]
    app.diyBoardLeft = app.width/2 + 47 - app.diyPixelsWide * 5 
    app.diyBoardTop = app.height/2 - app.diyPixelsTall * 5

    #variables for color select
    app.colorSelect = None
    app.diyColorSelect = None
    app.diyMouseX = app.diyMouseY = 0

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

####USED IN DIY SCREEN
def updateColor(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
    print(app.drawShape, app.drawingRect, app.drawingOval)
    if not app.drawingRect and not app.drawingOval:
        if isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
            row, col = findSquare(app, mouseX, mouseY, board, boardLeft, boardTop)
            board[row][col] = app.diyColorSelect
    else:
        print('bye')
        print(app.boardSelected)
        for square in app.boardSelected:
            row, col = square
            board[row][col] = app.diyColorSelect
        # else:

            
    return board

##ADJUSTS GRIDS##
def image_change(app):
    (app.imageWidthSlider, app.imageHeightSlider, app.imagePixelsWide, 
     app.imagePixelsTall) = calculateGridDimensions(app, app.imageWidthSlider, 
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
    app.diyPixelsTall) = calculateGridDimensions(app, app.diyWidthSlider, 
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
def calculateGridDimensions(app, widthSlider, heightSlider, pixelsWide, pixelsTall):
    #changes width display
    pixelsWide = int(widthSlider//5)
    #changes height display
    pixelsTall = int(heightSlider*3/10)

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

    drawLabel('Tools', 100, 320)

    #images from iconmonstr
    #select and move tool
    drawImage('move icon.png', 28.25, 348.25, width = 30, height = 30)
    #fill tool
    drawImage('fill icon.png', 65.75, 348.25, width = 30, height = 30)
    #square tool
    drawImage('square icon.png', 103.25, 348.25, width = 30, height = 30)
    #circle tool
    drawImage('circle icon.png', 141.75, 349.25, width = 28, height = 28)

    #draws outlines
    for i in range(4):
        drawRect(25 + i * 37.5, 345, 37.5, 37.5, fill = None, border = 'black', borderWidth = 1)
    drawRect(25, 345, 150, 37.5, fill = None, border = 'black')

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
    drawImage('color dropper.png', 670.5, 156.5, width = 15, height = 15)
    drawRect(668, 154, 20, 20, fill = None, border = 'black')

    #color wheel
    #image from PNGWing
    drawImage('colorwheel icon.png', 688.5, 156.5, width = 15, height = 15)
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

    if app.selectColorDropper:
        app.colorSelect = None

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
    if app.selectColorDropper == True:
        drawImage('color dropper.png', mouseX, mouseY, width = 15, height = 15)

def checkEditingTools(app, mouseX, mouseY):
    if 345 <= mouseY <= 382:
        if 25 <= mouseX < 62:
            app.dragSelection = not app.dragSelection
        elif 62 <= mouseX < 100:
            app.fillSelection = not app.fillSelection
        elif 100 <= mouseX < 137:
            app.rectTool = not app.rectTool
        elif 137 <= mouseX <= 175:
            app.ovalTool = not app.ovalTool

def drawEditingTools(app, mouseX, mouseY):
    if app.dragSelection == True:
        drawImage('move icon.png', mouseX, mouseY, width = 20, height = 20)
    if app.fillSelection == True:
        drawImage('fill icon.png', mouseX, mouseY, width = 20, height = 20)
    if app.ovalTool == True:
        drawImage('circle icon.png', mouseX, mouseY, width = 20, height = 20)
    if app.rectTool == True:
        drawImage('square icon.png', mouseX, mouseY, width = 20, height = 20)

# def fillTool(app, mouseX, mouseY, board):
#     startX = 

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
        if app.selectColorDropper == True:
            row, col = findSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop)
            findColorDropperColor(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyBoardLeft, app.diyPixelsTall)
            app.colorSelect = app.diyBoard[row][col]
        else:
            app.colorDropperColor = None
    
    getColorWheelColor(app, mouseX, mouseY)

def diy_onMouseDrag(app, mouseX, mouseY):
    if app.drawingRect:
        app.rectToolEnd = mouseX, mouseY
        xStart, yStart = app.rectToolStart
        for x in range(xStart, mouseX, 10):
            for y in range(yStart, mouseY, 10):
                if isSquare(app, x, y, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall):
                    print('hi')
                    row, col = findSquare(app, x, y, app.diyBoard, app.diyBoardLeft, app.diyBoardTop)
                    app.boardSelected.add((row, col))

    
    if app.drawingOval:
        app.ovalToolEnd = mouseX, mouseY

    if app.drawingDrag:
        app.dragEnd = mouseX, mouseY

    app.diyBoard = updateColor(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)


def diy_onMousePress(app, mouseX, mouseY):
    if app.rectTool:
        app.drawingRect = True

    if app.ovalTool:
        app.drawingOval = True

    if app.dragSelection:
        app.drawingDrag = True

    app.selectColorDropper = app.dragSelection = app.fillSelection = app.ovalTool = app.rectTool = False
    app.boardSelected = set()

    if app.colorSelect != None:
        app.diyColorSelect = app.colorSelect
    
    app.diyWidthSlider, app.diyHeightSlider = mousePress(app, mouseX, mouseY, app.diyWidthSlider, app.diyHeightSlider)
    diy_change(app)
    app.diyBoard = updateColor(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)
    checkButtons(app, mouseX, mouseY)
    checkColorControls(app, mouseX, mouseY)
    checkEditingTools(app, mouseX, mouseY)

    if app.drawingRect:
        app.rectToolStart = mouseX, mouseY
        app.rectToolEnd = mouseX + 1, mouseY + 1

    if app.drawingOval:
        app.ovalToolStart = mouseX, mouseY
        app.ovalToolEnd = mouseX + 1, mouseY + 1

    if app.drawingDrag:
        app.dragStart = mouseX, mouseY
        app.dragEnd = mouseX + 1, mouseY + 1

def diy_onMouseRelease(app, mouseX, mouseY):
    if app.drawingRect:
        app.rectToolEnd = mouseX, mouseY
        app.drawingRect = False
        app.drawShape = True

    if app.drawingOval:
        app.ovalToolEnd = mouseX, mouseY
        app.drawingOval = False
        app.drawShape = True

    if app.drawingDrag:
        app.dragEnd = mouseX, mouseY
        app.drawingDrag = False

def diy_redrawAll(app):
    drawGrid(app, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, 447)
    drawControls(app, app.diyWidthSlider, app.diyHeightSlider, app.diyPixelsWide, app.diyPixelsTall)
    drawColorPanel(app, app.diyColors, app.diyMouseX, app.diyMouseY)
    drawUserColorSelection(app, app.diyMouseX, app.diyMouseY)
    drawEditingTools(app, app.diyMouseX, app.diyMouseY)

    if app.drawingRect:
        startX, startY = app.rectToolStart
        endX, endY = app.rectToolEnd
        drawRect(startX, startY, endX - startX, endY - startY, fill = None, border = 'black')

    if app.drawingOval:
        x0, y0 = app.ovalToolStart
        x1, y1 = app.ovalToolEnd
        centerX, centerY = (x0 + x1)//2, (y0 + y1)//2
        drawOval(centerX, centerY, x1 - x0, y1 - y0, fill = None, border = 'black')

    if app.drawingDrag:
        startX, startY = app.dragStart
        endX, endY = app.dragEnd
        #make them move!!
        drawRect(startX, startY, endX - startX, endY - startY, fill = None, border = 'black', dashes = True)


####IMAGE SCREEN####
def image_onMousePress(app, mouseX, mouseY):
    app.selectColorDropper = app.dragSelection = app.fillSelection = app.ovalTool = app.rectTool = False

    #checks if checked aspect ratio button
    if 760 <= mouseX <= 780 and 40 <= mouseY <= 60:
        app.preserveAspectRatio = not app.preserveAspectRatio

    #if mouse hovering over valid color option and user presses, assigns "brush" as that color
    if app.colorSelect != None:
        app.imageColorSelect = app.colorSelect

    oldWidth, oldHeight = app.imageWidthSlider, app.imageHeightSlider
    if app.preserveAspectRatio:
        widthToHeightRatio = app.originalImageWidth/app.originalImageHeight
        #if user just checked aspect ratio box and hasn't adjusted controls
        app.imageWidthSlider = int(widthToHeightRatio * app.imageHeightSlider * 3/2)
        if 130 <= mouseY <= 160 and 25 <= mouseX <= 175:
            app.imageWidthSlider = mouseX
            app.imageHeightSlider = app.imageWidthSlider / widthToHeightRatio * 2/3
        elif 210 <= mouseY <= 240 and 25 <= mouseX <= 175:
            app.imageHeightSlider = mouseX
            app.imageWidthSlider = app.imageHeightSlider * widthToHeightRatio * 3/2
    
        if app.imageHeightSlider > 175:
                app.imageHeightSlider = 175
                app.imageWidthSlider = app.imageHeightSlider * widthToHeightRatio * 3/2
        elif app.imageHeightSlider < 25:
                app.imageHeightSlider = 25
                app.imageWidthSlider = app.imageHeightSlider * widthToHeightRatio * 3/2

        if app.imageWidthSlider > 175:
                app.imageWidthSlider = 175
                app.imageHeightSlider = app.imageWidthSlider / widthToHeightRatio * 2/3
        elif app.imageWidthSlider < 25:
                app.imageWidthSlider = 25
                app.imageHeightSlider = app.imageWidthSlider / widthToHeightRatio * 2/3

    else:
        app.imageWidthSlider, app.imageHeightSlider = mousePress(app, mouseX, mouseY, app.imageWidthSlider, app.imageHeightSlider)
    
    if oldWidth != app.imageWidthSlider or oldHeight != app.imageHeightSlider:
        image_change(app)
    
    #starts filling in squares
    if isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop)
        app.imageBoard[row][col] = app.imageColorSelect

    checkButtons(app, mouseX, mouseY)
    checkColorControls(app, mouseX, mouseY)
    checkEditingTools(app, mouseX, mouseY)

def image_onMouseDrag(app, mouseX, mouseY):
    oldWidth, oldHeight = app.imageWidthSlider, app.imageHeightSlider
    if app.preserveAspectRatio:
        widthToHeightRatio = app.originalImageWidth/app.originalImageHeight
        #if user just checked aspect ratio box and hasn't adjusted controls
        app.imageWidthSlider = widthToHeightRatio * app.imageHeightSlider * 3/2
        if 130 <= mouseY <= 160 and 25 <= mouseX <= 175:
            app.imageWidthSlider = mouseX
            app.imageHeightSlider = app.imageWidthSlider / widthToHeightRatio * 2/3
        elif 210 <= mouseY <= 240 and 25 <= mouseX <= 175:
            app.imageHeightSlider = mouseX
            app.imageWidthSlider = app.imageHeightSlider * widthToHeightRatio * 3/2
    else:
        #changes width
        if 130 <= mouseY <= 160 and abs(mouseX - app.imageWidthSlider) <= 15:
            app.imageWidthSlider = max(25, min(mouseX, 175))   
        #changes height
        elif 210 <= mouseY <= 240 and abs(mouseX - app.imageHeightSlider) <= 15:
            app.imageHeightSlider = max(25, min(mouseX, 175))
            #change labels and pixelization image
    if oldWidth != app.imageWidthSlider or oldHeight != app.imageHeightSlider:
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

    #preserve aspect ratio checkbox
    drawLabel('Preserve Aspect Ratio:', 690, 50)
    color = None
    if app.preserveAspectRatio == True:
        color = 'pink'
        #draw white checkmark
    drawRect(760, 40, 20, 20, fill = color, border = 'black')

####CHOOSE IMAGE SCREEN####
def imageOptions_onMousePress(app, mouseX, mouseY):
    if 650 <= mouseX <= 750 and 450 <= mouseY <= 480:
        setActiveScreen('image')
    elif 50 <= mouseX <= 150 and 450 <= mouseY <= 480:
        setActiveScreen('start')

def imageOptions_redrawAll(app):
    drawLabel('Choose an Image:', app.width/2, app.height/6, size = 30)

    #draw images

    #create button
    drawRect(650, 450, 100, 30, fill = 'pink')
    drawLabel('Create', 700, 465, size = 15)
    #back button
    drawRect(50, 450, 100, 30, fill = 'pink')
    drawLabel('Back', 100, 465, size = 15)

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
        setActiveScreen('imageOptions')
        app.prevScreen = 'image'

def start_redrawAll(app):
    drawLabel('DIY or image?', app.width/2, app.height/2, size = 40)
    drawRect(app.width/4, app.height * 7/10, app.width/3, app.height/8, fill = 'pink', align = 'center')
    drawLabel('DIY', app.width/4, app.height * 7/10, size = 25)
    drawRect(app.width*3/4, app.height * 7/10, app.width/3, app.height/8, fill = 'pink', align = 'center')
    drawLabel('Image', app.width*3/4, app.height * 7/10, size = 25)

def main():
    runAppWithScreens(initialScreen = 'start', width = app.width, height = app.height)

main()