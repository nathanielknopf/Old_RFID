# March 17th, 2014
#
# Changes:
# * Added 'cages' dictionary which matches Arduino input to cage number. This allows for
#   more flexibility down the line.

import serial
from time import time
from time import asctime
from decimal import *

port = '/dev/ttyACM0'

cages = {'wheel1': 1, 'wheel2': 2, 'wheel3': 3, 'wheel4': 4, 'wheel5': 5, 'wheel6': 6, 'wheel7': 7}

# This function returns the time since the Epoch in seconds as a string.
# It fixes the value to two places past the decimal.
def getTime():
	twoPlaces = Decimal(10) ** -2 # For quantizing 2 decimal places
	timeDec = Decimal(time()).quantize(twoPlaces) # Time since Epoch in Seconds
	timeString = str(timeDec) # Converts to a string for recording in the CSV
	return timeString

def writeToFile(fileNum):
	timeRead = getTime()
	file = open('data' + str(fileNum) + '.csv', 'a')
	file.write('"wheel","-","' + timeRead + '","' + str(asctime()) + '"\n')
	file.close()

try:
	connection = serial.Serial(port, 9600)
except:
	print('NO CONNECTION ESTABLISHED WITH WHEEL')

while True:
    line = connection.readline()
    if line[:6] == "wheel1":
        writeToFile(cages['wheel1'])
        print("wheel1 " + str(asctime()))
    elif line[:6] == "wheel2":
        writeToFile(cages['wheel2'])
        print("wheel2 " + str(asctime()))
    elif line[:6] == "wheel3":
        writeToFile(cages['wheel3'])
        print("wheel3 " + str(asctime()))
    elif line[:6] == "wheel4":
        writeToFile(cages['wheel4'])
        print("wheel4 " + str(asctime()))
    elif line[:6] == "wheel5":
        writeToFile(cages['wheel5'])
        print("wheel5 " + str(asctime()))
    elif line[:6] == "wheel6":
        writeToFile(cages['wheel6'])
        print("wheel6 " + str(asctime()))
    elif line[:6] == "wheel7":
        writeToFile(cages['wheel7'])
        print("wheel7 " + str(asctime()))
