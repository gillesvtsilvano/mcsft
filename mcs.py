#!/usr/bin/env python

import sys

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
	inputfname='data'
	outputfname='out.sharpe'

	def __init__(self):
		self.top = ''
		self.nodes = {}
		self.target = ''
	
	def parse(self):

		with open(self.inputfname) as f:
			content = [ x.strip('\n') for x in f.readlines()]
		f.close()

		state=States.TOP

		while state is not States.END:
			if state is States.TOP:
				self.top = content[0].split(' ')[0]

				state = States.NODES
			elif state is States.NODES:
				for i in content[1].split(' '):
					n=Node()
					n.identifier = i
					self.nodes[i] = n
		
				n=len(self.nodes)
				state = States.LAMBDAS
			elif state is States.LAMBDAS:
				if n > 0:
					l=content[n+1].split(' ')
					i, p = l[0], l[1]
					self.nodes[i].param=float(p)
					n-=1
				else:
					n = len(self.nodes) - 1
					state = States.MCS
			elif state is States.MCS:
				if n > 0:
					l=content[n+7].split('=')
					i,m = l[0], l[1].split('+')
					self.nodes[i].mcs=m
					n-=1
				else:
					state = States.END
			elif state is States.END:
				break


		
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
			
			s+='kofn koon0 %d,%d,' % (int(k), int(n))

			for k,n in nodes:
				if not (n.identifier is self.target):	
					s+=" %s_or0" % (n.identifier)
			s+="\n"
			
		else:
			andCount=0
			expr=self.top.split('+')
			for e in expr:
				if len(e) > 1:
					s+='and and__%d' % andCount
					andCount+=1
					for i in e:
						s+=' %s_or0' % i
				s+='\n'
	
			andCount=0
			orCount=0
			s+='or or__%d' % orCount
			for e in expr:
				orCount+=1
				if len(e) == 1:
					s+=' %s_or0' % e
				else:
					s+=' and__%d'% andCount
					andCount+=1

			s+='\n'





		s+="end\n\n"
		s+="func Reliability(t) 1-tvalue(t; model)\n"
		s+="loop t,0,1000,10\n"
		s+="expr Reliability(t)\n"
		s+="end\n\n"
		s+="end"
		
		with open(self.outputfname, 'w') as f:
			f.write(s)
		f.close()


if __name__=="__main__":
	parser=MCSParser()
	if len(sys.argv) == 2:
		parser.inputfname=sys.argv[1]

	parser.parse()
