from cmu_graphics import *
import os

class ImageOptions:
    def __init__(self, name, leftEdge, topEdge):
        self.name = name
        self.boxLeftEdge = leftEdge
        self.boxTopEdge = topEdge
        self.boxWidth = 200
        self.boxHeight = 150
        self.image = os.path.join('images', f'{self.name}.png')
        self.width, self.height = self.adjustImageSize()
        self.imageCenterX = self.boxLeftEdge + self.boxWidth/2
        self.imageCenterY = self.boxTopEdge + self.boxHeight/2

    def adjustImageSize(self):
        originalWidth, originalHeight = getImageSize(self.image)
        width, height = 0, 0
        factor = 1
        if originalHeight > originalWidth:
            factor = self.boxHeight/originalHeight
            originalHeight *= factor
            originalWidth *= factor
        else:
            factor = self.boxWidth/originalWidth
            originalWidth *= factor
            originalHeight *= factor
        width, height = originalWidth, originalHeight
        return width, height

    def isSelected(self, mouseX, mouseY):
        return (self.boxLeftEdge <= mouseX <= self.boxLeftEdge + self.boxWidth
                and self.boxTopEdge <= mouseY <= self.boxTopEdge + self.boxHeight)

    def draw(self):
        drawRect(self.boxLeftEdge, self.boxTopEdge, self.boxWidth, self.boxHeight, 
                 fill = 'white')
        drawImage(self.image, self.imageCenterX - self.width/2, self.imageCenterY 
                  - self.height/2, width = self.width, height = self.height)
        drawRect(self.boxLeftEdge, self.boxTopEdge, self.boxWidth, self.boxHeight, 
                 fill = None, border = 'black')
        
    def drawHighlight(self):
        whiteSpace = 25
        boxWidth = self.boxWidth + whiteSpace
        boxHeight = self.boxHeight + whiteSpace
        drawImage('imageHighlight.png', self.boxLeftEdge - whiteSpace/2, 
                  self.boxTopEdge - whiteSpace/2, width = boxWidth, 
                  height = boxHeight)
        drawImage(self.image, self.imageCenterX - self.width/2, self.imageCenterY 
                  - self.height/2, width = self.width, height = self.height)
        
    def drawSelected(self):
        whiteSpace = 25
        boxWidth = self.boxWidth + whiteSpace
        boxHeight = self.boxHeight + whiteSpace
        drawImage('imageSelected.png', self.boxLeftEdge - whiteSpace/2, 
                  self.boxTopEdge - whiteSpace/2, width = boxWidth, 
                  height = boxHeight)
        drawImage(self.image, self.imageCenterX - self.width/2, self.imageCenterY 
                  - self.height/2, width = self.width, height = self.height)
    