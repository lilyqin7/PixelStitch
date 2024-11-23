#could also make it so the slider only works to preserve the original aspect ratio of the image
    #keep aspect ratio button????
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

    #####variables for image####

    # url = 'https://www.w3schools.com/images/picture.jpg'
    url = 'https://tinyurl.com/great-pitch-gif'
    #loadPilImage only loads some images???

    #turns url into PIL image
    app.pilImage = loadPilImage(url)
    app.imageWidth, app.imageHeight = app.pilImage.size

    #sets necessary variables for controlling size/pixels of image
    app.imagePixelsWide = app.imagePixelsTall = 20
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
    app.imageBoardLeft = app.width/2 - app.imagePixelsWide * 10 / 2
    app.imageBoardTop = app.height/2 - app.imagePixelsTall * 10 / 2
    
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
    app.diyBoardLeft = app.width/2 - app.diyPixelsWide * 10 / 2
    app.diyBoardTop = app.height/2 - app.diyPixelsTall * 10 / 2

    #variables for color select
    app.colorSelect = None
    app.diyColorSelect = None
    app.diyMouseX = 0
    app.diyMouseY = 0

    #colors on screen
    app.diyColors = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'white', 'black', 'brown']

#only used in image
def calculateMostFrequentHex(app):
    frequent = []
    hexFrequncy = app.hexCodeToFrequency.copy()
    #app.mostFrequentHex can hold UP TO 10 values
    #if there aren't 10 vastly unique colors, loop will still terminate
    while len(frequent) < 10 and len(hexFrequncy) > 0:
        num = 0
        code = None
        #searches through app.hexCodeToFrequency for most frequent hex code
        for val in hexFrequncy:
            if hexFrequncy[val] > num:
                num = hexFrequncy[val]
                code = val
        frequent.append(code)
        hexFrequncy.pop(code)
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
#only used in image
def calculateHexCodes(app, pilImage):
    d = {}
    for x in range(pilImage.width):
        for y in range(pilImage.height):
            rgb = pilImage.getpixel((x, y))
            d[rgb] = d.get(rgb, 0) + 1
    return d

#only used in image
def pixelate(image, pixelsWide, pixelsTall, width, height):
    image = image.resize((pixelsWide, pixelsTall), Image.NEAREST)
    return image.resize((width, height), Image.NEAREST)

#changes pixelsWide and pixelsTall when bar is slid in increments of 5 pixels
#used in both
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

#changes image size based on pixels (they should be square)
#only used in image
def changeImageDimensions(app):
    app.pixelWidth = app.pixelHeight = 10
    app.imageWidth = app.pixelWidth * app.imagePixelsWide
    app.imageHeight = app.pixelHeight * app.imagePixelsTall
    
#used in both
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
#from ChatGPT
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
####DRAWS THE GRID####
#modified from Tetris creative task
def drawGrid(app, board, boardLeft, boardTop):
    drawBoard(app, board, boardLeft, boardTop)
    drawBoardBorder(app, board)
def drawBoard(app, board, boardLeft, boardTop):
    for row in range(len(board)):
        for col in range(len(board[row])):
            drawCell(app, row, col, board[row][col], boardLeft, boardTop)
def drawBoardBorder(app, board):
  #draw the board outline (with double-thickness)
  drawRect(app.width/2, app.height/2, len(board[0]) * 10, len(board) * 10,
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

#adjust grids
def image_change(app):
    (app.imageWidthSlider, app.imageHeightSlider, app.imagePixelsWide, app.imagePixelsTall) = calculateGridDimensions(app.imageWidthSlider, 
                                                     app.imageHeightSlider,
                                                     app.imagePixelsWide, app.imagePixelsTall)
    changeImageDimensions(app)
    print(app.imagePixelsWide, app.imagePixelsTall)
    app.imageBoard = resizingBoard(app, app.imageBoard, app.imagePixelsWide, app.imagePixelsTall)
    app.imageBoardLeft = app.width/2 - app.imagePixelsWide * 10 / 2
    app.imageBoardTop = app.height/2 - app.imagePixelsTall * 10 / 2

    pilImage = pixelate(app.pilImage, app.imagePixelsWide, 
                        app.imagePixelsTall, app.imageWidth, app.imageHeight)
    
    #currently cannot "save" drawings made prior to resizing
    for row in range(app.imagePixelsTall):
        for col in range(app.imagePixelsWide):
            color = pilImage.getpixel((col * 10 + 5, row * 10 + 5))
            rgbColor = rgb(color[0], color[1], color[2])
            app.imageBoard[row][col] = rgbColor

def diy_change(app):
    app.diyWidthSlider, app.diyHeightSlider, app.diyPixelsWide, app.diyPixelsTall = calculateGridDimensions(app.diyWidthSlider, 
                                                   app.diyHeightSlider, 
                                                   app.diyPixelsWide, app.diyPixelsTall)
    
    app.diyBoard = resizingBoard(app, app.diyBoard, app.diyPixelsWide, app.diyPixelsTall)
    app.diyBoardLeft = app.width/2 - app.diyPixelsWide * 10 / 2
    app.diyBoardTop = app.height/2 - app.diyPixelsTall * 10 / 2

####NECESSARY FOR BOTH####
def resizingBoard(app, board, pixelsWide, pixelsTall):
    oldBoard = board
    #create new board of the updated size
    newBoard = [([None] * pixelsWide) for row in range(pixelsTall)]
    #copy existing values into new board
    #may need to change logic later
    for row in range(min(len(oldBoard), len(newBoard))):
        for col in range(min(len(oldBoard[0]), len(newBoard[0]))):
            newBoard[row][col] = oldBoard[row][col]
    return newBoard

def designingMousePress(app, mouseX, mouseY, widthSlider, heightSlider):
    #changes width
    if 130 <= mouseY <= 160 and 25 <= mouseX <= 175:
        widthSlider = mouseX
    #changes height
    elif 210 <= mouseY <= 240 and 25 <= mouseX <= 175:
        heightSlider = mouseX
    #if back button pressed
    elif 50 <= mouseX <= 150 and 450 <= mouseY <= 480:
        setActiveScreen('start')
    return widthSlider, heightSlider

def mouseMove(app, mouseX, mouseY, colorList):
    if 700 <= mouseX <= 720:
        if 0 <= mouseY <= 20:
            app.colorSelect = colorList[0]
        elif 50 <= mouseY <= 70:
            app.colorSelect = colorList[1]
        elif 100 <= mouseY <= 120:
            app.colorSelect = colorList[2]
        elif 150 <= mouseY <= 170:
            app.colorSelect = colorList[3]
        elif 200 <= mouseY <= 220:
            app.colorSelect = colorList[4]
        elif 250 <= mouseY <= 270:
            app.colorSelect = colorList[5]
        elif 300 <= mouseY <= 320:
            app.colorSelect = colorList[6]
        elif 350 <= mouseY <= 370:
            app.colorSelect = colorList[7]
        elif 400 <= mouseY <= 420:
            app.colorSelect = colorList[8]
        elif 450 <= mouseY <= 470:
            app.colorSelect = colorList[9]
        else:
            app.colorSelect = None
    else:
        app.colorSelect = None    

def isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
    if (boardLeft <= mouseX <= boardLeft + pixelsWide * 10 and
        boardTop <= mouseY <= boardTop + pixelsTall * 10):
            return True
    return False

def findSquare(app, mouseX, mouseY, board, boardLeft, boardTop):
    for row in range(len(board)):
        for col in range(len(board[0])):
            cellLeft, cellTop = getCellLeftTop(app, row, col, boardLeft, boardTop)
            if cellLeft <= mouseX <= cellLeft + 10 and cellTop <= mouseY <= cellTop + 10:
                return row, col

####DIY SCREEN####
def diy_onMouseMove(app, mouseX, mouseY):
    app.diyMouseX, app.diyMouseY = mouseX, mouseY
    mouseMove(app, mouseX, mouseY, app.diyColors)

def diy_onMouseDrag(app, mouseX, mouseY):
    if isSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall):
        row, col = findSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop)
        app.diyBoard[row][col] = app.diyColorSelect

def diy_onMousePress(app, mouseX, mouseY):
    if app.colorSelect != None:
        app.diyColorSelect = app.colorSelect
    app.diyWidthSlider, app.diyHeightSlider = designingMousePress(app, mouseX, mouseY, app.diyWidthSlider, app.diyHeightSlider)
    diy_change(app)

def diy_redrawAll(app):
    drawGrid(app, app.diyBoard, app.diyBoardLeft, app.diyBoardTop)
    drawControls(app, app.diyWidthSlider, app.diyHeightSlider, app.diyPixelsWide, app.diyPixelsTall)
    #draws selected colors
    for i in range(len(app.diyColors)):
        drawRect(700, 50 * i, 20, 20, fill = app.diyColors[i], border = 'black')
    #if mouse hovering over color, draw color selector
    if app.colorSelect != None:
        drawTeardrop(app.diyMouseX, app.diyMouseY, 10, 10, app.colorSelect)

####IMAGE SCREEN####
def image_onMousePress(app, mouseX, mouseY):
    if app.colorSelect != None:
        app.imageColorSelect = app.colorSelect

    oldWidth, oldHeight = app.imageWidthSlider, app.imageHeightSlider
    app.imageWidthSlider, app.imageHeightSlider = designingMousePress(app, mouseX, mouseY, app.imageWidthSlider, app.imageHeightSlider)
    if oldWidth != app.imageWidthSlider or oldHeight != app.imageHeightSlider:
        image_change(app)

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
    if app.colorSelect != None:
        app.colorSelect = rgb(app.colorSelect[0], app.colorSelect[1], app.colorSelect[2])

def image_redrawAll(app):
    # drawImage(app.cmuImage, app.width/2, app.height/2, align = 'center')
    drawControls(app, app.imageWidthSlider, app.imageHeightSlider, app.imagePixelsWide, app.imagePixelsTall)
    drawGrid(app, app.imageBoard, app.imageBoardLeft, app.imageBoardTop)
    #draws most common colors
    for i in range(len(app.mostFrequentHex)):
        rgbVal = app.mostFrequentHex[i]
        color = rgb(rgbVal[0], rgbVal[1], rgbVal[2])
        drawRect(700, 50 * i, 20, 20, fill = color, border = 'black')

    if app.colorSelect != None:
        drawTeardrop(app.imageMouseX, app.imageMouseY, 10, 10, app.colorSelect)

####START SCREEN####
def start_onMousePress(app, mouseX, mouseY):
    if app.width/12 <= mouseX <= app.width*5/12 and app.height*102/160 <= mouseY <= app.height*122/160:
        app.diy = True
        setActiveScreen('diy')
    elif app.width*7/12 <= mouseX <= app.width*11/12 and app.height*102/160 <= mouseY <= app.height*122/160:
        setActiveScreen('image')

def start_redrawAll(app):
    drawLabel('DIY or image?', app.width/2, app.height/2, size = 40)
    drawRect(app.width/4, app.height * 7/10, app.width/3, app.height/8, fill = 'pink', align = 'center')
    drawLabel('DIY', app.width/4, app.height * 7/10, size = 25)
    drawRect(app.width*3/4, app.height * 7/10, app.width/3, app.height/8, fill = 'pink', align = 'center')
    drawLabel('Image', app.width*3/4, app.height * 7/10, size = 25)

def main():
    runAppWithScreens(initialScreen = 'start', width = app.width, height = app.height)

main()