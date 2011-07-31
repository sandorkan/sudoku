import math

class test(object):
	def find_block(self,row,col):
	    x = int(math.floor(row / 3.0)) * 3
	    y = int(math.ceil((col+1) / 3.0))
	    
	    return x+y-1
	    
	def test_find_block(self):
		for i in range(9):
			for j in range(9):
				print "Zeile: " + str(i) + " Reihe: " + str(j) + " = Block " + str(self.find_block(i,j))