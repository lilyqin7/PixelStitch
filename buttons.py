from cmu_graphics import *
from PIL import Image

class Button:
    def __init__(self, text, leftEdge, topEdge, width, height, fontSize):
        self.text = text
        self.leftEdge = leftEdge
        self.topEdge = topEdge
        self.width = width
        self.height = height
        self.color = gradient(rgb(255, 191, 230), rgb(236, 125, 191))
        self.border = 'black'
        self.fontSize = fontSize

    def isSelected(self, mouseX, mouseY):
        return (self.leftEdge <= mouseX <= self.leftEdge + self.width and 
            self.topEdge <= mouseY <= self.topEdge + self.height)
    
    def drawHighlight(self):
        drawRect(self.leftEdge, self.topEdge, self.width, self.height, fill = None, border = 'black')
            
    def drawButton(self):
        #image from https://stock.adobe.com/search?k=%22pink+button%22&asset_id=537039436
        drawImage('pinkButton.png', self.leftEdge, self.topEdge, width = self.width, height = self.height)
        drawLabel(self.text, (self.leftEdge + self.leftEdge + self.width)/2, 
                  (self.topEdge + self.topEdge + self.height)/2, size = self.fontSize)    