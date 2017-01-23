import sys
import re
import os
from glob import glob

def returnDictionary(filePath):
	dictionary={}
	for file_name in filePath:
		fileObject=open(file_name,"r")
		
		for word in fileObject.read().split():
			if "..." in word:
				processedText=word.split("...")
			else:
				processedText=[word]
			
			for txt in processedText:
				text=re.sub('[^a-z0-9]*','', txt.lower())
				if text.strip() != "":
					dictionary.setdefault(text,0)
					dictionary[text]= dictionary.get(text)+1
		
		fileObject.close()

	return dictionary

if __name__ == "__main__":

	dir_name= sys.argv[1]
	positive_deceptive_dir=dir_name+"/positive_polarity/deceptive_from_MTurk"
	positive_deceptive_file=glob(positive_deceptive_dir+"/*/*.txt")
	posDecDict=returnDictionary(positive_deceptive_file)
	
	positive_truthful_dir=dir_name+"/positive_polarity/truthful_from_TripAdvisor"
	positive_truthful_file=glob(positive_truthful_dir+"/*/*.txt")
	posTruthDict=returnDictionary(positive_truthful_file)
	
	negative_deceptive_dir=dir_name+"/negative_polarity/deceptive_from_MTurk"
	negative_deceptive_file=glob(negative_deceptive_dir+"/*/*.txt")
	negDecDict=returnDictionary(negative_deceptive_file)
	
	negative_truthful_dir=dir_name+"/negative_polarity/truthful_from_Web"
	negative_truthful_file=glob(negative_truthful_dir+"/*/*.txt")
	negTruthDict=returnDictionary(negative_truthful_file)
	
	joinDictionary=dict.fromkeys(posDecDict.keys()+posTruthDict.keys()+negDecDict.keys()+negTruthDict.keys())
	
	fileWrite=open("nbmodel.txt","w")
	
	needSmoothing=0
	for text in sorted(joinDictionary.keys()):
		posDecDict.setdefault(text,0)
		posTruthDict.setdefault(text,0)
		negDecDict.setdefault(text,0)
		negTruthDict.setdefault(text,0)
		if posDecDict.get(text)==0 or posTruthDict.get(text)==0 or negDecDict.get(text)==0 or negTruthDict.get(text)==0:
			needSmoothing=1
			break
	
	if needSmoothing==1:
		for text in sorted(joinDictionary.keys()):
			posDecDict.setdefault(text,0)
			posTruthDict.setdefault(text,0)
			negDecDict.setdefault(text,0)
			negTruthDict.setdefault(text,0)
			fileWrite.write(text+"\t")
			fileWrite.write(str(posDecDict.get(text)+1)+"\t")
			fileWrite.write(str(posTruthDict.get(text)+1)+"\t")
			fileWrite.write(str(negDecDict.get(text)+1)+"\t")
			fileWrite.write(str(negTruthDict.get(text)+1)+"\n")

	fileWrite.close()