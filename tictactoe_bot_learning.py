import os, random

PLAYER = 'O'    # Change to 'X' if you want to start

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
        print()


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


def choose_field(ttt): 
    global ALL_X, ALL_O   
    board_str = ''
    for item in ttt.board:
        if item not in 'XO': board_str += '-'
        else: board_str += item
    
    if board_str not in data:
        moves = []
        for i, item in enumerate(ttt.board):
            if item not in 'XO': moves.append(i+1)
        data[board_str] = moves.copy()

    if len(data[board_str]) != 0:
        field = random.choice(list(set(data[board_str])))
        if ttt.turn == 'X': ALL_X.append((board_str, field))
        else:               ALL_O.append((board_str, field))
        return field
    else:
        return random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9])


# Loading data
with open('ttt_bot.data', 'a', encoding='utf-8'): pass  # create file if not existing
data = {}
with open('ttt_bot.data', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        line = line.strip()
        board_str, moves = line.split('|')
        moves = moves.split(',')
        moves = [int(move) for move in moves] if moves != [''] else []
        data[board_str] = moves


if __name__ == '__main__':
    os.system(CLEAR)

    ALL_X = []
    ALL_O = []

    ttt = TicTacToe()
    ttt.draw_board()
    while not ttt.has_winner():
        if ttt.turn != PLAYER: ttt.pick_field(choose_field(ttt))
        else: ttt.pick_field(int(input(ttt.turn + '\'s turn: ')))
        os.system(CLEAR)
        ttt.draw_board()


    winner = ttt.get_winner()
    if winner != None:
        print('\n\n' + winner, 'wins!')

        # Update learned data
        if winner == 'X':
            if PLAYER == 'O':
                for move in ALL_X:
                    if len(data[move[0]]) >= 1:
                        data[move[0]].append(move[1])
                data[ALL_X[-1][0]] = [ALL_X[-1][1]]
            else:
                data[ALL_O[-1][0]].remove(ALL_O[-1][1])
                for move in ALL_O:
                    while data[move[0]].count(move[1]) > 1:
                        data[move[0]].remove(move[1])
        else:
            if PLAYER == 'X':
                for move in ALL_O:
                    if len(data[move[0]]) >= 1:
                        data[move[0]].append(move[1])
                data[ALL_O[-1][0]] = [ALL_O[-1][1]]
            else:
                data[ALL_X[-1][0]].remove(ALL_X[-1][1])
                for move in ALL_X:
                    while data[move[0]].count(move[1]) > 1:
                        data[move[0]].remove(move[1])
    else:
        print('\n\nNobody wins!')

        # Update learned data
        for move in ALL_X + ALL_O:
            while data[move[0]].count(move[1]) >= 2: data[move[0]].remove(move[1])
            while data[move[0]].count(move[1]) >= 2: data[move[0]].remove(move[1])

    for board_str in data:
        if len(data[board_str]) > 0 and data[board_str].count(max(data[board_str], key=data[board_str].count)) >= 25:
            data[board_str] = [max(data[board_str], key=data[board_str].count)]


with open('ttt_bot.data', 'w', encoding='utf-8') as file:
    for board_str in data:
        if len(data[board_str]) > 0 and data[board_str].count(max(data[board_str], key=data[board_str].count)) >= 25:
            data[board_str] = [max(data[board_str], key=data[board_str].count)]
        
        file.write(board_str + '|' + ','.join([str(x) for x in data[board_str]]) + '\n')
