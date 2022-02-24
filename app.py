"""
Sudoku Game GUI
Created by: Madeo Arturi
"""

import pygame
import math
import random
from sudoku import solve_sudoku
from typing import List, Tuple, Optional

# initialize pygame
pygame.init()
pygame.font.init()

# create window
screen = pygame.display.set_mode((1010, 610))
pygame.display.set_caption("Sudoku V1.0")
icon = pygame.image.load("images/Sudoku16.gif")
pygame.display.set_icon(icon)

# font creation
font_30 = pygame.font.SysFont("Arial", 30)
font_40 = pygame.font.SysFont("Arial", 40)
font_50 = pygame.font.SysFont("Arial", 50)
font_60 = pygame.font.SysFont("Arial", 60)
title = font_40.render("m4deo", False, (0, 0, 0))
title2 = font_40.render("Sudoku", False, (0, 0, 0))
incorrect_str = font_40.render("Incorrect Attempts", False, (255, 0, 0))
incorrect_x = font_60.render("X", False, (255, 0, 0))


# Button Class
class Button:
    """Class for a clickable button
    """
    def __init__(self, colour: Tuple[int, int, int], x: int, y: int, width: int,
                 height: int, b_font, text='') -> None:
        self.colour = colour
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.font = b_font

    def draw(self, window) -> None:
        """Draw the button onto the screen"""
        # outline
        pygame.draw.rect(window, (0, 0, 0), (self.x - 2, self.y - 2,
                                             self.width + 4, self.height + 4))
        pygame.draw.rect(window, self.colour, (self.x, self.y, self.width,
                                               self.height))
        if self.text != '':
            text = self.font.render(self.text, False, (0, 0, 0))
            window.blit(text, (self.x + (self.width // 2 -
                                         text.get_width() // 2),
                               self.y + (self.height // 2 -
                                         text.get_height() // 2)))

    def is_hovering(self, mouse_pos: Tuple[int, int]) -> bool:
        """Return True if mouse is hovering over this button
        False otherwise
        """
        if self.x <= mouse_pos[0] <= self.x + self.width:
            if self.y <= mouse_pos[1] <= self.y + self.height:
                return True
        return False


# create a class for each square
class Tile:
    """Class representing each tile on a sudoku board
    A Sudoku board is in this form
    0,0 0,1 0,2 | 0,3 0,4 0,5 | 0,6, 0,7, 0,8
    1,0 1,1 1,2 | 1,3 1,4 1,5 | 1,6, 1,7, 1,8
    2,0 2,1 2,2 | 2,3 2,4 2,5 | 2,6, 2,7, 2,8
    -----------------------------------------
    3,0 3,1 3,2 | 3,3 3,4 3,5 | 3,6, 3,7, 3,8
    4,0 4,1 4,2 | 4,3 4,4 4,5 | 4,6, 4,7, 4,8
    5,0 5,1 5,2 | 5,3 5,4 5,5 | 5,6, 5,7, 5,8
    -----------------------------------------
    6,0 6,1 6,2 | 6,3 6,4 6,5 | 6,6, 6,7, 6,8
    7,0 7,1 7,2 | 7,3 7,4 7,5 | 7,6, 7,7, 7,8
    8,0 8,1 8,2 | 8,3 8,4 8,5 | 8,6, 8,7, 8,8

    === Attributes ===
    number: the number stored in this Tile, None if empty Tile
    x: the horizontal location of the Tile on the Board
        (after adjusting the above coordinates to the screen dimensions)
    y: the vertical location of the Tile on the Board
        (after adjusting the above coordinates to the screen dimensions)
    _locked: True iff the Tile contains the right answer, False if empty
    selected: True iff Tile is selected, False otherwise

    === Representation Invariants ===
    1 <= number <= 9
    0 <= x, y <= 8
    """
    number: Optional[int]
    x: int
    y: int
    _locked: bool

    def __init__(self, number: Optional[int],
                 location: Tuple[int, int], is_locked: bool) -> None:
        """Initialize given Tile object"""

        self.number = number
        self.loc_x = location[0]
        self.loc_y = location[1]
        self.x = 410 + self.loc_x * 65 + 5 * math.floor(location[0] / 3)
        self.y = 10 + self.loc_y * 65 + 5 * math.floor(location[1] / 3)
        self._locked = is_locked
        self.selected = False

    def is_locked(self) -> bool:
        """Return True if the Tile has been correctly answered already
        return False otherwise
        """
        return self._locked

    def draw(self, window) -> None:
        if self.selected:
            pygame.draw.rect(window, (153, 255, 51),
                             (self.x + 5, self.y + 5, 50, 50))

        if self.number != 0:
            text = font_40.render(str(self.number), False, (0, 0, 0))
            window.blit(text, (self.x + (30 - text.get_width() // 2),
                               self.y + (30 - text.get_height() // 2)))

    def hovering(self, mouse_pos) -> bool:
        if self.x <= mouse_pos[0] <= self.x + 60:
            if self.y <= mouse_pos[1] <= self.y + 60:
                return True
        return False

    def accept_input(self, board) -> None:
        """Accept an integer input and update the tiles number
        Do nothing if input is invalid (look representation invariants)
        """
        pass


class Board:
    """Class representing a sudoku board

    === Attributes ===
    tiles: the tiles that make up the board

    === Representation Invariants ===
    len(tiles) == 9
    len(tiles[0]) == 9
    len(tiles[1]) == 9
    len(tiles[2]) == 9
    """
    tiles: List[List[Tile]]

    def __init__(self, tiles: List[List[Tile]]) -> None:
        self.tiles = tiles

    def draw_tiles(self, window) -> None:
        for row in self.tiles:
            for tile in row:
                tile.draw(window)

    def tile_to_int(self) -> List[List[int]]:
        board = []
        for row in self.tiles:
            row2 = []
            for tile in row:
                row2.append(tile.number)
            board.append(row2)
        return board

    def solve(self):
        board = self.tile_to_int()
        solve_sudoku(board)
        return Board(int_to_Board(board))

    def selected_tile(self, mouse_pos) -> Tuple[bool, Optional[Tile]]:
        """Checks if mouse is on a tile in the board
        Returns True and the selected Tile
        Returns False otherwise"""
        for row in self.tiles:
            for tile in row:
                if tile.hovering(mouse_pos):
                    return True, tile
        return False, None


def int_to_Board(board: List[List[int]]) -> List[List[Tile]]:
    new_board = []
    for i in range(9):  # 0, 1, 2, ... , 8
        new_board.append([])
        for j in range(9):  # 0, 1, 2, ... , 8
            if board[i][j] == 0:
                new_board[i].append(Tile(board[i][j], (j, i), False))
            else:
                new_board[i].append(Tile(board[i][j], (j, i), True))
    return new_board


def check_correct(solved: "Board", tile: Tile, ans: int) -> bool:
    """Checks if the given answer is correct
    """
    x = tile.loc_x
    y = tile.loc_y
    if solved.tiles[y][x].number == ans:
        return True
    return False


# create button instances
new_board_button = Button((150, 150, 150), 50, 150, 300, 100, font_50,
                          "New Board")
solve_button = Button((150, 150, 150), 50, 300, 300, 100, font_50, "Solve")

# Other boards
extra_boards = [[[5, 3, 0, 0, 7, 0, 0, 0, 0],
                 [6, 0, 0, 1, 9, 5, 0, 0, 0],
                 [0, 9, 8, 0, 0, 0, 0, 6, 0],

                 [8, 0, 0, 0, 6, 0, 0, 0, 3],
                 [4, 0, 0, 8, 0, 3, 0, 0, 1],
                 [7, 0, 0, 0, 2, 0, 0, 0, 6],

                 [0, 6, 0, 0, 0, 0, 2, 8, 0],
                 [0, 0, 0, 4, 1, 9, 0, 0, 5],
                 [0, 0, 0, 0, 8, 0, 0, 7, 9]],

                [[3, 9, 0, 0, 5, 0, 0, 0, 0],
                 [0, 0, 0, 2, 0, 0, 0, 0, 5],
                 [0, 0, 0, 7, 1, 9, 0, 8, 0],

                 [0, 5, 0, 0, 6, 8, 0, 0, 0],
                 [2, 0, 6, 0, 0, 3, 0, 0, 0],
                 [0, 0, 0, 0, 0, 0, 0, 0, 4],

                 [5, 0, 0, 0, 0, 0, 0, 0, 0],
                 [6, 7, 0, 1, 0, 5, 0, 4, 0],
                 [1, 0, 9, 0, 0, 0, 2, 0, 0]]

                ]

ready_boards = []
for board in extra_boards:
    tile_list = int_to_Board(board)
    ready_boards.append(Board(tile_list))

# Get first board
curr_board = random.choice(ready_boards)
solved_board = curr_board.solve()

# Variable creation
playing_board = True
selected = None
poss_keys = [49, 50, 51, 52, 53, 54, 55, 56, 57]
incorrect = 0

# game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = event.pos

            # Check if button is clicked
            if solve_button.is_hovering(pos):
                curr_board = solved_board

            if new_board_button.is_hovering(pos):
                curr_board = random.choice(ready_boards)
                solved_board = curr_board.solve()
                incorrect = 0
                selected = None
                playing_board = True

            # Check if a Tile is clicked
            sel_tile = curr_board.selected_tile(pos)
            if sel_tile[0]:
                if isinstance(selected, Tile):
                    selected.selected = False
                if sel_tile[0] == selected:
                    selected.selected = False
                    selected = None
                else:
                    sel_tile[1].selected = True
                    selected = sel_tile[1]

        if event.type == pygame.KEYDOWN and selected is not None:
            if event.key in poss_keys:
                attempt = int(chr(event.key))
                if check_correct(solved_board, selected, attempt):
                    selected.number = attempt
                else:
                    incorrect += 1

    if incorrect == 3:
        curr_board = solved_board

    # draw background
    screen.fill((102, 255, 255))

    # draw sudoku grid
    pygame.draw.rect(screen, (255, 255, 255), (410, 0, 610, 610))

    pygame.draw.rect(screen, (0, 0, 0), (400, 0, 10, 610))  # Left Border
    pygame.draw.rect(screen, (0, 0, 0), (410, 0, 600, 10))  # Top Border
    pygame.draw.rect(screen, (0, 0, 0), (410, 600, 600, 10))  # Bottom Border
    pygame.draw.rect(screen, (0, 0, 0), (1000, 0, 10, 610))  # Right Border

    pygame.draw.rect(screen, (0, 0, 0), (410, 200, 690, 10))  # X1-2
    pygame.draw.rect(screen, (0, 0, 0), (410, 400, 690, 10))  # X2-3
    pygame.draw.rect(screen, (0, 0, 0), (600, 0, 10, 600))  # Y1-2
    pygame.draw.rect(screen, (0, 0, 0), (800, 0, 10, 600))  # Y2-3

    pygame.draw.rect(screen, (0, 0, 0), (410, 70, 690, 5))  # X1.1-2
    pygame.draw.rect(screen, (0, 0, 0), (410, 135, 690, 5))  # X1.2-3
    pygame.draw.rect(screen, (0, 0, 0), (410, 270, 690, 5))  # X2.1-2
    pygame.draw.rect(screen, (0, 0, 0), (410, 335, 690, 5))  # X2.2-3
    pygame.draw.rect(screen, (0, 0, 0), (0, 470, 1010, 5))  # X3.1-2
    pygame.draw.rect(screen, (0, 0, 0), (410, 535, 690, 5))  # X3.2-3

    pygame.draw.rect(screen, (0, 0, 0), (470, 0, 5, 600))  # Y1.1-2
    pygame.draw.rect(screen, (0, 0, 0), (535, 0, 5, 600))  # Y1.2-3
    pygame.draw.rect(screen, (0, 0, 0), (670, 0, 5, 600))  # Y2.1-2
    pygame.draw.rect(screen, (0, 0, 0), (735, 0, 5, 600))  # Y2.2-3
    pygame.draw.rect(screen, (0, 0, 0), (870, 0, 5, 600))  # Y3.1-2
    pygame.draw.rect(screen, (0, 0, 0), (935, 0, 5, 600))  # Y3.2-3

    # Title
    screen.blit(title, (200 - title.get_width() // 2, 20))
    screen.blit(title2, (200 - title2.get_width() // 2, 70))

    # Buttons
    new_board_button.draw(screen)
    solve_button.draw(screen)

    # Incorrect Attempts
    pygame.draw.rect(screen, (0, 76, 153), (0, 475, 400, 135))
    screen.blit(incorrect_str, (200 - incorrect_str.get_width() // 2, 480))
    for inc in range(incorrect):
        screen.blit(incorrect_x, (105 + inc * 70, 540))

    # Draw board
    curr_board.draw_tiles(screen)

    pygame.display.update()
