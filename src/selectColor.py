#checks if mouse is hovering over valid color grid option
from PIL import Image

def mouseMove(app, mouseX, mouseY, colorList):
    row, col = 0, 0
    #calculate row based on mouseX position
    if 650 <= mouseX <= 668:
        col = 1
    elif 668 <= mouseX <= 686:
        col = 2
    elif 686 <= mouseX <= 704:
        col = 3
    
    #calculate col based on mouseY position
    if 100 <= mouseY <= 118:
        row = 1
    elif 118 <= mouseY <= 136:
        row = 2
    elif 136 <= mouseY <= 154:
        row = 3
    elif 154 <= mouseY <= 172:
        row = 4

    #calculates the index in colorList
    if row > 0 and col > 0:
        index = (row - 1) * 3 + (col - 1)
        if index < len(colorList):
            app.colorSelect = colorList[index]
        else:
            app.colorSelect = None
    else:
        app.colorSelect = None

#with assistance from chatGPT
def getGradientColor(app, mouseX, x0, x1, startColor, middleColor, endColor):
    midX = (x0 + x1) / 2
    if mouseX <= midX:
        r1, g1, b1 = startColor
        r2, g2, b2 = middleColor
        factor = (mouseX - x0) / (midX - x0)
    else:
        r1, g1, b1 = middleColor
        r2, g2, b2 = endColor
        factor = (mouseX - midX) / (x1 - midX)
    factor = max(0, min(1, factor))

    r = r1 + (r2 - r1) * factor
    g = g1 + (g2 - g1) * factor
    b = b1 + (b2 - b1) * factor

    return (int(r), int(g), int(b))

def getColorWheelColor(app, mouseX, mouseY):
    #check if mouse is in color wheel or in color rectangle beneath
    if app.selectColorWheel == True:
        if distance(mouseX, mouseY, 695, 280) <= 50:
            color = app.colorWheel.getpixel((mouseX - 645, mouseY - 230))
            app.colorSelect = rgb(color[0], color[1], color[2])
        elif 635 <= mouseX <= 755 and 350 <= mouseY <= 370:
            app.colorSelect = getGradientColor(app, mouseX, 635, 755, (255, 255, 255), app.selectedColorFromWheel[:3], (0, 0, 0))

    if app.colorSelect != None:
        if (isinstance(app.colorSelect, tuple) and len(app.colorSelect) == 3 and all(isinstance(c, int) for c in app.colorSelect)): #with assistance from chatGPT
            app.colorSelect = rgb(app.colorSelect[0], app.colorSelect[1], app.colorSelect[2])


def distance(x0, y0, x1, y1):
    return ((x0 - x1)**2 + (y0 - y1)**2)**0.5