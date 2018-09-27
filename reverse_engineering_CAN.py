import math
'''
w_count = 0
W = 50
k = 0.5
div = 0.5
Ra = 0
Rn = 0
Rt = 0
id_i = 0
H_id_i = 0
H_I = 0
canid_list = list()
#with open("1min_CANtraffic.log") as f:
with open("1min_DoStraffic.log") as f:
	for log in f:
		log_split = log.split(" ")
		canpacket = log_split[2].split("#")
		canid_list.append(canpacket[0])
		id_i += 1
		if id_i == W:
			w_count += 1
			id_count = [0 for i in range(2048)]
			for canid in canid_list:
				id_count[int(canid, 16)] += 1
			for canid_i in range(0, 2048):
				if id_count[canid_i] != 0:
					#print("id_i = %x, count = %d" % (canid_i, id_count[canid_i]))
					H_id_i += (float(id_count[canid_i])/W)*(math.log(float(W)/id_count[canid_i])) 
					#print( (id_count[canid_i]/W)*(math.log(W/id_count[canid_i])) )
			H_I = H_id_i
			H_id_i = 0
			print("[%d] H_I=%f" % (w_count, H_I))
			#list clear
			canid_list = []
			id_i = 0
		#print(log_split[2], end="")
'''

def 

def PreProcessing(messageList, DLC):
	payloadLen = len(messageList)
	bitFlip = [0 for i in range(DLC)]
	magnitude = [0 for i in range(DLC)]
	previous = messageList[0]

	while item in messageList:
		for ix in range(0, DLC):
			if item[ix] != previous[ix]:
				bitFlip[ix] += 1

	for ix in range(0, DLC):
		bitFlip[ix] = bitFlip[ix]/payloadLen
		magnitude = math.log10(bitFlip[ix])

	return bitFlip,magnitude

def Phase1(magnitude, DLC):
	ref = list()
	prevMagnitude = magnitude[0]
	ixS = 0
	for ix in range(0, DLC):
		if magnitude[ix] < prevMagnitude :
			ref.add((ixS, ix-1))
			ixS = ix
		prevMagnitude = magnitude[ix]
	ref.add((ixS, DLC-1))
	return ref

def Phase2(ref, bitFlip):
	rRef = list()
	for sign in ref :
		ixS = sign
		ixE = sign
		mu = mean(bitFlip[ixS:ixE])
		std = stdDev(bitFlip[ixS:ixE])
		if bitFlip[ixE] = 0 and matchCounter(bitFlip[ixS:ixE]):
			rRef.add((ixS, ixE, COUNTER))
		else if all(bitFlip[ixS:ixE]=0) and 0.5-std <= mu <= 0.5+std:
			rRef.add((ixS, ixE, CRC))
		else :
			rRef.add((ixS, ixE, PHYS))
	return rRef


if __name__=='__main__':

	for 
		PreProcessing()










