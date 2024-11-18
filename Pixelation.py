#pixelation!!
from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image

def loadPilImage(url):
    image = Image.open(urlopen(url))
    return image.convert('RGB')

def onAppStart(app):
    app.width = 800
    app.height = 500
    url = 'https://www.w3schools.com/images/picture.jpg'
    #app.url does not work
    #loadPilImage only loads some images???
    app.url = 'tree-736885_1280.jpg'
    pilImage = loadPilImage(url)
    imageWidth, imageHeight = pilImage.size
    print(imageWidth, imageHeight)
    pilImage2 = pixelate(pilImage, 20, 20, imageWidth, imageHeight)
    app.cmuImage = CMUImage(pilImage2)

def pixelate(image, pixelsWide, pixelsHeight, width, height):
    image = image.resize((pixelsWide, pixelsHeight), Image.NEAREST)
    return image.resize((width, height), Image.NEAREST)

def redrawAll(app):
    drawImage(app.cmuImage, app.width/2, app.height/2, align = 'center')
    # drawImage(app.url, app.width/2, app.height/2, align = 'center')

def main():
    runApp(width = app.width, height = app.height)

main()