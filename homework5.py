############################################################
# CIS 521: Homework 5
############################################################

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import collections
import copy
import itertools
import random
import math

############################################################

student_name = "Xinyuan Quan"

############################################################
# Sudoku Solver
############################################################


def sudoku_cells():
    return [(row, col) for row in range(9) for col in range(9)]


def sudoku_arcs():
    ans = []
    for cell1 in sudoku_cells():
        row1, col1 = cell1
        for cell2 in sudoku_cells():
            row2, col2 = cell2
            same_row = row1 == row2
            same_column = col1 == col2

            cell1_block_row = row1 // 3
            cell1_block_column = col1 // 3

            cell2_block_row = row2 // 3
            cell2_block_column = col2 // 3

            same_block = (
                cell1_block_row == cell2_block_row
                and cell1_block_column == cell2_block_column
            )

            if cell1 != cell2 and (same_row or same_column or same_block):
                ans.append((cell1, cell2))

    return ans


def read_board(path):
    board = {}
    with open(path, "r") as puzzle_file:
        lines = puzzle_file.readlines()

    rows = []
    for line in lines:
        row = [character for character in line if character not in " ,\n\t"]
        if row:
            rows.append(row)

    if len(rows) != 9 or any(len(row) != 9 for row in rows):
        raise ValueError("A Sudoku board must contain 9 rows of 9 cells.")

    consider_number = set(range(1, 10))

    for row in range(9):
        for col in range(9):
            value = rows[row][col]
            if value in {"*", "0"}:
                board[(row, col)] = set(consider_number)
            elif value in "123456789":
                board[(row, col)] = {int(value)}
            else:
                raise ValueError("Board cells must be digits, '*' or '0'.")
    return board


def sudoku_units():
    rows = [[(row, col) for col in range(9)] for row in range(9)]
    columns = [[(row, col) for row in range(9)] for col in range(9)]

    blocks = []
    for r in range(3):
        for c in range(3):
            block = []
            for row in range(r * 3, r * 3 + 3):
                for col in range(c * 3, c * 3 + 3):
                    block.append((row, col))
            blocks.append(block)

    return rows + columns + blocks


class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()
    UNITS = sudoku_units()
    PEERS = {cell: set() for cell in CELLS}

    for cell1, cell2 in ARCS:
        PEERS[cell1].add(cell2)

    def __init__(self, board):
        self.board = {cell: set(values) for cell, values in board.items()}

    def get_values(self, cell):
        return self.board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        old_one = self.board[cell1]

        consider_member = {
            i
            for i in old_one
            if any(i != j for j in self.board[cell2])
        }

        if consider_member == old_one:
            return False
        
        self.board[cell1] = consider_member
        return True

    def infer_ac3(self):
        queue = collections.deque(self.ARCS)

        while queue:
            cell1, cell2 = queue.popleft()

            if self.remove_inconsistent_values(cell1, cell2):
                if not self.board[cell1]:
                    return False
                for i in self.PEERS[cell1] - {cell2}:
                    queue.append((i, cell1))

        return True

    def infer_improved(self):
         while True:

            if not self.infer_ac3():
                return False

            indictor = False
            for unit in self.UNITS:
                for value in range(1, 10):
                    consider_member = [
                        cell for cell in unit if value in self.board[cell]
                    ]
                    if not consider_member:
                        return False
                    if len(consider_member) == 1:
                        cell = consider_member[0]
                        if self.board[cell] != {value}:
                            self.board[cell] = {value}
                            indictor = True

            if not indictor:
                return True

    def infer_with_guessing(self):

        def search(board):
            puzzle = Sudoku(board)

            if not puzzle.infer_improved():
                return None

            if all(len(puzzle.board[cell]) == 1 for cell in self.CELLS):
                return puzzle.board

            cell = min(
                (
                    current_one
                    for current_one in self.CELLS
                    if len(puzzle.board[current_one]) > 1
                ),
                key=lambda current_one: len(puzzle.board[current_one]),
            )

            for i in sorted(puzzle.board[cell]):
                guessed_board = {
                    current_one: set(values)
                    for current_one, values in puzzle.board.items()
                }

                guessed_board[cell] = {i}

                solution = search(guessed_board)
                if solution is not None:
                    return solution
                    
            return None

        solution = search(self.board)
        if solution is None:
            return False
        
        self.board = solution
        return True

############################################################
# Feedback
############################################################


# Just an approximation is fine.
feedback_question_1 = """
8
"""

feedback_question_2 = """
It's kind of hard to understand the text and whole process.
"""

feedback_question_3 = """
Clear structure.
"""
