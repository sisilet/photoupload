import os,re


class ConfigFile:
	def __init__(self,filepath):
		if os.path.exists(filepath):
			f = open(filepath,'r')
			lines = f.readlines()
			for line in lines:
				matchequal = re.match(r'^\s*(\S+)\s*=\s*(\S+)',line)
				if matchequal:
					self.__dict__[matchequal.group(1)] = matchequal.group(2)
			f.close()
	
	def __setattr__(self,key,value):
		self.__dict__[key] = value
	
	def __getattr__(self,key):
		return self.__dict__[key]

	def writeFile(self,filepath):
		f = open(filepath,'w')
		for key in self.__dict__.iterkeys():
			f.write(key+'='+self.__dict__[key]+'\n')
		f.close()

class ParseFacebookUrl:
	def __init__(self,uri):
		urilist = uri.split('?')
		self.url = urilist[0]
		queries = urilist[1].split('&')
		self.query = {}
		for q in queries:
			pair = q.split('=')
			if len(pair) == 2:
				self.query[pair[0]] = pair[1]		

if __name__ == '__main__':
	config_file_path = os.path.join(os.path.expanduser('~'),'fb.ini')
	cf = ConfigFile(config_file_path)
	cf.test = '100'
	cf.test2 = '200'
	cf.test3 = '300'
	cf.test4 = '300'
	cf.writeFile(config_file_path)


