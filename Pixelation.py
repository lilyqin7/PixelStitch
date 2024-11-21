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
    #screen dimensions 
    app.width = 800
    app.height = 500

    # url = 'https://www.w3schools.com/images/picture.jpg'
    url = 'https://tinyurl.com/great-pitch-gif'
    #loadPilImage only loads some images???

    #turns url into PIL image
    app.pilImage = loadPilImage(url)
    app.imageWidth, app.imageHeight = app.pilImage.size

    #sets necessary variables for controlling size/pixels of image
    app.pixelsWide = 20
    app.pixelsTall = 20
    app.widthSlider = 100
    app.heightSlider = 100

    #changes size of image so the pixels are square
    changeImageDimensions(app)
    
    #changes PIL image to CMU image
    app.cmuImage = adjustImage(app, app.pilImage)

    #create dictionary to store all the hex codes and the frequency they appear
    app.hexCodeToFrequency = calculateHexCodes(app, app.pilImage)
    app.mostFrequentHex = calculateMostFrequentHex(app)

    #variables for diy
    app.board = [([None] * app.pixelsWide) for row in range(app.pixelsTall)]
    app.cellBorderWidth = 1
    app.boardWidth = app.pixelsWide * 10
    app.boardHeight = app.pixelsTall * 10
    app.boardLeft = app.width/2 - app.pixelsWide * 10 / 2
    app.boardTop = app.height/2 - app.pixelsTall * 10 / 2

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
def calculateHexCodes(app, pilImage):
    d = {}
    for x in range(pilImage.width):
        for y in range(pilImage.height):
            rgb = pilImage.getpixel((x, y))
            d[rgb] = d.get(rgb, 0) + 1
    return d

#converts PIL image to CMU image
def adjustImage(app, pilImage):
    pilImage = pixelate(pilImage, app.pixelsWide, app.pixelsTall, app.imageWidth, app.imageHeight)
    return CMUImage(pilImage)

def pixelate(image, pixelsWide, pixelsTall, width, height):
    image = image.resize((pixelsWide, pixelsTall), Image.NEAREST)
    return image.resize((width, height), Image.NEAREST)

#changes app.pixelsWide and app.pixelsTall when bar is slid in increments of 5 pixels
def calculate(app):
    #changes width display
    if 25 <= app.widthSlider < 30:
        app.pixelsWide = 5
    elif 30 <= app.widthSlider < 35:
        app.pixelsWide = 6
    elif 35 <= app.widthSlider < 40:
        app.pixelsWide = 7
    elif 40 <= app.widthSlider < 45:
        app.pixelsWide = 8
    elif 45 <= app.widthSlider < 50:
        app.pixelsWide = 9
    elif 50 <= app.widthSlider < 55:
        app.pixelsWide = 10
    elif 55 <= app.widthSlider < 60:
        app.pixelsWide = 11
    elif 60 <= app.widthSlider < 65:
        app.pixelsWide = 12
    elif 65 <= app.widthSlider < 70:
        app.pixelsWide = 13
    elif 70 <= app.widthSlider < 75:
        app.pixelsWide = 14
    elif 75 <= app.widthSlider < 80:
        app.pixelsWide = 15
    elif 80 <= app.widthSlider < 85:
        app.pixelsWide = 16
    elif 85 <= app.widthSlider < 90:
        app.pixelsWide = 17
    elif 90 <= app.widthSlider < 95:
        app.pixelsWide = 18
    elif 95 <= app.widthSlider < 100:
        app.pixelsWide = 19
    elif 100 <= app.widthSlider < 105:
        app.pixelsWide = 20
    elif 105 <= app.widthSlider < 110:
        app.pixelsWide = 21
    elif 110 <= app.widthSlider < 115:
        app.pixelsWide = 22
    elif 115 <= app.widthSlider < 120:
        app.pixelsWide = 23
    elif 120 <= app.widthSlider < 125:
        app.pixelsWide = 24
    elif 125 <= app.widthSlider < 130:
        app.pixelsWide = 25
    elif 130 <= app.widthSlider < 135:
        app.pixelsWide = 26
    elif 135 <= app.widthSlider < 140:
        app.pixelsWide = 27
    elif 140 <= app.widthSlider < 145:
        app.pixelsWide = 28
    elif 145 <= app.widthSlider < 150:
        app.pixelsWide = 29
    elif 150 <= app.widthSlider < 155:
        app.pixelsWide = 30
    elif 155 <= app.widthSlider < 160:
        app.pixelsWide = 31
    elif 160 <= app.widthSlider < 165:
        app.pixelsWide = 32
    elif 165 <= app.widthSlider < 170:
        app.pixelsWide = 33
    elif 170 <= app.widthSlider <= 175:
        app.pixelsWide = 34
    #changes height display
    if 25 <= app.heightSlider < 30:
        app.pixelsTall = 5
    elif 30 <= app.heightSlider < 35:
        app.pixelsTall = 6
    elif 35 <= app.heightSlider < 40:
        app.pixelsTall = 7
    elif 40 <= app.heightSlider < 45:
        app.pixelsTall = 8
    elif 45 <= app.heightSlider < 50:
        app.pixelsTall = 9
    elif 50 <= app.heightSlider < 55:
        app.pixelsTall = 10
    elif 55 <= app.heightSlider < 60:
        app.pixelsTall = 11
    elif 60 <= app.heightSlider < 65:
        app.pixelsTall = 12
    elif 65 <= app.heightSlider < 70:
        app.pixelsTall = 13
    elif 70 <= app.heightSlider < 75:
        app.pixelsTall = 14
    elif 75 <= app.heightSlider < 80:
        app.pixelsTall = 15
    elif 80 <= app.heightSlider < 85:
        app.pixelsTall = 16
    elif 85 <= app.heightSlider < 90:
        app.pixelsTall = 17
    elif 90 <= app.heightSlider < 95:
        app.pixelsTall = 18
    elif 95 <= app.heightSlider < 100:
        app.pixelsTall = 19
    elif 100 <= app.heightSlider < 105:
        app.pixelsTall = 20
    elif 105 <= app.heightSlider < 110:
        app.pixelsTall = 21
    elif 110 <= app.heightSlider < 115:
        app.pixelsTall = 22
    elif 115 <= app.heightSlider < 120:
        app.pixelsTall = 23
    elif 120 <= app.heightSlider < 125:
        app.pixelsTall = 24
    elif 125 <= app.heightSlider < 130:
        app.pixelsTall = 25
    elif 130 <= app.heightSlider < 135:
        app.pixelsTall = 26
    elif 135 <= app.heightSlider < 140:
        app.pixelsTall = 27
    elif 140 <= app.heightSlider < 145:
        app.pixelsTall = 28
    elif 145 <= app.heightSlider < 150:
        app.pixelsTall = 29
    elif 150 <= app.heightSlider < 155:
        app.pixelsTall = 30
    elif 155 <= app.heightSlider < 160:
        app.pixelsTall = 31
    elif 160 <= app.heightSlider < 165:
        app.pixelsTall = 32
    elif 165 <= app.heightSlider < 170:
        app.pixelsTall = 33
    elif 170 <= app.heightSlider <= 175:
        app.pixelsTall = 34

#changes image size based on pixels (they should be square)
def changeImageDimensions(app):
    app.pixelWidth = app.pixelHeight = 10
    app.imageWidth = app.pixelWidth * app.pixelsWide
    app.imageHeight = app.pixelHeight * app.pixelsTall

####CREATE OWN DESIGN SCREEN####
def diy_redrawAll(app):
    #draw squares
    drawBoard(app)
    drawBoardBorder(app)

    #similar slider thingy that controls squares on each dimension
    drawLabel('Adjust Size', 100, 90)

    #pixels wide
    drawLabel('Width', 100, 170)
    drawRect(100, 145, 150, 5, align = 'center')
    drawRect(225, 145, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{app.pixelsWide}', 225, 145)
    drawOval(app.widthSlider, 145, 5, 15, fill = 'blue')

    #pixels tall
    drawLabel('Height', 100, 250)
    drawRect(100, 225, 150, 5, align = 'center')
    drawRect(225, 225, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{app.pixelsTall}', 225, 225)
    drawOval(app.heightSlider, 225, 5, 15, fill = 'blue')
    #some color boxes on the side with color

def diy_onMousePress(app, mouseX, mouseY):
    #changes width
    if 130 <= mouseY and mouseY <= 160 and 25 <= mouseX and mouseX <= 175:
        app.widthSlider = mouseX
        calculate(app)
#need a different calculate function for diy
    #changes height
    elif 210 <= mouseY and mouseY <= 240 and 25 <= mouseX and mouseX <= 175:
        app.heightSlider = mouseX
        calculate(app)

#from Tetris creative task
def drawBoard(app):
    for row in range(app.pixelsWide):
        for col in range(app.pixelsTall):
            drawCell(app, row, col, app.board[row][col])

#from Tetris creative task
def drawBoardBorder(app):
  #draw the board outline (with double-thickness)
  drawRect(app.width/2, app.height/2, app.boardWidth, app.boardHeight,
           fill=None, border='black', borderWidth=2*app.cellBorderWidth, align = 'center')

#from Tetris creative task
def drawCell(app, row, col, color):
    cellLeft, cellTop = getCellLeftTop(app, row, col)
    cellWidth, cellHeight = 10, 10
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,fill=color, 
             border='black', borderWidth=app.cellBorderWidth)

#from Tetris creative task
def getCellLeftTop(app, row, col):
    cellWidth, cellHeight = 10, 10
    cellLeft = app.boardLeft + col * cellWidth
    cellTop = app.boardTop + row * cellHeight
    return (cellLeft, cellTop)

####SELECTED IMAGE SCREEN####
def imageUpload_onMousePress(app, mouseX, mouseY):
    #changes width
    if 130 <= mouseY and mouseY <= 160 and 25 <= mouseX and mouseX <= 175:
        app.widthSlider = mouseX
        #changes label and pixelization of images
        calculate(app)
        changeImageDimensions(app)
        app.cmuImage = adjustImage(app, app.pilImage)
    #changes height
    elif 210 <= mouseY and mouseY <= 240 and 25 <= mouseX and mouseX <= 175:
        app.heightSlider = mouseX
        #changes label and pixelization of images
        calculate(app)
        changeImageDimensions(app)
        app.cmuImage = adjustImage(app, app.pilImage)

def imageUpload_onMouseDrag(app, mouseX, mouseY):
    #changes width
    if 130 <= mouseY and mouseY <= 160 and abs(mouseX - app.widthSlider) <= 15:
        app.widthSlider = max(25, min(mouseX, 175))
        #change labels and pixelization image
        calculate(app)
        changeImageDimensions(app)
        app.cmuImage = adjustImage(app, app.pilImage)
        
    #changes height
    elif 210 <= mouseY and mouseY <= 240 and abs(mouseX - app.heightSlider) <= 15:
        app.heightSlider = max(25, min(mouseX, 175))
        #change labels and pixelization image
        calculate(app)
        changeImageDimensions(app)
        app.cmuImage = adjustImage(app, app.pilImage)

# def imageUpload_onMouseMove(app, mouseX, mouseY):
    #hover tool basically, with color dropper

def imageUpload_redrawAll(app):
    drawImage(app.cmuImage, app.width/2, app.height/2, align = 'center')
    #label and rectangles below are hardcoded in place
    #may move later
    drawLabel('Adjust Size', 100, 90)

    #pixels wide
    drawLabel('Width', 100, 170)
    drawRect(100, 145, 150, 5, align = 'center')
    drawRect(225, 145, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{app.pixelsWide}', 225, 145)
    drawOval(app.widthSlider, 145, 5, 15, fill = 'blue')

    #pixels tall
    drawLabel('Height', 100, 250)
    drawRect(100, 225, 150, 5, align = 'center')
    drawRect(225, 225, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{app.pixelsTall}', 225, 225)
    drawOval(app.heightSlider, 225, 5, 15, fill = 'blue')

    #draws most common colors
    for i in range(len(app.mostFrequentHex)):
        rgbVal = app.mostFrequentHex[i]
        color = rgb(rgbVal[0], rgbVal[1], rgbVal[2])
        drawRect(700, 50 * i, 20, 20, fill = color, border = 'black')

def main():
    runAppWithScreens(initialScreen = 'diy', width = app.width, height = app.height)

main()