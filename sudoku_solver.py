def find_empty(board):
    # Looping thru the whole board to find a empty spot indicated by a vaule of 0
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 0:
                return (row, col)
    return None

def valid_num(board, num, pos):
    #Check row
    for number in range(len(board[pos[0]])):
        if board[pos[0]][number] == num and number != pos[1]: # Invalid Num
            return False
    
    # Check col
    for col in range(9):
        if board[col][pos[1]] == num and col != pos[0]:
            return False

    # Check Sub-Grid
    grid_x = (pos[1] // 3) * 3 # Checking to see what subgrid we are in
    grid_y = (pos[0] // 3) * 3

    for row in range(grid_y, grid_y + 3):
        for col in range(grid_x, grid_x + 3):
            if board[row][col] == num and (row, col) != pos:
                return False

    # The num is a valid input
    return True


def solve_sudoku(board):
    empty_pos = find_empty(board)

    # The board is full which mean we solved the sudoku (Base Case)
    if empty_pos is None:
        return True

    row, col = empty_pos
    for number in range(1, 10):
        if valid_num(board, number, (row, col)): # if valid placement
            board[row][col] = number
            if solve_sudoku(board):
                return True
            board[row][col] = 0 # Backtracking, our past placements did not work so try another number
    return False # A solution has not been found yet