#!/usr/bin/python
import sys

def findAnagram(input):
	result=[]
	if len(input)==1:
		result.append(input)
	else:		
		for i in range(len(input)):
			char=input[i]
			beforeChar=input[:i]
			afterChar=input[i+1:]
			for j in findAnagram(beforeChar+afterChar):
				result.append(j+char)
	return result;

if __name__ == "__main__":	
	input=sys.argv[1]
	list=findAnagram(input)
	list.sort()

	file_name="anagram_out.txt"
	fileObject= open(file_name,"w")

	length=len(list)
	for i in range(length):
		fileObject.write(list[i]+"\n")
	fileObject.close()
