####FEATURES I STILL NEED TO DO####
###################################
# "move" selection on diy screen
    # rectangle shape is not preserved
# drag in specific shapes on diy screen
    # make them better
# scroll bar
# maybe random image chooser based on categories user selects
# ui
# no magic numbers


#TOMORROW
#-color wheel class
#-make color selection work

#all backgrounds and images used in backgrounds: 
#https://www.canva.com/design/DAGYShQAujk/OxH7z5xjpadCdniyeZAEgg/edit?utm_content=DAGYShQAujk&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton

#link to all image files: https://drive.google.com/file/d/17dOcwpKakfRUy7UWX38UtOujxa9dMTBI/view?usp=sharing 

#image citations: https://docs.google.com/document/d/1fT-UJPKzTpPlPjaDBd1HXdmDL1TBXOJUnp3GDQunrz8/edit?usp=sharing

from cmu_graphics import *
from PIL import Image
# import copy
import os
import time
from drawGrid import drawGrid
from hexCodeFunctions import calculateMostFrequentHex, calculateHexCodes
from squareFunctions import isSquare, findSquare
from floodFill import fillShape
from buttons import Button
from scrollbar import Scrollbar
from slider import Slider, Handle
from imageIcons import Icon

def diyScreenVariables(app):
    #sets necessary variables for controlling size/pixels of diy
    app.diyPixelsWide, app.diyPixelsTall = 27, 27
    app.diyWidthSlider = app.diyHeightSlider = 150, 350

    #variables for drawing board
    app.diyBoard = [([None] * app.diyPixelsWide) for row in range(app.diyPixelsTall)]
    app.diyBoardLeft = app.width/2 - app.diyPixelsWide * 5 
    app.diyBoardTop = app.height/2 - app.diyPixelsTall * 5

    app.diyColorSelect = None

    #colors on screen
    app.diyColors = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 'purple', 'white', 'black', 'brown']

def imageScreenVariables(app):
    #https://www.freepik.com/free-vector/gradient-pink-green-background_40130129.htm
    app.pilImage = Image.open(os.path.join('images', '2.png')).convert('RGB')

    app.originalImageWidth, app.originalImageHeight = app.pilImage.size

    app.imageWidth, app.imageHeight = app.pilImage.size

    #sets necessary variables for controlling size/pixels of image
    app.imagePixelsWide, app.imagePixelsTall = 27, 27
    app.imageWidthSlider = app.imageHeightSlider = 100

    #changes size of image so the pixels are square
    changeImageDimensions(app)

    #create dictionary to store all the hex codes and the frequency they appear
    app.hexCodeToFrequency = calculateHexCodes(app, app.pilImage)
    app.mostFrequentHex = calculateMostFrequentHex(app)

    #variables for drawing board
    app.imageBoard = [([None] * app.imagePixelsWide) for row in range(app.imagePixelsTall)]
    app.imageBoardLeft = app.width/2 - app.imagePixelsWide * 5
    app.imageBoardTop = app.height/2 - app.imagePixelsTall * 5
    
    pilImage = pixelate(app.pilImage, app.imagePixelsWide, 
                        app.imagePixelsTall, app.imageWidth, app.imageHeight)
    
    updateImageBoard(app, pilImage)

    #variables for color select
    app.imageColorSelect = None

    app.preserveAspectRatio = False

def doubleClickVariables(app):
    app.doubleClickThreshold = 300
    app.clickPosition = (0, 0)
    app.lastClickTime = 0
    app.doubleClickColor = None

def editingVariables(app):
    #tracks color hoovering over
    app.colorSelect = None

    app.selectColorDropper = False
    app.selectColorDropperHighlight = False

    app.selectColorWheel = False
    app.selectColorWheelHighlight = False

    app.colorDropperColor = None
    #https://www.clipartmax.com/download/m2i8G6N4A0N4A0H7_color-color-wheel-wheel-icon-color-wheel-transparent-background/ 
    wheel = Image.open('colorwheel.png')
    app.colorWheel = wheel.resize((100, 100))
    app.selectedFromColorWheel = False
    app.selectedColorFromWheel = (0, 0, 0)

    app.dragSelection = False
    app.dragHighlight = False
    app.dragStart = 0, 0
    app.dragEnd = 0, 0
    app.drawingDrag = False

    app.moveShape = False
    app.moveStart = 0, 0
    app.moveEnd = 0, 0
    app.selectionWidth = 0
    app.selectionHeight = 0

    app.fillSelection = False
    app.fillHighlight = False
    app.filling = False

    app.ovalTool = False
    app.ovalHighlight = False
    app.ovalToolStart = 0, 0
    app.ovalToolEnd = 0, 0
    app.drawingOval = False

    app.rectTool = False
    app.rectHighlight = False
    app.rectToolStart = 0, 0
    app.rectToolEnd = 0, 0
    app.drawingRect = False

    app.drawShape = False
    
    app.eraser = False
    app.eraserHighlight = False
    
    app.boardSelected = set()

def screenVariables(app):
    app.width = 800
    app.height = 500
    app.mouseX, app.mouseY = 0, 0        
    app.prevScreen = 'welcome'
    app.currentScreen = 'welcome'

def buttons(app):
    #used in welcome screen
    app.instructionsButton = Button('Instructions', app.width/3, app.height*7/16,
                                     app.width/3, app.height/8, 25)
    app.startButton = Button('Start', app.width/3, app.height*10/16, app.width/3, 
                             app.height/8, 25 )

    #used in start screen
    app.diyButton = Button('Create Your Own', app.width/12, app.height/7, 
                           app.width/3, app.height/8, 25)
    app.imageButton = Button('Image', app.width*7/12, app.height/7, 
                             app.width/3, app.height/8, 25)

    #used in image options screen
    app.createButton = Button('Create', 650, 450, 100, 30, 15)

    #used in image and diy screens
    app.generateButton = Button('Generate', 650, 450, 100, 30, 15)

    #used in almost all screens
    app.backButton = Button('Back', 50, 450, 100, 30, 15)

def sliders(app):
    #draw backgrounds
    app.widthSlider = Slider(770, 75)
    app.heightSlider = Slider(770, 275)
    #draw controllers
    app.sliderCenter = (app.widthSlider.leftEdge * 2 + app.widthSlider.width)/2
    app.diyWidthSliderHandle = Handle(app.sliderCenter, 150, app.widthSlider)
    app.diyHeightSliderHandle = Handle(app.sliderCenter, 350, app.heightSlider)
    app.imageWidthSliderHandle = Handle(app.sliderCenter, 150, app.widthSlider)
    app.imageHeightSliderHandle = Handle(app.sliderCenter, 350, app.heightSlider)

def toolIcons(app):
    #keep even borders (of 15px) on each side, takes into account border (3.25 px)
    offset = 3.25
    leftEdge = 15 - offset
    width = height = 30

    #selected color box
    app.selectedColorTop = app.height/2 - height*4 - offset*4
    app.selectedColorLeft = leftEdge - offset
    app.selectedColorWidth = app.selectedColorHeight = width + offset*2

    #color wheel icon, https://www.pngwing.com/en/free-png-zxmtj 
    colorTopEdge = app.height/2 - height*3 - offset*3
    app.colorIcon = Icon('color_wheel', leftEdge, colorTopEdge, width, height)

    #color dropper, https://www.iconarchive.com/show/ios7-icons-by-icons8/Editing-Color-Dropper-icon.html
    dropperTopEdge = app.height/2 - height*2 - offset*2
    app.colorDropperIcon = Icon('color_dropper', leftEdge, dropperTopEdge, 
                                width, height)

    #eraser tool, https://iconmonstr.com/eraser-2-png/
    eraserTopEdge = app.height/2 - height - offset
    app.eraserIcon = Icon('eraser', leftEdge, eraserTopEdge, width, height)

    #fill tool, https://iconmonstr.com/paint-bucket-10-png/
    fillTopEdge = app.height/2 #centered!!
    app.fillIcon = Icon('fill', leftEdge, fillTopEdge, width, height)

    #lasso tool, https://iconmonstr.com/cursor-11-png/
    lassoTopEdge = app.height/2 + height + offset
    app.lassoIcon = Icon('lasso', leftEdge, lassoTopEdge, width, height)

    #square tool, https://iconmonstr.com/eraser-2-png/
    squareTopEdge = app.height/2 + height*2 + offset*2
    app.squareIcon = Icon('square', leftEdge, squareTopEdge, width, height)

    #circle tool, 
    circleTopEdge = app.height/2 + height*3 + offset*3
    app.circleIcon = Icon('circle', leftEdge, circleTopEdge, width, height)

def onAppStart(app):
    app.setMaxShapeCount(3000)
    screenVariables(app)
    diyScreenVariables(app)
    imageScreenVariables(app)
    editingVariables(app)
    doubleClickVariables(app)
    buttons(app)
    sliders(app)
    toolIcons(app)

    # app.scrollbar = Scrollbar(8)

####USED ON IMAGE SCREEN
def pixelate(image, pixelsWide, pixelsTall, width, height):
    image = image.resize((pixelsWide, pixelsTall), Image.NEAREST)
    return image.resize((width, height), Image.NEAREST)

#update app.imageBoard with the appropriate colors
def updateImageBoard(app, pilImage):
    for row in range(app.imagePixelsTall):
        for col in range(app.imagePixelsWide):
            color = pilImage.getpixel((col * 10 + 5, row * 10 + 5))
            rgbColor = rgb(color[0], color[1], color[2])
            app.imageBoard[row][col] = rgbColor

#changes image size based on pixels (they should be square)
def changeImageDimensions(app):
    app.pixelWidth = app.pixelHeight = 10
    app.imageWidth = app.pixelWidth * app.imagePixelsWide
    app.imageHeight = app.pixelHeight * app.imagePixelsTall

####USED IN DIY SCREEN
def updateColor(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
    if not app.drawingRect and not app.drawingOval and not app.moveShape and not app.drawingDrag and not app.filling:
        if isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
            row, col = findSquare(app, mouseX, mouseY, board, boardLeft, boardTop)
            board[row][col] = app.diyColorSelect
    #doesn't work properly
    elif app.moveShape:
        xStart, yStart = app.moveStart
        xEnd, yEnd = app.moveEnd
        xDif = (xStart - xEnd)
        yDif = (yStart - yEnd)
        # newSelected = set()
        for row, col in app.boardSelected:
            newRow, newCol = row + yDif//10, col + xDif//10
            if isSquare(app, newRow * 10, newCol * 10, board, boardLeft, boardTop, pixelsWide, pixelsTall):
                board[newRow][newCol] = board[row][col]
                # newSelected.add((newRow, newCol))
                board[row][col] = None
        # app.boardSelected = newSelected
    else:
        for square in app.boardSelected:
            row, col = square
            board[row][col] = app.diyColorSelect
        # else:

            
    return board

##ADJUSTS GRIDS##
def image_change(app):
    # (app.imageWidthSlider, app.imageHeightSlider, app.imagePixelsWide, 
    #  app.imagePixelsTall) = calculateGridDimensions(app, app.imageWidthSlider, 
    #                                                 app.imageHeightSlider,
    #                                                 app.imagePixelsWide, app.imagePixelsTall)

    changeImageDimensions(app)
    app.imageBoard = resizingBoard(app, app.imageBoard, app.imagePixelsWide, app.imagePixelsTall)
    app.imageBoardLeft = app.width/2 - app.imagePixelsWide*5
    app.imageBoardTop = app.height/2 - app.imagePixelsTall*5

    pilImage = pixelate(app.pilImage, app.imagePixelsWide, 
                        app.imagePixelsTall, app.imageWidth, app.imageHeight)
    
    for row in range(app.imagePixelsTall):
        for col in range(app.imagePixelsWide):
            color = pilImage.getpixel((col * 10 + 5, row * 10 + 5))
            rgbColor = rgb(color[0], color[1], color[2])
            app.imageBoard[row][col] = rgbColor

def diy_change(app):
    # (app.diyWidthSlider, app.diyHeightSlider, app.diyPixelsWide, 
    # app.diyPixelsTall) = calculateGridDimensions(app, app.diyWidthSlider, 
    #                                                app.diyHeightSlider, 
    #                                                app.diyPixelsWide, app.diyPixelsTall)
    
    app.diyBoard = resizingBoard(app, app.diyBoard, app.diyPixelsWide, app.diyPixelsTall)
    app.diyBoardLeft = app.width/2 - app.diyPixelsWide * 5
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

def distance(x0, y0, x1, y1):
    return ((x0 - x1)**2 + (y0 - y1)**2)**0.5

def updateMouse(app, mouseX, mouseY):
    app.mouseX, app.mouseY = mouseX, mouseY

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
    app.backButton.drawButton()
    app.generateButton.drawButton()

    drawLabel('Tools', 100, 320)

    #lasso tool, https://iconmonstr.com/cursor-11-png/
    drawImage('move icon.png', 28.25, 348.25, width = 30, height = 30)
    #fill tool, https://iconmonstr.com/paint-bucket-10-png/
    drawImage('fill icon.png', 65.75, 348.25, width = 30, height = 30)
    #square tool, https://iconmonstr.com/eraser-2-png/
    drawImage('square icon.png', 103.25, 348.25, width = 30, height = 30)
    #circle tool, https://iconmonstr.com/circle-6-svg/
    drawImage('circle icon.png', 141.75, 349.25, width = 28, height = 28)

    #draws outlines
    for i in range(4):
        drawRect(25 + i * 37.5, 345, 37.5, 37.5, fill = None, border = 'black', borderWidth = 1)
    drawRect(25, 345, 150, 37.5, fill = None, border = 'black')

def drawColorPanel(app, colorList, mouseX, mouseY, leftEdge, topEdge):
    # drawLabel('Color Bank', 678, 80, align = 'center')

    #draw eraser, https://iconmonstr.com/eraser-2-png/
    # drawImage('eraser icon.png', 745.5, 157.2, width = 15, height = 15)
    # drawRect(743, 155, 20, 20, fill = None, border = 'black')

    #draws colors
    for i in range(len(colorList)):
        row, col = i % 5, i // 5
        width, height = 20, 20
        borderWidth = 2
        if isinstance(colorList[i], str):
            drawRect(leftEdge + row*width, topEdge + col*height, width +
                     borderWidth, height + borderWidth, fill = colorList[i], 
                     border = 'black')
        else:
            rgbVal = colorList[i]
            color = rgb(rgbVal[0], rgbVal[1], rgbVal[2])
            drawRect(leftEdge + row*width, topEdge + col*height, width + 
                     borderWidth, height + borderWidth, fill = color, 
                     border = 'black')
    
    # #selected color
    # if app.colorSelect != None:
    #     drawRect(738, 120, 30, 30, fill = app.colorSelect, border = 'black')
    # elif app.currentScreen == 'diy':
    #     drawRect(738, 120, 30, 30, fill = app.diyColorSelect, border = 'black')
    # elif app.currentScreen == 'image':
    #     drawRect(738, 120, 30, 30, fill = app.imageColorSelect, border = 'black')

    #color dropper
    #image from Icon Archive
    # drawImage('color dropper.png', 670.5, 156.5, width = 15, height = 15)
    # drawRect(668, 154, 20, 20, fill = None, border = 'black')

    # #color wheel
    # #https://www.pngwing.com/en/free-png-zxmtj 
    # drawImage('colorwheel icon.png', 688.5, 156.5, width = 15, height = 15)
    # drawRect(686, 154, 20, 20, fill = None, border = 'black')

    #draws color wheel
    # if app.selectColorWheel == True:
    #     #https://www.clipartmax.com/download/m2i8G6N4A0N4A0H7_color-color-wheel-wheel-icon-color-wheel-transparent-background/ 
    #     drawImage(CMUImage(app.colorWheel), 645, 230)
    #     drawRect(620, 205, 150, 200, fill = None, border = 'black')
    #     if distance(mouseX, mouseY, 695, 280) <= 50 and app.colorSelect != None:
    #         drawRect(635, 350, 120, 20, fill = gradient('white', app.colorSelect, 'black', start = 'left'), border = 'black')
    #     elif app.selectedFromColorWheel == True:
    #         color = rgb(app.selectedColorFromWheel[0], app.selectedColorFromWheel[1], app.selectedColorFromWheel[2])
    #         drawRect(635, 350, 120, 20, fill = gradient('white', color, 'black', start = 'left'), border = 'black')
    #     else:
    #         drawRect(635, 350, 120, 20, fill = gradient('white', 'black', start = 'left'), border = 'black')

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

    #check if eraser selected
    if 743 <= mouseX <= 763 and 155 <= mouseY <= 175:
        if app.prevScreen == 'diy':
            app.diyColorSelect = None
        elif app.prevScreen == 'image':
            app.imageColorSelect = None

# def drawUserColorSelection(app, mouseX, mouseY):
#     if app.selectColorDropper == True:
#         drawImage('color dropper.png', mouseX, mouseY, width = 15, height = 15)

# def checkEditingTools(app, mouseX, mouseY):
#     if 345 <= mouseY <= 382:
#         if 25 <= mouseX < 62:
#             app.dragSelection = not app.dragSelection
#         elif 62 <= mouseX < 100:
#             app.fillSelection = not app.fillSelection
#         elif 100 <= mouseX < 137:
#             app.rectTool = not app.rectTool
#         elif 137 <= mouseX <= 175:
#             app.ovalTool = not app.ovalTool

def drawIconTools(app, mouseX, mouseY):
    if app.selectColorWheel:
        leftEdge = topEdge = 100
        borderWidth = 25
        width = 150
        height = 250
        drawRect(leftEdge - borderWidth, topEdge - borderWidth, width, height, 
                 fill = 'white', border = 'black')
        drawImage(CMUImage(app.colorWheel), leftEdge, topEdge)

        #draws color panels
        if app.currentScreen == 'diy':
            drawColorPanel(app, app.diyColors, mouseX, mouseY, leftEdge, 260)
        elif app.currentScreen == 'image':
            drawColorPanel(app, app.mostFrequentHex, mouseX, mouseY, leftEdge, 260)

        #draws gradients
        rectLeft, rectTop= leftEdge - 10, topEdge + 120
        rectWidth, rectHeight = 120, 20
        circleRadius = 50
        #if mouse is hoovering over the gradient
        if (distance(mouseX, mouseY, (rectLeft*2 + rectWidth)/2, 
                    (rectTop*2 + rectHeight)/2) <= circleRadius 
                    and app.colorSelect) != None:
            drawRect(rectLeft, rectTop, rectWidth, rectHeight, fill = 
                     gradient('white', app.colorSelect, 'black', start = 'left'), 
                     border = 'black')
        elif app.selectedFromColorWheel == True:
            color = rgb(app.selectedColorFromWheel[0], 
                        app.selectedColorFromWheel[1], app.selectedColorFromWheel[2])
            drawRect(rectLeft, rectTop, rectWidth, rectHeight, fill = 
                     gradient('white', color, 'black', start = 'left'), 
                     border = 'black')
        else:
            drawRect(rectLeft, rectTop, rectWidth, rectHeight, fill = 
                     gradient('white', 'black', start = 'left'), border = 'black')
    elif app.selectColorDropper:
        app.colorDropperIcon.drawMovingIcon(mouseX, mouseY)
    elif app.eraser:
        app.eraserIcon.drawMovingIcon(mouseX, mouseY)
    elif app.fillSelection:
        app.fillIcon.drawMovingIcon(mouseX, mouseY)
    elif app.dragSelection:
        app.lassoIcon.drawMovingIcon(mouseX, mouseY)
    elif app.rectTool:
        app.squareIcon.drawMovingIcon(mouseX, mouseY)
    elif app.ovalTool:
        app.circleIcon.drawMovingIcon(mouseX, mouseY)

#double click check from chatGPT, changing colors not
def checkDoubleClick(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall, colorSelect):
    #checks if click is in bounds
    if boardLeft <= mouseX <= boardLeft + pixelsWide * 10 and boardTop <= mouseY <= boardTop + pixelsTall * 10:
        clickedRow, clickedCol = findSquare(app, mouseX, mouseY, board, boardLeft, boardTop)
        currentTime = time.time() * 1000
        timeSinceLastClick = currentTime - app.lastClickTime
        if timeSinceLastClick <= app.doubleClickThreshold:
            if abs(mouseX - app.clickPosition[0]) < 10 and abs(mouseY - app.clickPosition[1]) < 10:
                for row in range(len(board)):
                    for col in range(len(board[0])):
                        if board[row][col] == app.doubleClickColor:
                            board[row][col] = colorSelect
        # Update the last click time and position
        app.lastClickTime = currentTime
        app.clickPosition = (mouseX, mouseY)

def rectTool(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
        app.rectToolEnd = mouseX, mouseY
        xStart, yStart = app.rectToolStart
        for x in range(min(xStart, mouseX), max(xStart, mouseX), 10):
            for y in range(min(yStart, mouseY), max(yStart, mouseY), 10):
                if isSquare(app, x, y, board, boardLeft, boardTop, pixelsWide, pixelsTall):
                    row, col = findSquare(app, x, y, board, boardLeft, boardTop)
                    app.boardSelected.add((row, col))

def ovalTool(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
    app.ovalToolEnd = mouseX, mouseY
    xStart, yStart = app.ovalToolStart
    a = abs(mouseX - xStart) / 2
    b = abs(mouseY - yStart) / 2
    xCenter = (mouseX + xStart) / 2
    yCenter = (mouseY + yStart) / 2
    for x in range(xStart, mouseX, 10):
        for y in range(yStart, mouseY, 10):
            #checks if is in oval, logic from chatGPT
            if (((x - xCenter)**2 / a**2) + ((y - yCenter)**2 / b**2) <= 1):
                if isSquare(app, x, y, board, boardLeft, boardTop, pixelsWide, pixelsTall):
                    row, col = findSquare(app, x, y, board, boardLeft, boardTop)
                    app.boardSelected.add((row, col))

def drawSliders(app):
    #box showing squares wide/tall
    width = 20
    height = 40
    drawRect(app.sliderCenter, app.height/2, width, height, fill = None, 
             border = 'black', align = 'center')
    drawLine(app.sliderCenter - width/2, app.height/2, app.sliderCenter + 
             width/2, app.height/2)
    
    app.widthSlider.draw()
    app.heightSlider.draw()
    if app.currentScreen == 'diy':
        app.diyWidthSliderHandle.draw()
        app.diyHeightSliderHandle.draw()
        drawLabel(f'{app.diyPixelsWide}', app.sliderCenter, app.height/2 - 
                  width/2, size = 10)
        drawLabel(f'{app.diyPixelsTall}', app.sliderCenter, app.height/2 + 
                  width/2, size = 10)
    elif app.currentScreen == 'image':
        app.imageWidthSliderHandle.draw()
        app.imageHeightSliderHandle.draw()
        drawLabel(f'{app.imagePixelsWide}', app.sliderCenter, app.height/2 -
                  width/2, size = 10)
        drawLabel(f'{app.imagePixelsTall}', app.sliderCenter, app.height/2 + 
                  width/2, size = 10)

def drawIcons(app):
    #selected color square
    drawRect(app.selectedColorLeft, app.selectedColorTop, app.selectedColorWidth, 
             app.selectedColorHeight, fill = app.colorSelect, border = 'black')
    app.colorIcon.drawIcon()
    app.colorDropperIcon.drawIcon()
    app.eraserIcon.drawIcon()
    app.fillIcon.drawIcon()
    app.lassoIcon.drawIcon()
    app.squareIcon.drawIcon()
    app.circleIcon.drawIcon()

def checkIconTools(app):
    if app.colorIcon.isSelected(app.mouseX, app.mouseY):
        app.selectColorWheel = not app.selectColorWheel
    elif app.colorDropperIcon.isSelected(app.mouseX, app.mouseY):
        app.selectColorDropper = not app.selectColorDropper
    elif app.eraserIcon.isSelected(app.mouseX, app.mouseY):
        app.eraser = not app.eraser
    elif app.fillIcon.isSelected(app.mouseX, app.mouseY):
        app.fillSelection = not app.fillSelection
    elif app.lassoIcon.isSelected(app.mouseX, app.mouseY):
        app.dragSelection = not app.dragSelection
    elif app.squareIcon.isSelected(app.mouseX, app.mouseY):
        app.rectTool = not app.rectTool
    elif app.circleIcon.isSelected(app.mouseX, app.mouseY):
        app.ovalTool = not app.ovalTool
    else:
        app.selectColorWheel = app.selectColorDropper = app.dragSelection = app.fillSelection = app.ovalTool = app.rectTool = app.eraser = False

def checkIconHighlights(app):
    if app.colorIcon.isSelected(app.mouseX, app.mouseY):
        app.selectColorWheelHighlight = True
    elif app.colorDropperIcon.isSelected(app.mouseX, app.mouseY):
        app.selectColorDropperHighlight = True
    elif app.eraserIcon.isSelected(app.mouseX, app.mouseY):
        app.eraserHighlight = True
    elif app.fillIcon.isSelected(app.mouseX, app.mouseY):
        app.fillHighlight = True
    elif app.lassoIcon.isSelected(app.mouseX, app.mouseY):
        app.dragHighlight = True
    elif app.squareIcon.isSelected(app.mouseX, app.mouseY):
        app.rectHighlight = True
    elif app.circleIcon.isSelected(app.mouseX, app.mouseY):
        app.ovalHighlight = True
    else: 
        app.selectColorWheelHighlight = app.selectColorDropperHighlight = app.eraserHighlight = app.fillHighlight = app.dragHighlight = app.rectHighlight = app.ovalHighlight = False
        
def drawIconHighlights(app):
    if app.selectColorWheelHighlight:
        app.colorIcon.drawSelected()
    elif app.selectColorDropperHighlight:
        app.colorDropperIcon.drawSelected()
    elif app.eraserHighlight:
        app.eraserIcon.drawSelected()
    elif app.fillHighlight:
        app.fillIcon.drawSelected()
    elif app.dragHighlight:
        app.lassoIcon.drawSelected()
    elif app.rectHighlight:
        app.squareIcon.drawSelected()
    elif app.ovalHighlight:
        app.circleIcon.drawSelected()

def changeSliders(app, mouseX, mouseY, handle):
    return handle.updateSquares(mouseX, mouseY)

####DIY SCREEN####
def diy_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'diy'
    updateMouse(app, mouseX, mouseY)

    checkIconHighlights(app)

    #for double click
    if isSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, 
                app.diyPixelsWide, app.diyPixelsTall):
        row, col = findSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                              app.diyBoardTop)
        app.doubleClickColor = app.diyBoard[row][col]

    mouseMove(app, mouseX, mouseY, app.diyColors)

    if isSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, 
                app.diyPixelsWide, app.diyPixelsTall):
        if app.selectColorDropper == True:
            row, col = findSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, app.diyBoardTop)
            findColorDropperColor(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                                  app.diyBoardTop, app.diyBoardLeft, app.diyPixelsTall)
            app.colorSelect = app.diyBoard[row][col]
        else:
            app.colorDropperColor = None
    
    getColorWheelColor(app, mouseX, mouseY)

def diy_onMouseDrag(app, mouseX, mouseY):
    if app.drawingRect:
        rectTool(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                 app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)

        #need to find way to make sure if user moves mouse the selected squares change too
        #maybe also make it so user can go other way too

    if app.drawingOval:
        ovalTool(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                 app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)

        #need to find way to make sure if user moves mouse the selected squares change too

    #size of move is not being preserved?????
    if app.moveShape:
        xStart, yStart = app.moveStart
        xOffset = mouseX - xStart
        yOffset = mouseY - yStart

        # Update the rectangle's position
        startX, startY = app.dragStart
        app.dragStart = (startX + xOffset, startY + yOffset)
        app.dragEnd = (startX + xOffset + app.selectionWidth, startY + yOffset + app.selectionHeight)
        app.moveStart = mouseX, mouseY


    if app.drawingDrag:
        app.dragEnd = mouseX, mouseY
        # xStart, yStart = app.dragStart
        # for x in range(xStart, mouseX, 10):
        #     for y in range(yStart, mouseY, 10):
        #         if isSquare(app, x, y, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall):
        #             row, col = findSquare(app, x, y, app.diyBoard, app.diyBoardLeft, app.diyBoardTop)
        #             app.boardSelected.add((row, col))
    # print(app.boardSelected)       

    app.diyBoard = updateColor(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                               app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)

def diy_onMousePress(app, mouseX, mouseY):
    if app.rectTool:
        app.drawingRect = True

    if app.ovalTool:
        app.drawingOval = True

    if app.dragSelection:
        app.drawingDrag = True
        app.moveShape = False

    if app.fillSelection:
        app.filling = True

    # app.selectColorDropper = app.dragSelection = app.fillSelection = app.ovalTool = app.rectTool = False
    app.boardSelected = set()

    checkIconTools(app)

    if app.colorSelect != None:
        app.diyColorSelect = app.colorSelect

    #change width and height sliders
    app.diyPixelsWide = changeSliders(app, mouseX, mouseY, app.diyWidthSliderHandle)
    app.diyPixelsTall = changeSliders(app, mouseX, mouseY, app.diyHeightSliderHandle)

    # app.diyWidthSlider, app.diyHeightSlider = mousePress(app, mouseX, mouseY, 
    #                                                      app.diyWidthSlider, app.diyHeightSlider)
    diy_change(app)
    app.diyBoard = updateColor(app, mouseX, mouseY, app.diyBoard, 
                               app.diyBoardLeft, app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)
    checkColorControls(app, mouseX, mouseY)
    # checkEditingTools(app, mouseX, mouseY)
    checkDoubleClick(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                     app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall, app.diyColorSelect)

    if app.drawingRect:
        app.rectToolStart = mouseX, mouseY
        app.rectToolEnd = mouseX + 1, mouseY + 1

    if app.drawingOval:
        app.ovalToolStart = mouseX, mouseY
        app.ovalToolEnd = mouseX + 1, mouseY + 1

    if app.filling:
        if isSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                    app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall):
            app.diyBoard = fillShape(app, app.diyColorSelect, mouseX, mouseY, 
                                     app.diyBoard, app.diyBoardLeft, app.diyBoardTop)

    if app.drawingDrag:
        startX, startY = min(app.dragStart[0], app.dragEnd[0]), min(app.dragStart[1], app.dragEnd[1])
        endX, endY = max(app.dragStart[0], app.dragEnd[0]), max(app.dragStart[1], app.dragEnd[1])
        if startX < mouseX < endX and startY < mouseY < endY:
            app.moveShape = True
            app.moveStart = mouseX, mouseY
            app.selectionWidth = endX - startX
            app.selectionHeight = endY - startY
        else: 
            app.dragStart = mouseX, mouseY
            app.dragEnd = mouseX + 1, mouseY + 1

    #check buttons
    if app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen(app.prevScreen)
        app.prevScreen = 'diy'
    elif app.generateButton.isSelected(mouseX, mouseY):
        setActiveScreen('result')
        app.prevScreen = 'diy'

def diy_onMouseRelease(app, mouseX, mouseY):
    if app.drawingRect:
        app.rectToolEnd = mouseX, mouseY
        app.drawingRect = False
        app.drawShape = True

    if app.drawingOval:
        app.ovalToolEnd = mouseX, mouseY
        app.drawingOval = False
        app.drawShape = True

    if app.moveShape:
        app.moveStart = mouseX, mouseY
        app.moveShape = False
        app.drawingDrag = False

    if app.drawingDrag:
        app.dragEnd = mouseX, mouseY

    if app.filling: 
        app.filling = False

def diy_redrawAll(app):
    drawGrid(app, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.width/2)
    # drawControls(app, app.diyWidthSlider, app.diyHeightSlider, app.diyPixelsWide, app.diyPixelsTall)
    # drawColorPanel(app, app.diyColors, app.mouseX, app.mouseY)
    # drawUserColorSelection(app, app.mouseX, app.mouseY)
    drawIcons(app)
    drawIconTools(app, app.mouseX, app.mouseY)
    drawSliders(app)
    print(app.diyWidthSliderHandle.cy)
    drawIconHighlights(app)

    if app.drawingRect:
        startX, startY = app.rectToolStart
        endX, endY = app.rectToolEnd
        drawRect(startX, startY, endX - startX, endY - startY, fill = None, border = 'black')

    if app.drawingOval:
        x0, y0 = app.ovalToolStart
        x1, y1 = app.ovalToolEnd
        centerX, centerY = (x0 + x1)//2, (y0 + y1)//2
        drawOval(centerX, centerY, x1 - x0, y1 - y0, fill = None, border = 'black')

    if app.drawingDrag or app.moveShape:
        startX, startY = app.dragStart
        endX, endY = app.dragEnd
        print(f'drawing shape {app.dragStart, app.dragEnd}')
        print(app.drawingDrag, app.moveShape)
        #make them move!!
        if endX - startX > 0 and endY - startY > 0:
            drawRect(startX, startY, endX - startX, endY - startY, fill = None, border = 'black', dashes = True)

    #checks if mouse is hoovering over
    if app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()
    elif app.generateButton.isSelected(app.mouseX, app.mouseY):
        app.generateButton.drawHighlight()

####IMAGE SCREEN####
def image_onMousePress(app, mouseX, mouseY):
    if app.rectTool:
        app.drawingRect = True

    if app.ovalTool:
        app.drawingOval = True

    if app.dragSelection:
        app.drawingDrag = True
        app.moveShape = False

    if app.fillSelection:
        app.filling = True

    app.selectColorDropper = app.dragSelection = app.fillSelection = app.ovalTool = app.rectTool = False
    app.boardSelected = set()

    #checks if checked aspect ratio button
    if 760 <= mouseX <= 780 and 40 <= mouseY <= 60:
        app.preserveAspectRatio = not app.preserveAspectRatio

    #if mouse hovering over valid color option and user presses, assigns "brush" as that color
    if app.colorSelect != None:
        app.imageColorSelect = app.colorSelect

    #aspect ratio
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
        app.imageWidthSlider, app.imageHeightSlider = mousePress(app, mouseX, 
                                                                 mouseY, app.imageWidthSlider, app.imageHeightSlider)
    
    if oldWidth != app.imageWidthSlider or oldHeight != app.imageHeightSlider:
        image_change(app)
    
    #starts filling in squares
    if isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop)
        app.imageBoard[row][col] = app.imageColorSelect

    #check buttons
    if app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen(app.prevScreen)
        app.prevScreen = 'image'
    elif app.generateButton.isSelected(mouseX, mouseY):
        setActiveScreen('result')
        app.prevScreen = 'image'

    checkColorControls(app, mouseX, mouseY)
    # checkEditingTools(app, mouseX, mouseY)
    checkDoubleClick(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                     app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall, app.imageColorSelect)

    if app.drawingRect:
        app.rectToolStart = mouseX, mouseY
        app.rectToolEnd = mouseX + 1, mouseY + 1

    if app.drawingOval:
        app.ovalToolStart = mouseX, mouseY
        app.ovalToolEnd = mouseX + 1, mouseY + 1

    if app.filling:
        if isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                    app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall):
            app.imageBoard = fillShape(app, app.imageColorSelect, mouseX, mouseY, 
                                     app.imageBoard, app.imageBoardLeft, app.imageBoardTop)

def image_onMouseDrag(app, mouseX, mouseY):
    if app.drawingRect:
        rectTool(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                 app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall)

    if app.drawingOval:
        ovalTool(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                 app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall)

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

    if (isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall) 
                and not app.drawingRect and not app.drawingOval):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop)
        app.imageBoard[row][col] = app.imageColorSelect

    for square in app.boardSelected:
        row, col = square
        app.imageBoard[row][col] = app.imageColorSelect

def image_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'image'
    updateMouse(app, mouseX, mouseY)

    #for double click
    if (isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                 app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall)):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, app.imageBoardTop)
        app.doubleClickColor = app.imageBoard[row][col]

    mouseMove(app, mouseX, mouseY, app.mostFrequentHex)

    #checks if mouse is hovering over an image square
    if (isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                 app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall)):
        if app.selectColorDropper == True:
            findColorDropperColor(app, mouseX, mouseY, app.imageBoard, 
                                  app.imageBoardLeft, app.imageBoardTop, 
                                  app.imagePixelsWide, app.imagePixelsTall)
            row, col = findSquare(app, mouseX, mouseY, app.imageBoard, 
                                  app.imageBoardLeft, app.imageBoardTop)
            app.colorSelect = app.imageBoard[row][col]
        else:
            app.colorDropperColor = None

    getColorWheelColor(app, mouseX, mouseY)

def image_onMouseRelease(app, mouseX, mouseY):
    if app.drawingRect:
        app.rectToolEnd = mouseX, mouseY
        app.drawingRect = False
        app.drawShape = True

    if app.drawingOval:
        app.ovalToolEnd = mouseX, mouseY
        app.drawingOval = False
        app.drawShape = True

    if app.moveShape:
        app.moveStart = mouseX, mouseY
        app.moveShape = False
        app.drawingDrag = False

def image_redrawAll(app):
    # drawControls(app, app.imageWidthSlider, app.imageHeightSlider, 
                #  app.imagePixelsWide, app.imagePixelsTall)
    drawGrid(app, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, 400)
    # drawColorPanel(app, app.mostFrequentHex, app.mouseX, app.mouseY)
    # drawUserColorSelection(app, app.mouseX, app.mouseY)
    drawIconTools(app, app.mouseX, app.mouseY)
    drawSliders(app)

    if app.drawingRect:
        startX, startY = app.rectToolStart
        endX, endY = app.rectToolEnd
        drawRect(startX, startY, endX - startX, endY - startY, fill = None, border = 'black')

    if app.drawingOval:
        x0, y0 = app.ovalToolStart
        x1, y1 = app.ovalToolEnd
        centerX, centerY = (x0 + x1)//2, (y0 + y1)//2
        drawOval(centerX, centerY, x1 - x0, y1 - y0, fill = None, border = 'black')

    #preserve aspect ratio checkbox
    drawLabel('Preserve Aspect Ratio:', 690, 50)
    color = None
    if app.preserveAspectRatio == True:
        color = 'pink'
        #draw white checkmark
    drawRect(760, 40, 20, 20, fill = color, border = 'black')

    #checks if mouse is hoovering over
    if app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()
    elif app.generateButton.isSelected(app.mouseX, app.mouseY):
        app.generateButton.drawHighlight()

####CHOOSE IMAGE SCREEN####
def imageOptions_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'imageOptions'
    updateMouse(app, mouseX, mouseY)

def imageOptions_onMousePress(app, mouseX, mouseY):
    if app.createButton.isSelected(mouseX, mouseY):
        setActiveScreen('image')
        app.prevScreen = 'imageOptions'
    elif app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen(app.prevScreen)
        app.prevScreen = 'imageOptions'

def imageOptions_redrawAll(app):
    drawLabel('Choose an Image:', app.width/2, app.height/6, size = 30)
    #draw images

    app.createButton.drawButton()
    app.backButton.drawButton()

    #checks if mouse is hoovering
    if app.createButton.isSelected(app.mouseX, app.mouseY):
        app.createButton.drawHighlight()
    elif app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()    

####RESULT SCREEN####
def result_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'result'
    updateMouse(app, mouseX, mouseY)

def result_onMousePress(app, mouseX, mouseY):
    if app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen(app.prevScreen)
        app.prevScreen = 'result'

def result_redrawAll(app):
    app.backButton.drawButton()

    if app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()

    drawLabel('Pattern', app.width/2, app.height/8, size = 20)

    #draws design
    if app.prevScreen == 'image':
        drawGrid(app, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, 400)
    elif app.prevScreen == 'diy':
        drawGrid(app, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, 400)

####START SCREEN####
def start_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'start'
    updateMouse(app, mouseX, mouseY)

def start_onMousePress(app, mouseX, mouseY):
    if app.diyButton.isSelected(mouseX, mouseY):
        setActiveScreen('diy')
        app.prevScreen = 'start'
    elif app.imageButton.isSelected(mouseX, mouseY):
        setActiveScreen('imageOptions')
        app.prevScreen = 'start'
    elif app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen('welcome')
        app.prevScreen = 'start'

def start_redrawAll(app):
    drawImage('startBackground.png', 0, 0)
    app.diyButton.drawButton()
    app.imageButton.drawButton()
    app.backButton.drawButton()

    #checks if mouse hoovering over button
    if app.diyButton.isSelected(app.mouseX, app.mouseY):
        app.diyButton.drawHighlight()
    elif app.imageButton.isSelected(app.mouseX, app.mouseY):
        app.imageButton.drawHighlight()
    elif app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()

####INSTRUCTIONS SCREEN####
def instructions_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'instructions'
    updateMouse(app, mouseX, mouseY)

def instructions_onMousePress(app, mouseX, mouseY):
    if app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen('welcome')
        app.prevScreen = 'instructions'

def instructions_redrawAll(app):
    app.backButton.drawButton()

    if app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()

####WELCOME SCREEN####
def welcome_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'welcome'
    updateMouse(app, mouseX, mouseY)

def welcome_onMousePress(app, mouseX, mouseY):
    if app.instructionsButton.isSelected(mouseX, mouseY):
        setActiveScreen('instructions')
        app.prevScreen = 'welcome'
    elif app.startButton.isSelected(mouseX, mouseY):
        setActiveScreen('start')
        app.prevScreen = 'welcome'

    # app.scrollbar.calculateHeight(1000)

def welcome_redrawAll(app):
    drawImage('welcomeBackground.png', 0, 0)
    app.instructionsButton.drawButton()
    app.startButton.drawButton()

    if app.instructionsButton.isSelected(app.mouseX, app.mouseY):
        app.instructionsButton.drawHighlight()
    elif app.startButton.isSelected(app.mouseX, app.mouseY):
        app.startButton.drawHighlight()
    
    # app.scrollbar.drawScrollBar()
    # app.scrollbar.drawHandle()

def main():
    runAppWithScreens(initialScreen = 'welcome', width = app.width, height = app.height)

main()