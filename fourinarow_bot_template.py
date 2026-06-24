import os

CLEAR = 'cls' if os.name == 'nt' else 'clear'

RED = '\x1b[41m \x1b[49m'
BLUE = '\x1b[44m \x1b[49m'

class FourInARow:
    def __init__(self) -> None:
        self.board = [['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.'],
                      ['.','.','.','.','.','.','.']]
        self.turn = 'X'

    
    def swap_turn(self) -> None:
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'


    def draw_board(self) -> None:
        print('1 2 3 4 5 6 7')
        for i in range(len(self.board)):
            print((' '.join(self.board[i])).replace('X', RED).replace('O', BLUE))

    
    def select_row(self, row: int) -> None:
        row = row - 1
        if self.board[0][row] != '.':
            return
        
        for i in range(5):
            if self.board[i][row] == '.' and self.board[i+1][row] != '.':
                self.board[i][row] = self.turn
                self.swap_turn()
                return
        self.board[5][row] = self.turn
        self.swap_turn()
        return


    
    def has_winner(self) -> None:
        for row in range(3):        # |
            for col in range(7):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] != '.':
                    return True
        
        for row in range(6):        # -
            for col in range(4):
                if self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3] != '.':
                    return True
        
        for row in range(3):        # \
            for col in range(4):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] != '.':
                    return True
        
        for row in range(3):        # /
            for col in range(4,7):
                if self.board[row][col] == self.board[row+1][col-1] == self.board[row+2][col-2] == self.board[row+3][col-3] != '.':
                    return True
                
        is_remis = True             # remis
        for row in self.board:
            if '.' in row:
                is_remis = False
                break
        
        if is_remis: return True

        return False


    def get_winner(self) -> None:
        for row in range(3):        # |
            for col in range(7):
                if self.board[row][col] == self.board[row+1][col] == self.board[row+2][col] == self.board[row+3][col] != '.':
                    return self.board[row][col]
        
        for row in range(6):        # -
            for col in range(4):
                if self.board[row][col] == self.board[row][col+1] == self.board[row][col+2] == self.board[row][col+3] != '.':
                    return self.board[row][col]
        
        for row in range(3):        # \
            for col in range(4):
                if self.board[row][col] == self.board[row+1][col+1] == self.board[row+2][col+2] == self.board[row+3][col+3] != '.':
                    return self.board[row][col]
        
        for row in range(3):        # /
            for col in range(4,7):
                if self.board[row][col] == self.board[row+1][col-1] == self.board[row+2][col-2] == self.board[row+3][col-3] != '.':
                    return self.board[row][col]
                
        return None


from random import randint

def choose_row(fiar):
    # This is where your code goes
    # What you can use:
    # fiar.board: the Four In A Row Board as a list of 7 lists of each 7 items; Attention: to check if a field is empty, use `fiar.board[i] != '.'`
    # fiar.turn: the symbol of the current player ('X' or 'O')

    # You are not allowed to:
    # ... change any variables in fiar
    # ... use the functions: swap_turn, select_row

    return randint(1, 7)


os.system(CLEAR)

fiar = FourInARow()
fiar.draw_board()
while not fiar.has_winner():
    #row = input('Select Row: ')        # Use this line to play player vs player
    row = choose_row(fiar)              # Use this line to let your bot play against itself
    
    fiar.select_row(row)
    
    os.system(CLEAR)
    fiar.draw_board()


winner = fiar.get_winner()
if winner != None:
    print('\n\n' + winner.replace('X', RED).replace('O', BLUE) + ' wins!')
else:
    print('\n\nNobody wins!')