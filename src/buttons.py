from cmu_graphics import *
from PIL import Image

class Button:
    def __init__(self, text, leftEdge, topEdge, width, height, fontSize, font):
        self.text = text
        self.leftEdge = leftEdge
        self.topEdge = topEdge
        self.width = width
        self.height = height
        self.fontSize = fontSize
        self.font = font

    def isSelected(self, mouseX, mouseY):
        return (self.leftEdge <= mouseX <= self.leftEdge + self.width and 
            self.topEdge <= mouseY <= self.topEdge + self.height)
    
    def drawHighlight(self):
        drawImage('buttonHighlight.png', self.leftEdge, self.topEdge, width = self.width, height = self.height)
            
    def drawButton(self):
        #image from https://stock.adobe.com/search?k=%22pink+button%22&asset_id=537039436
        drawImage('pinkButton.png', self.leftEdge, self.topEdge, width = 
                  self.width, height = self.height)
        drawLabel(self.text, (self.leftEdge + self.leftEdge + self.width)/2, 
                  (self.topEdge + self.topEdge + self.height)/2, size = 
                  self.fontSize, font = self.font)    