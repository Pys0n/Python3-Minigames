import os, random

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
    moves_count = 0
    for line in file.readlines():
        line = line.strip()
        board_str, moves = line.split('|')
        moves = moves.split(',')
        moves = [int(move) for move in moves] if moves != [''] else []
        moves_count += len(moves)
        data[board_str] = moves


runs = input('Number of thousand games to learn: ')
RUNS = int(runs)*1000 if runs.strip() != '' else 1000
X,  O,  D  = 0, 0, 0
X1, O1, D1 = 0, 0, 0
RANDOM = 'X'
for _ in range(RUNS):
    os.system(CLEAR)
    print(_+1, '/', RUNS)
    if RUNS//2 == _+1: RANDOM, X1, O1, D1, X, O, D = 'O', X, O, D, 0, 0, 0

    ALL_X = []
    ALL_O = []

    ttt = TicTacToe()
    while not ttt.has_winner():
        if ttt.turn != RANDOM: ttt.pick_field(choose_field(ttt))
        else: ttt.pick_field(random.randint(1,9))


    winner = ttt.get_winner()
    if winner != None:
        if winner == 'X':
            if RANDOM == 'O':
                for move in ALL_X:
                    if len(set(data[move[0]])) >= 1:
                        data[move[0]].append(move[1])
                data[ALL_X[-1][0]] = [ALL_X[-1][1]]
            else:
                data[ALL_O[-1][0]].remove(ALL_O[-1][1])
                for move in ALL_O:
                    while data[move[0]].count(move[1]) > 1:
                        data[move[0]].remove(move[1])

            X += 1
        else:
            if RANDOM == 'X':
                for move in ALL_O:
                    if len(set(data[move[0]])) >= 1:
                        data[move[0]].append(move[1])
                data[ALL_O[-1][0]] = [ALL_O[-1][1]]
            else:
                data[ALL_X[-1][0]].remove(ALL_X[-1][1])
                for move in ALL_X:
                    while data[move[0]].count(move[1]) > 1:
                        data[move[0]].remove(move[1])

            O += 1
    else:
        for move in ALL_X + ALL_O:
            while data[move[0]].count(move[1]) >= 2: data[move[0]].remove(move[1])
            while data[move[0]].count(move[1]) >= 2: data[move[0]].remove(move[1])
        D += 1
        pass

    for board_str in data:
        if len(data[board_str]) > 0 and data[board_str].count(max(data[board_str], key=data[board_str].count)) >= 25:
            data[board_str] = [max(data[board_str], key=data[board_str].count)]


with open('ttt_bot.data', 'w', encoding='utf-8') as file:
    moves_count_new = 0
    for board_str in data:
        if len(data[board_str]) > 0 and data[board_str].count(max(data[board_str], key=data[board_str].count)) >= 25:
            data[board_str] = [max(data[board_str], key=data[board_str].count)]
        if len(data[board_str]) > 1 and len(set(data[board_str])) == 1:
            data[board_str] = [data[board_str][0]]
        
        file.write(board_str + '|' + ','.join([str(x) for x in data[board_str]]) + '\n')
        moves_count_new += len(data[board_str])

print('\n', moves_count, '>', moves_count_new)

print('\nBot as O:')
print(f'Won : {O1} ({round(O1/(RUNS//2)*100, 1)}%)')
print(f'Lost: {X1} ({round(X1/(RUNS//2)*100, 1)}%)')
print(f'Draw: {D1} ({round(D1/(RUNS//2)*100, 1)}%)')

print('\nBot as X:')
print(f'Won : {X} ({round(X/(RUNS//2)*100, 1)}%)')
print(f'Lost: {O} ({round(O/(RUNS//2)*100, 1)}%)')
print(f'Draw: {D} ({round(D/(RUNS//2)*100, 1)}%)')