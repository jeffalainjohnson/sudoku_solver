# sudoku_solver
Sudoku_solver.py is a Python 3.x program that solves sudoku puzzles.

BACKGROUND & HISTORY

Watching my wife Karen solve the sudoku puzzles in the daily SF Chronicle, sometime in the 2010s I started solving them myself and we developed a friendly competition.  At first I could solve only simple sudokus -- the ones the Chronicle rated 1, 2, or 3, but I soon learned deductive patterns for solving harder sudokus -- ones the Chronicle rated 4, 5, or 6.  I've never resorted to guessing and backtracking.  It was a matter of learning to search for and spotting certain patterns in the grid.  At the time I didn't know that these patterns have common names; I only knew the patterns.  I got pretty good at recognizing them and at solving sudokus, but occasionally I would encounter ones I could not solve: I couldn't spot any of my known deductive patterns. I wasn't sure if I was missing familiar patterns or if there were more sophisticated deductive patterns I didn't yet know.

During the COVID-19 pandemic, over the summer of 2021 when we were staying mostly at home, I got the idea to write a sudoku solver, encoding the six deduction patterns I already knew about.  I teach college students to code in the Python programming language, which I learned mainly to teach it.  I decided to write the program in Python.  I figured writing a sudoku solver in Python would both help me become better at recognizing sudoku patterns -- making me a better human sudoku solver -- and would improve my Python skills.  Indeed it did both.  I wrote the program to modularize each rule, to allow me to specify which rules it would use to solve a soduku.  I decided NOT to include guessing and backtracking in the program, since as a human solver I don't use those.

About 350 lines of Python and a few weeks of debugging later, I had a program that surprised even me.  For readers familiar with AI jargon, the coded rules are essentially production rules: they look for a pattern in the grid cells and when they find it, they alter the grid accordingly, removing options from the appropriate cells.  With those six rules it can solve any sudoku the SF Chronicle publishes, including ones I hadn't solved.  If a deductive pattern is present in the sudoku grid and the corresponding rule has been turned ON for the puzzle, the program finds it.  Unlike me, it never misses any.  It applies its rules in repeated passes; harder sudokus require more passes.  The program is fast: solving even complicated sudokus in seconds.  Most of that time is spent outputting progress reports after each pass. 

I also grew interested in reading about sudoku: its history and rules.  I found a lot of information about sudoku online.  I learned the common names for the six patterns I already knew: naked single, hidden single, naked pair, naked triple, hidden n-ple, and locked single.  Visiting the many sudoku websites showed me that there are sudokus that are harder than the ones the SF Chronicle prints -- some MUCH harder.  I tried sudoku_solver with sudokus rated "very hard", "super hard", "expert", and "evil" and found that it solves many but not all.  After reading about "the world's hardest sudoku" developed by Finnish mathematician Arto Inkala, I fed it to my program and of course found that sudoku_solver can't solve it; with all rules active, it gets stuck on the second pass!  :-(

But hope springs eternal in the hearts of programmers.  Reading about sudoku also showed me that there are deductive patterns that are more sophisticated -- and harder to detect -- than the six I had already coded into sudoku_solver.  The best known three are X-wing, Swordfish, and Y-wing (aka XY-wing) [1, 2, 3].  Over the next several months, I added those three deductive rules to sudoku_solver.  There are more patterns, e.g., generalizations of those three, but for now I am leaving them for others to add.

After adding and debugging ~100 more lines of python, encoding pattern-rules for X-wing, Swordfish, and Y-wing, I tried sudoku_solver on the problems it previously could not solve.  Now it can solve problems requiring X-wing, Swordfish, Y-wing, or combinations of those.  However, there are still some "super hard" sudokus the program cannot solve.  E.g., when given Arto Inkala's "hardest sudoku", it still gets stuck on pass 2.  :-(

NOTE: While writing this Readme, I discovered articles indicating that in the late 2000s, Peter Norvig also wrote a sudoku solver in Python [4, 5].  I have not seen the code, but according to the articles it uses constraint propagation and guessing with backtracking.  I did not know about that program until today: April 5, 2022.  I don't know if that is fortunate or unfortunate.  Coincidentally, like me, Norvig got interested in sudoku after his wife did.

I am putting sudoku_solver.py on GitHub in the hopes that others will add more deductive rules and otherwise improve it.  (Please don't add guessing and backtracking, as that violates my idea of how sudokus should be solved.  If you want to go that route, fork-off your own development branch.)

Although some people consider puzzle solvers like sudoku_solver.py to be examples of artificial intelligence (AI), I do not.  We should not consider a puzzle-solving program to be "AI" simply because historically puzzle-solvers were classified as AI.  Sudoku_solver is no more intelligent than a program that calculates home mortgage payments or inverts matrices.  It uses simple search and compare methods to find static patterns that, via logic, allow digits to be eliminated from sudoku cells.


HOW TO USE SUDOKU_SOLVER

Run sudoku_solver like you would run any python program: download the sudoku.py, sudoku_solver.py, and sudoku.txt to your computer into a known directory, open a terminal, cd to the directory where the program is, and enter the command "python3 sudoku_solver.py".  Sudoku_solver reads the sudoku from the file sudoku.txt and solves it.

The program only reads -- and attempts to solve -- the top sudoku in the file.  It ignores everything after the first sudoku.  This allows the first sudoku to be followed by notes about it.  It also allows other sudokus (previously tested or to be tested) to be stored in sudoku.txt below the first sudoku.

The first line of the file indicates which of the eight rules to use, using the digits 0-8.  "0" means use rule 0 (naked single), "1" means use rule 1 (hidden single), "3" means use rule 3 (naked triple), etc.  (Note: if the program eventually has more than 10 rules, we'll have to use Hexidecimal symbols to indicate all the rules.)  The next 9 lines of the file specify the sudoku puzzle.  Each line specifies the initial contents of the nine cells in that row.  Known cells contain a single digit 0-9, unknown cells contain either spaces " ", hyphens "-", or underscores "_".  Any other character in the puzzle generates an error and causes the program to stop.  Here is an example of a puzzle:
Rules 012345678
----6-7--
4----58-3
--5--3-6-
-1---9---
--7-2-4--
---1---2-
-2-7--3--
1-35----9
--6-4----

When run, the program displays the rules it is using, then starts displaying the results of each pass at applying the selected rules.

If the program solves the puzzle, it reports that, and how many passes were required.

If the program gets stuck -- i.e., it can make no changes on a pass -- it stops and displays "Stuck!".

If the program encounters a sudoku error, such as an attempt to remove the last value from a cell, or two cells in a container with the same single number, it raises an exception and terminates.  That indicates that either:

1. the sudoku problem was entered incorrectly into sudoku.txt (most likely), or

2. there is a bug in the program.  Currently there are no known bugs in the program (Sudoku and Cell class definitions, main program, or deductive rules) and no sudoku errors have occurred for a long time.  However, if new deductive rules are added or other parts of the program are improved, new bugs could be introduced.


HOW SUDOKU_SOLVER WORKS

Sudoku_solver.py is implemented using a combination of object-oriented programming (OOP) and procedural programming.  It defines a Sudoku class and a Cell class.  The main program is mainly procedural but creates a Sudoku object (containing Cell objects) for each puzzle.  The deductive rules are also mainly procedural but operate on Sudoku and Cell objects.

The program starts by recording which rules are to be used on this run.  It then creates a 9x9 Sudoku grid, reads the data file, and fills in the cells of the grid.  Empty cells are initialized to a list of all possible digits [0-9].  Known cells are initialized to a list of one digit.

The main() function initializes the passes-count and other housekeeping variables and begins applying rules that are to be used on this run, from the most basic to the most complex.  Each rule looks for its deductive pattern.  Some rules apply to containers: rows, columns, or boxes, and so are applied row-by-row, column-by-column, or box-by-box.  Other rules apply to the entire grid.  If a rule finds its pattern, it removes the appropriate digits from the target cells.  If a rule removes options from any cell in the sudoku, it marks the sudoku as having been changed.

At the end of each pass through all specified rules, the current state of the sudoku is displayed, and the program checks to see if the sudoku is solved.  If so, it indicates that and quits.  If the sudoku has not been solved, the program checks if anything changed since the last pass.  If the last pass changed nothing, the program indicates that it is stuck; otherwise it proceeds to the next pass.


ADDITIONAL OBSERVATIONS

Sudoku_solver applies its deductive production rules -- those that have been turned ON for a given problem -- repeatedly in a series of passes.  One would expect harder sudokus to require more passes for the program to solve.

In testing sudoku_solver on many problems published in the SF Chronicle and on sudoku websites, I have found that if the rules the program is using are held constant, there is only a weak correlation between a problem's rated difficulty and the number of passes the program needs to solve it.  Higher-rated problems have slight tendency to require more passes.  However, with most of its rules engaged, sudoku_solver solves some problems rated 6 by the SF Chronicle in 2-3 passes while taking 5-6 to solve problems the Chronicle rates as 4 or 5.  The same is true of puzzles published on sudoku websites.

Users can select which rules the program will use for a given sudoku.  The only required rule is the most basic sudoku rule -- cells with only one digit in them rule out those options elsewhere in the same container (Rule O in sudoku_solver; aka Naked Single).  The remaining rules are optional.  One might expect that the more rules are made available to the program, the fewer passes it would need to solve sudokus.  Again, that is somewhat true (see below).

Rules 012
7---31-6-
---9-7-2-
----6-41-
-53---7--
----4----
--1---63-
-16-9----
-9-2-4---
-2-31---8
Hard (SF Chronicle 5, 6/16/2023)
• solved in 4 passes with R0+R1+R2+R3+R4+R5+R6+R7+R8
• solved in 4 passes with R0+R1+R2+R3+R4+R5+R6+R7
• solved in 4 passes with R0+R1+R2+R3+R4+R5+R6
• solved in 4 passes with R0+R1+R2+R3+R4+R5
• solved in 5 passes with R0+R1+R2+R3+R5
• solved in 6 passes with R0+R1+R2+R3+R4
• solved in 7 passes with R0+R1+R2+R3
• solved in 7 passes with R0+R1+R2
• solved in 8 passes with R0+R1

However, the correlation is weak.  The program solves some sudokus -- even some rated as hard -- in about the same number of passes even if restricted to only the simplest deductive rules.  For example, sudoku_solver solves the following sudoku, rated 5/6 (hard) by the SF Chronicle, in 5 passes with even with only its two most basic rules (see below):

Rules 012
7-2384---
--17-63--
-4-------
-2------3
-6--4--5-
3------1-
-------6-
--76-51--
---4382-5
Hard (SF Chronicle 5, 5/6/2022)
• solved in 3 passes with R0+R1+R2+R3+R4+R5+R6+R7+R8
• solved in 3 passes with R0+R1+R2+R3+R4+R5+R6+R7
• solved in 3 passes with R0+R1+R2+R3+R4+R5+R6
* solved in 4 passes with R0+R1+R2+R3+R4+R5
• solved in 4 passes with R0+R1+R2+R3+R4
• solved in 5 passes with R0+R1+R2+R3
• solved in 5 passes with R0+R1+R2
• solved in 5 passes with R0+R1
• solved in 10 passes with R0+R2
• cannot solve with only R0

The number of passes required to solve sudokus also correlates poorly with how hard the sudokus are for people to solve.  Some problems my wife and I find difficult to solve, the program solves in few passes, with only a few basic rules.  This suggests that difficulty ratings for published sudoku problems are based not only on the number or complexity of the rules required, but also how hard it is for people to detect the deductive patterns.  A given deductive pattern may be easier for human solvers to find in some puzzles than in others.  That isn't true for the program: if a pattern is present, the program finds it.

There is one perplexing observation regarding the relationship between which rules are active and the number of required passes.  For a few sudokus rated as very difficult, activating one of the three most complex pattern rules -- X-wing, Swordfish, or Y-Wing -- can actually increase the number of passes required.  This seems counterintuitive because no rule adds options to any cell; they all only remove options.  How can applying a rule increase the required number of passes?  The deductive rules vary in how many options they eliminate from cells.  It seems that a low-yield rule (i.e. a rule that when applied removes only one or two options from the cells it affects), if applied in an early pass, can eliminate options that would be part of another pattern that would eliminate more options.  Removing the low-yield rule allows the higher-yield rule to find its pattern, eliminating more options.

Sometimes a deductive rule triggers with no effect: any options it could eliminate are already gone.  Sudoku_solver announces when it finds X-wing, Y-wing, or Swordfish patterns (assuming those rules are turned ON), but much of the time, those rules are "duds".  For example, if an X-wing or Swordfish pattern is detected in the rows and reduces options in the corresponding columns, the same X-wing or Swordfish will be detected in the columns, but will have no effect because by definition the X-wing or Swordfish found in the rows has no relevant options to eliminate.  The same is true of Y-wing patterns.

Therefore, sudoku_solver contains inefficiencies: it spends time looking for patterns that can have no effect on the state of the puzzle.  However, since it solves puzzles (or gets stuck) in seconds or fractions thereof, there isn't much impetus to eliminate its inefficiencies.
 

References

1. Sudoku Essentials (undated), "How to Identify Sudoku X-Wing Pattern", https://sudokuessentials.com/x-wing/

2. Anthony, Simon (July 1, 2018), Cracking the Cryptic, YouTube video: https://www.youtube.com/watch?v=PpHOknAnh4g

3. Sudoku Essentials (undated), "Sudoku XY-Wing Solves Difficult Puzzles", https://sudokuessentials.com/Sudoku-XY-Wing/

4. Vermeer, Lucas (January 29, 2010), "Solving Every Sudoku Puzzle Faster", https://www.lukasvermeer.nl/publications/2011/01/29/solving-every-sudoku-puzzle-faster.html

5. Norvig, Peter (C. 2008?), "Solving Every Sudoku Puzzle", http://norvig.com/sudoku.html


===CANNOT SOLVE!!!======

Rules 012345678
-------7-
--48-----
1-946--3-
4---1----
-5--2----
-1-3-64--
-------98
5-----6-7
2--1-----
Very hard (Sudoku.com "expert")
• Cannot solve with R0+R1+R2+R3+R4+R5+R6+R7+R8

Rules 012345678
9-4-6--8-
8---1---2
1--9---7-
4-----5--
-16------
7---31---
-3---7-9-
6--2-4---
---------
Super hard (Sudoku.com "expert")
• Cannot solve with R0+R1+R2+R3+R4+R5+R6+R7+R8

Rules 012345678
--53-----
8------2-
-7--1-5--
4----53--
-1--7---6
--32---8-
-6-5----9
--4----3-
-----97--
World's hardest (by Arto Inkala)
• Cannot solve with R0+R1+R2+R3+R4+R5+R6+R7+R8

=====END CANNOT SOLVE=======
