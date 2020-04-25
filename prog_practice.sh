#!/bin/bash

if ! [ -d temp_2 ]; then
	mkdir temp_2
fi

cp num1_p.txt num2_p.txt mycal_practice.sh temp_2
set add sub div mul


echo "create temp directory.."
echo "copy files to temp directory.."

echo "1)add"
echo "2)sub"
echo "3)div"
echo "4)mul"
read -p "select menu: " OP
echo "$OP is selected"

./mycal_practice.sh $OP
