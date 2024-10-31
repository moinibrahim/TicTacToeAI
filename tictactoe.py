import copy
import sys
import pygame
import random
import numpy as np

from constants import *

# PYGAME SETUP 

pygame.init()
screen = pygame.display.set_mode( (width, height) )
pygame.display.set_caption('Tic Tac Toe')
screen.fill( background_color )

#  CLASSES 

class Board:

    def __init__(self):
        self.squares = np.zeros( (rows, column) )
        self.empty_sqrs = self.squares              # list of squares
        self.marked_sqrs = 0

    def final_state(self, show=False):
        

        # vertical wins
        for col in range(column):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = circle_color if self.squares[0][col] == 2 else cross_color
                    iPos = (col * square_size + square_size // 2, 20)
                    fPos = (col * square_size + square_size // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.squares[0][col]

        # horizontal wins
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = circle_color if self.squares[row][0] == 2 else cross_color
                    iPos = (20, row * square_size + square_size // 2)
                    fPos = (width - 20, row * square_size + square_size // 2)
                    pygame.draw.line(screen, color, iPos, fPos, line_width)
                return self.squares[row][0]

        # descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = circle_color if self.squares[1][1] == 2 else cross_color
                iPos = (20, 20)
                fPos = (width - 20, height - 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.squares[1][1]

        # ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = circle_color if self.squares[1][1] == 2 else cross_color
                iPos = (20, height - 20)
                fPos = (width - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, cross_width)
            return self.squares[1][1]

        # no wins yet
        return 0

    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(rows):
            for col in range(column):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player

    #  RANDOM 

    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx] # (row, col)

    #  MINIMAX 

    def minimax(self, board, maximizing):
        
        # terminal case
        case = board.final_state()

        # player 1 wins
        if case == 1:
            return 1, None # eval, move

        # player 2 wins
        if case == 2:
            return -1, None

        # draw
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move

    #  MAIN EVALALUATION 

    def eval(self, main_board):
        if self.level == 0:
            # random choice
            eval = 'random'
            move = self.rnd(main_board)
        else:
            # minimax algo choice
            eval, move = self.minimax(main_board, False)

        print(f'AI has chosen to mark the square in pos {move} with an eval of: {eval}')

        return move # row, col

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   #1 -> cross  #2 -> circles
        self.gamemode = 'ai' # player vs. player or ai
        self.running = True
        self.show_lines()

    # DRAW METHODS

    def show_lines(self):
        # background
        screen.fill( background_color )

        # vertical
        pygame.draw.line(screen, line_color, (square_size, 0), (square_size, height), line_width)
        pygame.draw.line(screen, line_color, (width - square_size, 0), (width - square_size, height), line_width)

        # horizontal
        pygame.draw.line(screen, line_color, (0, square_size), (width, square_size), line_width)
        pygame.draw.line(screen, line_color, (0, height - square_size), (width, height - square_size), line_width)

    def draw_fig(self, row, col):
        if self.player == 1:
            # draw cross
            # descending line
            start_desc = (col * square_size + offset, row * square_size + offset)
            end_desc = (col * square_size + square_size - offset, row * square_size + square_size - offset)
            pygame.draw.line(screen, cross_color, start_desc, end_desc, cross_width)
            # ascending line
            start_asc = (col * square_size + offset, row * square_size + square_size - offset)
            end_asc = (col * square_size + square_size - offset, row * square_size + offset)
            pygame.draw.line(screen, cross_color, start_asc, end_asc, cross_width)
        
        elif self.player == 2:
            # draw circle
            center = (col * square_size + square_size // 2, row * square_size + square_size // 2)
            pygame.draw.circle(screen, circle_color, center, radius, circle_width)

    # OTHER METHODS 

    def make_move(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.draw_fig(row, col)
        self.next_turn()

    def next_turn(self):
        self.player = self.player % 2 + 1

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.final_state(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():

    # OBJECTS 

    game = Game()
    board = game.board
    ai = game.ai

    # MAINLOOP

    while True:
        
        # pygame events
        for event in pygame.event.get():

            # quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # keydown event
            if event.type == pygame.KEYDOWN:

                # g -> gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                # r -> restart
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

                # 0 -> random ai
                if event.key == pygame.K_0:
                    ai.level = 0
                
                # 1 -> random ai
                if event.key == pygame.K_1:
                    ai.level = 1

            # click event
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // square_size
                col = pos[0] // square_size
                
                # human mark square
                if board.empty_sqr(row, col) and game.running:
                    game.make_move(row, col)

                    if game.isover():
                        game.running = False


        # AI initial call
        if game.gamemode == 'ai' and game.player == ai.player and game.running:

            # update the screen
            pygame.display.update()

            # eval
            row, col = ai.eval(board)
            game.make_move(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()