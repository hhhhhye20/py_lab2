#!/usr/bin/python

def bicon():
	binum = input("input binary number: ")
	binum = '0b' + binum

	intnum = int(binum, 2)
	octnum = oct(intnum)
	hexnum = hex(intnum).upper()
	octnum = octnum.replace('0o', "")
	hexnum = hexnum.replace('0X', "")
	hexnum = hexnum.upper()
	
	print("=>OCT>",octnum)
	print("=>DEC>",intnum)
	print("=>HEX>",hexnum)
	

