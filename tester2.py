#fill tool
import copy
def isSquare(mouseX, mouseY, board, boardLeft, boardTop, pixelsWide, pixelsTall):
    if (boardLeft <= mouseX <= boardLeft + pixelsWide * 10 and boardTop <= mouseY <= boardTop + pixelsTall * 10):
        return True
    return False

def findSquare(mouseX, mouseY, board, boardLeft, boardTop):
    for row in range(len(board)):
        for col in range(len(board[0])):
            cellLeft, cellTop = getCellLeftTop(row, col, boardLeft, boardTop)
            if cellLeft <= mouseX <= cellLeft + 10 and cellTop <= mouseY <= cellTop + 10:
                return row, col

def getCellLeftTop(row, col, boardLeft, boardTop):
    cellWidth, cellHeight = 10, 10
    cellLeft = boardLeft + col * cellWidth
    cellTop = boardTop + row * cellHeight
    return (cellLeft, cellTop)

def isBounded(row, col):
    if diyBoard[row][col] != None:
        return False
    else:
        for startRow in range(len(diyBoard)):
            for startCol in range(len(diyBoard[0])):
                if (startRow, startCol) != (row, col):
                    solution =  isBoundedHelper(startRow, startCol, [], None, None)
                    if solution:
                        return solution
        return False

#help from TA at OH 
def isBoundedHelper(startRow, startCol, visited, drowN, dcolN):
    if diyBoard[startRow][startCol] == None:
        return False 
    elif len(visited) > 2 and (startRow, startCol) == visited[0]:
        return True
    else:
        if len(visited) == 0: 
            visited.append((startRow, startCol))
        directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        for drow, dcol in directions:
            if isLegalMove(startRow, startCol, drow, dcol) and ((drowN, dcolN) == (None, None) or (-drowN != drow or -dcolN != dcol)) and (startRow + drow, startCol + dcol) not in visited[1:]:
                visited.append((startRow + drow, startCol + dcol))
                solution = isBoundedHelper(startRow + drow, startCol + dcol, visited, drow, dcol)
                if solution:
                    return visited
                visited.pop()
        return False  

def isLegalMove(startRow, startCol, drow, dcol):
    if 0 <= startRow + drow < len(diyBoard) and 0 <= startCol + dcol < len(diyBoard[0]):
        return True
    return False

def findBoundedSquaresHelper(pressedRow, pressedCol, boundedSquares):
    if diyBoard[pressedRow][pressedCol] != None:
        return False
    elif len(boundedSquares) == numSquares:
        return True
    else:
        if len(boundedSquares) == 0:
            boundedSquares.append((pressedRow, pressedCol))
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        for drow, dcol in directions:
            if isLegalMove(pressedRow, pressedCol, drow, dcol) and (pressedRow + drow, pressedCol + dcol) not in boundedSquares:
                boundedSquares.append((pressedRow + drow, pressedCol + dcol))
                solution = findBoundedSquaresHelper(pressedRow + drow, pressedCol + dcol, boundedSquares)
                if solution:
                    return boundedSquares
                boundedSquares.pop()
        return False

def findBoundedSquares(mouseX, mouseY):
    pressedRow, pressedCol = findSquare(mouseX, mouseY, diyBoard, diyBoardLeft, diyBoardTop)
    return findBoundedSquaresHelper(pressedRow, pressedCol, [])

def fillShape(color, mouseX, mouseY):
    squares = findBoundedSquares(mouseX, mouseY)
    for square in squares:
        row, col = square
        diyBoard[row][col] = color
    return diyBoard

def findNumSquaresToFill(board):
    numSquares = 0
    for row in board:
        if 'blue' in row:
            colStart = row.index('blue')
            colEnd = colStart
            row[colStart] = 0
            if 'blue' in row:
                colEnd = row.index('blue')
            for col in range(colStart + 1, colEnd):
                numSquares += 1
    return numSquares

diyBoard = [[None, 'blue', None, None, None, None],
            ['blue', None, 'blue', None, None, None],
            ['blue', None, None, 'blue', None, None],
            [None, 'blue', None, None, 'blue', None],
            [None, None, 'blue', None, 'blue', None],
            [None, None, None, 'blue', None, None]]

diyBoardLeft, diyBoardTop = 0, 0
diyPixelsWide = 4
diyPixelsTall = 4
board = copy.deepcopy(diyBoard)
numSquares = findNumSquaresToFill(board)
print(fillShape('blue', 15, 15))
# print(findNumSquaresToFill())

[[None, 'blue', None, None, None, None], 
 ['blue', 'blue', 'blue', None, None, None], 
 ['blue', 'blue', 'blue', 'blue', None, None], 
 [None, 'blue', 'blue', 'blue', 'blue', None], 
 [None, None, 'blue', 'blue', 'blue', None], 
 [None, None, None, 'blue', None, None]]