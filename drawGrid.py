from cmu_graphics import *

#modified from Tetris creative task: https://academy.cs.cmu.edu/exercise/24018

def drawGrid(app, board, boardLeft, boardTop, center):
    drawBoard(app, board, boardLeft, boardTop)
    drawBoardBorder(app, board, center)

def drawBoard(app, board, boardLeft, boardTop):
    for row in range(len(board)):
        for col in range(len(board[row])):
            drawCell(app, row, col, board[row][col], boardLeft, boardTop)

def drawBoardBorder(app, board, leftEdge):
  #draw the board outline (with double-thickness)
  drawRect(leftEdge, app.height/2, len(board[0]) * 10, len(board) * 10,
           fill=None, border='black', borderWidth=2*app.cellBorderWidth, align = 'center')
  
def drawCell(app, row, col, color, boardLeft, boardTop):
    cellLeft, cellTop = getCellLeftTop(app, row, col, boardLeft, boardTop)
    cellWidth, cellHeight = 10, 10
    drawRect(cellLeft, cellTop, cellWidth, cellHeight,fill=color, 
             border='black', borderWidth=app.cellBorderWidth)
    
def getCellLeftTop(app, row, col, boardLeft, boardTop):
    cellWidth, cellHeight = 10, 10
    cellLeft = boardLeft + col * cellWidth
    cellTop = boardTop + row * cellHeight
    return (cellLeft, cellTop)