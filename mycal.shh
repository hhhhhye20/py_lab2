#!/bin/bash
 
OP=$1

num1=$(<num1.txt)
num2=$(<num2.txt)

echo "num1 : $num1 "
echo "num2 : $num2 "
echo "op : $OP "

if [ $OP == add ]; then
	let RESULT=num1+num2
	echo "total : $RESULT"
elif [ $OP == sub ]; then
	let RESULT=num1-num2
	echo "total : $RESULT"
elif [ $OP == div ]; then
	let RESULT=num1/num2
	echo "total : $RESULT"
else
	let RESULT=num1*num2
	echo "total : $RESULT"
fi 

