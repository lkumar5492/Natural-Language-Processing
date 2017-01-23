import sys

if __name__ == "__main__":

	training_filename=sys.argv[1]
	training_fileObj=open(training_filename,"r")
	emission_dict={}
	transition_dict={}
	for line in training_fileObj.read().split("\n"):
		prev_tag="q0"
		for word in line.split():
			key= word[:-3]
			tag= word[-2:]
			emission_dict.setdefault(key,{})
			emission_dict[key].setdefault(tag,0)
			emission_dict[key][tag]=emission_dict[key].get(tag)+1

			transition_dict.setdefault(prev_tag,{})
			transition_dict[prev_tag].setdefault(tag,0)
			transition_dict[prev_tag][tag]=transition_dict[prev_tag].get(tag)+1
			prev_tag=tag

	training_fileObj.close()

	fileWrite=open("hmmmodel.txt","w")

	all_tags=transition_dict.keys()
	for prev_tag in transition_dict.keys():
		all_tags=all_tags + transition_dict[prev_tag].keys()

	jointTagsDict=dict.fromkeys(all_tags)
	fileWrite.write("$$_T_R_A_N_S_I_T_I_O_N_$$")
	for prev_tag in sorted(jointTagsDict.keys()):
		transition_dict.setdefault(prev_tag,{})
		fileWrite.write("\n"+prev_tag+"\t")
		for tag in sorted(jointTagsDict.keys()):
			if not(tag == "q0"):
				transition_dict[prev_tag].setdefault(tag,0)
				fileWrite.write(tag+":"+str(transition_dict[prev_tag].get(tag)+1)+"\t")

	fileWrite.write("\n$$_E_M_I_S_S_I_O_N_$$")
	for key in sorted(emission_dict.keys()):
		fileWrite.write("\n"+key+"\t")
		for tag in emission_dict[key].keys():
			fileWrite.write(tag+":"+str(emission_dict[key].get(tag))+"\t")

	


