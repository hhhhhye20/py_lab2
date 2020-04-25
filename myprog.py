#!/usr/bin/python

import calculator as cal

if __name__=='__main__':
	num1, num2 = map(int, (input("two numbers:").split()))

print(cal.plus(num1,num2))
print(cal.minus(num1,num2))
