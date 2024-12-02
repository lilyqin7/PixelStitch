# from cmu_graphics import *

# def onAppStart(app):
#     app.mouseX, app.mouseY = 0, 0
#     app.rectStart = 0, 0
#     app.rectEnd = 0, 0
#     app.drawingRect = False
#     app.isMoving = False
#     app.moveStart = 0, 0

# def onMousePress(app, mouseX, mouseY):
#     startX, startY = app.rectStart
#     endX, endY = app.rectEnd

#     # Normalize rectangle bounds
#     left = min(startX, endX)
#     right = max(startX, endX)
#     top = min(startY, endY)
#     bottom = max(startY, endY)

#     # Check if the mouse is within the normalized rectangle bounds
#     if left <= mouseX <= right and top <= mouseY <= bottom:
#         app.isMoving = True
#         app.moveStart = mouseX, mouseY
#     else:
#         app.drawingRect = True
#         app.rectStart = mouseX, mouseY
#         app.rectEnd = mouseX, mouseY  # Initialize end position

# def onMouseDrag(app, mouseX, mouseY):
#     if app.isMoving:
#         # Calculate the offset
#         xStart, yStart = app.moveStart
#         xOffset = mouseX - xStart
#         yOffset = mouseY - yStart

#         # Update the rectangle's position
#         startX, startY = app.rectStart
#         endX, endY = app.rectEnd
#         app.rectStart = startX + xOffset, startY + yOffset
#         app.rectEnd = endX + xOffset, endY + yOffset

#         # Update the start position for the next drag
#         app.moveStart = mouseX, mouseY
#     elif app.drawingRect:
#         # Update the rectangle end position as the mouse drags
#         app.rectEnd = mouseX, mouseY

# def onMouseRelease(app, mouseX, mouseY):
#     if app.isMoving:
#         app.isMoving = False  # Stop moving the rectangle
#     elif app.drawingRect:
#         app.drawingRect = False

# def redrawAll(app):
#     startX, startY = app.rectStart
#     endX, endY = app.rectEnd

#     # Normalize the rectangle's bounds
#     left = min(startX, endX)
#     right = max(startX, endX)
#     top = min(startY, endY)
#     bottom = max(startY, endY)

#     width = right - left
#     height = bottom - top

#     # Only draw if width and height are positive
#     if width > 0 and height > 0:
#         drawRect(left, top, width, height, fill=None, border='black', dashes=True)

# def main():
#     runApp(width=400, height=400)

# main()


#double click
from cmu_graphics import *
import time

def onAppStart(app):
    #miliseconds
    app.doubleClickThreshold = 300
    app.clickPosition = (0, 0)
    app.lastClickTime = 0

def onMousePress(app, mouseX, mouseY):
    currentTime = time.time() * 1000  # Current time in milliseconds
    timeSinceLastClick = currentTime - app.lastClickTime
    
    # Check if the time between clicks is less than the threshold
    if timeSinceLastClick <= app.doubleClickThreshold:
        # Check if the click happened near the last click (optional)
        if abs(mouseX - app.clickPosition[0]) < 10 and abs(mouseY - app.clickPosition[1]) < 10:
            print("Double Click Detected!")
            # You can put your double-click handling code here
    else:
        print("Single Click Detected")

    # Update the last click time and position
    app.lastClickTime = currentTime
    app.clickPosition = (mouseX, mouseY)

def main():
    runApp(width=400, height=400)

main()