import math

#some cchange

class Field(object):
	def __init__(self,number=0):
		self.number = number
		if number == 0:
			self.set = False
		else:
			self.set = True
            
	def setNumber(self, number):
		if number > 0 and number < 10 and not self.set:
			self.number = number
			#self.set = True
		else:
			print "Number has to be between 1 and 9 or Number has been set already"
			
	def getNumber(self):
		return self.number
		
	def delNumber(self):
		self.number = 0
		
	def __str__(self):
		return str(self.number)
		
	def __unicode__(self):
		return str(self.number)

class SudokuPart(list):
	def __init__(self,felder=None):
		self.felder = felder
		
		self.numbers = []
		self.first_third = []
		self.second_third = []
		self.third_third = []
		
		self.create_list()
		
		self.numbers_set = []
		self.numbers_free = []
		self.determine_used_numbers()
	
	def create_list(self):
		for feld in self.felder:
			self.numbers.append(feld.getNumber())
			
			#da die Block-Klasse auch eine Liste ist, werden ihr alle Felder
			#angehaengt
			self.append(feld)
		
		self.first_third = self.numbers[0:3]
		self.second_third = self.numbers[3:6]
		self.third_third = self.numbers[6:9]
		
		self.parts = {"first_third":self.first_third,
			"second_third":self.second_third,"third_third":self.third_third}
			
	def show_numbers(self):
		for feld in self.felder:
			print feld.getNumber(),
	
	#diese methode wird bei der initialisierung aufgerufen und zu determinieren,
	#welche nummern schon gesetzt sind und welche noch fehlen
	def determine_used_numbers(self):
	    for i in range(1,10):   
	        if i in self.numbers:
	            self.numbers_set.append(i)
	        else:
	            self.numbers_free.append(i)
	
	#sollten nummern dazugekommen sein, wird so sichergestellt das auch die
	#listen in denen man die nummern einfach sehen kann auf dem jeweils aktuellsten 
	#stand sind
	def refresh(self):
		self.numbers = []
		del self[0:9]
	    
		self.numbers_set = []
		self.numbers_free = []
	    
		self.create_list()
		self.determine_used_numbers()
		
class Block(SudokuPart):
		
	def show_numbers(self):
		for i in range(len(self.felder)):
			if i % 3 == 0:
				print ""
			print self.felder[i].getNumber(),		

class vLine(SudokuPart):
	pass
			
class hLine(SudokuPart):
	pass

class Sudoku(object):
	def __init__(self,file="sudoku1.txt"):
		self.solver = SudokuSolver(self)
        
		self.spielfeld = []
		self.load_fields(file)
		
		self.block = []
		self.create_blocks()
		
		self.vLine = []
		self.create_vLines()
		
		self.hLine = []
		self.create_hLines()
		
		self.parts = [self.block,self.vLine,self.hLine]
		
	def load_fields(self,file=None):
		f = open(file,"r")
		
		self.name = f.readline()
		lines = f.readlines()
		
		f.close()
		
		for line in lines:
			for number in [int(x) for x in line.split(',')]:
				self.spielfeld.append(Field(number))
	
	# ein sudoku spielfeld besteht aus 9 3*3 bloecken. die zahlen der bloecke werden zuerst
	# in listen gespeichert und dann den block-klassen uebergeben
	def create_blocks(self):
		blocks = [[],[],[],[],[],[],[],[],[]]
		
		feld = 0
		start = 0
		for block in range(9):
			
			for number in range(1,10):
				blocks[block].append(self.spielfeld[feld])
				
				if number % 3 == 0:
					feld += 7
				else:
					feld += 1
					
			start += 3
			
			if start == 9:
				start *= 3
				
			if start == 36:
				start = 54
				
			feld = start
				
		for b in blocks:
			self.block.append(Block(b))
			
	def create_vLines(self):
		vLines = [[],[],[],[],[],[],[],[],[]]
		
		line = 0
		for feld in range(1,82):
			
			vLines[line].append(self.spielfeld[feld-1])
			
			if feld % 9 == 0:
				line += 1
			
		for v in vLines:
			self.vLine.append(vLine(v))
			
	def create_hLines(self):
		hLines = [[],[],[],[],[],[],[],[],[]]
		
		for i in range(9):
			for j in range(9):
				hLines[i].append(self.spielfeld[i+j*9])

		for h in hLines:
			self.hLine.append(hLine(h))
			
	def print_blocks(self):
		for block in self.block:
			block.show_numbers()
			print ""
			
	def print_vLines(self,von=1,nach=9):
	    i = von - 1
	    j = nach - 1
	    
	    while i <= j:
	        self.vLine[i].show_numbers()
	        print ""
	        i += 1
	        
	def print_hLines(self,von=1,nach=9):
	
	    i = von - 1
	    j = nach - 1
	    
	    while i <= j:
	        self.hLine[i].show_numbers()
	        print ""
	        i += 1
			
	def print_all(self):
		print "***   Vertical Lines   ***"
		self.print_vLines()
		
		print ""
		
		print "***   Horizontal Lines   ***"
		self.print_hLines()
		
		print ""
		
		print "***   Blocks   ***"
		self.print_blocks()
		
	def use_solve_one_left(self):
	    self.solver.solve_one_left()
	    
	def use_search_rows(self):
	    self.solver.search_rows()
	
	def use_sweep_rows(self):
	    self.solver.sweep_rows()

class SudokuSolver(object):
    
	def __init__(self,sudoku):
		self.sudoku = sudoku
    #
    #ueberprueft alle bloecke, vLinien und hLinien darauf, ob nur noch 1 zahl
    #nicht ausgefuellt wurde und fuellt diese ein
    #der parameter lists erwartet eine liste in der alle bloecke vlinien und hlinien
    #enthalten sind [self.block,self.v_Line,h_Line]
	def solve_one_left(self,rounds=1):
		for round in range(rounds):
			for list in self.sudoku.parts:
				for i in range(9):
					list[i].refresh()
					
					if len(list[i].numbers_free) == 1:
						index_of_number = list[i].numbers.index(0)
						number = list[i].numbers_free[0]
						list[i][index_of_number].setNumber(number)
						list[i].refresh()
	
	#
	#diese methode untersucht jeweils 3 zeilen, zeile 1-3,4-6 und 7-9. ist
	#in 2 von diesen 3 reihen dieselbe zahl, wird versucht die zahl in der noch
	#fehlenden reihe einzusetzen
	def search_rows(self,rounds=1):
		for round in range(rounds):
			for number in range(1,10):
				zahlen_count = 0
				for row in range(9):
					if row % 3 == 0:
					    reihen = [row,row+1,row+2]
					    blocks = [row,row+1,row+2]
	                
					if number in self.sudoku.vLine[row].numbers:
						reihen.remove(row)
						zahlen_count += 1
						
					if number in self.sudoku.block[row].numbers:
						blocks.remove(row)
						
					if row in [2,5,8]:
						if zahlen_count == 2:
							reihe = reihen[0]
							block = blocks[0]
							#print "Zahl " + str(number) + " muss in Reihe " + str(reihen[0] + 1) + " Block " + str(blocks[0] + 1)
							self._search_rows_find_number(number,reihe,block)
							zahlen_count = 0
						else:
							zahlen_count = 0
	
	#
	#nachdem die search_rows methode herausgefunden hat, in welcher zeile und welchem
	#block eine gewisse nummer hinkommt, soll diese methode den genauen platz herausfinden
	#und die zahl einsetzen. und damit die search_rows methode nicht zu lang und unueber-
	#sichtlich wird, werden die angesprochenen funktionienen in diese methode verlagert
	def _search_rows_find_number(self,number,row,block):
	    
		if block in [0,1,2]:
			part = "first_third"
		
		if block in [3,4,5]:
			part = "second_third"
		
		if block in [6,7,8]:
			part = "third_third"
			
		if block in [0,3,6]:
		    cols = [0,1,2]

		if block in [1,4,7]:
		    cols = [3,4,5]

		if block in [2,5,8]:
		    cols = [6,7,8]
		
		possible_cols = cols
		
		#ist der teil  der hlinie im block voll, kann die nummer nicht dort
		#eingetragen werden
		for col in cols:
			if self.sudoku.hLine[col].parts[part].count(0) == 0:
				possible_cols.remove(col)
		        
		for col in cols:
			if number in self.sudoku.hLine[col].numbers:
				possible_cols.remove(col)
		        
		if len(possible_cols) == 1:
			col = possible_cols[0]    
			#print "Nummer " + str(number) + " gehoert in Reihe " + str(row+1) + " Kollone " + str(possible_cols[0]+1)
			self.sudoku.vLine[row][col].setNumber(number)
			self.sudoku.vLine[row].refresh()
	
	#
	#methode schreiben, die ueberprueft, welche nummern in einer zeile noch eingetragen werden
	#muessen und die kollonen in denen ueberhaupt noch eine nummer eingetragen werden kann
	#darauf ueberprueft, ob diese kollonnen diese nummern schon beinhalten
	def sweep_rows(self):
	    for row in range(9):
	        
	        numbers_free = self.sudoku.vLine[row].numbers_free
	        cols_free = []
	        
	        for col in range(9):
	            if self.sudoku.vLine[row].numbers[col] == 0:
	                cols_free.append(col)
	        
	        possible_cols = cols_free[:]
	        #print "In Reihe " + str(row+1) + " sind die Kolonnen " + str(cols_free) + " frei"
	        
	        if len(cols_free) == 1:
	            self.sudoku.vLine[row][cols_free[0]].setNumber(number)
	            self.sudoku.vLine[row].refresh()
	        else:
	            for number in numbers_free:
	                for col in cols_free:
	                    if number in self.sudoku.hLine[col].numbers:
	                        possible_cols.remove(col)
	                
	                if len(possible_cols) == 1:
	                    col = possible_cols[0]
	                    block = self.find_block(row,col)
	                    
	                    if number not in self.sudoku.block[block].numbers:
	                        self.sudoku.vLine[row][possible_cols[0]].setNumber(number)
	                        self.sudoku.vLine[row].refresh()
	                        #print "Zahl " + str(number) + " kommt in Reihe " + str(row+1) + " Kolonne " + str(possible_cols[0]+1)
	                        cols_free.remove(possible_cols[0])
	                        possible_cols = cols_free[:]
	                else:
	                    possible_cols = cols_free[:]
	                    
	#gibt den block andhand der zeilen und kolonnen-nr zurueck    
	def find_block(self,row,col):
	    x = int(math.floor(row / 3.0)) * 3
	    y = int(math.ceil((col+1) / 3.0))
	    
	    return x+y-1
	                