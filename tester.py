from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image

def loadPilImage(url):
    image = Image.open(url)
    return image.convert('RGB')

def onAppStart(app):
    # app.pilImage = Image.open('tree-736885_1280 (1).jpg')

    app.pilImage = loadPilImage('tree-736885_1280 (1).jpg')
    # app.pilImage = Image.open(urlopen('https://drive.google.com/file/d/1d8dGuM3HUxF371DxFhoxJ7NyvzH0JWBa/view'))
    app.cmuImage = CMUImage(app.pilImage)

def redrawAll(app):
    drawImage(app.cmuImage, 0, 0)

def main():
    runApp()

main()