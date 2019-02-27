#########################################################################
############################# sudoku.py #################################
############################ Leah Stern #################################
##################### Solves any Sudoku puzzle! #########################
## Uses backtacking search to solve a constraint satisfaction problem. ##
#########################################################################

import copy
import sys
import time
import argparse

# Functions to print in color. I found these in GeeksforGeeks article "Print
# Colors in Python terminal." 
# https://www.geeksforgeeks.org/print-colors-python-terminal/.
def prRed(skk): print("\033[91m {}\033[00m".format(skk), end="")
def prPurple(skk): print("\033[95m {}\033[00m".format(skk), end="")
def prLightGray(skk): print("\033[97m {}\033[00m".format(skk), end="")

# A puzzle is stored as a list of lists, where each sublist is a row. Each spot 
# in the puzzle is indexed as (row, column).

# Example easy puzzle
easy = [[6, 0, 8, 7, 0, 2, 1, 0, 0],
		[4, 0, 0, 0, 1, 0, 0, 0, 2],
		[0, 2, 5, 4, 0, 0, 0, 0, 0],
		[7, 0, 1, 0, 8, 0, 4, 0, 5],
		[0, 8, 0, 0, 0, 0, 0, 7, 0],
		[5, 0, 9, 0, 6, 0, 3, 0, 1],
		[0, 0, 0, 0, 0, 6, 7, 5, 0],
		[2, 0, 0, 0, 9, 0, 0, 0, 8],
		[0, 0, 6, 8, 0, 5, 2, 0, 3]]

# Example evil puzzle
evil = [[0, 7, 0, 0, 4, 2, 0, 0, 0],
		[0, 0, 0, 0, 0, 8, 6, 1, 0],
		[3, 9, 0, 0, 0, 0, 0, 0, 7],
		[0, 0, 0, 0, 0, 4, 0, 0, 9],
		[0, 0, 3, 0, 0, 0, 7, 0, 0],
		[5, 0, 0, 1, 0, 0, 0, 0, 0],
		[8, 0, 0, 0, 0, 0, 0, 7, 6],
		[0, 5, 4, 8, 0, 0, 0, 0, 0],
		[0, 0, 0, 6, 1, 0, 0, 5, 0]]

# Prints a list of lists to look like a Sudoku puzzle.
def printGrid(puzzle, position, mydigit):
	digitRow = position[0]
	digitCol = position[1]

	rowCount = 0
	spaceCount = 0

	print ("- - - - - - - - - - - -")

	for row in puzzle:
		for digit in row:
			if spaceCount%3==0:
				print ("|", end="")

			# Print new digit in purple
			if rowCount == digitRow and digit == mydigit:
				prPurple(digit)

			# Print empty spaces in red
			elif digit == 0:
				prRed(digit)

			# Print solved spaces in gray
			else:
				prLightGray(digit)
			spaceCount+=1

		print ("|\n", end="")

		rowCount+=1
		if rowCount%3==0:
			print ("- - - - - - - - - - - -")

# Checks a given row for a given digit and returns true if found in row.
def inRow(puzzle, row, digit):
	colCount = 0

	for col in puzzle:
		if puzzle[row][colCount] == digit:
			return True
		colCount+=1
	return False

# Checks a given column for a given digit and returns true if found in column.
def inCol(puzzle, col, digit):
	rowCount = 0

	for row in puzzle:
		if puzzle[rowCount][col] == digit:
			return True
		rowCount+=1
	return False

# Checks the box in which the current row and column are found for a given 
# digit and returns true if found.
def inBox(puzzle, firstRow, firstCol, digit):
	for row in range(3):
		for col in range(3):
			if puzzle[row+firstRow][col+firstCol] == digit:
				return True
	return False

# Calls inRow, inCol, and inBox to check if a given digit satisifes all
# 3 constraints.
def satisfiesConstraints(puzzle, row, col, digit):
	return (not inRow(puzzle, row, digit) and
		    not inCol(puzzle, col, digit) and
		    not inBox(puzzle, (row - row%3), (col - col%3), digit))

# Searches puzzle for first empty spot and returns a tuple for the row and 
# column where the empty spot is located. Returns (-1, -1) if no empty 
# spots are found.
def findEmptySpot(puzzle):
	for row in range(9):
		for col in range(9):
			if puzzle[row][col] == 0:
				return row, col
	return -1, -1

# Calls solvePuzzle to recursively solve the Sudoku puzzle. 
def startSolving(puzzle):
	# Copy puzzle into new puzzle used for printing each stage
	printPuzzle = copy.deepcopy(puzzle)

	return solvePuzzle(puzzle, printPuzzle)

# Uses backtracking search to solve a Sudoku puzzle and returns the solved 
# puzzle or false if the puzzle was not solved.
def solvePuzzle(puzzle, printPuzzle):
	# Base case; if there are no empty spots left, return the current puzzle
	if findEmptySpot(puzzle) == (-1, -1):
		return puzzle

	# Get the first empty spot in the puzzle
	currSpot = findEmptySpot(puzzle)
	currRow  = currSpot[0]
	currCol  = currSpot[1]

 	# Loop through digits 1-9 and test each digit to see if it satisifies
 	# constraints
	for digit in range(1, 10):
		if satisfiesConstraints(puzzle, currRow, currCol, digit):
 			# If current digit does satisfy constraints, then the current
 			# spot gets that digit
			puzzle[currRow][currCol] = digit

 			# Check if this new digit fits in the rest of the final puzzle and 
 			# return the solved puzzle if it does
			if solvePuzzle(puzzle, printPuzzle):
				# Print each stage atop the previous stage
				sys.stdout.write('\033[H')
				print ("\nSolving puzzle...")
				print ("Inserting", digit, "at", currSpot)			
				sys.stdout.flush()
				
				# Delay printing each stage so the user can watch it solve
				# the puzzle
				# NOTE: comment this line to see how fast we can really go!
				time.sleep(0.3)

				# Print the current stage in solving
				printCurrentStage(printPuzzle, currSpot, digit)

				# Finally return the puzzle when solved
				return puzzle

 			# If the current digit does not work, set the current location 
 			# back to 0
			puzzle[currRow][currCol] = 0

 	# Return false if the puzzle was not solved
	return False

# Prints the current stage of the puzzle in the solving process. 
def printCurrentStage(puzzle, index, digit):
	# Get the row and column from the index
	digitRow = index[0]
	digitCol = index[1]

	# Place the digit in the puzzle
	puzzle[digitRow][digitCol] = digit

	# Print the current puzzle
	printGrid(puzzle, index, digit)

# Main!
def main():
	# Argparse for CLI
	parser = argparse.ArgumentParser(description='Which puzzle should I solve?')
	parser.add_argument('puzzle', help='Use the name of the puzzle.')
	args = parser.parse_args()

	# Evaluate input string
	puzzle = eval(args.puzzle)

	# Clear the terminal just to look pretty!
	print("\033[H\033[J", end="")

	# Check whether puzzle can be solved
	if not startSolving(puzzle):
		prRed("I can't solve this puzzle!\n")
	else:
		startSolving(puzzle)
		print ("Solved!")

main()