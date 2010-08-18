#!/usr/bin/python
# Filename: ExcelFileReader.py

import xlrd

class ExcelFileReader:
	def __init__(self):
		self.filename = ""
		self.wb = None
		self.datasheet = -1
		self.datarow = -1
		self.datacol = -1
		self.header = True
		self.curr_record = 0
	
	def __iter__(self):
		return self

	def __len__(self):
		ret = self.wb.sheet_by_index(self.datasheet).nrows - self.datarow
		if self.header:
			return ret - 1
		else:
			return ret

	def load(self, filename, header = True, keyword = ''):
		self.wb = xlrd.open_workbook(filename) # book class
		
		if(self.wb != None):
			self.filename = filename

		for si in range(self.wb.nsheets):
			s = self.wb.sheet_by_index(si)
			for r in range(s.nrows):
				for c in range(s.ncols):
					if keyword != '':
						if s.cell(r,c) == keyword:
							self.datasheet = si
							self.datarow = r
							self.datacol = c
							return
					else:
						if s.cell(r,c).ctype != xlrd.XL_CELL_EMPTY:
							self.datasheet = si
							self.datarow = r
							self.datacol = c
							return

#		# search for first non-empty sheet
#		for n in range(self.wb.nsheets):
#			if(self.wb.sheet_by_index(n).nrows):
#				break
#		if n==range(self.wb.nsheets):
#			raise ReaderError('File empty')
#
#		self.datasheet = n
#		sheet = self.wb.sheet_by_index(n)
#		# search for first non-empty row
#		for m in range(sheet.nrows):
#			rv = sheet.row_values(m)
#			for o in range(len(rv)):
#				if rv[o] != '':
#					break
#			if o != len(rv)-1:
#				break
#		self.datarow = m
#		self.datacol = o
#		self.header = header

	def getHeader(self):
		if self.header:
			ret = self.wb.sheet_by_index(self.datasheet).row_values(self.datarow,self.datacol)
		else:
			ret = []
		return ret

	def next(self):
		if self.header:
			headerskip = 1
		else:
			headerskip = 0

		if self.wb.sheet_by_index(self.datasheet).nrows > self.datarow+self.curr_record+headerskip:
			ret = self.wb.sheet_by_index(self.datasheet).row_values(self.datarow+self.curr_record+headerskip,self.datacol)
		else:
			raise StopIteration

		self.curr_record = self.curr_record + 1
		return ret
			
	
if __name__ == "__main__":
	reader = ExcelFileReader()
	reader.load('C:\\temp\\facebookupload\\book1.xls')
	print reader.getHeader()
	print len(reader)
	for r in reader:
		print r

		



	
	
	
