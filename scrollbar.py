from cmu_graphics import *

class Scrollbar:
    def __init__(self):
        self.yLocation = 0
        self.height = 500

    def updatePosition(self, contentHeight, currentContentLocation):
        self.height = 500 / (contentHeight/500)
        bounds = 500 - self.height
        self.yLocation = currentContentLocation * bounds / 500

    #draws scrollbars
    def drawScrollBar(self):
        drawRect(788, 0, 12, 500, fill = 'lightGray')

    def drawHandle(self):
        drawRect(788, self.yLocation, 12, self.height, fill = 'gray')
    
    