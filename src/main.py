from cmu_graphics import *
from PIL import Image
import random
import os
import time
import webbrowser
from drawGrid import drawGrid
from hexCodeFunctions import calculateMostFrequentHex, calculateHexCodes
from squareFunctions import isSquare, findSquare
from floodFill import fillShape
from buttons import Button
from slider import Slider, Handle
from imageIcons import Icon
from colorWheel import ColorSelection
from imageOptions import ImageOptions
from speech import SpeechBubble

####INITIALIZING VARIABLES####
def loadFont(app):
    app.font = 'Times New Roman'  

def diyScreenVariables(app):
    #sets necessary variables for controlling size/pixels of diy
    app.diyPixelsWide, app.diyPixelsTall = 27, 27
    app.diyWidthSlider = app.diyHeightSlider = 150, 350

    #variables for drawing board
    app.diyBoard = [([None] * app.diyPixelsWide) for row 
                    in range(app.diyPixelsTall)]
    app.diyBoardLeft = app.width/2 - app.diyPixelsWide * 5 
    app.diyBoardTop = app.height/2 - app.diyPixelsTall * 5

    app.diyColorSelect = None
    app.diyPrevColor = None

    #colors on screen, standard rainbow
    app.diyColors = ['pink', 'red', 'orange', 'yellow', 'green', 'blue', 
                     'purple', 'white', 'black', 'brown']

def imageScreenVariables(app):
    #no image selected, will get updated on imageOptions screen
    app.pilImage = None
    app.originalImageWidth, app.originalImageHeight = None, None
    app.imageWidth, app.imageHeight = None, None

    #sets necessary variables for controlling size/pixels of image
    #27 is middle
    app.imagePixelsWide, app.imagePixelsTall = 27, 27

    #create dictionary to store all the hex codes and the frequency they appear
    app.hexCodeToFrequency = None
    #list of most frequent ones, to be displayed in color panel
    app.mostFrequentHex = None

    #variables for drawing board
    app.imageBoard = [([None] * app.imagePixelsWide) for row 
                      in range(app.imagePixelsTall)]
    app.imageBoardLeft = app.width/2 - app.imagePixelsWide * 5
    app.imageBoardTop = app.height/2 - app.imagePixelsTall * 5

    #variables for color select
    app.imageColorSelect = None
    app.imagePrevColor = None

    #a tiny button
    app.preserveAspectRatio = False

def imageOptions(app):
    #no images selected, will be updated on imageOptions
    app.selectedImages = set()
    app.imageSelected = False
    app.selectedImage = None

def doubleClickVariables(app):
    #double clicking changes all instances of a color
    app.doubleClickThreshold = 300
    app.clickPosition = (0, 0)
    app.lastClickTime = 0
    app.doubleClickColor = None

def editingVariables(app):
    #tracks color hoovering over
    app.colorSelect = None

    #many icons
    app.selectColorDropper = False
    app.selectColorDropperHighlight = False
    app.colorDropperColor = None

    app.selectColorWheel = False
    app.selectColorWheelHighlight = False

    app.eraser = False
    app.eraserHighlight = False

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

    app.lineTool = False
    app.lineHighlight = False
    app.lineToolStart = 0, 0
    app.lineToolEnd = 0, 0
    app.drawingLine = 0, 0
    
    #color panels
    app.diyColorSelectionPanel = ColorSelection(75, 75, 25, 150, 250, 
                                                app.diyColors)
    app.imageColorSelectionPanel = ColorSelection(75, 75, 25, 150, 250, 
                                                  app.mostFrequentHex)

    #icon tools
    app.selectedFromColorWheel = False
    app.selectedColorFromWheel = (0, 0, 0)
    app.colorPanelSelected = False

    app.drawShape = False
    
    #for line, rect, oval tools
    #used in updatinb board
    app.boardSelected = set()

def screenVariables(app):
    app.width = 800
    app.height = 500
    app.mouseX, app.mouseY = 0, 0        
    app.prevScreen = 'welcome'
    app.currentScreen = 'welcome'
    app.pixelWidth = app.pixelHeight = 10

def buttons(app):
    #used in welcome screen
    app.instructionsButton = Button('Instructions', app.width/3, app.height*7/16
                                    , app.width/3, app.height/8, 25, app.font)
    app.startButton = Button('Start', app.width/3, app.height*10/16, app.width/3 
                             , app.height/8, 25, app.font)

    #used in start screen
    app.diyButton = Button('Create Your Own', app.width/12, app.height/7, 
                           app.width/3, app.height/8, 25, app.font)
    app.imageButton = Button('Image', app.width*7/12, app.height/7, 
                             app.width/3, app.height/8, 25, app.font)

    #used in image options screen
    app.createButton = Button('Create', 650, 450, 100, 30, 15, app.font)

    #used in image and diy screens
    app.generateButton = Button('Generate', 650, 450, 100, 30, 15, app.font)

    #used in almost all screens
    app.backButton = Button('Back', 50, 450, 100, 30, 15, app.font)

    #links to external site
    #used in instructions screen
    app.instructionsVideoButton = Button('Watch Me!', 90, 225, 120, 30, 15, 
                                         app.font)
    #used in result screen
    app.videoButton = Button('Tutorial', 20, 20, 120, 30, 15, app.font)

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

    #line tool, https://iconmonstr.com/cursor-11-png/
    lineTopEdge = app.height/2 + height + offset
    app.lineIcon = Icon('line', leftEdge, lineTopEdge, width, height)

    #square tool, https://iconmonstr.com/eraser-2-png/
    squareTopEdge = app.height/2 + height*2 + offset*2
    app.squareIcon = Icon('square', leftEdge, squareTopEdge, width, height)

    #circle tool, https://iconmonstr.com/circle-6-svg/
    circleTopEdge = app.height/2 + height*3 + offset*3
    app.circleIcon = Icon('circle', leftEdge, circleTopEdge, width, height)

#all the speech bubbles for cats
def speechVariables(app):
    app.speech = False
    app.welcomeBubble = SpeechBubble("wow you're so cool!", 10, 250, 150, 90, 
                                     None)
    app.instructionsBubble = SpeechBubble("let's learn!", 130, 270, 150, 90, 
                                          'reverse')
    app.resultsBubble = SpeechBubble('you did it!!', 620, 160, 150, 90, None)
    app.chooseDIY = SpeechBubble('wow I love yarn', 460, 120, 150, 90, None)
    app.chooseImage = SpeechBubble('off to the yarn store!', 230, 180, 120, 70,
                                   'reverse')

def onAppStart(app):
    app.setMaxShapeCount(3000)
    loadFont(app)
    screenVariables(app)
    diyScreenVariables(app)
    imageScreenVariables(app)
    editingVariables(app)
    doubleClickVariables(app)
    buttons(app)
    sliders(app)
    toolIcons(app)
    imageOptions(app)
    speechVariables(app)

#opens video in exterman browser to video on how to do c2c
def openLink():
    #video from Bella Coco on YouTube
    webbrowser.open('https://youtu.be/I5G9IM24LFU?si=iJNF4AvXXI77joLn')

####USED ON IMAGE SCREEN
#creates pixelated version of image to be analzyed
def pixelate(image, pixelsWide, pixelsTall, width, height):
    image = image.resize((pixelsWide, pixelsTall), Image.NEAREST)
    return image.resize((width, height), Image.NEAREST)

#update app.imageBoard with the appropriate colors
def updateImageBoard(app, pilImage):
    for row in range(app.imagePixelsTall):
        for col in range(app.imagePixelsWide):
            color = pilImage.getpixel((col*app.pixelWidth + app.pixelWidth/2, 
                                       row*app.pixelHeight + app.pixelHeight/2))
            rgbColor = rgb(color[0], color[1], color[2])
            app.imageBoard[row][col] = rgbColor

#changes image size based on pixels (they should be square)
def changeImageDimensions(app):
    app.imageWidth = app.pixelWidth * app.imagePixelsWide
    app.imageHeight = app.pixelHeight * app.imagePixelsTall

####USED IN DIY SCREEN
#updates colors in app.diyBoard
def updateColor(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, 
                pixelsTall):
    if (not app.drawingRect and not app.drawingOval and not app.drawingLine and 
        not app.filling and not app.diyColorSelectionPanel.isDragging and not 
        app.selectColorDropper):
        if isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide,
                     pixelsTall):
            row, col = findSquare(app, mouseX, mouseY, board, boardLeft, 
                                  boardTop)
            board[row][col] = app.diyColorSelect
    else:
        #if cirlce or rectangle or line tool used and drawn with
        for square in app.boardSelected:
            row, col = square
            board[row][col] = app.diyColorSelect
    return board

##ADJUSTS GRIDS##
def image_change(app):
    #adjust image in background
    changeImageDimensions(app)
    #change board size
    app.imageBoard = resizingBoard(app, app.imageBoard, app.imagePixelsWide, 
                                   app.imagePixelsTall)
    #change board coordinates
    app.imageBoardLeft = app.width/2 - app.imagePixelsWide*5
    app.imageBoardTop = app.height/2 - app.imagePixelsTall*5
    #pixelate image to new size
    pilImage = pixelate(app.pilImage, app.imagePixelsWide, 
                        app.imagePixelsTall, app.imageWidth, app.imageHeight)
    #update board with appropriate colored squares
    updateImageBoard(app, pilImage)

#change board and board variables
def diy_change(app):
    app.diyBoard = resizingBoard(app, app.diyBoard, app.diyPixelsWide, 
                                 app.diyPixelsTall)
    app.diyBoardLeft = app.width/2 - app.diyPixelsWide * 5
    app.diyBoardTop = app.height/2 - app.diyPixelsTall * 5

####NECESSARY FOR BOTH####
def resizingBoard(app, board, pixelsWide, pixelsTall):
    oldBoard = board
    #create new board of the updated size
    newBoard = [([None] * pixelsWide) for row in range(pixelsTall)]
    #copy existing values into new board
    for row in range(min(len(oldBoard), len(newBoard))):
        for col in range(min(len(oldBoard[0]), len(newBoard[0]))):
            newBoard[row][col] = oldBoard[row][col]
    return newBoard

def updateMouse(app, mouseX, mouseY):
    app.mouseX, app.mouseY = mouseX, mouseY

#if color dropper tool is selected, return color of square hoovering over
def findColorDropperColor(app, mouseX, mouseY, board, boardLeft, boardTop, 
                          pixelsWide, pixelsTall):
    #checks if mouse is hovering over a square
    if app.colorSelect == None:
        if isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, 
                    pixelsWide, pixelsTall):
            row, col = findSquare(app, mouseX, mouseY, board, boardLeft, boardTop)
            app.colorDropperColor = board[row][col]

#draw left toolbar
def drawIconTools(app, mouseX, mouseY):
    if app.selectColorDropper:
        app.colorDropperIcon.drawMovingIcon(mouseX, mouseY)
    elif app.eraser:
        app.eraserIcon.drawMovingIcon(mouseX, mouseY)
    elif app.fillSelection:
        app.fillIcon.drawMovingIcon(mouseX, mouseY)
    elif app.lineTool:
        app.lineIcon.drawMovingIcon(mouseX, mouseY)
    elif app.rectTool:
        app.squareIcon.drawMovingIcon(mouseX, mouseY)
    elif app.ovalTool:
        app.circleIcon.drawMovingIcon(mouseX, mouseY)

#double click check from chatGPT, changing colors not
def checkDoubleClick(app, mouseX, mouseY, board, boardLeft, boardTop, 
                     pixelsWide, pixelsTall, colorSelect):
    #checks if click is in bounds
    if (boardLeft <= mouseX <= boardLeft + pixelsWide * 10 and 
        boardTop <= mouseY <= boardTop + pixelsTall * 10):
        currentTime = time.time() * 1000
        timeSinceLastClick = currentTime - app.lastClickTime
        if timeSinceLastClick <= app.doubleClickThreshold:
            if (abs(mouseX - app.clickPosition[0]) < 10 and 
                abs(mouseY - app.clickPosition[1]) < 10):
                for row in range(len(board)):
                    for col in range(len(board[0])):
                        if board[row][col] == app.doubleClickColor:
                            board[row][col] = colorSelect
        # Update the last click time and position
        app.lastClickTime = currentTime
        app.clickPosition = (mouseX, mouseY)

#adds selected squares to app.boardSelected
def lineTool(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, 
             pixelsTall):
    app.lineToolEnd = mouseX, mouseY
    xStart, yStart = app.lineToolStart
    #if vertical line
    if mouseX == xStart:
        for y in range(min(yStart, mouseY), max(yStart, mouseY), 10):
            if isSquare(app, mouseX, y, board, boardLeft, boardTop, pixelsWide, 
                        pixelsTall):
                    row, col = findSquare(app, mouseX, y, board, boardLeft, 
                                          boardTop)
                    app.boardSelected.add((row, col))
    else:
        slope = (mouseY - yStart)/(mouseX - xStart)
        intercept = yStart - slope*xStart

        #do horizontal first
        for x in range(min(xStart, mouseX), max(xStart, mouseX), 10):
            y = slope*x + intercept
            if isSquare(app, x, y, board, boardLeft, boardTop, pixelsWide, 
                        pixelsTall):
                row, col = findSquare(app, x, y, board, boardLeft, boardTop)
                app.boardSelected.add((row, col))
            
        #vertical
        for y in range(min(yStart, mouseY), max(yStart, mouseY), 10):
            #no dividing by 0!!
            if slope != 0:
                x = (y - intercept)/slope
                if isSquare(app, x, y, board, boardLeft, boardTop, pixelsWide, 
                            pixelsTall):
                    row, col = findSquare(app, x, y, board, boardLeft, boardTop)
                    app.boardSelected.add((row, col))

#adds selected squares to app.boardSelected
def rectTool(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, 
             pixelsTall):
        app.rectToolEnd = mouseX, mouseY
        xStart, yStart = app.rectToolStart
        for x in range(min(xStart, mouseX), max(xStart, mouseX), 10):
            for y in range(min(yStart, mouseY), max(yStart, mouseY), 10):
                if isSquare(app, x, y, board, boardLeft, boardTop, pixelsWide,
                            pixelsTall):
                    row, col = findSquare(app, x, y, board, boardLeft, boardTop)
                    app.boardSelected.add((row, col))

#adds selected squares to app.boardSelected
def ovalTool(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, 
             pixelsTall):
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
                if isSquare(app, x, y, board, boardLeft, boardTop, pixelsWide, 
                            pixelsTall):
                    row, col = findSquare(app, x, y, board, boardLeft, boardTop)
                    app.boardSelected.add((row, col))

#during drag, updates endpoints to shape moves with it
def checkDrawingShapesDrag(app, mouseX, mouseY, board, boardLeft, boardTop,
                           pixelsWide, pixelsTall):
    if app.drawingLine:
        lineTool(app, mouseX, mouseY, board, boardLeft, boardTop,
                           pixelsWide, pixelsTall)
    elif app.drawingRect:
        rectTool(app, mouseX, mouseY, board, boardLeft, boardTop,
                           pixelsWide, pixelsTall)
    elif app.drawingOval:
        ovalTool(app, mouseX, mouseY, board, boardLeft, boardTop,
                           pixelsWide, pixelsTall)

#during press, right before drawing begins
def checkDrawingShapesPress(app, mouseX, mouseY):
    if app.drawingLine:
        app.lineToolStart = mouseX, mouseY
        app.lineToolEnd = mouseX + 1, mouseY + 1
    elif app.drawingRect:
        app.rectToolStart = mouseX, mouseY
        app.rectToolEnd = mouseX + 1, mouseY + 1
    elif app.drawingOval:
        app.ovalToolStart = mouseX, mouseY
        app.ovalToolEnd = mouseX + 1, mouseY + 1

#on mouse release, sets endpoint
def checkDrawingShapesRelease(app, mouseX, mouseY):
    if app.drawingLine:
        app.lineToolEnd = mouseX, mouseY
        app.drawingLine = False
    elif app.drawingRect:
        app.rectToolEnd = mouseX, mouseY
        app.drawingRect = False
        app.drawShape = True
    elif app.drawingOval:
        app.ovalToolEnd = mouseX, mouseY
        app.drawingOval = False
        app.drawShape = True

#draw shapes, endopints move as drawing because of drag
def checkDrawingShapesDraw(app):
    if app.drawingLine:
        startX, startY = app.lineToolStart
        endX, endY = app.lineToolEnd
        drawLine(startX, startY, endX, endY)
    elif app.drawingRect:
        startX, startY = app.rectToolStart
        endX, endY = app.rectToolEnd
        drawRect(startX, startY, endX - startX, endY - startY, fill = None, 
                 border = 'black')
    elif app.drawingOval:
        x0, y0 = app.ovalToolStart
        x1, y1 = app.ovalToolEnd
        centerX, centerY = (x0 + x1)//2, (y0 + y1)//2
        drawOval(centerX, centerY, x1 - x0, y1 - y0, fill = None, 
                 border = 'black')

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
    color = None
    if app.colorSelect != None:
        color = app.colorSelect
    elif app.currentScreen == 'diy':
        color = app.diyColorSelect
    elif app.currentScreen == 'image':
        color = app.imageColorSelect
    drawRect(app.selectedColorLeft, app.selectedColorTop, app.selectedColorWidth, 
             app.selectedColorHeight, fill = color, border = 'black')
    app.colorIcon.drawIcon()
    app.colorDropperIcon.drawIcon()
    app.eraserIcon.drawIcon()
    app.fillIcon.drawIcon()
    app.lineIcon.drawIcon()
    app.squareIcon.drawIcon()
    app.circleIcon.drawIcon()

def checkIconEditing(app):
    if app.eraser:
        app.diyColorSelect = None
        app.imageColorSelect = None
    elif app.fillSelection:
        app.filling = True
    elif app.lineTool:
        app.drawingLine = True
    elif app.rectTool:
        app.drawingRect = True
    elif app.ovalTool:
        app.drawingOval = True

def checkIconTools(app):
    if app.colorIcon.isSelected(app.mouseX, app.mouseY):
        app.selectColorWheel = not app.selectColorWheel
    elif app.colorDropperIcon.isSelected(app.mouseX, app.mouseY):
        app.selectColorDropper = not app.selectColorDropper
    elif app.eraserIcon.isSelected(app.mouseX, app.mouseY):
        app.eraser = not app.eraser
    elif app.fillIcon.isSelected(app.mouseX, app.mouseY):
        app.fillSelection = not app.fillSelection
    elif app.lineIcon.isSelected(app.mouseX, app.mouseY):
        app.lineTool = not app.lineTool
    elif app.squareIcon.isSelected(app.mouseX, app.mouseY):
        app.rectTool = not app.rectTool
    elif app.circleIcon.isSelected(app.mouseX, app.mouseY):
        app.ovalTool = not app.ovalTool
    elif app.eraser:
        if not isSquare(app, app.mouseX, app.mouseY, app.imageBoard, 
                        app.imageBoardLeft, app.imageBoardTop, 
                        app.imagePixelsWide, app.imagePixelsTall):
            app.eraser = False
    else:
        app.selectColorDropper = app.fillSelection = app.ovalTool = False
        app.rectTool = app.lineTool = False

#if mouse hoovering over, make icon bigger for ui
def checkIconHighlights(app):
    if app.colorIcon.isSelected(app.mouseX, app.mouseY):
        app.selectColorWheelHighlight = True
    elif app.colorDropperIcon.isSelected(app.mouseX, app.mouseY):
        app.selectColorDropperHighlight = True
    elif app.eraserIcon.isSelected(app.mouseX, app.mouseY):
        app.eraserHighlight = True
    elif app.fillIcon.isSelected(app.mouseX, app.mouseY):
        app.fillHighlight = True
    elif app.lineIcon.isSelected(app.mouseX, app.mouseY):
        app.lineHighlight = True
    elif app.squareIcon.isSelected(app.mouseX, app.mouseY):
        app.rectHighlight = True
    elif app.circleIcon.isSelected(app.mouseX, app.mouseY):
        app.ovalHighlight = True
    else: 
        app.selectColorWheelHighlight = app.selectColorDropperHighlight = False
        app.eraserHighlight = app.fillHighlight = app.lineHighlight = False
        app.rectHighlight = app.ovalHighlight = False
        
#if mouse has pressed icon, make it move with mouse
def drawIconHighlights(app):
    if app.selectColorWheelHighlight:
        app.colorIcon.drawSelected()
    elif app.selectColorDropperHighlight:
        app.colorDropperIcon.drawSelected()
    elif app.eraserHighlight:
        app.eraserIcon.drawSelected()
    elif app.fillHighlight:
        app.fillIcon.drawSelected()
    elif app.lineHighlight:
        app.lineIcon.drawSelected()
    elif app.rectHighlight:
        app.squareIcon.drawSelected()
    elif app.ovalHighlight:
        app.circleIcon.drawSelected()

#returns pixels wide and tall
def changeSliders(app, mouseX, mouseY, handle):
    return handle.updateSquares(mouseX, mouseY)

def checkAspectRatio(app, mouseX, mouseY):
    widthToHeightRatio = app.originalImageWidth/app.originalImageHeight
    sliderLeft, sliderRight = 760, 795
    widthSliderTop, widthSliderBottom = 75, 225
    heightSliderTop, heightSliderBottom = 275, 425
   
    if app.widthSlider.inBounds(mouseX, mouseY):
        app.imageWidthSliderHandle.cy = max(min(mouseY, widthSliderBottom), 
                                            widthSliderTop)
        app.imageHeightSliderHandle.cy = (((app.imageWidthSliderHandle.cy - 
                                            widthSliderTop) / widthToHeightRatio)
                                             + heightSliderTop)
    elif app.heightSlider.inBounds(mouseX, mouseY):
        app.imageHeightSliderHandle.cy = max(min(mouseY, heightSliderBottom), 
                                             heightSliderTop)
        app.imageWidthSliderHandle.cy = (((app.imageHeightSliderHandle.cy - 
                                           heightSliderTop) * widthToHeightRatio)
                                            + widthSliderTop)
    else: 
        app.imageWidthSliderHandle.cy = (widthToHeightRatio * 
                                        (app.imageHeightSliderHandle.cy - 
                                         heightSliderTop)) + widthSliderTop
    
    if app.imageHeightSliderHandle.cy > heightSliderBottom:
        app.imageHeightSliderHandle.cy = heightSliderBottom
        app.imageWidthSliderHandle.cy = (((app.imageHeightSliderHandle.cy - 
                                           heightSliderTop) * widthToHeightRatio)
                                             + widthSliderTop)
    elif app.imageHeightSliderHandle.cy < heightSliderTop:
        app.imageHeightSliderHandle.cy = heightSliderTop
        app.imageWidthSliderHandle.cy = (((app.imageHeightSliderHandle.cy - 
                                           heightSliderTop) * widthToHeightRatio)
                                             + widthSliderTop)
    elif app.imageWidthSliderHandle.cy > widthSliderBottom:
        app.imageWidthSliderHandle.cy = widthSliderBottom
        app.imageHeightSliderHandle.cy = (((app.imageWidthSliderHandle.cy - 
                                            heightSliderTop) / widthToHeightRatio)
                                              + widthSliderTop)
    elif app.imageWidthSliderHandle.cy < widthSliderTop:
        app.imageWidthSliderHandle.cy = widthSliderTop
        app.imageHeightSliderHandle.cy = (((app.imageWidthSliderHandle.cy - 
                                            heightSliderTop) / widthToHeightRatio))

####DIY SCREEN####
def diy_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'diy'
    updateMouse(app, mouseX, mouseY)
    checkIconHighlights(app)

    #for double click
    if isSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall):
        row, col = findSquare(app, mouseX, mouseY, app.diyBoard, 
                              app.diyBoardLeft, app.diyBoardTop)
        app.doubleClickColor = app.diyBoard[row][col]

    if app.selectColorWheel:
        #checks if mouse in color grid
        app.colorSelect = app.diyColorSelectionPanel.colorGridSelected(mouseX, 
                                                                       mouseY)
        #checks if in gradient grid or in color wheel
        app.colorSelect = app.diyColorSelectionPanel.getColorWheelColor(mouseX, 
                                                                        mouseY)
    #if mouse hoovering over square and color dropper is selected, return color
    if isSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall):
        if app.selectColorDropper == True:
            row, col = findSquare(app, mouseX, mouseY, app.diyBoard, 
                                  app.diyBoardLeft, app.diyBoardTop)
            findColorDropperColor(app, mouseX, mouseY, app.diyBoard, 
                                  app.diyBoardLeft, app.diyBoardTop, 
                                  app.diyBoardLeft, app.diyPixelsTall)
            app.colorSelect = app.diyBoard[row][col]
        else:
            app.colorDropperColor = None

def diy_onMouseDrag(app, mouseX, mouseY):
    #drag color panel
    if app.diyColorSelectionPanel.startDragging:
        app.diyColorSelectionPanel.move(mouseX, mouseY)
    checkDrawingShapesDrag(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                           app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall)
    app.diyBoard = updateColor(app, mouseX, mouseY, app.diyBoard, 
                               app.diyBoardLeft, app.diyBoardTop, 
                               app.diyPixelsWide, app.diyPixelsTall)

def diy_onMousePress(app, mouseX, mouseY):
    #updates color
    if app.selectColorWheel:
        if app.diyColorSelectionPanel.wheelSelected(mouseX, mouseY):
            app.diyColorSelectionPanel.selectedColorFromWheel = app.diyColorSelectionPanel.getPixel(mouseX, mouseY)
            app.diyColorSelectionPanel.selectedFromColorWheel = True
        #potential start dragging the panel
        elif app.diyColorSelectionPanel.isSelected(mouseX, mouseY):
            app.diyColorSelectionPanel.startMove(mouseX, mouseY)
        else:
            app.diyColorSelectionPanel.selectedFromColorWheel = False

    app.boardSelected = set()
    
    checkIconEditing(app)
    checkIconTools(app)

    #if user is hoovering over a color, app.diyColorSelect hold last clicked color
    if app.colorSelect != None:
        app.diyColorSelect = app.colorSelect
   
    #change width and height sliders
    app.diyPixelsWide = changeSliders(app, mouseX, mouseY, 
                                      app.diyWidthSliderHandle)
    app.diyPixelsTall = changeSliders(app, mouseX, mouseY, 
                                      app.diyHeightSliderHandle)

    diy_change(app)
    app.diyBoard = updateColor(app, mouseX, mouseY, app.diyBoard, 
                               app.diyBoardLeft, app.diyBoardTop,
                               app.diyPixelsWide, app.diyPixelsTall)

    checkDoubleClick(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                     app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall, 
                     app.diyColorSelect)
    checkDrawingShapesPress(app, mouseX, mouseY)

    #if fill tool selected
    if app.filling:
        if isSquare(app, mouseX, mouseY, app.diyBoard, app.diyBoardLeft, 
                    app.diyBoardTop, app.diyPixelsWide, app.diyPixelsTall):
            app.diyBoard = fillShape(app, app.diyColorSelect, mouseX, mouseY, 
                                     app.diyBoard, app.diyBoardLeft, 
                                     app.diyBoardTop)
            app.filling = False

    #check buttons
    if app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen('start')
        app.prevScreen = 'diy'
    elif app.generateButton.isSelected(mouseX, mouseY):
        setActiveScreen('result')
        app.prevScreen = 'diy'

def diy_onMouseRelease(app, mouseX, mouseY):
    app.diyColorSelectionPanel.endMove()

    checkDrawingShapesRelease(app, mouseX, mouseY)

    if app.filling: 
        app.filling = False

def diy_redrawAll(app):
    app.backButton.drawButton()
    app.createButton.drawButton()
    drawGrid(app, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, app.width/2)
    drawSliders(app)
    if app.selectColorWheel:
        app.diyColorSelectionPanel.draw()
    drawIcons(app)
    drawIconHighlights(app)
    drawIconTools(app, app.mouseX, app.mouseY)

    checkDrawingShapesDraw(app)

    #checks if mouse is hoovering over
    if app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()
    elif app.generateButton.isSelected(app.mouseX, app.mouseY):
        app.generateButton.drawHighlight()

####IMAGE SCREEN####
def image_onMousePress(app, mouseX, mouseY):
    app.boardSelected = set()

    checkIconEditing(app)
    checkIconTools(app)

    if app.selectColorWheel:
        if app.imageColorSelectionPanel.wheelSelected(mouseX, mouseY):
            app.imageColorSelectionPanel.selectedColorFromWheel = app.imageColorSelectionPanel.getPixel(mouseX, mouseY)
            app.imageColorSelectionPanel.selectedFromColorWheel = True
        #potential start dragging the panel
        elif app.imageColorSelectionPanel.isSelected(mouseX, mouseY):
            app.imageColorSelectionPanel.startMove(mouseX, mouseY)
        else:
            app.imageColorSelectionPanel.selectedFromColorWheel = False

    #checks if checked aspect ratio button
    boxTop = 30
    width = 20
    if (app.sliderCenter - width/2 <= mouseX <= app.sliderCenter + width/2 and 
        boxTop <= mouseY <= boxTop + width/2):
        app.preserveAspectRatio = not app.preserveAspectRatio

    #aspect ratio
    oldWidth, oldHeight = app.imagePixelsWide, app.imagePixelsTall
    if app.preserveAspectRatio:
        checkAspectRatio(app, mouseX, mouseY)

    #change width and height sliders
    app.imagePixelsWide = changeSliders(app, mouseX, mouseY, 
                                        app.imageWidthSliderHandle)
    app.imagePixelsTall = changeSliders(app, mouseX, mouseY, 
                                        app.imageHeightSliderHandle)

    if oldWidth != app.imagePixelsWide or oldHeight != app.imagePixelsTall:
        image_change(app)
    
    #starts filling in squares
    if (isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall) and 
                not app.drawingRect and not app.drawingLine and not 
                app.drawingOval and not app.selectColorDropper):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, 
                              app.imageBoardLeft, app.imageBoardTop)
        app.imageBoard[row][col] = app.imageColorSelect

    #check buttons
    if app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen('imageOptions')
        app.prevScreen = 'image'
    elif app.generateButton.isSelected(mouseX, mouseY):
        setActiveScreen('result')
        app.prevScreen = 'image'

    checkDoubleClick(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                     app.imageBoardTop, app.imagePixelsWide, 
                     app.imagePixelsTall, app.imageColorSelect)

    checkDrawingShapesPress(app, mouseX, mouseY)

    #if mouse hovering over valid color option and user presses, 
    # assigns "brush" as that color
    if app.colorSelect != None:
        app.imageColorSelect = app.colorSelect

def image_onMouseDrag(app, mouseX, mouseY):
    if app.imageColorSelectionPanel.startDragging:
        app.imageColorSelectionPanel.move(mouseX, mouseY)

    checkDrawingShapesDrag(app, mouseX, mouseY, app.imageBoard, 
                           app.imageBoardLeft, app.imageBoardTop, 
                           app.imagePixelsWide, app.imagePixelsTall)

    #drag color on grid
    if (isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall) 
                and not app.drawingRect and not app.drawingOval and not 
                app.drawingLine and not app.selectColorDropper):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, 
                              app.imageBoardLeft, app.imageBoardTop)
        app.imageBoard[row][col] = app.imageColorSelect

    #for square in oval, rectangle, line tools
    for square in app.boardSelected:
        row, col = square
        app.imageBoard[row][col] = app.imageColorSelect

def image_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'image'
    updateMouse(app, mouseX, mouseY)
    checkIconHighlights(app)
    if app.selectColorWheel:
        #checks if in color grid
        app.colorSelect = app.imageColorSelectionPanel.colorGridSelected(mouseX, 
                                                                         mouseY)
        #checks if in gradient grid or in color wheel
        app.colorSelect = app.imageColorSelectionPanel.getColorWheelColor(mouseX, 
                                                                          mouseY)

    #for double click
    if (isSquare(app, mouseX, mouseY, app.imageBoard, app.imageBoardLeft, 
                 app.imageBoardTop, app.imagePixelsWide, app.imagePixelsTall)):
        row, col = findSquare(app, mouseX, mouseY, app.imageBoard, 
                              app.imageBoardLeft, app.imageBoardTop)
        app.doubleClickColor = app.imageBoard[row][col]

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

def image_onMouseRelease(app, mouseX, mouseY):
    app.imageColorSelectionPanel.endMove()
    checkDrawingShapesRelease(app, mouseX, mouseY)

def image_redrawAll(app):
    app.backButton.drawButton()
    app.createButton.drawButton()
    drawGrid(app, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, 400)
    drawSliders(app)
    if app.selectColorWheel:
        app.imageColorSelectionPanel.draw()
    drawIcons(app)
    drawIconHighlights(app)
    drawIconTools(app, app.mouseX, app.mouseY)

    checkDrawingShapesDraw(app)

    #preserve aspect ratio checkbox
    if app.preserveAspectRatio:
        top = 30
        height, width = 20, 20
        #image from Canva, linked in full-submission.txt
        drawImage('checkmark.png', app.sliderCenter - 10, top, width = width, 
                  height = height)
    else:
        drawRect(app.sliderCenter, 40, 20, 20, fill = None, border = 'pink', 
                 align = 'center')

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
        if app.imageSelected:
            setActiveScreen('image')
            app.prevScreen = 'imageOptions'
            updateSelectedImage(app)
    elif app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen('start')
        app.prevScreen = 'imageOptions'

    #if user selects image, keeps track of image details in app.selectedImage
    for image in app.selectedImages:
        if image.isSelected(mouseX, mouseY):
            app.imageSelected = True
            app.selectedImage = image.name

def imageOptions_redrawAll(app):
    #background
    #image designed by me on Canva w/ existing graphics, link full-submission.txt
    drawImage('imageOptionsBackground.png', 0, 0)
    #draw images
    imagesAcross = 3
    imagesDown = 2
    whiteSpace = 50
    #12 is num of images
    #add all images to app.selectedImages list
    potentialNums = [num for num in range(1, 12)]
    if len(app.selectedImages) < imagesAcross * imagesDown:
        for i in range(imagesAcross):
            for j in range(imagesDown):
                #randomize images
                num = random.choice(potentialNums)
                image = ImageOptions(num, whiteSpace*(i + 1) + i*200, 100 + 
                                     whiteSpace/2*(j) + 150*(j))
                app.selectedImages.add(image)
                #prevents duplicates
                potentialNums.remove(num)

    #if mouse is hoovering above image
    for image in app.selectedImages:
        if image.isSelected(app.mouseX, app.mouseY):
            image.drawHighlight()
        else:
            image.draw()
    
    #if there is an image selected, update 
    if app.imageSelected:
        for image in app.selectedImages:
            if image.name == app.selectedImage:
                image.drawSelected()

    app.createButton.drawButton()
    app.backButton.drawButton()

    #checks if mouse is hoovering
    if app.createButton.isSelected(app.mouseX, app.mouseY):
        app.createButton.drawHighlight()
    elif app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()    

#updates necessary variables for image screen
def updateSelectedImage(app):
    app.pilImage = Image.open(os.path.join('images', f'{app.selectedImage}.png')
                              ).convert('RGB')
    app.originalImageWidth, app.originalImageHeight = app.pilImage.size
    app.imageWidth, app.imageHeight = app.pilImage.size
    app.hexCodeToFrequency = calculateHexCodes(app, app.pilImage)
    app.mostFrequentHex = calculateMostFrequentHex(app)
    changeImageDimensions(app)
    pilImage = pixelate(app.pilImage, app.imagePixelsWide, 
                        app.imagePixelsTall, app.imageWidth, app.imageHeight)
    updateImageBoard(app, pilImage)
    app.imageColorSelectionPanel.colorList = app.mostFrequentHex

####RESULT SCREEN####
def result_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'result'
    updateMouse(app, mouseX, mouseY)
    #for cat speech bubble
    catHeadLeft = 650
    catHeadTop = 290
    catHeadWidth = 130
    catHeadHeight = 90
    if (catHeadLeft <= mouseX <= catHeadLeft + catHeadWidth and catHeadTop <= 
        mouseY <= catHeadTop + catHeadHeight):
        app.speech = True
    else:
        app.speech = False

def result_onMousePress(app, mouseX, mouseY):
    if app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen(app.prevScreen)
        app.prevScreen = 'result'
    elif app.videoButton.isSelected(mouseX, mouseY):
        openLink()    

def result_redrawAll(app):
    #image designed on Canva w/ existing graphics, link in full-submission.txt
    drawImage('resultBackground.png', 0, 0)
    app.backButton.drawButton()
    #in top left
    app.videoButton.drawButton()
    if app.prevScreen == 'diy':
        drawLabel(f'{app.diyPixelsWide} x {app.diyPixelsTall} squares', 
                  (app.videoButton.leftEdge*2 + app.videoButton.width)/2, 
                  (app.videoButton.topEdge*2 + app.videoButton.height), 
                  font = app.font)
    elif app.prevScreen == 'image':
        drawLabel(f'{app.imagePixelsWide} x {app.imagePixelsTall} squares',
                  (app.videoButton.leftEdge*2 + app.videoButton.width)/2, 
                  (app.videoButton.topEdge*2 + app.videoButton.height),
                  font = app.font)


    if app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()

    if app.videoButton.isSelected(app.mouseX, app.mouseY):
        app.videoButton.drawHighlight()

    #draws design
    if app.prevScreen == 'image':
        drawGrid(app, app.imageBoard, app.imageBoardLeft, app.imageBoardTop, 400)
    elif app.prevScreen == 'diy':
        drawGrid(app, app.diyBoard, app.diyBoardLeft, app.diyBoardTop, 400)

    #speech bubble
    if app.speech:
        app.resultsBubble.draw()

####START SCREEN####
def start_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'start'
    updateMouse(app, mouseX, mouseY)
    #for cat speech bubble
    catHeadLeft = 155
    catHeadTop = 250
    catHeadWidth = 60
    catHeadHeight = 50
    catHeadLeft2 = 590
    catHeadTop2 = 190
    catHeadWidth2 = 60
    catHeadHeight2 = 60
    if (catHeadLeft <= mouseX <= catHeadLeft + catHeadWidth and catHeadTop <= 
        mouseY <= catHeadTop + catHeadHeight):
        app.speech = True
    elif (catHeadLeft2 <= mouseX <= catHeadLeft2 + catHeadWidth2 and catHeadTop2
          <= mouseY <= catHeadTop2 +  catHeadHeight2):
        app.speech = True
    else:
        app.speech = False

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
    #image designed on Canva w/ existing graphics, link full-submission.txt
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

    #speech bubbles for cats
    if app.speech:
        if app.mouseX < app.width/2:
            app.chooseImage.draw()
        else:
            app.chooseDIY.draw()

####INSTRUCTIONS SCREEN####
def instructions_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'instructions'
    updateMouse(app, mouseX, mouseY)
    #for silly little cat speech bubble
    catHeadLeft = 35
    catHeadTop = 300
    catHeadWidth = 90
    catHeadHeight = 60
    if (catHeadLeft <= mouseX <= catHeadLeft + catHeadWidth and catHeadTop <= 
        mouseY <= catHeadTop + catHeadHeight):
        app.speech = True
    else:
        app.speech = False

def instructions_onMousePress(app, mouseX, mouseY):
    if app.backButton.isSelected(mouseX, mouseY):
        setActiveScreen('welcome')
        app.prevScreen = 'instructions'
    elif app.instructionsVideoButton.isSelected(mouseX, mouseY):
        openLink()

def instructions_redrawAll(app):
    #image designed on Canva w/ existing graphics, link full-submission.txt
    drawImage('instructionsBackground.png', 0, 0)
    app.instructionsVideoButton.drawButton()
    app.backButton.drawButton()

    #if mouse is hoovering over buttons
    if app.backButton.isSelected(app.mouseX, app.mouseY):
        app.backButton.drawHighlight()
    elif app.instructionsVideoButton.isSelected(app.mouseX, app.mouseY):
        app.instructionsVideoButton.drawHighlight()

    #speech bubble
    if app.speech:
        app.instructionsBubble.draw()

####WELCOME SCREEN####
def welcome_onMouseMove(app, mouseX, mouseY):
    app.currentScreen = 'welcome'
    updateMouse(app, mouseX, mouseY)

    #for silly little cat speech bubble
    catHeadLeft = 135
    catHeadTop = 325
    catHeadWidth = 70
    catHeadHeight = 60
    if (catHeadLeft <= mouseX <= catHeadLeft + catHeadWidth and catHeadTop <= 
        mouseY <= catHeadTop + catHeadHeight):
        app.speech = True
    else:
        app.speech = False

def welcome_onMousePress(app, mouseX, mouseY):
    if app.instructionsButton.isSelected(mouseX, mouseY):
        setActiveScreen('instructions')
        app.prevScreen = 'welcome'
    elif app.startButton.isSelected(mouseX, mouseY):
        setActiveScreen('start')
        app.prevScreen = 'welcome'

def welcome_redrawAll(app):
    #image designed on Canva w/ existing graphics, link full-submission.txt
    drawImage('welcomeBackground.png', 0, 0)
    app.instructionsButton.drawButton()
    app.startButton.drawButton()
    if app.instructionsButton.isSelected(app.mouseX, app.mouseY):
        app.instructionsButton.drawHighlight()
    elif app.startButton.isSelected(app.mouseX, app.mouseY):
        app.startButton.drawHighlight()
    #speech bubble!
    if app.speech:
        app.welcomeBubble.draw()

####MAIN####
def main():
    runAppWithScreens(initialScreen = 'welcome', width = app.width, 
                      height = app.height)

main()