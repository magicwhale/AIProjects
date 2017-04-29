This project contains an AI to solve sudoku puzzles using both the AC-3 and backtracking
search algorithm.

To run the AI, run the command:
python3 driver_3.py <input_string>

where input_string is a txt file containing sudoku puzzles separated by a newline.
The puzzles should be encoded row by row from left to right, using 0s in place of
empty spaces.

The file sudokus_start.txt is included with many example sudokus to test. These can
be tested using the command:
python3 driver_3.py sudokus_start.txt

The filled sudoku boards will be output into a file called output.txt
