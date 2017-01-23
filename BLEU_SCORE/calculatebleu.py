import sys
import os
from glob import glob
import copy
import math

def fetchNGrams(words,grams):
	gram_list=[]
	index=0
	i=0
	j=i
	while j < len(words) and len(words) >= grams+1:
		gram_list.append(" ")
		j=i
		count=0
		while count < grams+1:
			gram_list[index]= gram_list[index]+ words[j] + " "
			j=j+1
			count=count+1
		index=index+1
		i=i+1

	return gram_list

if __name__ == "__main__":

	candidate= sys.argv[1]
	reference= sys.argv[2]

	candFile= open(candidate,"r")
	candFileList=candFile.readlines()
	refFileList=[]
	if os.path.isfile(reference):
		refFileObj= open(reference,"r")
		refFileList.append(refFileObj.readlines())
	elif os.path.isdir(reference):
		refFilePath=glob(reference + "/*.txt")	
		for refFile in refFilePath:
			refFileObj= open(refFile,"r")
			refFileList.append(refFileObj.readlines())

	GRAM_1=0
	GRAM_2=1
	GRAM_3=2
	GRAM_4=3

	ref=[]
	candi=[]
	match_count=[0]*4
	total_gram_count=[0]*4

	c=0
	for gram in range(GRAM_1,GRAM_4+1):
		refList=copy.deepcopy(refFileList)
		count=0
		total_count=0
		for i,line in enumerate(candFileList):
			r=0
			line=line.strip("\n")
						
			words=line.split()
			
			gram_list =fetchNGrams(words,gram)
			
			total_count=total_count+len(gram_list)
			
			flag=0
			ref_gram_list=[]
			if gram == GRAM_1:
				c=len(gram_list)
			for word in gram_list:
			
				findMatch=word
				wordExists=0
			
				for fileNo,refFileLines in enumerate(refList):
					if flag == 0:
						if gram == GRAM_1:
							size=len(refFileLines[i].split())
							if abs(size - c) < abs(r-c) :
								r=size
							elif abs(size - c) == abs(r-c) :
								if size < r:
									r=size
						refFileLines[i]= " "+refFileLines[i]+" "
						ref_gram_list.append(fetchNGrams(refFileLines[i].split(),gram))
					
					if  findMatch in ref_gram_list[fileNo]:	
						wordExists = 1	
						ref_gram_list[fileNo].remove(findMatch)
				flag=1
				if wordExists == 1:
					count=count+1

			if gram == GRAM_1:
				candi.append(c)
				ref.append(r)

		match_count[gram]=count
		total_gram_count[gram]=total_count

	final_c=0
	final_r=0
	for c in candi:
		final_c=final_c + c

	for r in ref:
		final_r = final_r + r

	bp =0
	if final_c > final_r:
		bp = 1
	else:
		bp = math.exp(1- (float(final_r)/final_c))
	
	wn=float(1.0/4)
	sum=0
	for gram in range(GRAM_1,GRAM_4+1):
		pn= float(match_count[gram])/float(total_gram_count[gram])
		logpn= math.log(pn)
		sum=sum+(wn * logpn)
	
	bleu_score = bp * math.exp(float(sum))

	outFile=open("bleu_out.txt","w")
	outFile.write(str(float(bleu_score)))
	

