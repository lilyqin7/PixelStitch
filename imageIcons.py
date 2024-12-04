from cmu_graphics import *

class Icon:
    def __init__(self, iconName, leftEdge, topEdge, width, height):
        self.name = iconName
        self.leftEdge = leftEdge
        self.topEdge = topEdge
        self.width = width
        self.height = height

    def isSelected(self, mouseX, mouseY):
        return (self.leftEdge <= mouseX <= self.leftEdge + self.width and 
            self.topEdge <= mouseY <= self.topEdge + self.height)
    
    def drawIcon(self):
        drawRect(self.leftEdge - 3.25, self.topEdge - 3.25, self.width + 7.5, 
                 self.height + 7.5, fill = 'white', border = 'black')
        drawImage(f'{self.name}.png', self.leftEdge, self.topEdge, width = 
                  self.width, height = self.height)

    def drawSelected(self):
        drawRect(self.leftEdge - 8.25, self.topEdge - 8.25, self.width + 17.5, 
                 self.height + 17.5, fill = 'white', border = 'black')
        drawImage(f'{self.name}.png', self.leftEdge - 5, self.topEdge - 5, 
                  width = self.width + 10, height = self.height + 10)