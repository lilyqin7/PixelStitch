from cmu_graphics import *
import os

class Icon:
    def __init__(self, iconName, leftEdge, topEdge, width, height):
        self.name = iconName
        self.leftEdge = leftEdge
        self.topEdge = topEdge
        self.rightEdge = leftEdge + width
        self.bottomEdge = topEdge + height
        self.width = width
        self.height = height

    def isSelected(self, mouseX, mouseY):
        return (self.leftEdge <= mouseX <= self.rightEdge and 
                self.topEdge <= mouseY <= self.bottomEdge)
    
    #default icon
    def drawIcon(self):
        iconBorder = 3.25
        drawRect(self.leftEdge - iconBorder, self.topEdge - iconBorder, 
                 self.width + 2 * iconBorder, self.height + 2 * iconBorder, 
                 fill = 'white', border = 'black')
        drawImage(os.path.join('icons', f'{self.name}.png'), self.leftEdge, 
                  self.topEdge, width = self.width, height = self.height)

    #moves with mouse
    def drawMovingIcon(self, mouseX, mouseY):
        drawImage(os.path.join('icons', f'{self.name}.png'), mouseX, mouseY, 
                  width = 20, height = 20)

    #animates to be larger if mouse hoovering over
    def drawSelected(self):
        iconBorder = 8.25
        drawRect(self.leftEdge - iconBorder, self.topEdge - iconBorder, 
                 self.width + 2 * iconBorder, self.height + 2 * iconBorder, 
                 fill = 'white', border = 'black')
        drawImage(os.path.join('icons', f'{self.name}.png'), self.leftEdge - 5, self.topEdge - 5, 
                  width = self.width + 10, height = self.height + 10)