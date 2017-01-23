import sys
import math

if __name__ == "__main__":

	testFilePath=sys.argv[1]

	modelPath="hmmmodel.txt"
	modelFileObj=open(modelPath,"r")

	transition_dict={}
	emission_dict={}
	flag=-1
	for line in modelFileObj.read().split("\n"):
		if line == "$$_T_R_A_N_S_I_T_I_O_N_$$":
			flag=0
			continue

		if flag==0:
			key=""
			for word in line.split("\t"):
				if ":" not in word:
					key=word
					transition_dict.setdefault(key,{})
				else:
					tag=word[:2]
					count=word[3:]
					transition_dict[key].setdefault(tag,0)
					transition_dict[key][tag]=count

		if line == "$$_E_M_I_S_S_I_O_N_$$":
			flag=1
			continue
		if flag==1:
			key=""
			for word in line.split("\t"):
				if ":" not in word:
					key=word
					emission_dict.setdefault(key,{})
				else:
					tag=word[:2]
					count=word[3:]
					emission_dict[key].setdefault(tag,0)
					emission_dict[key][tag]=count

	modelFileObj.close()
	# for key in sorted(emission_dict.keys()):
	# 	print key+"\t"
	# 	for tag in emission_dict[key].keys():
	# 		print tag+":"+str(emission_dict[key].get(tag))+"\t"

	countTransDict={}
	for key in transition_dict.keys():
		countTransDict.setdefault(key,0)
		for tag in transition_dict[key].keys():
			countTransDict[key]=countTransDict[key]+int(transition_dict[key][tag])

	countEmissionDict={}
	for key in transition_dict.keys():
		if key != "q0":
			countEmissionDict.setdefault(key,0)
			for word in emission_dict.keys():
				if emission_dict[word].get(key) is not None:
					countEmissionDict[key]=countEmissionDict[key]+int(emission_dict[word][key])


	testFileObj=open(testFilePath,"r")
	outputFile=open("hmmoutput.txt","w")

	for line in testFileObj.read().split("\n"):
		prev_tag="q0"
		prev_tag_prob=math.log(1)
		for word in line.split():
			outputFile.write(word+"/")
			max_prob=(-1)*float("inf")
			max_prob_tag=""
			unknown_word=0
			for tag in transition_dict[prev_tag].keys():
				prob=float(prev_tag_prob)+ math.log(float(transition_dict[prev_tag][tag])/float(countTransDict[prev_tag]))
				if emission_dict.get(word) is not None:
					if emission_dict[word].get(tag) is None:
						continue
					else:
						prob=prob + math.log(float(emission_dict[word][tag])/float(countEmissionDict[tag]))
				else:
					if word[0].isupper():
						tag="NP"					
						prev_tag_prob=float(prev_tag_prob)+ math.log(float(transition_dict[prev_tag][tag])/float(countTransDict[prev_tag]))
						prev_tag=tag
						unknown_word=1
						break

					elif word.replace('.','',1).isdigit():
						tag="ZZ"					
						prev_tag_prob=float(prev_tag_prob)+ math.log(float(transition_dict[prev_tag][tag])/float(countTransDict[prev_tag]))
						prev_tag=tag
						unknown_word=1
						break
					

				if prob > max_prob:
					max_prob=prob
					max_prob_tag=tag

			if unknown_word==1:
				outputFile.write(tag+" ")
			else:
				prev_tag=max_prob_tag
				prev_tag_prob=max_prob
				outputFile.write(max_prob_tag+" ")
		outputFile.write("\n")

	outputFile.close()
	testFileObj.close()

