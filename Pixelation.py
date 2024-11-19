#Lily Qin, lilyq, section J
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
    #url is from www.w3schools.com
    # url = 'https://www.w3schools.com/images/picture.jpg'
    url = 'https://tinyurl.com/great-pitch-gif'
    #loadPilImage only loads some images???
    pilImage = loadPilImage(url)
    imageWidth, imageHeight = pilImage.size
    app.pixelsWide = 20
    app.pixelsTall = 20
    pilImage2 = pixelate(pilImage, app.pixelsWide, app.pixelsTall, imageWidth, imageHeight)
    app.cmuImage = CMUImage(pilImage2)

def pixelate(image, pixelsWide, pixelsTall, width, height):
    image = image.resize((pixelsWide, pixelsTall), Image.NEAREST)
    return image.resize((width, height), Image.NEAREST)

def redrawAll(app):
    drawImage(app.cmuImage, app.width/2, app.height/2, align = 'center')
    #label and rectangles below are hardcoded in place
    #may move later
    drawLabel('Adjust Size', 100, 90)

    #piexels wide
    drawLabel('Width', 100, 170)
    drawRect(100, 145, 150, 5, align = 'center')
    drawRect(225, 145, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{app.pixelsWide}', 225, 145)
    drawOval(100, 145, 5, 15, fill = 'blue')

    #pixels tall
    drawLabel('Height', 100, 250)
    drawRect(100, 225, 150, 5, align = 'center')
    drawRect(225, 225, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{app.pixelsTall}', 225, 225)
    drawOval(100, 225, 5, 15, fill = 'blue')

def main():
    runApp(width = app.width, height = app.height)

main()