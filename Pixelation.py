#app.pixelWidth, pixelHeight???
from cmu_graphics import *
from urllib.request import urlopen
from PIL import Image

def loadPilImage(url):
    image = Image.open(urlopen(url))
    return image.convert('RGB')

def onAppStart(app):
    #screen dimensions 
    app.width = 800
    app.height = 500

    #url = 'https://www.w3schools.com/images/picture.jpg'
    url = 'https://tinyurl.com/great-pitch-gif'
    #loadPilImage only loads some images???
    app.pilImage = loadPilImage(url)
    app.imageWidth, app.imageHeight = app.pilImage.size
    app.pixelsWide = 20
    app.pixelsTall = 20
    app.widthSlider = 100
    app.heightSlider = 100
    adjustImage(app, app.pilImage)

def adjustImage(app, pilImage):
    pilImage = pixelate(pilImage, app.pixelsWide, app.pixelsTall, app.imageWidth, app.imageHeight)
    app.cmuImage = CMUImage(pilImage)
    return app.cmuImage

def pixelate(image, pixelsWide, pixelsTall, width, height):
    image = image.resize((pixelsWide, pixelsTall), Image.NEAREST)
    return image.resize((width, height), Image.NEAREST)

def calculate(app):
    #changes width display
    if 25 <= app.widthSlider < 30:
        app.pixelsWide = 5
    elif 30 <= app.widthSlider < 35:
        app.pixelsWide = 6
    elif 35 <= app.widthSlider < 40:
        app.pixelsWide = 7
    elif 40 <= app.widthSlider < 45:
        app.pixelsWide = 8
    elif 45 <= app.widthSlider < 50:
        app.pixelsWide = 9
    elif 50 <= app.widthSlider < 55:
        app.pixelsWide = 10
    elif 55 <= app.widthSlider < 60:
        app.pixelsWide = 11
    elif 60 <= app.widthSlider < 65:
        app.pixelsWide = 12
    elif 65 <= app.widthSlider < 70:
        app.pixelsWide = 13
    elif 70 <= app.widthSlider < 75:
        app.pixelsWide = 14
    elif 75 <= app.widthSlider < 80:
        app.pixelsWide = 15
    elif 80 <= app.widthSlider < 85:
        app.pixelsWide = 16
    elif 85 <= app.widthSlider < 90:
        app.pixelsWide = 17
    elif 90 <= app.widthSlider < 95:
        app.pixelsWide = 18
    elif 95 <= app.widthSlider < 100:
        app.pixelsWide = 19
    elif 100 <= app.widthSlider < 105:
        app.pixelsWide = 20
    elif 105 <= app.widthSlider < 110:
        app.pixelsWide = 21
    elif 110 <= app.widthSlider < 115:
        app.pixelsWide = 22
    elif 115 <= app.widthSlider < 120:
        app.pixelsWide = 23
    elif 120 <= app.widthSlider < 125:
        app.pixelsWide = 24
    elif 125 <= app.widthSlider < 130:
        app.pixelsWide = 25
    elif 130 <= app.widthSlider < 135:
        app.pixelsWide = 26
    elif 135 <= app.widthSlider < 140:
        app.pixelsWide = 27
    elif 140 <= app.widthSlider < 145:
        app.pixelsWide = 28
    elif 145 <= app.widthSlider < 150:
        app.pixelsWide = 29
    elif 150 <= app.widthSlider < 155:
        app.pixelsWide = 30
    elif 155 <= app.widthSlider < 160:
        app.pixelsWide = 31
    elif 160 <= app.widthSlider < 165:
        app.pixelsWide = 32
    elif 165 <= app.widthSlider < 170:
        app.pixelsWide = 33
    elif 170 <= app.widthSlider <= 175:
        app.pixelsWide = 34
    #changes height display
    if 25 <= app.heightSlider < 30:
        app.pixelsTall = 5
    elif 30 <= app.heightSlider < 35:
        app.pixelsTall = 6
    elif 35 <= app.heightSlider < 40:
        app.pixelsTall = 7
    elif 40 <= app.heightSlider < 45:
        app.pixelsTall = 8
    elif 45 <= app.heightSlider < 50:
        app.pixelsTall = 9
    elif 50 <= app.heightSlider < 55:
        app.pixelsTall = 10
    elif 55 <= app.heightSlider < 60:
        app.pixelsTall = 11
    elif 60 <= app.heightSlider < 65:
        app.pixelsTall = 12
    elif 65 <= app.heightSlider < 70:
        app.pixelsTall = 13
    elif 70 <= app.heightSlider < 75:
        app.pixelsTall = 14
    elif 75 <= app.heightSlider < 80:
        app.pixelsTall = 15
    elif 80 <= app.heightSlider < 85:
        app.pixelsTall = 16
    elif 85 <= app.heightSlider < 90:
        app.pixelsTall = 17
    elif 90 <= app.heightSlider < 95:
        app.pixelsTall = 18
    elif 95 <= app.heightSlider < 100:
        app.pixelsTall = 19
    elif 100 <= app.heightSlider < 105:
        app.pixelsTall = 20
    elif 105 <= app.heightSlider < 110:
        app.pixelsTall = 21
    elif 110 <= app.heightSlider < 115:
        app.pixelsTall = 22
    elif 115 <= app.heightSlider < 120:
        app.pixelsTall = 23
    elif 120 <= app.heightSlider < 125:
        app.pixelsTall = 24
    elif 125 <= app.heightSlider < 130:
        app.pixelsTall = 25
    elif 130 <= app.heightSlider < 135:
        app.pixelsTall = 26
    elif 135 <= app.heightSlider < 140:
        app.pixelsTall = 27
    elif 140 <= app.heightSlider < 145:
        app.pixelsTall = 28
    elif 145 <= app.heightSlider < 150:
        app.pixelsTall = 29
    elif 150 <= app.heightSlider < 155:
        app.pixelsTall = 30
    elif 155 <= app.heightSlider < 160:
        app.pixelsTall = 31
    elif 160 <= app.heightSlider < 165:
        app.pixelsTall = 32
    elif 165 <= app.heightSlider < 170:
        app.pixelsTall = 33
    elif 170 <= app.heightSlider <= 175:
        app.pixelsTall = 34
    
#changes image size based on pixels (they should be square)
def changeImageDimensions(app, dimension):
    if dimension == 'width':
        app.imageWidth = int(app.pixelsWide * (app.imageHeight/app.pixelsTall))
    elif dimension == 'height':
        app.imageHeight = int(app.pixelsTall * (app.imageWidth/app.pixelsWide))

def onMousePress(app, mouseX, mouseY):
    #changes width
    if 130 <= mouseY and mouseY <= 160 and 25 <= mouseX and mouseX <= 175:
        app.widthSlider = mouseX
        #changes label and pixelization of images
        calculate(app)
        adjustImage(app, app.pilImage)
        changeImageDimensions(app, 'height')
    #changes height
    elif 210 <= mouseY and mouseY <= 240 and 25 <= mouseX and mouseX <= 175:
        app.heightSlider = mouseX
        #changes label and pixelization of images
        calculate(app)
        adjustImage(app, app.pilImage)
        changeImageDimensions(app, 'width')

def onMouseDrag(app, mouseX, mouseY):
    #changes width
    if 130 <= mouseY and mouseY <= 160 and abs(mouseX - app.widthSlider) <= 15:
        app.widthSlider = max(25, min(mouseX, 175))
        #change labels and pixelization image
        calculate(app)
        adjustImage(app, app.pilImage)
        
    #changes height
    elif 210 <= mouseY and mouseY <= 240 and abs(mouseX - app.heightSlider) <= 15:
        app.heightSlider = max(25, min(mouseX, 175))
        #change labels and pixelization image
        calculate(app)
        adjustImage(app, app.pilImage)

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
    drawOval(app.widthSlider, 145, 5, 15, fill = 'blue')

    #pixels tall
    drawLabel('Height', 100, 250)
    drawRect(100, 225, 150, 5, align = 'center')
    drawRect(225, 225, 40, 40, align = 'center', fill = None, border = 'black')
    drawLabel(f'{app.pixelsTall}', 225, 225)
    drawOval(app.heightSlider, 225, 5, 15, fill = 'blue')

def main():
    runApp(width = app.width, height = app.height)

main()