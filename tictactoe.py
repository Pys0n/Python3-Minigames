import os

CLEAR = 'cls' if os.name == 'nt' else 'clear'

class TicTacToe:
    def __init__(self) -> None:
        self.board = [f'\033[90m{str(x)}\033[0m' for x in range(1,10)]
        self.turn = 'X'
        
    
    def draw_board(self) -> None:
        print('', self.board[0], '|', self.board[1], '|', self.board[2])
        print('---+---+---')
        print('', self.board[3], '|', self.board[4], '|', self.board[5])
        print('---+---+---')
        print('', self.board[6], '|', self.board[7], '|', self.board[8])


    def pick_field(self, id: int) -> None:
        if isinstance(id, int) and 0 < id < 10 and self.board[id-1] not in 'XO':
            self.board[id-1] = self.turn
            self.swap_turn()

    def swap_turn(self) -> None:
        if self.turn == 'X':
            self.turn = 'O'
        elif self.turn == 'O':
            self.turn = 'X'
    
    def has_winner(self):
        if self.board[0] == self.board[1] == self.board[2] or \
           self.board[3] == self.board[4] == self.board[5] or \
           self.board[6] == self.board[7] == self.board[8]:
            return True
        
        elif self.board[0] == self.board[3] == self.board[6] or \
           self.board[1] == self.board[4] == self.board[7] or \
           self.board[2] == self.board[5] == self.board[8]:
            return True
        
        elif self.board[0] == self.board[4] == self.board[8] or \
           self.board[6] == self.board[4] == self.board[2]:
            return True
        
        for field in self.board:
            if not 'X' in field and not 'O' in field:
                return False
    
        return True

    def get_winner(self):
        if self.board[0] == self.board[1] == self.board[2]:
            return self.board[0]
        elif self.board[3] == self.board[4] == self.board[5]:
            return self.board[3]
        elif self.board[6] == self.board[7] == self.board[8]:
            return self.board[6]
        
        elif self.board[0] == self.board[3] == self.board[6]:
            return self.board[0]
        elif self.board[1] == self.board[4] == self.board[7]:
            return self.board[1]
        elif self.board[2] == self.board[5] == self.board[8]:
            return self.board[2]
        
        elif self.board[0] == self.board[4] == self.board[8]:
            return self.board[0]
        elif self.board[6] == self.board[4] == self.board[2]:
            return self.board[6]

os.system(CLEAR)

ttt = TicTacToe()
ttt.draw_board()
while not ttt.has_winner():
    ttt.pick_field(int(input(ttt.turn + '\'s turn: ')))
    os.system(CLEAR)
    ttt.draw_board()


winner = ttt.get_winner()
if winner != None:
    print('\n\n' + ttt.get_winner(), 'wins!')
else:
    print('\n\nNobody wins!')