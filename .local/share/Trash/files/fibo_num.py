#!/usr/bin/python

num = int(input("fibonacci number? "))
f1 = 1
f2 = 1
for i in range(1, num+1):
	if(i==1):
		print("1")
	elif(i==2):
		print("1")

	else:
		f3= f1 + f2
		print(f3)
		f1 = f2
		f2 = f3
print("F",num,"=",f3)
