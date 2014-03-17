# March 17th, 2014
#
# Changes:
# * Removed ASCII Date/Time from Raw Data - Useless

import serial
from time import time
from time import asctime
from decimal import *

connection = serial.Serial('/dev/ttyACM0', 9600)

dataFileName = 'data1.csv' # Include .csv extension

# Returns the time since the Epoch in seconds as a string
# Also returns ASCII Time
# Quantized to two decimal places
def getTime():
	twoPlaces = Decimal(10) ** -2 #for quantizing 2 decimal places
	timeDec = Decimal(time()).quantize(twoPlaces) # Time since Epoch in seconds
	timeString = str(timeDec) #converts to a string for recording in the CSV
	return timeString

# Sets up the data file
# Includes header with start time
f = open(dataFileName, 'a')
f.write('START TIME: ' + str(time()) + '\n')
f.close()

def main():
	while True:
		try:
			# Read the incoming line
			line = connection.readline()
			# print line[:-1]
			tag = line[3:-4]
			gate = line[-3:-2]
			# print tag
			# print gate
			timeEpoch = getTime()
			data = open(dataFileName, 'a')
			data.write('"' + tag + '","' + gate + '","' + timeEpoch + '"\n')
			data.close()
			print tag + " " + gate + " " + timeEpoch

		except:
			pass

main()

