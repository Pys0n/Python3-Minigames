from copy import deepcopy
import os

CLEAR = 'cls' if os.name == 'nt' else 'clear'

class Chess:
    def __init__(self) -> None:
        self.data = {
            'board': [
                ['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                ['bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP'],
                ['', '', '', 'bR', '', 'bR', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['', '', '', '', '', '', '', ''],
                ['bR', '', '', '', '', '', '', ''],
                ['', '', '', '', 'wK', '', '', ''],
            ],
            'turn': 'w',
            'fifty_moves_rule_count': 0,
            'castling': {
                'w': [True, True, True],    # White: Rook (a1); King, Rook (h1)     -> if True: piece hasn't moved
                'b': [True, True, True],    # Black: Rook (a8); King, Rook (h8)     -> if True: piece hasn't moved
            },
            'en_passent_pos': '',           # '' = en passent not possible
            'boards': {},
        }


    def convert_integers_to_field(self, x: int, y: int) -> str:
        return chr(x+97) + str(8-y)


    def convert_field_to_integers(self, field: str) -> tuple[int, int]:
        return ('abcdefgh'.index(field[0]), 8-int(field[1]))

    
    def get_all_moves(self, turn: str = None, *, check_depth: bool = True) -> dict:
        if turn == None: turn = self.data['turn']

        all_moves = {}

        for y, line in enumerate(self.data['board']):
            for x, field in enumerate(line):
                if field == '' or field[0] != turn: continue
                
                piece = field[1]
                field_str = self.convert_integers_to_field(x, y)
                all_moves[field_str] = []


                if piece == 'B':    # Bishop
                    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
                    
                    for direction in directions:
                        x_offset, y_offset = direction
                        while 0 <= x+x_offset <= 7 and 0 <= y+y_offset <= 7:
                            if self.data['board'][y+y_offset][x+x_offset] == '':
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+x_offset, y+y_offset), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+x_offset, y+y_offset))
                            elif self.data['board'][y+y_offset][x+x_offset][0] != turn:
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+x_offset, y+y_offset), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+x_offset, y+y_offset))
                                break
                            else:
                                break

                            x_offset += direction[0]
                            y_offset += direction[1]

                elif piece == 'K':  # King
                    # move 1 field in any direction
                    for x_offset in [-1, 0, 1]:
                        for y_offset in [-1, 0, 1]:
                            if x_offset == y_offset == 0: continue
                            if  0 <= x+x_offset <= 7 and 0 <= y+y_offset <= 7 and (self.data['board'][y+y_offset][x+x_offset] == '' or self.data['board'][y+y_offset][x+x_offset][0] != turn):
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+x_offset, y+y_offset), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+x_offset, y+y_offset))
                    
                    # castle
                    if self.data['castling'][turn][1] and self.data['castling'][turn][0]:
                        # queenside castle (O-O-O)
                        if check_depth:
                            through_check = False
                            enemy_moves = self.get_all_moves('w' if turn != 'w' else 'b', check_depth=False)
                            for moves in enemy_moves.values():
                                if self.convert_integers_to_field(x-1, y) in moves or \
                                   self.convert_integers_to_field(x-2, y) in moves or \
                                   self.convert_integers_to_field(x-3, y) in moves:
                                    through_check = True
                                    break

                            if not through_check and self.data['board'][y][x-1] == self.data['board'][y][x-2] == self.data['board'][y][x-3] == '':
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x-2, y), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x-2, y))
                        else:
                            if self.data['board'][y][x-1] == self.data['board'][y][x-2] == self.data['board'][y][x-3] == '':
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x-2, y), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x-2, y))

                    if self.data['castling'][turn][1] and self.data['castling'][turn][2]:
                        # kingside castle (O-O)
                        if check_depth:
                            through_check = False
                            enemy_moves = self.get_all_moves('w' if turn != 'w' else 'b', check_depth=False)
                            for moves in enemy_moves.values():
                                if self.convert_integers_to_field(x+1, y) in moves or \
                                   self.convert_integers_to_field(x+2, y) in moves:
                                    through_check = True
                                    break

                            if not through_check and self.data['board'][y][x+1] == self.data['board'][y][x+2] == '':
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+2, y), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+2, y))
                        else:
                            if self.data['board'][y][x+1] == self.data['board'][y][x+2] == '':
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+2, y), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+2, y))

                elif piece == 'N':  # Knight
                    if x-1 >= 0 and y-2 >= 0 and (self.data['board'][y-2][x-1] == '' or self.data['board'][y-2][x-1][0] != turn):
                        # move 2 fields up and 1 field to the right
                        if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x-1, y-2), turn):
                            all_moves[field_str].append(self.convert_integers_to_field(x-1, y-2))
                    if x+1 <= 7 and y-2 >= 0 and (self.data['board'][y-2][x+1] == '' or self.data['board'][y-2][x+1][0] != turn):
                        # move 2 fields up and 1 field to the left
                        if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+1, y-2), turn):
                            all_moves[field_str].append(self.convert_integers_to_field(x+1, y-2))
                    if x-1 >= 0 and y+2 <= 7 and (self.data['board'][y+2][x-1] == '' or self.data['board'][y+2][x-1][0] != turn):
                        # move 2 fields down and 1 field to the right
                        if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x-1, y+2), turn):
                            all_moves[field_str].append(self.convert_integers_to_field(x-1, y+2))
                    if x+1 <= 7 and y+2 <= 7 and (self.data['board'][y+2][x+1] == '' or self.data['board'][y+2][x+1][0] != turn):
                        # move 2 fields down and 1 field to the left
                        if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+1, y+2), turn):
                            all_moves[field_str].append(self.convert_integers_to_field(x+1, y+2))
                    if x-2 >= 0 and y-1 >= 0 and (self.data['board'][y-1][x-2] == '' or self.data['board'][y-1][x-2][0] != turn):
                        # move 2 fields left and 1 field up
                        if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x-2, y-1), turn):
                            all_moves[field_str].append(self.convert_integers_to_field(x-2, y-1))
                    if x-2 >= 0 and y+1 <= 7 and (self.data['board'][y+1][x-2] == '' or self.data['board'][y+1][x-2][0] != turn):
                        # move 2 fields left and 1 field down
                        if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x-2, y+1), turn):
                            all_moves[field_str].append(self.convert_integers_to_field(x-2, y+1))
                    if x+2 <= 7 and y-1 >= 0 and (self.data['board'][y-1][x+2] == '' or self.data['board'][y-1][x+2][0] != turn):
                        # move 2 fields right and 1 field up
                        if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+2, y-1), turn):
                            all_moves[field_str].append(self.convert_integers_to_field(x+2, y-1))
                    if x+2 <= 7 and y+1 <= 7 and (self.data['board'][y+1][x+2] == '' or self.data['board'][y+1][x+2][0] != turn):
                        # move 2 fields right and 1 field down
                        if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+2, y+1), turn):
                            all_moves[field_str].append(self.convert_integers_to_field(x+2, y+1))

                elif piece == 'P':  # Pawn
                    if turn == 'w':
                        if y == 6 and self.data['board'][y-1][x] == '' and self.data['board'][y-2][x] == '':
                            # move 2 fields forward; only when on 2nd rank and both fields in front are empty
                            if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x, y-2), turn):
                                all_moves[field_str].append(self.convert_integers_to_field(x, y-2))
                        if self.data['board'][y-1][x] == '':
                            # move 1 field forward; only if field is empty
                            if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x, y-1), turn):
                                all_moves[field_str].append(self.convert_integers_to_field(x, y-1))
                        if (x-1 >= 0 and self.data['board'][y-1][x-1] != '' and self.data['board'][y-1][x-1][0] != turn) or self.convert_integers_to_field(x-1, y-1) == self.data['en_passent_pos']:
                            # move 1 field diagonal (left); only if enemy piece is on this field or en passent is possible
                            if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x-1, y-1), turn):
                                all_moves[field_str].append(self.convert_integers_to_field(x-1, y-1))
                        if (x+1 <= 7 and self.data['board'][y-1][x+1] != '' and self.data['board'][y-1][x+1][0] != turn) or self.convert_integers_to_field(x+1, y-1) == self.data['en_passent_pos']:
                            # move 1 field diagonal (right); only if enemy piece is on this field or en passent is possible
                            if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+1, y-1), turn):
                                all_moves[field_str].append(self.convert_integers_to_field(x+1, y-1))
                    else:
                        if y == 1 and self.data['board'][y+1][x] == '' and self.data['board'][y+2][x] == '':
                            # move 2 fields forward; only when on 7th rank and both fields in front are empty
                            if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x, y+2), turn):
                                all_moves[field_str].append(self.convert_integers_to_field(x, y+2))
                        if self.data['board'][y+1][x] == '':
                            # move 1 field forward; only if field is empty
                            if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x, y+1), turn):
                                all_moves[field_str].append(self.convert_integers_to_field(x, y+1))
                        if (x-1 >= 0 and self.data['board'][y+1][x-1] != '' and self.data['board'][y+1][x-1][0] != turn) or self.convert_integers_to_field(x-1, y+1) == self.data['en_passent_pos']:
                            # move 1 field diagonal (left); only if enemy piece is on this field
                            if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x-1, y+1), turn):
                                all_moves[field_str].append(self.convert_integers_to_field(x-1, y+1))
                        if (x+1 <= 7 and self.data['board'][y+1][x+1] != '' and self.data['board'][y+1][x+1][0] != turn) or self.convert_integers_to_field(x+1, y+1) == self.data['en_passent_pos']:
                            # move 1 field diagonal (right); only if enemy piece is on this field
                            if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+1, y+1), turn):
                                all_moves[field_str].append(self.convert_integers_to_field(x+1, y+1))

                elif piece == 'Q':  # Queen
                    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (1, 0), (-1, 0), (0, 1), (0, -1)]
                    
                    for direction in directions:
                        x_offset, y_offset = direction
                        while 0 <= x+x_offset <= 7 and 0 <= y+y_offset <= 7:
                            if self.data['board'][y+y_offset][x+x_offset] == '':
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+x_offset, y+y_offset), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+x_offset, y+y_offset))
                            elif self.data['board'][y+y_offset][x+x_offset][0] != turn:
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+x_offset, y+y_offset), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+x_offset, y+y_offset))
                                break
                            else:
                                break

                            x_offset += direction[0]
                            y_offset += direction[1]

                elif piece == 'R':  # Rook
                    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
                    
                    for direction in directions:
                        x_offset, y_offset = direction
                        while 0 <= x+x_offset <= 7 and 0 <= y+y_offset <= 7:
                            if self.data['board'][y+y_offset][x+x_offset] == '':
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+x_offset, y+y_offset), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+x_offset, y+y_offset))
                            elif self.data['board'][y+y_offset][x+x_offset][0] != turn:
                                if not check_depth or not self.is_illegal_because_check(field_str, self.convert_integers_to_field(x+x_offset, y+y_offset), turn):
                                    all_moves[field_str].append(self.convert_integers_to_field(x+x_offset, y+y_offset))
                                break
                            else:
                                break

                            x_offset += direction[0]
                            y_offset += direction[1]

        return all_moves


    def is_illegal_because_check(self, position: str, destination: str, turn: str = None) -> str:
        if turn == None:
            turn = self.data['turn']

        org_data = deepcopy(self.data)

        self.move(position, destination, check_depth=False)

        enemy_moves = self.get_all_moves('w' if turn == 'b' else 'b', check_depth=False)

        for y, row in enumerate(self.data['board']):
            if turn+'K' in row:
                king = (y, row.index(turn+'K'))
        
        for moves in enemy_moves.values():
            if self.convert_integers_to_field(king[1], king[0]) in moves:
                self.data = deepcopy(org_data)
                return True
                
        self.data = deepcopy(org_data)
        return False


    def is_checkmate(self) -> tuple[bool, str]:
        white_moves = self.get_all_moves('w')
        black_moves = self.get_all_moves('b')

        for y, row in enumerate(self.data['board']):
            if 'bK' in row:
                black_king = (y, row.index('bK'))
            if 'wK' in row:
                white_king = (y, row.index('wK'))
        
        black_moves_count = 0
        for moves in black_moves.values():
            black_moves_count += len(moves)

        white_moves_count = 0
        for moves in white_moves.values():
            white_moves_count += len(moves)

        if black_moves_count == 0:
            for moves in white_moves.values():
                if self.convert_integers_to_field(black_king[1], black_king[0]) in moves:
                    return True, 'White'
        if white_moves_count == 0:
            for moves in black_moves.values():
                if self.convert_integers_to_field(white_king[1], white_king[0]) in moves:
                    return True, 'Black'
                
        return False, ''
    

    def is_draw(self) -> tuple[bool, str]:
        # stalemate
        all_moves = self.get_all_moves()
        len_moves = 0
        for moves in all_moves.values():
            len_moves += len(moves)

        if len_moves == 0: 
            return True, 'stalemate'

        # fifty-move rule
        if self.data['fifty_moves_rule_count'] >= 50:
            return True, '50-move rule'

        # insufficient mating material
        pieces = []
        c_pieces = {}
        for y, line in enumerate(self.data['board']):
            for x, field in enumerate(line):
                if field == '': continue
                pieces.append(field[1])
                c_pieces[field] = [x, y]
        pieces.sort()
        c_pieces.cort()

        if pieces in (['K', 'K'], ['B', 'K', 'K'], ['K', 'K', 'N']):
            return True, 'insufficient mating material'
        if pieces == ['B', 'B', 'K', 'K'] and 'wB' in c_pieces and 'bB' in c_pieces and sum(c_pieces['wB'])%2 == sum(c_pieces['bB'])%2:
            return True, 'insufficient mating material'
        
        # threefold repetition
        if max(self.data['boards'].values()) >= 3:
            return True, 'threefold repetition'

        return False, ''


    def move(self, position: str, destination: str, promoto_to: str = 'Q', *, check_depth: bool = True):
        position, destination = position.lower(), destination.lower()
        promoto_to = promoto_to.upper()

        all_moves = self.get_all_moves(self.data['turn'], check_depth=check_depth)
        if position not in all_moves: return
        if destination not in all_moves[position]: return
        if promoto_to not in 'BNQR': promoto_to = 'Q'

        x_position, y_position = self.convert_field_to_integers(position)
        x_destination, y_destination = self.convert_field_to_integers(destination)

        # update castling status
        if self.data['board'][y_position][x_position][1] == 'R':
            if self.data['turn'] == 'w':
                if (x_position, y_position) == (0, 7): self.data['castling']['w'][0] = False
                elif (x_position, y_position) == (7, 7): self.data['castling']['w'][2] = False
            else:
                if (x_position, y_position) == (0, 0): self.data['castling']['b'][0] = False
                elif (x_position, y_position) == (7, 0): self.data['castling']['b'][2] = False
        elif self.data['board'][y_position][x_position][1] == 'K':
            self.data['castling'][self.data['turn']][1] = False

        if self.data['board'][y_position][x_position][1] == 'P' and destination[1] in '18':
            # pawn promotion
            self.data['board'][y_destination][x_destination] = self.data['turn'] + promoto_to

            # update fifty moves rule
            self.data['fifty_moves_rule_count'] = 0
        elif self.data['board'][y_position][x_position][1] == 'P' and destination == self.data['en_passent_pos']:
            # do en passent
            self.data['board'][y_destination][x_destination] = self.data['board'][y_position][x_position]
            self.data['board'][y_position][x_position] = ''

            self.data['board'][y_position][x_destination] = ''
        elif self.data['board'][y_position][x_position] == self.data['turn']+'K' and self.data['board'][y_position][7] == self.data['turn']+'R' and x_position+2 == x_destination:
            # kingside castle
            self.data['castling'][self.data['turn']][1] = False

            self.data['board'][y_destination][x_destination] = self.data['board'][y_position][x_position]   # move king
            self.data['board'][y_destination][x_destination-1] = self.data['board'][y_position][7]          # move rook
            self.data['board'][y_position][x_position] = ''                                         # clear kings original position
            self.data['board'][y_position][7] = ''                                                  # clear rooks original position
        elif self.data['board'][y_position][x_position] == self.data['turn']+'K' and self.data['board'][y_position][0] == self.data['turn']+'R' and x_position-2 == x_destination:
            # queenside castle
            self.data['castling'][self.data['turn']][1] = False

            self.data['board'][y_destination][x_destination] = self.data['board'][y_position][x_position]   # move king
            self.data['board'][y_destination][x_destination+1] = self.data['board'][y_position][0]          # move rook
            self.data['board'][y_position][x_position] = ''                                         # clear kings original position
            self.data['board'][y_position][0] = ''                                                  # clear rooks original position
        else:
            # normal move
            self.data['board'][y_destination][x_destination] = self.data['board'][y_position][x_position]

            # update fifty moves rule
            if self.data['board'][y_destination][x_destination] == '':
                self.data['fifty_moves_rule_count'] += 1
            else:
                self.data['fifty_moves_rule_count'] = 0
        self.data['board'][y_position][x_position] = ''


        # en passent reset
        self.data['en_passent_pos'] = ''

        # pawn moves 2 fields -> en passent possible
        if self.data['board'][y_destination][x_destination] != '' and self.data['board'][y_destination][x_destination][1] == 'P' and y_position+2 == y_destination:
            self.data['en_passent_pos'] = self.convert_integers_to_field(x_position, y_position+1)
        elif self.data['board'][y_destination][x_destination] != '' and self.data['board'][y_destination][x_destination][1] == 'P' and y_position-2 == y_destination:
            self.data['en_passent_pos'] = self.convert_integers_to_field(x_position, y_position-1)

        # add board to played boards (threefold repetition)
        board_str = str(self.data['board'])
        if board_str in self.data['boards']:
            self.data['boards'][board_str] += 1
        else:
            self.data['boards'][board_str] = 0

        # Change turn
        if self.data['turn'] == 'w':
            self.data['turn'] = 'b'
        else:
            self.data['turn'] = 'w'


chess = Chess()
while not chess.is_checkmate()[0] and not chess.is_draw()[0]:
    os.system(CLEAR)
    print(chess.get_all_moves())

    for y, line in enumerate(chess.data['board']):
        for x, item in enumerate(line):
            print(f'{item:2}{'|' if x != 7 else '\n'}', end='')
        if y != 7: print('——+——+——+——+——+——+——+——')
    print()

    print('\n' + ('White' if chess.data['turn'] == 'w' else 'Black') + ' to move!')
    pos = input('From: ')
    des = input('To  : ')

    chess.move(pos, des)

if chess.is_checkmate()[0]:
    print(chess.is_checkmate()[1] + ' wins!')
else:
    print('Draw because of ' + chess.is_draw()[1] + '!')