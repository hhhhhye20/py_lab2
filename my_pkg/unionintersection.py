#!/usr/bin/python

def uni_inter():
	f_list = input("1st list: ")
	s_list = input("2st list: ")

	f_list = f_list.replace('[',"").replace(']', "").replace(" ","").replace(',',"")
	s_list = s_list.replace("[", "").replace(']',"").replace(" ",'').replace(',',"")

	in_list=[]
	uni_list=[]

	for ch in f_list:
		if ch in s_list:
			in_list.append(ch)
			uni_list.append(ch)
		elif ch not in s_list:
			uni_list.append(ch)
	for ch in s_list:
		if ch not in uni_list:
			uni_list.append(ch)

	print(sorted(list(map(int, uni_list))))
	print(sorted(list(map(int, in_list))))

 	
