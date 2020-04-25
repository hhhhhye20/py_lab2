#!/usr/bin/python

import my_pkg

if __name__=='__main__':
	num = int(input("Select menu: "))
	if(num==1):
		binum=my_pkg.oct(num)	
		print(binum)	
