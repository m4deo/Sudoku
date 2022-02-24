def find_next_empty(puzzle):
    """
    finds the next row, col on the puzzle that's not filled yet --> rep with 0
    
    return row, col tuple (or (None, None) if there is none)
    """

    for row in range(9):
        for col in range(9):
            if puzzle[row][col] == 0:
                return row, col

    return None, None  # if no spaces left


def is_valid(puzzle, guess, row, col):
    """
    figures out whether the guess at the row/col of the puzzle is a valid guess

    returns True if valid, false otherwise
    """

    # row
    row_values = puzzle[row]
    if guess in row_values:
        return False

    # column
    col_values = [puzzle[i][col] for i in range(9)]
    if guess in col_values:
        return False

    # 3x3 grid
    row_start = (row // 3) * 3  # finds if in first, second or third set of 3 rows
    col_start = (col // 3) * 3  # finds if in first, second or third set of 3 columns

    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False

    # Passed all checks
    return True


def solve_sudoku(puzzle):
    """
    solve sudoku using backtracking
    our puzzle is a list of lists, where each inner list is a row in our
    sudoku puzzle
    return whether a solution exists
    mutates puzzle to be solution (if solution exists)
    """

    # choose the next free tile on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # if theres nowhere left, then we're done
    if row is None:
        return True

    # if theres a place to put guess, make a guess between 1-9
    for guess in range(1, 10):
        # check if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            # if this is valid, then place that guess on the puzzle
            puzzle[row][col] = guess
            # recurse using this new puzzle
            if solve_sudoku(puzzle):
                return True

        # if not valid or guess does not solve puzzle, then backtrack and try a new number
        puzzle[row][col] = 0 # reset guess

    # if none of numbers work, then puzzle is Unsolvable
    return False


if __name__ == '__main__':
    ex_board = [[3, 9, 0, 0, 5, 0, 0, 0, 0],
                [0, 0, 0, 2, 0, 0, 0, 0, 5],
                [0, 0, 0, 7, 1, 9, 0, 8, 0],

                [0, 5, 0, 0, 6, 8, 0, 0, 0],
                [2, 0, 6, 0, 0, 3, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 4],

                [5, 0, 0, 0, 0, 0, 0, 0, 0],
                [6, 7, 0, 1, 0, 5, 0, 4, 0],
                [1, 0, 9, 0, 0, 0, 2, 0, 0]]

    ex_board2 = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
                 [6, 0, 0, 1, 9, 5, 0, 0, 0],
                 [0, 9, 8, 0, 0, 0, 0, 6, 0],

                 [8, 0, 0, 0, 6, 0, 0, 0, 3],
                 [4, 0, 0, 8, 0, 3, 0, 0, 1],
                 [7, 0, 0, 0, 2, 0, 0, 0, 6],

                 [0, 6, 0, 0, 0, 0, 2, 8, 0],
                 [0, 0, 0, 4, 1, 9, 0, 0, 5],
                 [0, 0, 0, 0, 8, 0, 0, 7, 9]]

    print(solve_sudoku(ex_board2))
    print(ex_board2)
