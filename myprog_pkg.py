#!/usr/bin/python

import my_pkg

if __name__=='__main__':
	while True:
		num =int(input("Select menu: 1)conversion 2) union/intersection 3) exit?"))
		if(num == 1):
			my_pkg.bicon()
		elif(num ==2):
			my_pkg.uni_inter()
		else:
			break
	print("exit the program..")
