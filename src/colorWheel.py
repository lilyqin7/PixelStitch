from cmu_graphics import *
from PIL import Image

class ColorSelection:
    def __init__(self, leftEdge, topEdge, whiteSpace, width, height, colorList):
        #box variables
        self.leftEdge = leftEdge
        self.topEdge = topEdge
        self.whiteSpace = whiteSpace
        self.width = width
        self.height = height
        self.colorList = colorList
        #wheel variables
        self.wheelWidth, self.wheelHeight = 100, 100
        self.wheelLeft = self.leftEdge + self.whiteSpace
        self.wheelTop = self.topEdge + self.whiteSpace
        self.wheelRadius = 50
        #gradient box variables
        self.rectLeft = self.leftEdge + self.whiteSpace - 10
        self.rectTop = self.topEdge + self.height - 4.5*self.whiteSpace
        self.rectWidth, self.rectHeight = 120, 20
        #https://www.clipartmax.com/download/m2i8G6N4A0N4A0H7_color-color-wheel-wheel-icon-color-wheel-transparent-background/ 
        self.wheelImage = Image.open('colorwheel.png').resize((self.wheelWidth, 
                                                              self.wheelHeight))
        #colorselect variables
        #self.colorSelect for hoovering only
        self.colorSelect = None
        self.selectedFromColorWheel = False
        self.selectedColorFromWheel = (0, 0, 0)

        #dragging state
        self.startDragging = False
        self.isDragging = False
        self.distanceFromMouseXtoLeft = 0
        self.distanceFromMouseYtoTop = 0

    def draw(self):
        if self.isDragging:
            drawImage('panelHighlight.png', self.leftEdge - 10, self.topEdge - 
                      10, width = self.width + 20, height = self.height + 20)
        #draw background
        else:
            drawRect(self.leftEdge, self.topEdge, self.width, self.height, 
                 fill = 'white', border = 'black')
        #draw color wheel
        drawImage(CMUImage(self.wheelImage), self.wheelLeft, self.wheelTop)
        #draw color panels
        self.drawColorPanel()
        #draw gradient box
        self.drawGradientBox()

    def drawSelected(self, mouseX, mouseY):
        #background, must move with mouse
        self.move(mouseX, mouseY)
        drawImage('buttonHighlight.png', self.leftEdge - 10, self.topEdge - 10,
                  width = self.width + 20, height = self.height + 20)
        #draw color wheel
        drawImage(CMUImage(self.wheelImage), self.leftEdge + self.whiteSpace, 
                  self.topEdge + self.whiteSpace)
        #draw color panels
        self.drawColorPanel()
        #draw gradient box
        self.drawGradientBox()

    def drawGradientBox(self):
        #if user has selected color from wheel
        if self.selectedFromColorWheel:
            color = rgb(self.selectedColorFromWheel[0], 
                        self.selectedColorFromWheel[1], 
                        self.selectedColorFromWheel[2])
            print(color)
            drawRect(self.rectLeft, self.rectTop, self.rectWidth, 
                     self.rectHeight, fill = gradient('white', color, 'black', 
                     start = 'left'), border = 'black')
        #if mouse is hoovering over circle or grid
        elif self.colorSelect != None:
            print(self.colorSelect)
            drawRect(self.rectLeft, self.rectTop, self.rectWidth, 
                     self.rectHeight, fill = gradient('white', self.colorSelect,
                                                      'black', start = 'left'), 
                                                      border = 'black')
        else:
            drawRect(self.rectLeft, self.rectTop, self.rectWidth, 
                     self.rectHeight, fill = gradient('white', 'black', start = 
                                                      'left'), border = 'black')
        
    def drawColorPanel(self):
        for i in range(len(self.colorList)):
            row, col = i % 5, i // 5
            width, height = 20, 20
            borderWidth = 2
            topEdge = self.topEdge + self.height - self.whiteSpace - 40
            if isinstance(self.colorList[i], str):
                drawRect(self.leftEdge + self.whiteSpace + row*width, topEdge + 
                         col*height, width + borderWidth, height + borderWidth, 
                         fill = self.colorList[i], border = 'black')
            else:
                rgbVal = self.colorList[i]
                color = rgb(rgbVal[0], rgbVal[1], rgbVal[2])
                drawRect(self.leftEdge + row*width + self.whiteSpace, topEdge + 
                         col*height, width + borderWidth, height + borderWidth, 
                         fill = color, border = 'black')
                
    def isSelected(self, mouseX, mouseY):
        return (self.leftEdge <= mouseX <= self.leftEdge + self.width and 
                self.topEdge <= mouseY <= self.topEdge + self.height)

    def wheelSelected(self, mouseX, mouseY):
        cx = (self.wheelLeft*2 + self.wheelWidth)/2
        cy = (self.wheelTop*2 + self.wheelHeight)/2
        return (distance(mouseX, mouseY, cx, cy) <= self.wheelRadius)
    
    def gradientSelected(self, mouseX, mouseY):
        return (self.rectLeft <= mouseX <= self.rectLeft + self.rectWidth and 
                self.rectTop <= mouseY <= self.rectTop + self.rectHeight)
    
    def colorGridSelected(self, mouseX, mouseY):
        row, col = -1, -1
        width, height = 20, 20
        startX = self.leftEdge + self.whiteSpace
        startY = self.topEdge + self.height - self.whiteSpace - 40
        borderWidth = 2
        #calculate row based on mouseX position
        if (startX <= mouseX <= startX + width):
            col = 0
        elif (startX + width + borderWidth <= mouseX <= startX + width*2 + 
              borderWidth):
            col = 1
        elif (startX + width*2 + borderWidth*2 <= mouseX <= startX + width*3 + 
              borderWidth*2):
            col = 2
        elif (startX + width*3 + borderWidth*3 <= mouseX <= startX + width*4 + 
              borderWidth*3):
            col = 3
        elif (startX + width*4 + borderWidth*4 <= mouseX <= startX + width*5 + 
              borderWidth*4):
            col = 4
        #calculate col based on mouseY position
        if (startY <= mouseY <= startY + height):
            row = 0
        elif (startY + height + borderWidth <= mouseY <= startY + height*2 + 
              borderWidth):
            row = 1
        #calculates the index in colorList
        if row > -1 and col > -1:
            numCols = 5
            index = row*numCols + col
            # print('hi', index)
            if index < len(self.colorList):
                self.colorSelect = self.colorList[index]
            else:
                self.colorSelect = None
        else:
            self.colorSelect = None
        self.convertToRGB()
        return self.colorSelect

    def distance(x0, y0, x1, y1):
        return (((x0 - x1)**2 + (y0 - y1)**2)**0.5)
    
    def getPixel(self, mouseX, mouseY):
        return self.wheelImage.getpixel((mouseX - self.wheelLeft, mouseY - 
                                         self.wheelTop))
    
    #with assistance from chatGPT
    def getGradientColor(self, mouseX, x0, x1, startColor, middleColor, 
                         endColor):
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

    def getColorWheelColor(self, mouseX, mouseY):
        #check wheel
        if self.wheelSelected(mouseX, mouseY):
            color = self.getPixel(mouseX, mouseY)
            self.colorSelect = rgb(color[0], color[1], color[2])
        #check gradient box
        elif self.gradientSelected(mouseX, mouseY):
            self.colorSelect = self.getGradientColor(mouseX, self.rectLeft, 
                                                self.rectLeft + self.rectWidth, 
                                                (255, 255, 255), 
                                                self.selectedColorFromWheel[:3],
                                                (0, 0, 0))
        self.convertToRGB()
        return self.colorSelect
    
    def startMove(self, mouseX, mouseY):
        self.startDragging = True
        self.distanceFromMouseXtoLeft = mouseX - self.leftEdge
        self.distanceFromMouseYtoTop = mouseY - self.topEdge

    def move(self, mouseX, mouseY):
        if self.startDragging:
            self.isDragging = True
        self.leftEdge = mouseX - self.distanceFromMouseXtoLeft
        self.topEdge = mouseY - self.distanceFromMouseYtoTop
        self.rectLeft = self.leftEdge + self.whiteSpace - 10
        self.rectTop = self.topEdge + self.height - 4.5*self.whiteSpace
        self.wheelLeft = self.leftEdge + self.whiteSpace
        self.wheelTop = self.topEdge + self.whiteSpace

    def endMove(self):
        self.startDragging = False
        self.isDragging = False

    #converts (r, g, b) to rgb(r, g, b), necessary for drawing color
    def convertToRGB(self):
        if self.colorSelect != None:
            #with minor assistance from chatGPT on all() part
            if (isinstance(self.colorSelect, tuple) and len(self.colorSelect) 
                == 3 and all(isinstance(c, int) for c in self.colorSelect)): 
                self.colorSelect = rgb(self.colorSelect[0], self.colorSelect[1], 
                                      self.colorSelect[2])