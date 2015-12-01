#!/usr/bin/env python
# Input:
# KooN | AND | OR
# A B C D E S
# A 0.001
# B 0.001
# C 0.001
# D 0.001
# E 0.001
# S 0.001
# A+BD+BE+CD+CE+S
# B+CE+DC+S
# D+CE+BE+S
# C+S
# E+S
#


class States:
	TOP=0
	NODES=1
	LAMBDAS=2
	MCS=3
	END=4


class Node:
	def __init__(self):
		self.identifier = ''
		self.param = 0.0
		self.mcs = []

	def __repr__(self):
		return '%s(%f)=%s' % (self.identifier, self.param, self.mcs)


class MCSParser:
	def __init__(self):
		self.top = ''
		self.nodes = {}
		self.target = ''

	def parse(self):
		s='bind\n'
		nodes = self.nodes.items()
		for k,n in nodes:
			s+='lambda_%s %f\n' % (n.identifier, n.param)		
		s+="end\n\n"
		s+="ftree model\n"
		counter = 0

		for k,n in nodes:
			if n.mcs == []:
				self.target = k
				print("Target: %s" % k)

		for k,n in nodes:
			if counter is 0:
				s+="basic %s exp(lambda_%s)\n" % (n.identifier, n.identifier)
				counter += 1
			else:
				s+="repeat %s exp(lambda_%s)\n" % (n.identifier, n.identifier)
		
		for k,n in nodes:
			andCount=0
			for ands in n.mcs:
				if len(ands) > 1:
					s+="and %s_and%d" % (n.identifier, andCount)
					for e in ands.split('.'):
						s+=" %s" % e
					s+="\n"
					andCount+=1
			orCount=0
			andCount=0
			if not (n.identifier is self.target):
				s+="or %s_or%d" % (n.identifier, orCount)
				for ors in n.mcs:
					orCount+=1
					if len(ors) is 1:
						s+=" %s" % ors
					else:
						s+=" %s_and%d" % (n.identifier, andCount)
						andCount+=1
				s+="\n"

		if self.top.find('oo') is 1:
			k = self.top.split('oo')[0]
			n = self.top.split('oo')[1]
			
			s+='kofn koon0,%d,%d' % (int(k), int(n))

			for k,n in nodes:
				s+=" %s_or0" % (n.identifier)
			s+="\n"
					
		elif self.top is "AND":
			pass
		elif self.top is "OR":
			pass				
				
		s+="end\n\n"
		s+="func Reliability(t) 1-tvalue(t; model)\n"
		s+="loop t,0,1000,10\n"
		s+="expr Reliability(t)\n"
		s+="end\n\n"
		s+="end"
		
		with open('out.sharpe', 'w') as f:
			f.write(s)
		f.close()



with open('data') as f:
	content = [ x.strip('\n') for x in f.readlines()]
f.close()
print(content)

state=States.TOP

parser=MCSParser()

while state is not States.END:
	if state is States.TOP:
		parser.top = content[0].split(' ')[0]

		state = States.NODES
	elif state is States.NODES:
		for i in content[1].split(' '):
			n=Node()
			n.identifier = i
			parser.nodes[i] = n
		n=len(parser.nodes)
		state = States.LAMBDAS
	elif state is States.LAMBDAS:
		if n > 0:
			l=content[n+1].split(' ')
			i, p = l[0], l[1]
			parser.nodes[i].param=float(p)
			n-=1
		else:
			n = len(parser.nodes) - 1
			state = States.MCS
	elif state is States.MCS:
		if n > 0:
			l=content[n+7].split('=')
			i,m = l[0], l[1].split('+')
			parser.nodes[i].mcs=m
			n-=1
		else:
			state = States.END
	elif state is States.END:
		break

for k,d in parser.nodes.items():
	print('%s' % d)

parser.parse()
