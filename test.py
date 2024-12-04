from cmu_graphics import *
from scrollbar import Scrollbar

def onAppStart(app):
    app.scrollbar = Scrollbar()

def onMousePress(app, mouseX, mouseY):
    app.scrollbar.updatePosition(1000, 500)
    
def onMouseScroll(app, direction):
    if direction == 'up':
        print('hi')

def redrawAll(app):
    app.scrollbar.drawScrollBar()
    app.scrollbar.drawHandle()

def main():
    runApp(width=800, height=500)

main()