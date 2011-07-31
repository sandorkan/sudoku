class Field(object):
	def __init__(self,number=0):
		self.number = number
		self.set = False
		
	def setNumber(self, number):
		if(number > 0 and number < 10):
			self.number = number
		else:
			print "Number has to be between 1 and 9"
			
	def getNumber(self):
		return self.number
		
	def delNumber(self):
		self.number = -1
		
	def __str__(self):
		return str(self.number)
		
	def __unicode__(self):
		return str(self.number)
		
class Block(object):
	def __init__(self,block_felder=None):
		self.block_felder = block_felder
		
		self.block_liste = []
		self.create_list()
		
	def show_numbers(self):
		for i in range(len(self.block_felder)):
			if i % 3 == 0:
				print ""
			print self.block_felder[i].getNumber(),
			
	def create_list(self):
		for feld in self.block_felder:
			self.block_liste.append(feld.getNumber())

class vLine(object):
	def __init__(self,vLine_felder=None):
		self.vLine_felder = vLine_felder
		
		self.vLine_liste = []
		self.create_list()
		
	def show_numbers(self):
		for line in self.vLine_felder:
			print line.getNumber(),
			
	def create_list(self):
		for feld in self.vLine_felder:
			self.vLine_liste.append(feld.getNumber())
			
class hLine(object):
	def __init__(self,hLine_felder=None):
		self.hLine_felder = hLine_felder
		
		self.hLine_liste = []
		self.create_list()
		
	def show_numbers(self):
		for line in self.hLine_felder:
			print line.getNumber(),
			
	def create_list(self):
		for feld in self.hLine_felder:
			self.hLine_liste.append(feld.getNumber())

class Sudoku(object):
	def __init__(self,file="sudoku1.txt"):
		self.spielfeld = []
		self.load_fields(file)
		
		self.block = []
		self.create_blocks()
		
		self.v_Line = []
		self.create_vLines()
		
		self.h_Line = []
		self.create_hLines()
		
	def load_fields(self,file=None):
		f = open(file,"r")
		
		self.name = f.readline()
		lines = f.readlines()
		
		for line in lines:
			for number in [int(x) for x in line.split(',')]:
				self.spielfeld.append(Field(number))
	
	# ein sudoku spielfeld besteht aus 9 3*3 bloecken. die zahlen der bloecke werden zuerst
	# in listen gespeichert und dann den block-klassen uebergeben
	def create_blocks(self):
		blocks = [[],[],[],[],[],[],[],[],[]]
		#self.block = []
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
			self.v_Line.append(vLine(v))
			
	def create_hLines(self):
		hLines = [[],[],[],[],[],[],[],[],[]]
		
		for i in range(9):
			for j in range(9):
				hLines[i].append(self.spielfeld[i+j*9])

		for h in hLines:
			self.h_Line.append(hLine(h))
			
	def print_blocks(self):
		for block in self.block:
			block.show_numbers()
			print ""
			
	def print_vLines(self):
		for vLine in self.v_Line:
			vLine.show_numbers()
			print ""
			
	def print_hLines(self):
		for hLine in self.h_Line:
			hLine.show_numbers()
			print ""
			
	def print_all(self):
		print "***   Vertical Lines   ***"
		self.print_vLines()
		
		print ""
		
		print "***   Horizontal Lines   ***"
		self.print_hLines()
		
		print ""
		
		print "***   Blocks   ***"
		self.print_blocks()