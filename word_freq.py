#!/usr/bin/python

import sys

num = int(sys.argv[2])

fp = open("/home/hyeye/textfile.txt","r")
document = fp.read()
fp.close()

document = document.lower()

for ch in '!.?,~*':
	document = document.replace(ch, ' ')

words = document.split()

d = {}
for i in words:
	if i in d:
		d[i] += 1
	else:
		d[i] = 1
d = sorted(d.items(), key = lambda x:x[1], reverse = True)

for i in range(0, num):
	print(d[i][0].ljust(10), str(d[i][1]).rjust(10))
