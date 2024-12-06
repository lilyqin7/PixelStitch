from cmu_graphics import *

#modified from Tetris creative task: https://academy.cs.cmu.edu/exercise/24018

app.cellBorderWidth = 1

def drawGrid(app, board, boardLeft, boardTop, center):
    drawBoard(app, board, boardLeft, boardTop)
    drawBoardBorder(app, board, center)

#draws many cells
def drawBoard(app, board, boardLeft, boardTop):
    for row in range(len(board)):
        for col in range(len(board[row])):
            drawCell(app, row, col, board[row][col], boardLeft, boardTop)

#draw the board outline (with double-thickness)
def drawBoardBorder(app, board, leftEdge):
  drawRect(leftEdge, app.height/2, len(board[0]) * 10, len(board) * 10,
           fill=None, border='black', borderWidth=2*app.cellBorderWidth, 
           align = 'center')
  
#draws cell using specified inicies
def drawCell(app, row, col, color, boardLeft, boardTop):
    cellLeft, cellTop = getCellLeftTop(app, row, col, boardLeft, boardTop)
    cellWidth, cellHeight = 10, 10
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,fill=color, 
             border='black', borderWidth=app.cellBorderWidth)
    
#finds coordinates necessary to draw
def getCellLeftTop(app, row, col, boardLeft, boardTop):
    cellWidth, cellHeight = 10, 10
    cellLeft = boardLeft + col * cellWidth
    cellTop = boardTop + row * cellHeight
    return (cellLeft, cellTop)