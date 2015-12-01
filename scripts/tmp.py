# coding: utf-8
s1='asdasaadadaf'
s2=''
for i in s1:
	print('%s is on %s ?' % (i, s2))
	if s2.find(i) is  -1:
		print('No')
		s2+=i
print(s2)
