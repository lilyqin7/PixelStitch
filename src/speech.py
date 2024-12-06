from cmu_graphics import *

class SpeechBubble:
    def __init__(self, name, left, top, width, height, reverse):
        self.name = name
        self.bubbleLeft = left
        self.bubbleTop = top
        self.bubbleWidth = width
        self.bubbleHeight = height
        self.bubbleCenterX = (self.bubbleLeft*2 + self.bubbleWidth)/2
        self.bubbleCenterY = (self.bubbleTop*2 + self.bubbleHeight)/2
        if reverse == 'reverse':
            self.reverse = True
        else:
            self.reverse = False

    def draw(self):
        if self.reverse:
            #image from Canva, linked in full-submission.txt
            drawImage('reverseSpeechBubble.png', self.bubbleLeft, self.bubbleTop, width = 
                    self.bubbleWidth, height = self.bubbleHeight)
            drawLabel(self.name, self.bubbleCenterX, self.bubbleCenterY, 
                    font = app.font)
        else:
            #image from Canva, linked in full-submission.txt
            drawImage('speechBubble.png', self.bubbleLeft, self.bubbleTop, width = 
                    self.bubbleWidth, height = self.bubbleHeight)
            drawLabel(self.name, self.bubbleCenterX, self.bubbleCenterY, 
                    font = app.font)