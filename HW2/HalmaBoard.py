class HalmaBoard:
    def __init__(self):
        self.mode = None        # string SINGLE or GAME
        self.player = None      # string BLACK or WHITE
        self.time = None        # floating point number indicating remaining time
        self.white_pieces = set()  # white chess pieces
        self.black_pieces = set()  # black chess pieces
        self.layout = []        # board layout

    # read from an input file to a HalmaBoard
    def read_input(self,file_name):
        self.mode = None        # string SINGLE or GAME
        self.player = None      # string BLACK or WHITE
        self.time = None        # floating point number indicating remaining time
        self.white_pieces = set()  # white chess pieces
        self.black_pieces = set()  # black chess pieces
        self.layout = []        # board layout
        with open(file_name) as f:
            for line_count, line in enumerate(f):
                if line_count == 0:
                    self.mode = line.strip()
                elif line_count == 1:
                    self.player = line.strip()
                elif line_count == 2:
                    self.time = float(line.strip())
                else:
                    line = line.strip()
                    row = line_count - 3
                    to_be_added = []
                    for col, entry in enumerate(line):
                        to_be_added.append(entry)
                        if entry == 'W':
                            self.white_pieces.add((row, col))
                        elif entry == 'B':
                            self.black_pieces.add((row, col))
                    self.layout.append(to_be_added)

    # update board layout according to chess pieces
    def update_layout(self):
        self.layout = [['.' for col in range(16)] for row in range(16)]
        for row, col in self.white_pieces:
            self.layout[row][col] = 'W'
        for row, col in self.black_pieces:
            self.layout[row][col] = 'B'

    # write a HalmaBoard to an input file
    def write_input(self, file_name):
        with open(file_name, 'w') as f:
            if self.mode == None or self.player == None or self.time == None:
                print('ERROR: HalmaBoard is not complete, mode/player/time is NoneType!!!')
                return
            f.write(self.mode + '\n')
            f.write(self.player + '\n')
            f.write(str(self.time) + '\n')
            self.update_layout()
            for line, row in enumerate(self.layout):
                f.write(''.join(row))
                if line < len(self.layout) - 1:
                    f.write('\n')

    def switch_player(self):
        if self.player == 'BLACK':
            self.player = 'WHITE'
        else:
            self.player = 'BLACK'

    # check to see whether an output move is valid
    def is_valid_move(self, moves):
        if self.player == None or self.mode == None or self.time == None:
            print('Error: not a valid board: player/mode/time is of NoneType')
            return False

        # get the first move
        move = moves
        # if chess is not there
        if self.player == 'BLACK':
            if move[0] not in self.black_pieces:
                print('Not a valid move: start position is invalid for black: {}'.format(move[0]))
                return False
        if self.player == 'WHITE':
            if move[0] not in self.white_pieces:
                print('Not a valid move: start position is invalid for white: {}'.format(move[0]))
                return False
        # if didn't move
        if move[0] == move[1]:
            print('Not a valid move: not moved')
            return False
        # if jumped a space
        if abs(move[0][0] - move[1][0]) > 1 or abs(move[0][1] - move[1][1]) > 1:
            print('Not a valid move: jumped from {} to {}'.format(move[0],move[1]))
            return False
        if self.layout[move[1][0]][move[1][1]] != '.':
            print('Not a valid move: ended on an occupied space')
            return False
        return True

    # check to see whether an output jump is valid
    def is_valid_jump(self, jumps):
        if self.player == None or self.mode == None or self.time == None:
            print('Error: not a valid board: player/mode/time is of NoneType')
            return False

        if self.player == 'BLACK':
            if jumps[0][0] not in self.black_pieces:
                print('Not a valid jump: start position is invalid for black: {}'.format(jumps[0][0]))
                return False
        if self.player == 'WHITE':
            if jumps[0][0] not in self.white_pieces:
                print('Not a valid jump: start position is invalid for white: {}'.format(jumps[0][0]))
                return False

        layout = [[entry for entry in row] for row in self.layout]
        black_pieces = set([i for i in self.black_pieces])
        white_pieces = set([i for i in self.white_pieces])
        for count, jump in enumerate(jumps):
            if count != 0:
                if jump[0] != jumps[count-1][1]:
                    print('Not a valid jump: start position does not match last end position: {}'.format(jump[0], jumps[count-1][1]))
                    return False
            # if didn't move
            if jump[0] == jump[1]:
                print('Not a valid move: not jumped')
                return False
            # if jumped a space
            if abs(jump[0][0] - jump[1][0]) not in [0,2] or abs(jump[0][1] - jump[1][1]) not in [0,2]:
                print('Not a valid jump: jumped from {} to {}'.format(jump[0], jump[1]))
                return False
            if self.layout[jump[1][0]][jump[1][1]] != '.':
                print('Not a valid move: ended on an occupied space.')
                return False
            # is a possible valid jump, check whether there are chess piece in between
            check_piece = ((jump[0][0]+jump[1][0])//2, (jump[0][1]+jump[1][1])//2)
            if self.layout[check_piece[0]][check_piece[1]] == '.':
                print('Not a valid move: jumped over nothing.')
                return False
            self.layout[jump[0][0]][jump[0][1]] = '.'
            if self.player == 'BLACK':
                self.layout[jump[1][0]][jump[1][1]] = 'B'
                self.black_pieces.remove(jump[0])
                self.black_pieces.add(jump[1])
            else:
                self.layout[jump[1][0]][jump[1][1]] = 'W'
                self.white_pieces.remove(jump[0])
                self.white_pieces.add(jump[1])

        # check finished, reset game board
        self.layout = layout
        self.black_pieces = black_pieces
        self.white_pieces = white_pieces
        return True

    # def look_around(self, pos: tuple):
    #     row, col = pos
    #     candidates = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
    #                  (row, col - 1), (row, col + 1),
    #                  (row + 1,col - 1), (row + 1,col), (row + 1,col + 1)]
    #     res = []
    #     for row, col in candidates:
    #         if row < 0 or row >= 16 or col < 0 or col >= 16:
    #             continue
    #         res.append((row, col))
    #     return res

    # code for agent's use ####################################################################################
    def look_around(self, pos: tuple):
        row, col = pos
        candidates = [(-1, -1), (-1, 0), (-1, 1),
                     (0, -1), (0, 1),
                     (1, -1), (1, 0), (1, 1)]
        res = []
        for row_change, col_change in candidates:
            if row + row_change < 0 or row + row_change >= 16 or col + col_change < 0 or col + col_change >= 16:
                continue
            res.append((row_change, col_change))
        return res

    #move a piece on the board
    def move_piece(self, pos1, pos2):
        if self.player == 'BLACK':
            self.black_pieces.remove(pos1)
            self.black_pieces.add(pos2)
            self.layout[pos1[0]][pos1[1]] = '.'
            self.layout[pos2[0]][pos2[1]] = 'B'

        else:
            self.white_pieces.remove(pos1)
            self.white_pieces.add(pos2)
            self.layout[pos1[0]][pos1[1]] = '.'
            self.layout[pos2[0]][pos2[1]] = 'W'


    # determine whether a play has won the game, return the player or NoneType
    def has_won(self):
        black_side = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4),
                      (1, 0), (1, 1), (1, 2), (1, 3), (1, 4),
                      (2, 0), (2, 1), (2, 2), (2, 3),
                      (3, 0), (3, 1), (3, 2),
                      (4, 0), (4, 1)}
        white_side = {(15, 15), (15, 14), (15, 13), (15, 12), (15, 11),
                      (14, 15), (14, 14), (14, 13), (14, 12), (14, 11),
                      (13, 15), (13, 14), (13, 13), (13, 12),
                      (12, 15), (12, 14), (12, 13),
                      (11, 15), (11, 14)}

        # check if white is winning
        win_condition = False
        for row,col in black_side:
            if self.layout[row][col] == 'W':
                win_condition = True
            elif self.layout[row][col] == 'B':
                continue
            else:
                win_condition = False
                break
        if win_condition:
            return 'WHITE'

        # check is black is winning
        for row,col in white_side:
            if self.layout[row][col] == 'B':
                win_condition = True
            elif self.layout[row][col] == 'W':
                continue
            else:
                win_condition = False
                break
        if win_condition:
            return 'BLACK'
        return None

    def to_string(self):
        res = ''
        for row in self.layout:
            res += ''.join(row)
        return res
