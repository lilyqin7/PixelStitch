from cmu_graphics import *

class Slider:
    def __init__(self, leftEdge, topEdge):
        self.leftEdge = leftEdge
        self.topEdge = topEdge
        self.width = 15
        self.height = 150

    def draw(self):
        drawImage('sliderBackground.png', self.leftEdge, self.topEdge, 
                  width = self.width, height = self.height)    
    
    #used to check if mouse is pressed on slider
    def inBounds(self, mouseX, mouseY):
        rightEdge = self.leftEdge + self.width
        bottomEdge = self.topEdge + self.height
        return (self.leftEdge <= mouseX <= rightEdge and 
                self.topEdge <= mouseY <= bottomEdge)

#seperate class
class Handle:
    def __init__(self, cx, cy, slider):
        self.cx = cx
        self.cy = cy
        self.width = 30
        self.height = 10
        self.slider = slider

    def draw(self):
        drawOval(self.cx, self.cy, self.width, self.height, fill = 'darkGray')

    #calculates number of squares based on handle position
    def updateSquares(self, mouseX, mouseY):
        if self.slider.inBounds(mouseX, mouseY):
            self.cy = mouseY
        #min squares: 5, max: 50
        minSquares = 5
        numPossibilities = 45
        squaresPerPixel = numPossibilities/self.slider.height
        offset = self.cy - self.slider.topEdge
        numSquares = int(offset * squaresPerPixel + minSquares)
        return numSquares
    