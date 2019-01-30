import sys
import math
from statistics import mean, median,variance,stdev

#classifer LABELs
COUNTER = "Counter"
CRC = "CRC"
PHYS = "Physical_Value"
CONSTANT = "Constant"

def matchCounter(bitFlip):
	if bitFlip == []:
		return False
	elif bitFlip[len(bitFlip)-1]==1 :
		return True
	else :
		return False

def PreProcessing(messageList, DLC):
	payloadLen = len(messageList)
	bitFlip = [0 for i in range(DLC)]
	magnitude = [0 for i in range(DLC)]
	previous = messageList[0]

	for item in messageList:
		DLC = len(item)
		for ix in range(0, DLC):
			if item[ix] != previous[ix]:
				bitFlip[ix] += 1

	for ix in range(0, DLC):
		bitFlip[ix] = float(bitFlip[ix])/payloadLen
		# eliminate log10(0.0)
		if bitFlip[ix] != 0.0 :
			magnitude[ix] = math.ceil(math.log10(bitFlip[ix]))
		else:
			magnitude[ix] = -100

	return bitFlip,magnitude

def Phase1(magnitude, DLC):
	ref = list()
	prevMagnitude = magnitude[0]
	ixS = 0
	for ix in range(1, DLC):
		if magnitude[ix] < prevMagnitude :
			ref.append((ixS, ix-1))
			ixS = ix
		prevMagnitude = magnitude[ix]
	ref.append((ixS, DLC-1))
	return ref

def Phase2(ref, bitFlip, magnitude):
	rRef = list()
	for sign in ref :
		ixS,ixE = sign
		if (ixE - ixS) > 1 :
			mu = mean(bitFlip[ixS:ixE])
			std = stdev(bitFlip[ixS:ixE])
		else  :
			mu = 0
			std = 0
		if magnitude[ixE] == 0 and matchCounter(bitFlip[ixS:ixE]):
			rRef.append((ixS, ixE, COUNTER))
		elif all(x == 0 for x in magnitude[ixS:ixE]) and 0.5-std <= mu <= 0.5+std:
			rRef.append((ixS, ixE, CRC))
		elif all(x == -100 for x in magnitude[ixS:ixE]):
			rRef.append((ixS, ixE, CONSTANT))
		else :
			rRef.append((ixS, ixE, PHYS))
	return rRef

if __name__=='__main__':
	argvs = sys.argv
	argc = len(argvs)

	if argc < 2:
		print('Usage: python3 %s filename' % argvs[0])
		print('[filename format]\n\t[CAN ID]#[PAYLOAD]\nex)\t000#00000000')
		quit()

	CANtraffic_log = argvs[1]

	canids = list()
	messageLists_11 = [list() for i in range(2048)] # for 11bit CAN
	messageLists_29 = [list() for i in range(2048)] # for 29bit CAN
	ID_num = 0
	canid_len = 0
	CANID11_LEN = 3
	CANID29_LEN = 9
	ID_table = {}

	# create list of canid, list of binary payload 
	with open(CANtraffic_log) as log_file:
		for log in log_file:
			canpacket = log.split("#")
			format_len = '0'+str((len(canpacket[1])-1)*4)+'b'
			payload = format(int(canpacket[1],16), format_len)
			canid_len = len(str(int(canpacket[0], 16)))
			if int(canpacket[0], 16) not in canids :
				if canid_len == CANID11_LEN:
					canids.append(int(canpacket[0], 16))
				elif canid_len == CANID29_LEN:
					ID_table.update({int(canpacket[0], 16):ID_num})
					canids.append(int(canpacket[0], 16))
					ID_num += 1
			if canid_len == CANID11_LEN:
				messageLists_11[int(canpacket[0], 16)].append(payload)
			elif canid_len == CANID29_LEN:
				messageLists_29[ID_table[int(canpacket[0], 16)]].append(payload)
	canids.sort()

	# perform Reverse Engineering of Automotive Data frames
	for canid in canids:
		if canid_len == CANID11_LEN:
			DLC = len(messageLists_11[canid][0])
			bitFlip, magnitude = PreProcessing(messageLists_11[canid], DLC)
		elif canid_len == CANID29_LEN:
			DLC = len(messageLists_29[ID_table[int(canpacket[0], 16)]][0])
			bitFlip, magnitude = PreProcessing(messageLists_29[ID_table[canid]], DLC)
		#print(hex(canid), bitFlip, magnitude)
		ref = Phase1(magnitude, DLC)
		#print(hex(canid), ref)
		rRef = Phase2(ref, bitFlip, magnitude)
		print(hex(canid), rRef)
