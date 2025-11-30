# Minesweeper SAT Solver
This project implements a SAT-based solver for a Minesweeper instance.
It takes a partially revealed Minesweeper board, as well as its number of rows and columns, as standard input, encodes all valid mine placements into a CNF formula, calls the SAT solver Glucose 4.1, and decodes the resulting assignment back into a more completed board.

## Problem description:
We are given a rectangular Minesweeper board of size R × C.
Each cell is either a number, representing the count of mines in its 8-neighboring cells, or a “?”, representing an unrevealed cell that may or may not contain a mine.
### Goal:
Determine whether there exists a placement of mines in the '?' cells that satisfies all numeric clues.
If such a placement exists, the solver outputs one valid assignment.
If not, the solver outputs “Unnsatisfiable!”.

## Parameters
### The problem takes as input:
   R - number of rows.
   C - number of columns.
   A board of R lines, each containing C seperated symbols - ? for unknown cells and an integer for clues.
### Example:
```
3 3
2 ? 2
? 4 ?
? ? ?
```
Optionally, after receving the output, you can input 'c' or 's' to receive CNF formula in DIMACS CNF format, or statistics about the SAT solver’s execution.

## Decision variables:
Each '?' adjacent to number clue becomes a variable. A given variable is true if its respective cell contains a mine.
Cells containing a known clue and unrestrained '?' cells do not receive a variable.

## Constraints:
Constrains are portrayed by cells containing integers. The integer represents the exact number of mines among its 8 adjacent cells.

## CNF-Encoding:
The script runs through every cell on the board. It initially ignores '?' cells. After finding a cell that contains a number 'k', it proceeds to:
  1) Check every surrounding cell. When it finds a '?' cell, it remembers its variable (or assigns one if the cell had not been encountered previously).
  2) Run functions 'min_clauses' and 'max_clauses' on the resulting list of variables. The function 'min_clauses' creates a list of clauses that assures at     that at least k variables are true (and therefore contain a mine). The function 'max_clauses' creates a list of clauses that assures at that at most k variables are true (and therefore contain a mine). The combination of these clauses assures that exactly k variables are true.
  3) Add all the resulting clauses to a set of all clauses found so far.

## Input Format:
The first line of input contains the number of rows and columns in the board.
The rest of standard input is dedicated to the board itself. Use parameters and the example provided above for reference.

## Output:
The output contains the board provided in the input, but the cells adjacent to numbers are replaced with '*' for mine and 's' for safe.
The '?' cells that are not adjacent to number clues are not replaced due to lack of constraints, but for purposes of satisfiability they can be considered safe.

## Included instances:
The first instance included contains a single row with 5 cells:
```
1 5
? 1 ? 2 ?
```
The instance is satisfiable, and when ran through the script outputs:
```
1 5
s 1 * 2 *
```

The second instance, containing the input
```
1 5
? 3 ? 3 ?
```
is unsatisfiable.

The third instance contains a 3x3 board:
```
2 ? 2
? 4 ?
? ? ?
```
The resulting output is:
```
2 * 2
* 4 *
* s s
```
It's worth noting that the given number of constraints is not enough to narrow down the instance to a single model, which means that the solution is not guaranteed to be true in a real game of Minesweeper.

The fourth instance also contains a 3x3 board:
```
3 3
2 ? ?
? 3 ?
? ? 2
```
However, it is unsatisfiable.

The fifth and final instance contains a column of 5 cells:
```
5 1
1
?
2
?
1
```
The output:
```
5 1
1
*
2
*
1
```
The search for a non-trivial instance was unsuccessful. The attempts included a 128x128 board with alternating '?' and '2' cells (8192 variables, 64515 clauses, 0.072s solution time), as well as a random 20x20 board from a real game of Minesweeper (solved in 0.19s). Evidently, a longer-running instance would take both a longer board and more varied cells, which cannot be generated randomly due to high risk of unsatisfiability, and is tricky to create by hand.
## Conclusion:
As evidenced by the instances above, the script can solve both sizeable and varied boards in a trivial amount of time. Particularly, the size of the board barely matters if it contains similar, overlapping patterns.
