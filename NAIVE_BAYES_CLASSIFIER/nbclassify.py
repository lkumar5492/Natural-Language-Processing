import sys
import re
import math
from glob import glob

def fetchModelParam():
	path="nbmodel.txt"
	fileObj=open(path,"r")
	dictionary={}
	
	sum_Pos_Dec=0
	sum_Pos_Truth=0
	sum_Neg_Dec=0
	sum_Neg_Truth=0

	for line in fileObj.readlines():
		line=line.rstrip("\n")
		values=line.split("\t")
		key=values[0]
		dictionary.setdefault(key,[0]*4)
		dictionary[key][0]=values[1]
		sum_Pos_Dec=sum_Pos_Dec+int(values[1])

		dictionary[key][1]=values[2]
		sum_Pos_Truth=sum_Pos_Truth+int(values[2])

		dictionary[key][2]=values[3]
		sum_Neg_Dec=sum_Neg_Dec+int(values[3])

		dictionary[key][3]=values[4]
		sum_Neg_Truth=sum_Neg_Truth+int(values[4])

	global sum_Pos_Deceptive
	sum_Pos_Deceptive=sum_Pos_Dec
	global sum_Pos_Truthful
	sum_Pos_Truthful=sum_Pos_Truth
	global sum_Neg_Deceptive
	sum_Neg_Deceptive=sum_Neg_Dec
	global sum_Neg_Truthful
	sum_Neg_Truthful=sum_Neg_Truth

	fileObj.close()
	
	return dictionary


if __name__ == "__main__":
	
	modelParam=fetchModelParam()
	dir_name=sys.argv[1]
	testFileName=glob(dir_name+"/*/*/*/*.txt")

	prior_prob_of_PosDec=0.25
	prior_prob_of_PosTruth=0.25
	prior_prob_of_NegDec=0.25
	prior_prob_of_NegTruth=0.25

	pos_dec=0
	pos_truth=1
	neg_dec=2
	neg_truth=3

	outFile=open("nboutput.txt","w")

	truePositive=0
	falsePositive=0
	falseNegative=0

	for fileName in testFileName:
		testFile= open(fileName,"r")

		prob_of_PosDec= math.log(float(prior_prob_of_PosDec))
		prob_of_PosTruth=math.log(float(prior_prob_of_PosTruth))
		prob_of_NegDec=math.log(float(prior_prob_of_NegDec))
		prob_of_NegTruth=math.log(float(prior_prob_of_NegTruth))

		for word in testFile.read().split():
			if "..." in word:
				processedText=word.split("...")
			else:
				processedText=[word]

			for txt in processedText:
				text=re.sub('[^a-z0-9]*','', txt.lower())
				if text.strip() == "" or modelParam.get(text) is None:
					pass
				else:
					prob_of_PosDec=prob_of_PosDec + math.log((float(modelParam[text][pos_dec])/float(sum_Pos_Deceptive)))
				
					prob_of_PosTruth=prob_of_PosTruth+ math.log((float(modelParam[text][pos_truth])/float(sum_Pos_Truthful)))
				
					prob_of_NegDec=prob_of_NegDec+ math.log((float(modelParam[text][neg_dec])/float(sum_Neg_Deceptive)))
					
					prob_of_NegTruth=prob_of_NegTruth+ math.log((float(modelParam[text][neg_truth])/float(sum_Neg_Truthful)))

		if (prob_of_PosDec >= prob_of_PosTruth) and (prob_of_PosDec >= prob_of_NegDec) and (prob_of_PosDec >= prob_of_NegTruth):
			outFile.write("deceptive positive "+fileName+"\n")
		elif (prob_of_PosTruth >= prob_of_PosDec) and (prob_of_PosTruth >= prob_of_NegDec) and (prob_of_PosTruth >= prob_of_NegTruth):
			outFile.write("truthful positive "+fileName+"\n")
		elif (prob_of_NegDec >= prob_of_PosDec) and (prob_of_NegDec >= prob_of_PosTruth) and (prob_of_NegDec >= prob_of_NegTruth):
			outFile.write("deceptive negative "+fileName+"\n")
		elif (prob_of_NegTruth >= prob_of_PosDec) and (prob_of_NegTruth >= prob_of_PosTruth) and (prob_of_NegTruth >= prob_of_NegDec):
			outFile.write("truthful negative "+fileName+"\n")

		testFile.close()

	outFile.close()