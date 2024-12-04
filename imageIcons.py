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
    
    def drawIcon(self):
        iconBorder = 3.25
        drawRect(self.leftEdge - iconBorder, self.topEdge - iconBorder, 
                 self.width + 2 * iconBorder, self.height + 2 * iconBorder, 
                 fill = 'white', border = 'black')
        drawImage(os.path.join('icons', f'{self.name}.png'), self.leftEdge, 
                  self.topEdge, width = self.width, height = self.height)

    def drawMovingIcon(self, mouseX, mouseY):
        drawImage(os.path.join('icons', f'{self.name}.png'), mouseX, mouseY, 
                  width = 20, height = 20)

    def drawSelected(self):
        iconBorder = 8.25
        drawRect(self.leftEdge - iconBorder, self.topEdge - iconBorder, 
                 self.width + 2 * iconBorder, self.height + 2 * iconBorder, 
                 fill = 'white', border = 'black')
        drawImage(os.path.join('icons', f'{self.name}.png'), self.leftEdge - 5, self.topEdge - 5, 
                  width = self.width + 10, height = self.height + 10)
        
    # def drawLabels(self):
    #     #https://www.pngwing.com/en/free-png-zsojt/download
    #     labelLeftEdge = self.leftEdge - 10
    #     labelWidth = self.width + 20
    #     drawImage('iconLabel.png', labelLeftEdge, self.bottomEdge, 
    #               width = labelWidth, height = self.height)
    #     drawLabel(self.name, (self.leftEdge + self.rightEdge)/2, 
    #               self.bottomEdge - self.height/2, size = 6)