import sys
from struct import *

def encodeToUTF8(code,outFile):
	binary=bin(code)
	pos=len(binary)-1
	if code>=0 and code<=127:
		head='0'
		emptyBits=8-len(head)
		byte1=''
		while pos!=1:
			byte1=binary[pos]+byte1
			pos=pos-1

		while len(byte1)!=emptyBits:
			byte1='0'+byte1

		if len(byte1)==emptyBits:
			byte1=head+byte1
		
		utf8=byte1
		packed=pack("i",int(utf8,2))
		outFile.write(packed[0])
		
	elif code>=128 and code<=2047:
		headByte2='110'
		byte2=''
		emptyBits2=8-len(headByte2)

		headByte1='10'
		byte1=''
		emptyBits1=8-len(headByte1)

		pos=len(binary)-1
		while pos!=1:
			if len(byte1)!=emptyBits1:
				byte1=binary[pos]+byte1
			elif len(byte2) != emptyBits2:
				byte2=binary[pos]+byte2
			pos=pos-1

		while len(byte1)!=emptyBits1:
			byte1='0'+byte1
		while len(byte2)!=emptyBits2:
			byte2='0'+byte2
		if len(byte1)==emptyBits1:
			byte1=headByte1+byte1
		if len(byte2)==emptyBits2:
			byte2=headByte2+byte2
		utf8=byte2+byte1
		packed=pack("i",int(utf8,2))
		outFile.write(packed[1]+packed[0])

	elif  code>=2048 and code<=65535:
		headByte3='1110'
		byte3=''
		emptyBits3=8-len(headByte3)

		headByte2='10'
		byte2=''
		emptyBits2=8-len(headByte2)

		headByte1='10'
		byte1=''
		emptyBits1=8-len(headByte1)
		pos=len(binary)-1
		while pos!=1:
			if len(byte1)!=emptyBits1:
				byte1=binary[pos]+byte1
			elif len(byte2) != emptyBits2:
				byte2=binary[pos]+byte2			
			elif len(byte3) != emptyBits3:
				byte3=binary[pos]+byte3
			pos=pos-1

		while len(byte1)!=emptyBits1:
			byte1='0'+byte1
		while len(byte2)!=emptyBits2:
			byte2='0'+byte2
		while len(byte3)!=emptyBits3:
			byte3='0'+byte3
		if len(byte1)==emptyBits1:
			byte1=headByte1+byte1
		if len(byte2)==emptyBits2:
			byte2=headByte2+byte2
		if len(byte3)==emptyBits3:
			byte3=headByte3+byte3
		
		utf8=byte3+byte2+byte1
		packed=pack("i",int(utf8,2))
		outFile.write(packed[2]+packed[1]+packed[0])
	
if __name__== "__main__":
	fileName=sys.argv[1]
	fileObject=open(fileName,"r")
	twoByte=fileObject.read(2)
	utf8=''

	outFile=open("utf8encoder_out.txt","w")

	while twoByte!="":
		code=unpack('>H',twoByte)
		encodeToUTF8(code[0],outFile)
		twoByte=fileObject.read(2)
	outFile.close()
	fileObject.close()	
