import os, random

CLEAR = 'cls' if os.name == 'nt' else 'clear'

class Game2048:
    def __init__(self):
        self.board = [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
        ]

        self.board[random.choice([1, 3])][random.randint(0, 3)] = random.choice([2, 4])
        self.board[random.choice([0, 2])][random.randint(0, 3)] = random.choice([2, 4])
    

    def draw_board(self):
        for line in self.board:
            for item in line:
                print(f'|{(item if item != 0 else ''):4}', end='')
            print('|')


    def move(self, direction: str):
        board_before = str(self.board)

        if direction.strip().lower() == 'w':
            for x in range(4):
                for y in range(1, 4):
                    while y > 0:
                        if self.board[y-1][x] == self.board[y][x] != 0:
                            self.board[y][x] = 0
                            self.board[y-1][x] *= 2
                            break
                        elif self.board[y-1][x] == 0:
                            self.board[y-1][x] = self.board[y][x]
                            self.board[y][x] = 0
                            y -= 1
                        else:
                            break
        elif direction.strip().lower() == 'a':
            for y in range(4):
                for x in range(1, 4):
                    while x > 0:
                        if self.board[y][x-1] == self.board[y][x] != 0:
                            self.board[y][x] = 0
                            self.board[y][x-1] *= 2
                            break
                        elif self.board[y][x-1] == 0:
                            self.board[y][x-1] = self.board[y][x]
                            self.board[y][x] = 0
                            x -= 1
                        else:
                            break
        elif direction.strip().lower() == 's':
            for x in range(4):
                for y in range(2, -1, -1):
                    while y < 3:
                        if self.board[y+1][x] == self.board[y][x] != 0:
                            self.board[y][x] = 0
                            self.board[y+1][x] *= 2
                            break
                        elif self.board[y+1][x] == 0:
                            self.board[y+1][x] = self.board[y][x]
                            self.board[y][x] = 0
                            y += 1
                        else:
                            break
        elif direction.strip().lower() == 'd':
            for y in range(4):
                for x in range(2, -1, -1):
                    while x < 3:
                        if self.board[y][x+1] == self.board[y][x] != 0:
                            self.board[y][x] = 0
                            self.board[y][x+1] *= 2
                            break
                        elif self.board[y][x+1] == 0:
                            self.board[y][x+1] = self.board[y][x]
                            self.board[y][x] = 0
                            x += 1
                        else:
                            break
        else:
            return

        empty = []
        for y in range(4):
            for x in range(4):
                if self.board[y][x] == 0:
                    empty.append([y, x])
        
        if len(empty) == 0:
            return
        
        if str(self.board) != board_before:
            pos = random.choice(empty)
            self.board[pos[0]][pos[1]] = 2

    
    def is_game_over(self):
        for line in self.board:
            if 2048 in line:
                return True, 'You Won!'
        for y, line in enumerate(self.board):
            for x, item in enumerate(line):
                if item == 0 or \
                    (y > 0 and self.board[y-1][x] == item) or \
                    (y < 3 and self.board[y+1][x] == item) or \
                    (x > 0 and self.board[y][x-1] == item) or \
                    (x < 3 and self.board[y][x+1] == item):
                    return False, ''
                
        
        return True, 'You Lost!'



def choose_move(g2048):
    # This is where your code goes
    # What you can use:
    # g2048.board: the 2048 Board as a list of 4 lists of each 4 items; Attention: to check if a field is empty, use `g2048.board[y][x] != 0`

    # You are not allowed to:
    # ... change any variables in g2048
    # ... use the functions: move

    return random.choice(['w', 'a', 's', 'd'])


g2048 = Game2048()
while not g2048.is_game_over()[0]:
    os.system(CLEAR)
    g2048.draw_board()
    g2048.move(input('Choose (w/a/s/d): '))

os.system(CLEAR)
g2048.draw_board()
print(g2048.is_game_over()[1])