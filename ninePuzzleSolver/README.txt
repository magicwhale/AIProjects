This project contains a sliding puzzle solver.

To run the code, run the command:
python driver.py [searchMethod] [board]

where [searchMethod] is either: bfs, dfs, ast, or ida

bfs searches the solution space using breadth-first search, dfs searches the solution
space using depth first search, ast searches the solution space using A-Star search,
and ida searches the solution space using IDA-Star search.

[board] should contain the starting format of the board, with each row input in order
from left to right, separated by commas. A 0 should be used to denote an empty space
in the sliding puzzle.

For example, to find a solution using bfs to the board:
  -   -   -
|   | 8 | 7 |
  -   -   - 
| 6 | 5 | 4 |
  -   -   - 
| 3 | 2 | 1 |
  -   -   -

run the command: python driver.py bfs 0,8,7,6,5,4,3,2,1
