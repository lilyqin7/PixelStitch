from drawGrid import getCellLeftTop

#determines if there is a valid grid (in bounds) at the specified location
def isSquare(app, mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, 
             pixelsTall):
    if (boardLeft <= mouseX <= boardLeft + pixelsWide * 10 and 
        boardTop <= mouseY <= boardTop + pixelsTall * 10):
            return True
    return False

#returns the row and column of the square at the specified location
def findSquare(app, mouseX, mouseY, board, boardLeft, boardTop):
    for row in range(len(board)):
        for col in range(len(board[0])):
            cellLeft, cellTop = getCellLeftTop(app, row, col, boardLeft,
                                                boardTop)
            if (cellLeft <= mouseX <= cellLeft + 10 and 
                cellTop <= mouseY <= cellTop + 10):
                return row, col
    return None, None