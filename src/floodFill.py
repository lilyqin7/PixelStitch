from squareFunctions import findSquare

#takes the point mouse is pressed (row, col) and finds the 'start' of the 'bound'
def isBounded(app, row, col, board):
    if board[row][col] != None:
        return False
    else:
        for startRow in range(row, len(board)):
            for startCol in range(col, len(board[0])):
                if (startRow, startCol) != (row, col):
                    solution =  isBoundedHelper(app, startRow, startCol, [], 
                                                None, None, board)
                    if solution:
                        return solution
        return False

#help from TA at OH 
#returns a list of indicies that are the bounds
def isBoundedHelper(app, startRow, startCol, visited, drowN, dcolN, board):
    if board[startRow][startCol] == None:
        return False 
    elif len(visited) > 2 and (startRow, startCol) == visited[0]:
        return True
    else:
        if len(visited) == 0: 
            visited.append((startRow, startCol))
        #diagonals too!
        directions = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), 
                      (-1, 0), (-1, -1)]
        for drow, dcol in directions:
            if (isLegalMove(app, startRow, startCol, drow, dcol, board) and 
                ((drowN, dcolN) == (None, None) or 
                 (-drowN != drow or -dcolN != dcol)) 
                and (startRow + drow, startCol + dcol) not in visited[1:]):
                visited.append((startRow + drow, startCol + dcol))
                solution = isBoundedHelper(app, startRow + drow, startCol + 
                                           dcol, visited, drow, dcol, board)
                if solution:
                    return visited
                visited.pop()
        return False  

#returns if next square is in the board
def isLegalMove(app, startRow, startCol, drow, dcol, board):
    return (0 <= startRow + drow < len(board) and 0 <= startCol + dcol < 
            len(board[0]))

#returns the MOST outer bounds in all directions
def findMinMaxFillBoundaries(app, boundaries):
    maxRow, maxCol = 0, 0
    if boundaries != False:
        for coordinate in boundaries:
            if coordinate[0] > maxRow:
                maxRow = coordinate[0]
            if coordinate[1] > maxCol:
                maxCol = coordinate[1]
        minRow, minCol = maxRow, maxCol
        for coordinate in boundaries: 
            if coordinate[0] < minRow:
                minRow = coordinate[0]
            if coordinate[1] < minCol:
                minCol = coordinate[1]
        return minRow, minCol, maxRow, maxCol

#goes through each square, determines if the square is "bounded" by identifying
#bounds in that row
def inBounds(app, selectedRow, selectedCol):
    #holds column indicies
    currentRow = set()
    #searches through bounded indicies, adds the column index of same row to set
    for coordinate in app.boundaries:
        if coordinate[0] == selectedRow:
            currentRow.add(coordinate[1])
    #if the selected column is on the boundaries
    if selectedCol in currentRow:
        return False
    #if it is out of bounds
    minCol = min(currentRow)
    maxCol = max(currentRow)
    if minCol > selectedCol or maxCol < selectedCol:
        return False
    return True

#returns squares inside bounds (to be filled)
def findBoundedSquaresHelper(app, pressedRow, pressedCol, boundedSquares, board):
    app.boundaries = isBounded(app, pressedRow, pressedCol, board)
    if app.boundaries:
        minRow, minCol, maxRow, maxCol = findMinMaxFillBoundaries(app, 
                                                                  app.boundaries)
        for row in range(minRow, maxRow):
            for col in range(minCol, maxCol):
                if inBounds(app, row, col):
                    boundedSquares.add((row, col))
    return boundedSquares

#returns squares inside bounds (to be filled)
def findBoundedSquares(app, mouseX, mouseY, board, boardLeft, boardTop):
    pressedRow, pressedCol = findSquare(app, mouseX, mouseY, board, boardLeft, 
                                        boardTop)
    return findBoundedSquaresHelper(app, pressedRow, pressedCol, set(), board)

#changes the identified squares in the board, returns board
def fillShape(app, fillColor, mouseX, mouseY, board, boardLeft, boardTop):
    squares = findBoundedSquares(app, mouseX, mouseY, board, boardLeft, boardTop)
    for square in squares:
        row, col = square
        board[row][col] = fillColor
    return board