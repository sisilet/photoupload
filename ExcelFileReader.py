#!/usr/bin/python
# Filename: ExcelFileReader.py

import xlrd

class ExcelSheet:
	class SheetIterator:
		def __init__(self,sheet,r1,c1,header):
			self.r1 = r1
			self.c1 = c1
			self.curr_record = 0
			self.sheet = sheet
			if header==True:
				self.header = 1

		def __first_record(self):
			return self.r1 + self.header

		def __nrecords(self):
			return self.sheet.nrows - self.r1 - self.header

		def next(self):
			if self.__nrecords() > self.curr_record:
				ret = self.sheet.row_values(self.curr_record+self.__first_record(),self.c1)
			else:
				raise StopIteration

			self.curr_record = self.curr_record + 1
			return ret

	def __init__(self,s):
		self.sheet = s
		self.Header(True)
		self.curr_record = 0
		if self.setPivotTopLeft() == False:
			raise Exception
		else:
			pass

	def __iter__(self):
		return ExcelSheet.SheetIterator(self.sheet,self.r1,self.c1,self.header)

	def __len__(self):
		ret = self.sheet.nrows - self.r1
		if self.header:
			return ret - 1
		else:
			return ret

	
	def Header(self,header):
		self.header = header

	def getHeader(self):
		if self.header:
			ret = self.sheet.row_values(self.r1,self.c1)
		else:
			ret = []
		return ret

	def setPivotTopLeft(self):
		s = self.sheet
		for r in range(s.nrows):
			for c in range(s.ncols):
				if s.cell(r,c).ctype != xlrd.XL_CELL_EMPTY:
					self.r1 = r
					self.c1 = c
					return True
		return False

	def setPivotKeyword(self,keyword):
		s = self.sheet
		for r in range(s.nrows):
			for c in range(s.ncols):
				if s.cell(r,c).ctype == keyword:
					self.r1 = r
					self.c1 = c

	def setPivot(self,row,col):
		self.r1 = row
		self.c1 = col
		
class ExcelFileReader:
	class BookIterator:
		def __init__(self,sheets):
			self.curr_sheet = 0
			self.sheets = sheets
		
		def next(self):
			if len(self.sheets) > self.curr_sheet:
				ret = self.sheets[self.curr_sheet]
			else:
				raise StopIteration

			self.curr_sheet = self.curr_sheet + 1
			return ret


	def __init__(self):
		self.filename = ""
		self.wb = None
		self.sheets = []

	def load(self, filename, header = True):
		self.wb = xlrd.open_workbook(filename) # book class
		self.header = header
		
		if(self.wb != None):
			self.filename = filename
			for si in range(self.wb.nsheets):
				try:
					s = ExcelSheet(self.wb.sheet_by_index(si))
					self.sheets.append(s)
				except:
					pass
			
	def __iter__(self):
		return ExcelFileReader.BookIterator(self.sheets)

	def __len__(self):
		return len(self.sheets)
	
if __name__ == "__main__":
	reader = ExcelFileReader()
	reader.load('C:\\temp\\facebookupload\\book1.xls')
	for s in reader:
		for r in s:
			print r
		print '\n'
		for r in s:
			print r
		print '\n'
	for s in reader:
		for r in s:
			print r
		print '\n'
		for r in s:
			print r
		print '\n'

		



	
	
	
