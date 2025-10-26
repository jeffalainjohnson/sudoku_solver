from itertools import combinations
from sudoku import Sudoku, Cell  # import Sudoku and Cell classes


### Sudoku Logic Rules -- operate on containers (row/col/box)

# Logic Rule 0: Naked single - Settled cells eliminate those options elsewhere in container (row/col/box)
def logic_rule_0(s, container):
	settled = [cell.get_possible()[0] for cell in container if cell.number_of_options() == 1] # Get numbers for settled cells
	for j in range(9):	# delete known numbers as possibilities in other cells of container
		before = container[j].number_of_options()
		if before != 1:
			container[j].remove_possible(settled)
			if before > container[j].number_of_options():	# did we actually remove any options?
				s.set_changed()		# yes; flag that we made a change

# Logic Rule 1: Hidden single - Numbers confined to only one cell in container (row/col/box) can be settled
def logic_rule_1(s, container):
	tally_d = make_tally_d(container)
	for n in tally_d:
		if len(tally_d[n]) == 1:	#if n is possible in only 1 cell
			if container[tally_d[n][0]].number_of_options() != 1: # and cell isn't settled, set to n
				container[tally_d[n][0]].set_possible([n])
				s.set_changed()		# flag that we made a change
				
# Logic Rule 2: Naked pair -- Two cells with same 2 options eliminate those options elsewhere in container
def logic_rule_2(s, container):
	pair_list = [cell.get_possible() for cell in container if cell.number_of_options() == 2]
	dup_pairs = set([tuple(pair) for pair in pair_list if pair_list.count(pair) == 2])
	while len(dup_pairs) > 0:
		pair = list(dup_pairs.pop())
		for cell in container:
			cell_possible = cell.get_possible()
			if cell_possible != pair and (pair[0] in cell_possible or pair[1] in cell_possible):
				cell.remove_possible(pair)
				s.set_changed()		# flag that we made a change

# Logic Rule 3: Naked triple -- Three cells with same 3 options eliminate those options elsewhere in container
def logic_rule_3(s, container):
	trio_list = [cell.get_possible() for cell in container if cell.number_of_options() == 3]
	dup_trios = set([tuple(trio) for trio in trio_list if trio_list.count(trio) == 3])
	while len(dup_trios) > 0:
		trio = list(dup_trios.pop())
		for cell in container:
			cell_possible = cell.get_possible()
			if cell_possible != trio and (trio[0] in cell_possible or trio[1] in cell_possible or trio[2] in cell_possible):
				cell.remove_possible(trio)
				s.set_changed()		# flag that we made a change

# Logic Rule 4: Hidden n-ples -- If N numbers are confined to N cells in a container, other options in those cells
#				(not so confined) can be eliminated
def logic_rule_4(s, container):
	group_name_d = {2: "pair", 3:"trio", 4:"quartet", 5:"quintet", 6:"sextet", 7:"septet"}
	for N in range(2,8):
		l = list(combinations([1,2,3,4,5,6,7,8,9],N))	# Make list of all combos of 1-9 taken N at a time
		combos_d = {}									# Create blank dictionary
		for t in l:										# Load dictionary with empty list for each combo
			combos_d[t] = []
		for combo in combos_d:							# For each combo, record all cells with possible
			for i in range(9):								# ... values matching any numbers in combo
				if set(combo) & set(container[i].get_possible()): # Non-empty set?  
					combos_d[combo].append(i)				# Number in combo is in cell.  Add cell index to combo's list.
		for combo in combos_d:							# Check each combo in dictionary
			if len(combos_d[combo]) == N:					# Are combo's numbers found in only N cells in container?
				cell_index_list = combos_d[combo]			# Yes.  Check if cells also have numbers not in combo.
				nested_possibles = [container[cell].get_possible() for cell in cell_index_list]	# All cells' possible lists
				flat_possibles = []						# Start with null list
				for sublist in nested_possibles:		# Flatten nested list of possible #s for the N cells
					flat_possibles += sublist
				if set(combo) < set(flat_possibles):		# Does possible set include numbers not in combo?
					if [flat_possibles.count(n) for n in combo if flat_possibles.count(n) < 2]: # Yes. If any of combo's...
						continue						# ... numbers not in at least 2 of N cells, skip this combo
				else:
					continue 							# Possibles include no options not in combo; skip this combo
				# If we get here, this combo passed all the tests
				for cell_index in cell_index_list:		# Remove extra options from those cells.
					old_possible = container[cell_index].get_possible()
					diff = set(old_possible).difference(set(combo))
					if diff:
						container[cell_index].remove_possible(diff)
						s.set_changed()		# flag that we made a change

# Logic Rule 5rc: Single locked in row/col -- If a number in a row or col is confined to a single box,
#				that number can be eliminated elsewhere in the box (AKA pointing pairs & triples)
def logic_rule_5rc(s, row_or_col, boxes):
	tally_d = make_tally_d(row_or_col)	# collect indices in container of cells for which each number is possible
	for n in tally_d:			# check each number 1-9 to see what cells it is possible in
		i_list = tally_d[n]		# get cell-index list for this number
		if len(i_list) > 1: 	# skip settled numbers
			cell_list = [row_or_col[i] for i in i_list]	# get list of cells from indices
			box_index_list = [cell.get_box() for cell in cell_list]	# get list of all boxes the cells are in
			if len(set(box_index_list)) == 1:	# if all the cells are in the same box...
				eliminate_elsewhere_in_container(s, n, cell_list, boxes[box_index_list[0]]) #cut options elsewhere in box

# Logic Rule 5b: Single locked in box -- If a number in a box is confined to a single row or col,
#				that number can be eliminated elsewhere in the row or column (AKA pointing pairs & triples)
def logic_rule_5b(s, box, rows, cols):
	tally_d = make_tally_d(box)	# collect indices in container of cells for which each number is possible
	for n in tally_d:			# check each number 1-9 to see what cells it is possible in
		i_list = tally_d[n]		# get cell-index list for this number
		if len(i_list) > 1: 	# skip settled numbers
			cell_list = [box[i] for i in i_list]	# get list of cells from indices
			row_index_list = [cell.get_row() for cell in cell_list]	# get list of all rows the cells are in
			if len(set(row_index_list)) == 1:	# if all the cells are in the same row...
				eliminate_elsewhere_in_container(s, n, cell_list, rows[row_index_list[0]]) # cut options elsewhere in row
			col_index_list = [cell.get_col() for cell in cell_list] # get list of cols the cells are in
			if len(set(col_index_list)) == 1:	# if all the cells are in the same col...
				eliminate_elsewhere_in_container(s, n, cell_list, cols[col_index_list[0]]) # cut options elsewhere in col

# Logic Rule 6: X-wing -- if 2 rows have the same number possible in only the same 2 cols (i.e., they are a conjugate pair) 
#				delete that number from other cells of those cols (replace "row" with "col" and vice-versa to apply to cols)
def logic_rule_6(s, rows, cols, direction):		# direction parameter used only to select debugging printout
	tally_d_list = [make_tally_d(row) for row in rows]  #make a tally_d_list for every row
	tally_d_list_pairs = [{},{},{},{},{},{},{},{},{}]   #create list of empty sets for recording conjugate pairs
	for i in range(9):
		for n in tally_d_list[i]:
			if len(tally_d_list[i][n]) == 2:	# Find all numbers that occur exactly 2x in row (conjugate pairs)
				tally_d_list_pairs[i][n] = tally_d_list[i][n]
	for i in range(8):						#Check list of row-dictionaries, looking for X-wing. Impossible after 2nd-to-last row.
		for n in tally_d_list_pairs[i]:		# find digits that occur in same 2 cols of 2 different rows
			for j in range(i+1, 9):			# does n occur in same 2 cols in a later row?
				if n in tally_d_list_pairs[j] and tally_d_list_pairs[j][n] == tally_d_list_pairs[i][n]:
					print("Found X-wing!")
					if direction == 'r':
						print("{} is in cols {} and {} of rows {} and {}".format(n, tally_d_list_pairs[i][n][0], tally_d_list_pairs[i][n][1], i, j))
					else:
						print("{} is in rows {} and {} of cols {} and {}".format(n, tally_d_list_pairs[i][n][0], tally_d_list_pairs[i][n][1], i, j))
					#Delete the candidate digit from other cells in the two cols
					col_l = cols[tally_d_list_pairs[j][n][0]]	# Left col (or upper row)
					cell_list_l = [col_l[i], col_l[j]]
					eliminate_elsewhere_in_container(s, n, cell_list_l, col_l) # cut n elsewhere in left col
					col_r = cols[tally_d_list_pairs[i][n][1]]	# Right col (or lower row)
					cell_list_r = [col_r[i], col_r[j]]
					eliminate_elsewhere_in_container(s, n, cell_list_r, col_r) # cut n elsewhere in right col

# Logic Rule 7: Swordfish -- if 3 rows have the same number possible in only the SAME 2 or 3 cols, delete that
#				number from other cells of those cols (replace "row" with "col" and vice-versa to apply to cols)
def logic_rule_7(s, rows, cols, direction):		# direction parameter used only to select debugging printout
	tally_d_list = [make_tally_d(row) for row in rows]
	tally_d_list_pairs_and_trios = [{},{},{},{},{},{},{},{},{}]
	for i in range(9):
		for n in tally_d_list[i]:
			times_in_row = len(tally_d_list[i][n])
			if times_in_row == 2 or times_in_row == 3:	# Record numbers that occur 2x or 3x in row
				tally_d_list_pairs_and_trios[i][n] = tally_d_list[i][n]
	for i in range(7):			# Check list of row-dictionaries, looking for swordfish. Impossible after 3rd-to-last row.
		for n in tally_d_list_pairs_and_trios[i]:		# find numbers that occur in same 2 or 3 cols of 3 different rows
			for j in range(i+1, 8):			# does n occur in same 2 or 3 cols in a later row?
				if n in tally_d_list_pairs_and_trios[j] and len(set(tally_d_list_pairs_and_trios[j][n]) & set(tally_d_list_pairs_and_trios[i][n])) >= 1:
					for k in range(j+1, 9):
						if n in tally_d_list_pairs_and_trios[k] and len(set(tally_d_list_pairs_and_trios[k][n]) & set(tally_d_list_pairs_and_trios[j][n])) >= 1:
							col_list = list(set(tally_d_list_pairs_and_trios[k][n]) | set(tally_d_list_pairs_and_trios[j][n]) | set(tally_d_list_pairs_and_trios[i][n]))
							if len(col_list) == 3:
								print("Found swordfish!")
								if direction == 'r':
									print("{} is in cols {} of rows {}, {}, and {}".format(n, col_list, i, j, k))
								else:
									print("{} is in rows {} of cols {}, {}, and {}".format(n, col_list, i, j, k))
								#Delete the candidate digit from other cells in the three cols
								col_l = cols[col_list[0]]	# Left col (or top row)
								cell_list_l = [col_l[i], col_l[j], col_l[k]]
								eliminate_elsewhere_in_container(s, n, cell_list_l, col_l) # cut n elsewhere in left col (top row)
								col_m = cols[col_list[1]]	# Middle col (or middle row)
								cell_list_m = [col_m[i], col_m[j], col_m[k]]
								eliminate_elsewhere_in_container(s, n, cell_list_m, col_m) # cut n elsewhere in middle col (middle row)
								col_r = cols[col_list[2]]	# Right col (or bottom row)
								cell_list_r = [col_r[i], col_r[j], col_r[k]]
								eliminate_elsewhere_in_container(s, n, cell_list_r, col_r) # cut n elsewhere in right col (bottom row)

# Logic Rule 8: Y-wing -- if 3 cells (A, B, C) contain only 2 numbers each, and cell A contains XY and sees
#				cells B and C, and cells B and C contain XZ and YZ and don't see each other, then Z can be
#				eliminated from any other cell that sees both cells B and C.
def logic_rule_8(s):
	rows = s.get_rows()
	cols = s.get_cols()
	boxes = s.get_boxes()
	pair_cells = []
	for row in rows:
		pair_cells.extend([cell for cell in row if cell.number_of_options() == 2])
	for cell in pair_cells: # search cell's containers for pair-cells sharing 1 of its 2 options
		if cell.number_of_options() != 2:	# Needed because pair-cells may lose options during this loop
			continue
		possible_wing_cells = [c for c in pair_cells if cell.sees(c) and len(c.get_possible()) == 2 and len(set(cell.get_possible()) & set(c.get_possible())) == 1]
		# search possible_wing_cells for two that don't see each other, and one has x, one has y, and they both have z
		# if only two possible wing cells, check if they see each other, and if not, if one has x, the other has y
		for i in range(len(possible_wing_cells)):
			for j in range(i+1, len(possible_wing_cells)):
				if len(set(cell.get_possible()) | set(possible_wing_cells[i].get_possible()) | set(possible_wing_cells[j].get_possible())) == 3:
					if not possible_wing_cells[i].sees(possible_wing_cells[j]) and possible_wing_cells[i].get_possible() != possible_wing_cells[j].get_possible():
						print("Found Y-wing!")
						print("  Wing cells: ", possible_wing_cells[i], possible_wing_cells[j])
						z = list(set(possible_wing_cells[i].get_possible()) & set(possible_wing_cells[j].get_possible()))
						print("z =", z[0])
						# Get list of cells both wing-cells can affect.
						# List cells that each wing-cell can see, convert to sets and take intersection.
						possible_affected_cells = list(can_see(s, possible_wing_cells[i]) & can_see(s, possible_wing_cells[j]))
						affected_cells = [c for c in possible_affected_cells if c.number_of_options() > 1 and c.is_possible(z[0])]
						if affected_cells:
							for c in affected_cells:
								print("  Affected cell before:", c, end = " ")
								c.remove_possible(z)
								s.set_changed()		# note that we made a change
								print("  After:", c)
						else:
							print("  No affected cells.")

# Logic Rule 9: Skyscraper -- Find two columns (or rows) that contain a conjugate pair of the same digit as candidates.
#				If two of those candidate digits are in the same row (or column), they form the "base" of the skyscraper
#				and the other two occurances of the candidate digits are in the "roof" cells of the skyscraper.  At least
#				one of the two roof cells will be the candidate digit, so that digit can be eliminated in any other cell 
#				that sees both roof cells.
def logic_rule_9(s, cols, rows, direction):
	boxes = s.get_boxes()
	tally_d_list = [make_tally_d(col) for col in cols]  #make a tally_d_list for every col
	tally_d_list_pairs = [{},{},{},{},{},{},{},{},{}]   #create list of empty sets for recording conjugate pairs
	for i in range(9):
		for n in tally_d_list[i]:
			if len(tally_d_list[i][n]) == 2:	# Find all numbers that occur exactly 2x in col (conjugate pairs)
				tally_d_list_pairs[i][n] = tally_d_list[i][n]
	for i in range(8):						#Check list of col-dictionaries, looking for skyscraper. Impossible after 2nd-to-last col.
		for n in tally_d_list_pairs[i]:		# find conjugate pairs of same digit in two cols that share one row
			for j in range(i+1, 9):			# look for second col containing same conjugate pair sharing only 1 row
				if n in tally_d_list_pairs[j]:
					conjugatepair1 = tally_d_list_pairs[i][n]
					conjugatepair2 = tally_d_list_pairs[j][n]
					intersection = set(conjugatepair1) & set(conjugatepair2)
					if len(intersection) == 1:
						print("Found possible skyscraper", end=" ")
						base = intersection.pop()
						if direction == 'c':
							print("in cols")
							col_i_cells = [s.get_cell(conjugatepair1[0], i), s.get_cell(conjugatepair1[1], i)]
							col_j_cells = [s.get_cell(conjugatepair2[0], j), s.get_cell(conjugatepair2[1], j)]
							all_four_cells = col_i_cells + col_j_cells
							print("  Skyscraper digit:", n)
							base_cells = [s.get_cell(base, i), s.get_cell(base, j)]
							print("  Base cells:", base_cells[0], base_cells[1])
							roof_cells = [c for c in all_four_cells if c not in base_cells]
							print("  Roof cells:", roof_cells[0], roof_cells[1])
						else:
							print("in rows.")
							row_i_cells = [s.get_cell(i, conjugatepair1[0]), s.get_cell(i, conjugatepair1[1])]
							row_j_cells = [s.get_cell(j, conjugatepair2[0]), s.get_cell(j, conjugatepair2[1])]
							all_four_cells = row_i_cells + row_j_cells
							print("  Skyscraper digit:", n)
							base_cells = [s.get_cell(i, base), s.get_cell(j, base)]
							print("  Base cells:", base_cells[0], base_cells[1])
							roof_cells = [c for c in all_four_cells if c not in base_cells]
							print("  Roof cells:", roof_cells[0], roof_cells[1])
						#Delete candidate digit from cells that see both roof cells
						# List cells that each roof-cell can see, convert to sets and take intersection.
						possible_affected_cells = list((can_see(s, roof_cells[0]) & can_see(s, roof_cells[1])) - set(roof_cells))
						affected_cells = [c for c in possible_affected_cells if c.number_of_options() > 1 and c.is_possible(n)]
						if affected_cells != []:
							if roof_cells[0].sees(roof_cells[1]):
								print("###Roof cells in same box.")
							for c in affected_cells:
								print("**Affected cell before:", c, end = " ")
								print("  Removing digit {}.".format(n))
								c.remove_possible([n])
								s.set_changed()		# note that we made a change
								print("  After:", c)
						else:
							print("  No affected cells.")

### Utility functions

def eliminate_elsewhere_in_container(s, n, save_cell_list, container):
	for cell in container:
		if cell not in save_cell_list and n in cell.get_possible():	#delete n from unsettled cells in which n is an option
			cell.remove_possible([n])	#cut n only from other cells in container
			s.set_changed()		# note that we made a change

def make_tally_d(container):
	d = {1:[],2:[],3:[],4:[],5:[],6:[],7:[],8:[],9:[]}  # initialize dictionary of digits as keys
	for j in range(9):	# collect indices in container of cells for which each number is possible
		cell_options = container[j].get_possible()
		for k in range(len(cell_options)):
			d[cell_options[k]].append(j)
	return d

def can_see(s, cell):	#Returns set of all cells this cell can see. Probably should be a sudoku method
	return set(s.get_rows()[cell.get_row()]) | set(s.get_cols()[cell.get_col()]) | set(s.get_boxes()[cell.get_box()])


### Main driver

def main():

	# Open data file
	ifile = open("sudoku.txt", "r")

	rules_to_use = ifile.readline() # first line of file is logic rules (0-9) to use
	print("Solving sudoku using", rules_to_use)

	s = Sudoku(ifile)		# initialize Sudoku from data file

	ifile.close()	# close data file 

	passes = 0
	keep_going = True
	while keep_going:	# Apply heuristics repeatedly until sudoku solved or stuck

		passes += 1
		s.clear_changed()			# Clear change-flag for this pass
		print("Pass", passes)

# On each cycle, invoke whichever of these Sudoku Deduction Patterns is allowed for this run
		if "0" in rules_to_use:			# Apply Logic Rule 0?  (Naked Single)
			for i in range(9):
				logic_rule_0(s, s.rows[i])	#These should probably be s.get_rows()[i]
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_0(s, s.cols[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_0(s, s.boxes[i])
		
		if "1" in rules_to_use:			# Apply Logic Rule 1? (Hidden Single)
			for i in range(9):
				logic_rule_1(s, s.rows[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_1(s, s.cols[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_1(s, s.boxes[i])
		
		if "2" in rules_to_use:			# Apply Logic Rule 2? (Naked Pair)
			for i in range(9):
				logic_rule_2(s, s.rows[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_2(s, s.cols[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_2(s, s.boxes[i])

		if "3" in rules_to_use:			# Apply Logic Rule 3? (Naked Triple)
			for i in range(9):
				logic_rule_3(s, s.rows[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_3(s, s.cols[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_3(s, s.boxes[i])

		if "4" in rules_to_use:			# Apply Logic Rule 4? (Hidden N-ple)
			for i in range(9):
				logic_rule_4(s, s.rows[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_4(s, s.cols[i])
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_4(s, s.boxes[i])

		if "5" in rules_to_use:  		# Apply Logic Rule 5? (Locked Single)
			for i in range(9):
				logic_rule_5rc(s, s.rows[i], s.boxes)
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_5rc(s, s.cols[i], s.boxes) 
			for i in range(9):			# comment out to interleave applying rules to rows, cols, boxes
				logic_rule_5b(s, s.boxes[i], s.rows, s.cols)

		if "6" in rules_to_use and passes > 1:  	# Apply Logic Rule 6? (X-wing)
			logic_rule_6(s, s.rows, s.cols, 'r')	# Look for X-wings in rows
			logic_rule_6(s, s.cols, s.rows, 'c')	# Look for X-wings in columns

		if "7" in rules_to_use and passes > 1:			# Apply Logic Rule 7? (Swordfish)
			logic_rule_7(s, s.rows, s.cols, 'r')	# Look for Swordfish in rows
			logic_rule_7(s, s.cols, s.rows, 'c')	# Look for Swordfish in columns

		if "8" in rules_to_use and passes > 1:			# Apply Logic Rule 8? (Y-wing)
			logic_rule_8(s)

		if "9" in rules_to_use and passes > 1:  		# Apply Logic Rule 9? (skyscraper)
			logic_rule_9(s, s.cols, s.rows, 'c')	# Look for skyscraper in columns
			logic_rule_9(s, s.rows, s.cols, 'r')	# Look for skyscraper in rows

		s.print_sudoku(s.rows)

		if s.is_solved():
			print("Solved in", passes, "passes.")
			keep_going = False
		elif not s.is_changed():
			print("Stuck on pass", passes)
			keep_going = False
		else:
			continue

main()

