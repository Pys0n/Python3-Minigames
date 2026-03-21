import random, os

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


    def pick_field(self, id: int) -> None:
        if isinstance(id, int) and 0 < id < 10 and self.board[id-1] not in ['X', 'O']:
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



def choose_field(map, symbol):
    if symbol == 'X':
        othersymbol = 'O'
    else:
        if (map[4] == 'X' and map[0] == 'O' and map[8] == 'X' and map[2] not in ['X', 'O']):
            return 3
        othersymbol = 'X'

    if map.count('X') + map.count('O') <= 1:
        if map[4] not in ['X', 'O']:
            return 5
    
    if (map.count('X') + map.count('O') <= 2 and (map[0] == othersymbol or map[2] == othersymbol or map[6] == othersymbol or map[8] == othersymbol)):
        corners = [0, 2, 6, 8]
        for corner in corners:
            if map[corner] not in ['X', 'O']:
                return corner+1

    # can win or block?
    symbols = [symbol, othersymbol]
        
    for s in symbols:
        if s == 'X':
            os = 'O'
        else:
            os = 'X'

        # search horizontal doubles
        for row in range(3):
            fields = [map[0+(row*3)], map[1+(row*3)], map[2+(row*3)]]
            if fields.count(s) == 2:
                for item in fields:
                    if item != s and item != os:
                        return map.index(item)+1

        # search vertical doubles
        for row in range(3):
            fields = [map[0+(row)], map[3+(row)], map[6+(row)]]
            if fields.count(s) == 2:
                for item in fields:
                    if item != s and item != os:
                        return map.index(item)+1
                    
        # search diagonal doubles
        fields = [[map[0], map[4], map[8]],
                [map[2], map[4], map[6]]]
        for field in fields:
            if field.count(s) == 2:
                for item in field:
                    if item != s and item != os:
                        return map.index(item)+1

    # search and build doubles
    for i in range(9):
        if map[i] in ['X', 'O']:
            continue
        board = map.copy()
        board[i] = symbol
        doubles = 0
        othersymbols = 0

        # check horizontal
        if i in [0,1,2]:
            doubles += 1 if [board[0], board[1], board[2]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[1], board[2]].count(othersymbol) != 0 else 0
        elif i in [3,4,5]:
            doubles += 1 if [board[3], board[4], board[5]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[3], board[4], board[5]].count(othersymbol) != 0 else 0
        elif i in [6,7,8]:
            doubles += 1 if [board[6], board[7], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[6], board[7], board[8]].count(othersymbol) != 0 else 0

        # check vertical
        if i in [0,3,6]:
            doubles += 1 if [board[0], board[3], board[6]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[3], board[6]].count(othersymbol) != 0 else 0
        elif i in [1,4,7]:
            doubles += 1 if [board[1], board[4], board[7]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[1], board[4], board[7]].count(othersymbol) != 0 else 0
        elif i in [2,5,8]:
            doubles += 1 if [board[2], board[5], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[2], board[5], board[8]].count(othersymbol) != 0 else 0

        # check diagonal
        if i in [0,4,8]:
            doubles += 1 if [board[0], board[4], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[4], board[8]].count(othersymbol) != 0 else 0
        if i in [2,4,6]:
            doubles += 1 if [board[2], board[4], board[6]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[2], board[4], board[6]].count(othersymbol) != 0 else 0

        if doubles >= 2 and othersymbols <= 1:
            return i+1

    # block doubles
    symbol, othersymbol = othersymbol, symbol
    if (map[0] == symbol and map[8] == symbol) or \
        (map[2] == symbol and map[6] == symbol):
        if map[1] not in ['X', 'O'] or map[5] not in ['X', 'O']:
            return random.choice([2, 6])
        elif map[3] not in ['X', 'O'] or map[7] not in ['X', 'O']:
            return random.choice([4, 8])
        elif map[4] not in ['X', 'O']:
            return 5
        
    block_positions = []
    for i in range(9):
        if map[i] in ['X', 'O']:
            continue
        board = map.copy()
        board[i] = symbol
        doubles = 0
        othersymbols = 0

        # check horizontal
        if i in [0,1,2]:
            doubles += 1 if [board[0], board[1], board[2]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[1], board[2]].count(othersymbol) != 0 else 0
        elif i in [3,4,5]:
            doubles += 1 if [board[3], board[4], board[5]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[3], board[4], board[5]].count(othersymbol) != 0 else 0
        elif i in [6,7,8]:
            doubles += 1 if [board[6], board[7], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[6], board[7], board[8]].count(othersymbol) != 0 else 0

        # check vertical
        if i in [0,3,6]:
            doubles += 1 if [board[0], board[3], board[6]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[3], board[6]].count(othersymbol) != 0 else 0
        elif i in [1,4,7]:
            doubles += 1 if [board[1], board[4], board[7]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[1], board[4], board[7]].count(othersymbol) != 0 else 0
        elif i in [2,5,8]:
            doubles += 1 if [board[2], board[5], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[2], board[5], board[8]].count(othersymbol) != 0 else 0

        # check diagonal
        if i in [0,4,8] and doubles < 2:
            doubles += 1 if [board[0], board[4], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[4], board[8]].count(othersymbol) != 0 else 0
        if i in [2,4,6] and doubles < 2:
            doubles += 1 if [board[2], board[4], board[6]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[2], board[4], board[6]].count(othersymbol) != 0 else 0

        #print(doubles, othersymbols)
        if doubles >= 2 and othersymbols == 0:
            block_positions.append(i+1)
    
    if len(block_positions) == 1:
        return block_positions[0]
    
    else:
        for i in range(9):
            if map[i] in ['X', 'O']:
                continue
            else:
                if i in [0,1,2] and [map[0], map[1], map[2]].count(symbol) == 1 and [map[0], map[1], map[2]].count(othersymbol) == 0:
                    return i+1
                elif i in [3,4,5] and [map[3], map[4], map[5]].count(symbol) == 1 and [map[3], map[4], map[5]].count(othersymbol) == 0:
                    return i+1
                elif i in [6,7,8] and [map[6], map[7], map[8]].count(symbol) == 1 and [map[6], map[7], map[8]].count(othersymbol) == 0:
                    return i+1
                elif i in [0,3,6] and [map[0], map[3], map[6]].count(symbol) == 1 and [map[0], map[3], map[6]].count(othersymbol) == 0:
                    return i+1
                elif i in [1,4,7] and [map[1], map[4], map[7]].count(symbol) == 1 and [map[1], map[4], map[7]].count(othersymbol) == 0:
                    return i+1
                elif i in [2,5,8] and [map[2], map[5], map[8]].count(symbol) == 1 and [map[2], map[5], map[8]].count(othersymbol) == 0:
                    return i+1
                elif i in [0,4,8] and [map[0], map[4], map[8]].count(symbol) == 1 and [map[0], map[4], map[8]].count(othersymbol) == 0:
                    return i+1
                elif i in [2,4,6] and [map[2], map[4], map[6]].count(symbol) == 1 and [map[2], map[5], map[8]].count(othersymbol) == 0:
                    return i+1


    symbol, othersymbol = othersymbol, symbol

    print('! ERROR !')
    # search best move
    for i in range(9):
        if map[i] in ['X', 'O']:
            continue
        board = map.copy()
        board[i] = symbol
        doubles = 0
        othersymbols = 0

        # check horizontal
        if i in [0,1,2]:
            doubles += 1 if [board[0], board[1], board[2]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[1], board[2]].count(othersymbol) == 0 else 0
        elif i in [3,4,5]:
            doubles += 1 if [board[3], board[4], board[5]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[3], board[4], board[5]].count(othersymbol) == 0 else 0
        elif i in [6,7,8]:
            doubles += 1 if [board[6], board[7], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[6], board[7], board[8]].count(othersymbol) == 0 else 0

        # check vertical
        if i in [0,3,6]:
            doubles += 1 if [board[0], board[3], board[6]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[3], board[6]].count(othersymbol) == 0 else 0
        elif i in [1,4,7]:
            doubles += 1 if [board[1], board[4], board[7]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[1], board[4], board[7]].count(othersymbol) == 0 else 0
        elif i in [2,5,8]:
            doubles += 1 if [board[2], board[5], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[2], board[5], board[8]].count(othersymbol) == 0 else 0

        # check diagonal
        if i in [0,4,8]:
            doubles += 1 if [board[0], board[4], board[8]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[0], board[4], board[8]].count(othersymbol) == 0 else 0
        if i in [2,4,6]:
            doubles += 1 if [board[2], board[4], board[6]].count(symbol) >= 2 else 0
            othersymbols += 1 if [board[2], board[4], board[6]].count(othersymbol) == 0 else 0

        if doubles >= 1 and othersymbols <= 0:
            return i+1

    if othersymbol in [map[0], map[2], map[6], map[8]] and map[4] not in ['X', 'O']:
        return 5
    corners = [0, 2, 6, 8]
    random.shuffle(corners)
    for i in corners:
        if map[i] not in ['X', 'O']:
            return i+1
    if map[4] not in ['X', 'O']:
        return 5
    
    return random.randint(1,9)


os.system(CLEAR)

ttt = TicTacToe()
ttt.draw_board()
while not ttt.has_winner():
    if ttt.turn == PLAYER:
        ttt.pick_field(int(input(ttt.turn + '\'s turn: ')))
    else:
        ttt.pick_field(choose_field(ttt.board, ttt.turn))
    os.system(CLEAR)
    ttt.draw_board()

winner = ttt.get_winner()
if winner != None:
    print('\n\n' + ttt.get_winner(), 'wins!')
else:
    print('\n\nNobody wins!')