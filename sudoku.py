import pygame
import sudoku_solver
pygame.init()


WIDTH = 600
HEIGHT = 600
GRID_BORDER = 8
SQUARE_BORDER = 2
SQUARE = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


EASY_BOARD = [
    [2, 0, 0, 4, 5, 0, 0, 1, 8],
    [0, 0, 5, 0, 2, 0, 4, 0, 0],
    [4, 8, 6, 0, 0, 9, 0, 3, 5],
    [0, 0, 1, 0, 0, 0, 0, 8, 0],
    [8, 0, 0, 0, 9, 0, 0, 0, 1],
    [0, 3, 0, 0, 0, 0, 5, 0, 0],
    [6, 4, 0, 7, 0, 0, 8, 2, 3],
    [0, 0, 7, 0, 8, 0, 9, 0, 0],
    [5, 2, 0, 0, 4, 3, 0, 0, 7],
]

MEDIUM_BOARD = [
    [0, 3, 0, 0, 2, 0, 7, 6, 0],
    [0, 0, 6, 9, 0, 7, 0, 0, 1],
    [0, 0, 7, 0, 0, 8, 0, 0, 0],
    [4, 0, 3, 5, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 3, 9, 0, 5],
    [0, 0, 0, 8, 0, 0, 3, 0, 0],
    [5, 0, 0, 2, 0, 6, 4, 0, 0],
    [0, 8, 1, 0, 7, 0, 0, 5, 0],
]

HARD_BOARD = [
    [0, 8, 0, 0, 1, 0, 0, 0, 5],
    [6, 0, 0, 0, 0, 0, 3, 0, 0],
    [1, 0, 3, 0, 0, 6, 0, 0, 4],
    [0, 0, 0, 3, 0, 0, 1, 4, 0],
    [0, 0, 0, 6, 0, 7, 0, 0, 0],
    [0, 5, 4, 0, 0, 9, 0, 0, 0],
    [3, 0, 0, 8, 0, 0, 4, 0, 9],
    [0, 0, 7, 0, 0, 0, 0, 0, 2],
    [5, 0, 0, 0, 2, 0, 0, 1, 0],
]

SUPER_HARD_BOARD = [
    [0, 0, 5, 1, 0, 0, 0, 4, 0],
    [0, 0, 2, 0, 0, 0, 8, 0, 0],
    [0, 0, 0, 0, 7, 0, 6, 0, 3],
    [4, 0, 6, 0, 0, 2, 0, 0, 0],
    [0, 0, 0, 5, 0, 1, 0, 0, 0],
    [0, 0, 0, 9, 0, 0, 1, 0, 2],
    [5, 0, 7, 0, 9, 0, 0, 0, 0],
    [0, 0, 9, 0, 0, 0, 4, 0, 0],
    [0, 3, 0, 0, 0, 8, 9, 0, 0],
]

class Sudoku:
    def __init__(self, board):
        self._board = [ [board[row][col] for col in range(9)] for row in range(9) ]
        self._window = pygame.display.set_mode((WIDTH, HEIGHT))
        self._running = False
        self.chosen = None # position of square that was chosen if applicable
        self.squares = [ [Square(self._board[row][col], (row, col), self._window) for col in range(9)] for row in range(9) ]

    def run(self):
        """
        Main loop of the sudoku board.
        Takes care of keyboard input and updating/drawing the board
        """
        pygame.display.set_caption("Sudoku")
        self._running = True
        key = None
        keys = {pygame.K_1: 1, pygame.K_2: 2, pygame.K_3: 3, pygame.K_4: 4, pygame.K_5: 5, pygame.K_6: 6, pygame.K_7: 7, pygame.K_8: 8, pygame.K_9: 9}

        while self._running:

            # In order to clear red rects
            self._window.fill(WHITE)
            self.draw_grid()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    self._running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.chosen = self.square_chosen(pygame.mouse.get_pos())
                if event.type == pygame.KEYDOWN:
                    if event.key in keys: # Key number that was chosen
                        key = keys[event.key]
                    if event.key == pygame.K_RETURN and self.chosen: # Enter key to confirm number key input on chosen square 
                        self.squares[self.chosen[0]][self.chosen[1]].confirm_change()
                        self.chosen = None
                        self.update_board()

                        # Checks to see if board is complete and a valid solution was found
                        if self.board_complete() and self.valid_sudoku():
                            print("You solved the sudoku board!!")
                    # Solves sudoku automatically using Backtracking algorithm
                    if event.key == pygame.K_ESCAPE:
                        self.solve_sudoku()

            # Draw selected number key on square that was selected
            if self.chosen and key:
                self.squares[self.chosen[0]][self.chosen[1]].set_key(key)
                key = None


    def draw_grid(self):
        """
        Draws the grid of the sudoku board and
        the values within each single square
        """
        #The space between each square
        space = WIDTH / 9
        for row in range(10):
            # Thick border to indicate the whole board and subgrids
            if row % 3 == 0 and row != 0:
                # Vertical Line and then Horizontal Line
                pygame.draw.line(self._window, BLACK, (row * space, 0), (row * space, HEIGHT), GRID_BORDER)
                pygame.draw.line(self._window, BLACK, (0, row * space), (WIDTH, row * space), GRID_BORDER)
            # Border to seperate each square
            else:
                pygame.draw.line(self._window, BLACK, (row * space, 0), (row * space, HEIGHT), SQUARE_BORDER)
                pygame.draw.line(self._window, BLACK, (0, row * space), (WIDTH, row * space), SQUARE_BORDER)

        # Draw the values for each square
        for row in range(9):
            for col in range(9):
                self.squares[row][col].draw()

    def square_chosen(self, mouse_pos):
        """
        Calculates which square was chosen
        and returns the row and col of that square
        """
        # Reset all squares labeled chosen in self.squares to not chosen
        for row in range(9):
            for col in range(9):
                if self.squares[row][col].chosen:
                    self.squares[row][col].chosen = False
        space = WIDTH / 9
        row = int(mouse_pos[1] // space)
        col = int(mouse_pos[0] // space)
        self.squares[row][col].chosen = True
        return (row, col)
    
    def update_board(self):
        """
        Updates self._board to reflect the values
        of the squares in self.squares
        """
        self._board = [ [self.squares[row][col].value for col in range(9)] for row in range(9) ]

    def board_complete(self):
        """
        Checks to see if the board is completed
        by checking to see if each squares has a
        value that does != 0
        """
        for row in range(9):
            for col in range(9):
                if self._board[row][col] == 0:
                    return False
        return True

    def valid_sudoku(self):
        """
        Checks to see if completed board is a valid solution
        """
        for row in range(9):
            for col in range(9):
                if not sudoku_solver.valid_num(self._board, self._board[row][col], (row, col)):
                    return False
        return True

    def solve_sudoku(self):
        """
        Solves sudoku board using the Backtracking algorithm
        Draws the values the algorithm is testing to visualize
        how it backtracks
        """
        empty_pos = sudoku_solver.find_empty(self._board)

        # The board is full which mean we solved the sudoku (Base Case)
        if empty_pos is None:
            return True

        row, col = empty_pos
        for number in range(1, 10):
            if sudoku_solver.valid_num(self._board, number, (row, col)): # if valid placement

                self._board[row][col] = number
                self.squares[row][col].value = number
                self.squares[row][col].backtrack()
                pygame.display.update()
                # Delay to show backtracking in action
                pygame.time.delay(10)

                if self.solve_sudoku():
                    return True
                
                self._board[row][col] = 0 # Backtracking, our past placements did not work so try another number
                self.squares[row][col].value = 0
                self.squares[row][col].backtrack()
                pygame.display.update()
                pygame.time.delay(10)
        
        return False # A solution has not been found yet
    

class Square:
    def __init__(self, value, pos, window):
        self.value = value
        self.row = pos[0]
        self.col = pos[1]
        self.change = 0 # Represents the number key that was entered for this square
        self.chosen = False
        self.window = window
        self.font = pygame.font.SysFont('Times New Roman', 35)

    def draw(self):
        """
        Draws the value for the sqaure positioned at self.row and self.col
        If the square has a value of 0 then self.change is drawn instead
        """
        x = self.col * (WIDTH / 9)
        y = self.row * (WIDTH / 9)
        center = (WIDTH / 9) / 2
        
        if self.change != 0:
            text_surface = self.font.render(str(self.change), True, (0, 0, 255))
            self.window.blit(text_surface, (x + (center - text_surface.get_width() / 2), y + (center - text_surface.get_height() / 2)))
        elif self.value != 0:
            text_surface = self.font.render(str(self.value), True, BLACK)
            self.window.blit(text_surface, (x + (center - text_surface.get_width() / 2), y + (center - text_surface.get_height() / 2)))

        if self.chosen:
            pygame.draw.rect(self.window, (255, 0, 0), (x, y, WIDTH / 9, WIDTH / 9), 2)

    def set_key(self, key):
        """
        Changes the value of self.change to key
        """
        self.change = key

    def confirm_change(self):
        """
        Changes the value of self.value to the value of self.change.
        Function is ran when user uses the 'Enter' key to confirm the value
        of a square.
        """
        self.value = self.change
        self.change = 0

    def backtrack(self):
        """
        Draws the values for square when Backtracking
        algorithm is being used
        """
        pygame.event.get()
        x = self.col * (WIDTH / 9)
        y = self.row * (WIDTH / 9)
        center = (WIDTH / 9) / 2

        # Fill square with white rect to 'erase' previous value in square
        pygame.draw.rect(self.window, WHITE, (x, y, WIDTH / 9, WIDTH / 9))

        if self.value != 0:
            text_surface = self.font.render(str(self.value), True, (255, 0, 0))
            self.window.blit(text_surface, (x + (center - text_surface.get_width() / 2), y + (center - text_surface.get_height() / 2)))
        
        pygame.draw.rect(self.window, BLACK, (x, y, WIDTH / 9, WIDTH / 9), 2)

if __name__ == '__main__':
    board = None
    while True:
        choice = int(input(''' 
    Please choose what board you want by entering the corresponding number:
        1: Easy Board
        2: Medium Board
        3: Hard Board
        4: Super Hard Board
        '''))
        if choice == 1:
            board = EASY_BOARD
            break
        elif choice == 2:
            board = MEDIUM_BOARD
            break
        elif choice == 3:
            board = HARD_BOARD
            break
        elif choice == 4:
            board = SUPER_HARD_BOARD
            break
    Sudoku(board).run()