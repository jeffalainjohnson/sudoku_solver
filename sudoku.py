class Sudoku:

	def __init__(self, ifile):
		# Initialize sudoku with all numbers possible in all cells
		self.rows = [[],[],[],[],[],[],[],[],[]]	# List of rows; each is a list of Cells
		self.cols = [[],[],[],[],[],[],[],[],[]]	# list of cols; each is a list of Cells
		self.boxes = [[],[],[],[],[],[],[],[],[]]	# List of boxes; each is a list of Cells
		self.__changed = False
		
		for i in range(9):
			line = ifile.readline()

			for j in range(9):
				c = line[j]
				if c in "-_ ":						# empty Cells are marked with '-', '_', or ' '
					this_cell = Cell([1,2,3,4,5,6,7,8,9])	# empty Cells start with all numbers possible
				elif c in "123456789":
					this_cell = Cell([int(c)])		# known Cells start with single value
				else:
					raise Exception ("Invalid character {} in input.".format(c))

				this_cell.set_row(i)
				this_cell.set_col(j)

				self.rows[i].append(this_cell)
				self.cols[j].append(this_cell)
				self.boxes[this_cell.get_box()].append(this_cell)

	def get_rows(self):
		return self.rows

	def get_cols(self):
		return self.cols

	def get_boxes(self):
		return self.boxes

	def clear_changed(self):
		self.__changed = False

	def set_changed(self):
		self.__changed = True

	def is_changed(self):
		return self.__changed

	def is_solved(self):
		for i in range(9):
			for j in range(9):
				if self.rows[i][j].number_of_options() > 1:
					return False
		return True

	def print_sudoku(self, container_type):
		print("-----------------------------")
		for i in range(9):
			for j in range(9):
				print(container_type[i][j], end="")
				if (j + 1) % 3 == 0 and j < 8:
					print("|", end="")
			print()
			if (i + 1) % 3 == 0:
				print("-----------------------------")
		print()


class Cell:
    
	def __init__(self, possible):
		self.__possible = possible
		self.__row_num = 0
		self.__col_num = 0

	def __str__(self):
		return str(self.__possible)
#		return str("{}: ({},{})".format(self.__possible, self.__row_num, self.__col_num))

	def get_possible(self):
		return self.__possible

	def set_possible(self, new_possible):
		if len(new_possible) == 0:
			print("!!! Attempt to set options to nothing!!!")	
			raise Exception ("Houston, we have a problem!")
		else:
			self.__possible = new_possible

	def remove_possible(self, l):
		if self.number_of_options() == 1 and self.__possible[0] in l:
			print("!!! Attempt to remove last option!!!")
			print("Possible numbers:", self.__possible, "numbers to remove:", l)
			raise Exception ("Houston, we have a problem!")
		elif set(self.__possible) <= set(l):
			print("!!! Attempt to remove all options!!!")
			print("Possible numbers:", self.__possible, "numbers to remove:", l)
			raise Exception ("Houston, we have a problem!")
		else:
			self.__possible = [n for n in self.__possible if n not in l]

	def is_possible(self, n):
		return n in self.__possible

	def number_of_options(self):
		return len(self.__possible)

	def set_row(self, row_num):
		self.__row_num = row_num

	def set_col(self, col_num):
		self.__col_num = col_num

	def get_row(self):
		return self.__row_num

	def get_col(self):
		return self.__col_num

	def get_box(self):
		return self.__row_num//3 * 3 + self.__col_num//3

	def get_box_cell_index(self):								# not currently used
		return (self.__row_num % 3) * 3 + (self.__col_num % 3)

	def share_container(self, other_cell):
		return self.get_row() == other_cell.get_row() or self.get_col() == other_cell.get_col() or self.get_box() == other_cell.get_box()
