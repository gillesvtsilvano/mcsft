#!/usr/bin/env python

class States:
	LINES=0
	COLUMNS=1
	MATRIX=2
	END=3

class MCS:
	def __init__(self, line=[], column=[], matrix=[[]]):
		self.line=line
		self.column=column
		self.matrix=matrix

	def parse(self): pass 
		#TODO
		

	def __repr__(self):
		l=[]
		for i in range(len(m)):
			for j in range(len(m[i])):
				if int(m[i][j]):
					l.append(self.line[i] + self.column[j])

		newList=[]
		tmp=''
		for item in l:
			for c in item:
				if tmp.find(c) is -1:
					tmp+=c
			newList.append(tmp)
			tmp=''
		s=''
		for item in newList:
			s+=item + ' + '
		return s[:-3]



if __name__ == "__main__":
	fname='./data'

	with open(fname) as f:
		content = [x.strip('\n') for x in f.readlines()]
	f.close()
	print(content)
	state=States.LINES
	lCounter=0
	m=[[]]
	for line in content:
		if state is States.LINES:
			l=line.split(' ')
			print(l)
			state=States.COLUMNS
		elif state is States.COLUMNS:
			c=line.split(' ')
			print(c)
			state=States.MATRIX
		elif state is States.MATRIX:	
			for i in line.split(' '):
				m[lCounter].append(i)
			if lCounter < len(l) - 1:
				lCounter += 1
				m.append([])
			else:
				state=States.END
		elif state is States.END:
			pass
	print(m)
	mcs=MCS(l, c, m)
	print(mcs)
