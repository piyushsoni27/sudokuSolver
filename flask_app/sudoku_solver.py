# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 20:15:37 2020

@author: Piyush Soni
"""

from math import sqrt

def isValidSudoku(board) -> bool:
    N = 9
    # If N=9, cell size is 3.
    cell_size = int(sqrt(N))

    rows = [set() for i in range(N)]
    cols = [set() for i in range(N)]
    cells = [set() for i in range(N)]
    
    for i in range(N):
        for j in range(N):
            if board[i][j] == '.':
                continue
                
            # Check rows
            if board[i][j] in rows[i]:
                return False

            # Check cols
            if board[i][j] in cols[j]:
                return False

            # Check cell by calculating cell num in range [0..N-1]
            cell_num = i//cell_size * cell_size + j//cell_size

            if board[i][j] in cells[cell_num]:
                return False
            
            # Add to rows, cols and cells sets.
            rows[i].add(board[i][j])
            cols[j].add(board[i][j])
            cells[cell_num].add(board[i][j])
                
    return True

def solveSudoku(sudoku):
        board=[x[:] for x in sudoku]
        n = len(board)        
        rows= [set() for _ in range(n)]
        cols = [set() for _ in range(n)]
        grids = [set() for _ in range(n)]
        
        def add_val_to_board(row, col, val):
            rows[row].add( val )
            cols[col].add( val )
            grids[(row//3)*3+ (col//3)].add( val )
            board[row][col] = str(val)
            
        def remove_val_from_board(row, col, val):
            rows[row].remove( val )
            cols[col].remove( val )
            grids[(row//3)*3+ (col//3)].remove( val )
            board[row][col] = "."
        
        def fill_board(row, col, val, board):
            
            if( row < 0 or col < 0 or row >= n or col >= n ):
                return
            
            ## GIST, incrementing row and col here
            while not board[row][col] == '.':
                col += 1
                if col == 9: 
                    col, row = 0, row+1
                if row == 9: 
                    return True
                
            for val in range( 1, n+1 ):
                if( val in rows[row] or val in cols[col] or val in grids[(row//3)*3+ (col//3)]):
                    continue
                    
                add_val_to_board(row, col, val)

                if( fill_board(row, col, val, board) ):
                    return board
                
                remove_val_from_board(row, col, val)

        for i in range(n):
            for j in range(n):
                if( not board[i][j] == "." ):
                    add_val_to_board( i, j, int(board[i][j]) )
        
        return fill_board(0, 0, board[0][0], board)
    
def main(board):
    if isValidSudoku(board):
        return True, solveSudoku(board)
    else:
        return False, []

if __name__ == '__main__':
    board = [[2, 5, '.', '.', 3, '.', 9, '.', 1], ['.', 1, '.', '.', '.', 4, '.', '.', '.'], [4, '.', 7, '.', '.', '.', 2, '.', 8], ['.', '.', 5, 2, '.', '.', '.', '.', '.'], ['.', '.', '.', '.', 9, 8, 1, '.', '.'], ['.', 4, '.', '.', '.', 3, '.', '.', '.'], ['.', '.', '.', 3, 5, '.', '.', 7, 2], ['.', 7, '.', '.', '.', '.', '.', '.', 3], [9, '.', 3, '.', '.', '.', 5, '.', 4]]
    _, solve=main(board)
    print(solve)
    print(board)
