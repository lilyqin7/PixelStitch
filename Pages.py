#maybe need to do some wireframing for pages
#change font!! for everything
#also choose color scheme
from cmu_graphics import *

def onAppStart(app):
    app.width = 800
    app.height = 500

def distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2)**0.5

#####START SCREEN####
def start_redrawAll(app):
    drawLabel('PixelStitch', app.width/2, app.height/2, size = 50)
    #draw a yarn ball and crochet hook or something for background aesthetic

    #draw a label with 'instructions' that leads to instructions
    drawRect(app.width/4, app.height * 3/5, app.width/2, app.height/5, fill = 'pink')
    drawLabel('Click here for instructions', app.width/2, app.height * 7/10, size = 20)

#if the user clicks within the 'Click here for instructions' box, take to instructions page
def start_onMousePress(app, mouseX, mouseY):
    if mouseX >= app.width/4 and mouseX <= app.width * 3/4 and mouseY >= app.height *3/5 and mouseY <= app.height * 4/5:
        setActiveScreen('instructions')

####INSTRUCTIONS PAGE####
def instructions_redrawAll(app):
    #list all the instructions here

    #button that leads to image selection screen
    drawRect(app.width/4, app.height * 3/5, app.width/2, app.height/5, fill = 'purple')
    drawLabel('Get started!', app.width/2, app.height * 7/10, size = 20)

#if user clicks on 'Get started' box, leads to image selection page
def instructions_onMousePress(app, mouseX, mouseY):
    if mouseX >= app.width/4 and mouseX <= app.width * 3/4 and mouseY >= app.height *3/5 and mouseY <= app.height * 4/5:
        setActiveScreen('imageSelection')

####IMAGE SELECTION PAGE####
def imageSelection_redrawAll(app):
    drawLabel('Select an image', app.width/2, app.height/2, size = 20)
    #display images here
    #maybe need multiple pages to display images depending on how many will be in database

####MAIN####
#start program on the 'start' screen
def main():
    runAppWithScreens(initialScreen='start', width = app.width, height = app.height)

main()