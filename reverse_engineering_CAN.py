import math

def PreProcessing(messageList, DLC):
	payloadLen = len(messageList)
	bitFlip = [0 for i in range(DLC)]
	magnitude = [0 for i in range(DLC)]
	previous = messageList[0]

	for item in messageList:
		for ix in range(0, DLC):
			if item[ix] != previous[ix]:
				bitFlip[ix] += 1

	for ix in range(0, DLC):
		bitFlip[ix] = bitFlip[ix]/payloadLen
		# eliminate log10(0.0)
		if bitFlip[ix] != 0 :
			magnitude[ix] = math.ceil(math.log10(bitFlip[ix]))
		else:
			magnitude[ix] = -1

	return bitFlip,magnitude

def Phase1(magnitude, DLC):
	ref = list()
	prevMagnitude = magnitude[0]
	ixS = 0
	for ix in range(0, DLC):
		if magnitude[ix] < prevMagnitude :
			ref.append((ixS, ix-1))
			ixS = ix
		prevMagnitude = magnitude[ix]
	ref.append((ixS, DLC-1))
	return ref

def Phase2(ref, bitFlip):
	rRef = list()
	for sign in ref :
		ixS = sign
		ixE = sign
		mu = mean(bitFlip[ixS:ixE])
		std = stdDev(bitFlip[ixS:ixE])
		if bitFlip[ixE] == 0 and matchCounter(bitFlip[ixS:ixE]):
			rRef.add((ixS, ixE, COUNTER))
		elif all(bitFlip[ixS:ixE]=0) and 0.5-std <= mu <= 0.5+std:
			rRef.add((ixS, ixE, CRC))
		else :
			rRef.add((ixS, ixE, PHYS))
	return rRef

if __name__=='__main__':

	canids = list()
	messageLists = [list() for i in range(2048)]

	# create list of canid, list of binary payload 
	with open("1min_CANtraffic.log") as log_file:
		for log in log_file:
			log_split = log.split(" ")
			canpacket = log_split[2].split("#")
			#print(canpacket[0], canpacket[1][0:len(canpacket[1])-1], len(canpacket[1][0:len(canpacket[1])-1]))
			format_len = '0'+str((len(canpacket[1])-1)*4)+'b'
			payload = format(int(canpacket[1][0],16), format_len)
			#print(canpacket[0], payload)
			messageLists[int(canpacket[0], 16)].append(payload)
			if int(canpacket[0], 16) not in canids :
				canids.append(int(canpacket[0], 16))
	canids.sort()

	# perform Reverse Engineering of Automotive Data frames
	for canid in canids:
		DLC = len(messageLists[canid][0])
		bitFlip, magnitude = PreProcessing(messageLists[canid], DLC)
		#print(hex(canid), magnitude)
		ref = Phase1(magnitude, DLC)
		#print(hex(canid), ref)
		#rRef = Phase2(ref, bitFlip)
