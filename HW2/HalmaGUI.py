import tkinter as tk
import argparse
import os, time
from HalmaBoard import HalmaBoard


class HalmaGUI(tk.Frame):
    def __init__(self, parent, rows=16, columns=16, size=24, color1="#ccc", color2="#888"):
        '''size is the size of a square, in pixels'''

        self.rows = rows
        self.columns = columns
        self.size = size
        self.color1 = color1
        self.color2 = color2
        self.BLACKpos = []
        self.WHITEpos = []
        self.moves = []

        canvas_width = columns * size
        canvas_height = rows * size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="white")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # this binding will cause a refresh if the user interactively
        # changes the window size
        self.canvas.bind("<Configure>", self.refresh)

    def place_chess(self, pos, player):
        radius = 10 if self.size<=18 else self.size-8

        row, column = pos
        x0 = (column * self.size) + int(self.size / 2)
        y0 = (row * self.size) + int(self.size / 2)
        color = 'black' if player == 'BLACK' else 'white'

        return self.canvas.create_oval(x0-radius/2, y0-radius/2, x0+radius/2, y0+radius/2, fill=color, tags='piece')

    # refresh the board when window resized
    def refresh(self, event):
        '''Redraw the board, possibly in response to window being resized'''
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        self.canvas.delete("piece")
        self.canvas.delete("move")
        self.canvas.delete("path")
        #color = self.color2
        for row in range(self.rows):
            #color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                color = self.color1 if (row-col)%2==0 else self.color2
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                #color = self.color1 if color == self.color2 else self.color2

        self.draw_movements(self.moves)
        self.draw_paths(self.moves)

        # place player 1 and player 2 chesses
        for p in self.BLACKpos:
            self.place_chess(p, 'BLACK')
        for p in self.WHITEpos:
            self.place_chess(p, 'WHITE')

        self.canvas.tag_raise("piece")
        self.canvas.tag_raise("path")
        self.canvas.tag_lower("square")

    # call this function when a movement has been made and a new board layout is created
    def refresh_chess(self, p1pos, p2pos):

        self.canvas.delete("piece")
        self.BLACKpos = p1pos
        self.WHITEpos = p2pos
        # place player 1 and player 2 chesses
        for p in self.BLACKpos:
            self.place_chess(p, 'BLACK')
        for p in self.WHITEpos:
            self.place_chess(p, 'WHITE')
        self.canvas.tag_raise("piece")

    def draw_movements(self, moves):
        self.canvas.delete("move")
        for col, row in moves:
            x1 = (col * self.size)
            y1 = (row * self.size)
            x2 = x1 + self.size
            y2 = y1 + self.size
            color = '#F00'
            self.canvas.create_rectangle(x1, y1, x2, y2, outline='black', fill=color, tags="move")
        self.canvas.tag_raise("piece")

    def draw_paths(self, moves):
        self.canvas.delete("path")
        last_col = None
        last_row = None
        for (count, (col, row)) in enumerate(moves):
            if count == 0:
                last_col = col
                last_row = row
            else:
                x1 = (last_col + 0.5) * self.size
                y1 = (last_row + 0.5) * self.size
                x2 = (col + 0.5) * self.size
                y2 = (row + 0.5) * self.size
                self.canvas.create_line(x1, y1, x2, y2, fill='blue', tags='path', width=2)
                last_col = col
                last_row = row

    def draw_output(self, output_file):
        moves = []
        with open(output_file) as f:
            for line_count, line in enumerate(f):
                info = line.strip().split(' ')
                if len(info) == 3:
                    if line_count == 0:
                        moves.append((int(info[1].split(',')[0]), int(info[1].split(',')[1])))
                        moves.append((int(info[2].split(',')[0]), int(info[2].split(',')[1])))
                    else:
                        moves.append((int(info[2].split(',')[0]), int(info[2].split(',')[1])))
        self.moves = moves
        self.draw_movements(self.moves)
        self.draw_paths(self.moves)

if __name__ == "__main__":
    root = tk.Tk()
    root.title('Halma GUI')
    board = HalmaGUI(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    # p1 = [(0,0),(0,1),(0,2),(0,3),(0,4),
    #       (1,0),(1,1),(1,2),(1,3),(1,4),
    #       (2,0),(2,1),(2,2),(2,3),
    #       (3,0),(3,1),(3,2),
    #       (4,0),(4,1)]
    #
    # p2 = [(18-i,18-j) for i,j in p1]
    #
    # for p in p1:
    #     board.BLACKpos.append(p)
    #     board.place_chess(p, 1)
    #
    # for p in p2:
    #     board.WHITEpos.append(p)
    #     board.place_chess(p, 1)

    input_file = 'input.txt'
    output_file = 'output.txt'

    halma_board = HalmaBoard()
    halma_board.read_input(input_file)
    board.refresh_chess(halma_board.black_pieces, halma_board.white_pieces)

    moddate_in = os.stat(input_file)[8]
    moddate_out = os.stat(output_file)[8]



    while True:
        tempmd_in = os.stat(input_file)[8]
        tempmd_out = os.stat(output_file)[8]

        if tempmd_in != moddate_in:
            moddate_in = tempmd_in
            print('input.txt change observed: {}.'.format(time.ctime(moddate_in)))
            halma_board.read_input(input_file)
            board.refresh_chess(halma_board.black_pieces, halma_board.white_pieces)

        if tempmd_out != moddate_out:
            moddate_out = tempmd_out
            print('output.txt change observed: {}.'.format(time.ctime(moddate_in)))
            board.draw_output(output_file)
        root.update_idletasks()
        root.update()
        time.sleep(0.1)