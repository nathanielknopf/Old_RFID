# 03/16/2014 - V_0.2.0b
# This script parses raw data created by TubeCode.py and WheelCode.py for use with CLOCKLAB.
#
# IN THIS VERSION:
# * Spared user from having to open code by implementing new functions for collecting necessary
#   prerequisite data from user modified text file.
# * Eliminated errors with inconsistencies in parsed data.
# * Heavily commented to maxamize comprehensibility and to minimize ambiguity in interpreting
#   methodology/functionality.
# * No longer prints the count of data points - significantly quickens run time
#
# For a highly-detailed description of the methodology implemented by this script, check the README
# 
# If this code works, it was written by Nathaniel Knopf.
# If it doesn't, I have no idea who wrote it.
#
# TODO:
# * OPTIMIZE CODE AND WRITE DOCUMENTATION

# Required Libraries:
import time
from os import system
import sys

# A counter which tracks the total revolutions in the current block.
# By convention, this is the actual number of turns. However, it's functionality
# can be changed in the CONFIG file. When this number is written to a CLOCKLAB
# file, its value is changed as described in the functionality of the Scaling variable
# in the README. This variable can function in either of two modes. To see descriptions 
# of the two modes, check the README.
totalRevolutionsBlock = 0.0

# Similar to totalRevolutionsBlock, but is never set to 0, and is never recorded.
totalRevolutions = 0.0

months = {'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'May': '05', 'Jun': '06', 
                        'Jul': '07', 'Aug': '08', 'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'}

# A function which waits while information is displayed on the screen
# Displays time remaining in wait period on the last line displayed in Terminal
def wait(text, seconds):
	while seconds > 0:
		toPrint = text + str(seconds)
		sys.stdout.write('%s\r' % toPrint)
		sys.stdout.flush()
		time.sleep(1)
		seconds -= 1

# These two functions find the date and the time in the preferred format for CLOCKLAB
# The input is the time since the Epoch in seconds. This is how time is recorded in the
# raw data.
def findAscDate(timeEpoch):
        ascRaw = time.ctime(timeEpoch)
        ascDate = ascRaw[-2:] + '/' +  months[ascRaw[4:7]] + '/' + ascRaw[8:10]
        return ascDate 

def findAscTime(timeEpoch):     
        ascRaw = time.ctime(timeEpoch)
        ascTime = ascRaw[11:19] + '.00'
        return ascTime

# For creating objects for each mouse --
# In this version of the Parsing Code, each mouse has its own object, in which relevant
# variables are stored. These include the tag, flags for the two gates, a flag for state
# of in/out of the wheel, a counter for wheel revolutions attributed to the specific
# mouse in the current block of time, and a counter for total revolutions attributed to the
# specific mouse. The file to which parsed data is written is also stored as an object
# within the mouse object.
class Mouse:
	# Called when an instance of Mouse class is created (i.e. new mouse object)
	# Sets defaults to vars, as well as opens the file for parsed data
	def __init__(self, inputTag):
		self.tag = inputTag
		self.gateOne = False
		self.gateTwo = False
		self.inWheel = False
		self.ranThisBlock = 0.0
		self.ranTotal = 0.0
		self.file = self.makeFile()

	# Makes a file for the mouse and writes headers to it for CLOCKLAB
	def makeFile(self):
		filename = self.tag + '.txt'
		mouseFile = open(filename, 'w')
		mouseFile.write('GROUP ' + self.tag + '                                                                                 :\n\n---------\nUNIT TIME=\n')
		return mouseFile              
	
	# Switches values of Boolean Vars (for gates)
	def switchValue(self, gate):
		if gate == '1':
			self.gateOne = not self.gateOne
		elif gate == '2':
			self.gateTwo = not self.gateTwo

	# Counts a turn for the specific mouse if it's in the wheel.
	# Adds to both the current block and the total counters.
	def countTurn(self):
		if self.inWheel:
			self.ranThisBlock += 1
			self.ranTotal += 1

	# Function which writes a data point to the file for CLOCKLAB
	def writeLine(self, dateAsc, timeAsc, scale):
		self.ranThisBlock = self.ranThisBlock / scale
		self.file.write(dateAsc + ' ' + timeAsc + '     ' + str(self.ranThisBlock) + '\n')

	# Function called at the end of the block - Clears data for that block period
	def finishBlock(self):
		self.ranThisBlock = 0.0

# Given the file in which configs are stored, pulls all needed data from config file.
def getConfigs(fileName):
	configs = []
	configsFile = open(fileName, 'r')
	configsFile.readline()
	for line in configsFile:
		configs.append(line[11:-1])
	return configs

# Called when newParsing.py is run - creates mouse objects and loads/stores configs
def setup():
	# Begins by loading configs
	try:
		configs = getConfigs('config.txt') # Default file for configs
	except IOError:
		# configs are not stored in configs.txt:
		configsFileName = raw_input("Enter configs file: (Include the file extension) ")
		configs = getConfigs(configsFileName)
	except:
		print "ERROR - FATAL: CONFIGS" # Error in collecting configs

	# Configure mouseOne
	print "Configuring MouseOne:"
	global mouseOne
	mouseOne = Mouse(configs[0])
	print "Tag: " + mouseOne.tag + "\n"
	
	# Configure mouseTwo
	print "Configuring MouseTwo:"
	global mouseTwo
	mouseTwo = Mouse(configs[1])
	print "Tag: " + mouseTwo.tag + "\n"

	# Configure mouseThree
	print "Configuring MouseThree:"
	global mouseThree
	mouseThree = Mouse(configs[2])
	print "Tag: " + mouseThree.tag + "\n"

	# Configure mouseFour
	print "Configuring MouseFour:"
	global mouseFour
	mouseFour = Mouse(configs[3])
	print "Tag: " + mouseFour.tag + "\n"

	# A list of the mouse objects - Used later in the code to iterate through mouse objects
	global mice
	mice = [mouseOne, mouseTwo, mouseThree, mouseFour]

	# Open raw data from CSV file specified in configs.
	global csvfile
	csvFilename = configs[4]
	if csvFilename[-4:] != '.csv':
		csvFilename += '.csv'
	print "CSV File: " + csvFilename + "\n"
	try:
		csvfile = open(csvFilename, 'r')
		print csvfile + " opened successfully."
	except IOError:
		# Could not find CSV File
		print "ERROR - FILE DOES NOT EXIST IN LOCAL DIRECTORY"
	except:
		print "ERROR - FATAL ERROR: CSVFILE" # Error in finding raw data

	# Interval - Length of block in seconds.
	global interval
	interval = float(configs[5])
	print "Interval: " + str(interval) + "\n"

	# endOfBlock - Time at which the block ends and data is recorded
	# Value is determined by adding interval to the START TIME logged in the CSV file.
	global endOfBlock	
	endOfBlock = float(csvfile.readline()[12:25]) + interval
	print "End of Block: " + str(endOfBlock) + "\n"

	# Scale factor - necessary for CLOCKLAB as all values >=1000 are ignored.
	# Results are scaled by a factor of 1/scale before being written to the CLOCKLAB files.
	global scale
	scale = float(configs[6])
	print "Scale: " + str(scale) + "\n"

	# Odometer vs. Summative mode for counting rotations in the cage
	# Is set to either 0 or 1 in the configs
	# If 1, odometerMode = True (counter in odometer mode)
	# If 0, odometerMode = False (counter in summative mode)
	global odometerMode
	odometerMode = bool(int(configs[7]))
	

	# Open the cage.txt file where info about the cage is stored
	global cageFile
	cageFile = open('cage.txt', 'w')
	cageFile.write('GROUP CAGE                                                                           :\n\n---------\nUNIT TIME=\n')
	print "Cage File has been created and opened.\n"

	wait("Beginning Parsing... ", 5)

	system('clear')

# This function checks for cases (typical and atypical) detailed in the README
# Function takes a list of mouse objects as input - Accommodates any length list 
# (i.e. any number of mice objects)
def checkCases(mice):
	# Iterate through all mice objects in the list of mice
	for mouse in mice:
		# CASE ONE - Gate One and Gate Two flags are both set to True
		if (mouse.gateOne and mouse.gateTwo):
			# RESULT - Mouse is in the wheel
			mouse.inWheel = True
		# CASE TWO - Gate One and Gate Two flags are both set to False
		elif (not(mouse.gateOne) and not(mouse.gateTwo)):
			# RESULT - Mouse is not in the wheel
			mouse.inWheel = False
		# CASE THREE - Gate One is False, Gate Two is True, and inWheel Flag is False
		elif (not(mouse.gateOne) and mouse.gateTwo and not(mouse.inWheel)):
			# RESULT - Mouse is in the wheel (ALSO: Set Gate One Flag to True)
			mouse.inWheel = True
			mouse.gateOne = True
		# CASE FOUR - Gate One is False, Gate Two is True, and inWheel Flag is True
		elif (not(mouse.gateOne) and mouse.gateTwo and mouse.inWheel):
			# RESULT - Mouse is not in the wheel (ALSO: Set Gate Two Flag to False)
			mouse.inWheel = False
			mouse.gateTwo = False

# This function writes data to all the files for CLOCKLAB when called
# Called at the end of each block in which data was recorded
# Takes a list of mouse objects as input
def writeData(mice):
	global totalRevolutionsBlock
	global scale
	global endOfBlock
	totalRevolutionsBlock = totalRevolutionsBlock / scale
	dateAsc = findAscDate(endOfBlock)
	timeAsc = findAscTime(endOfBlock)
	for mouse in mice:
		mouse.writeLine(dateAsc, timeAsc, scale)
		mouse.finishBlock()
	cageFile.write(dateAsc + ' ' + timeAsc + '     ' + str(totalRevolutionsBlock) + '\n')
	totalRevolutionsBlock = 0.0

# This function counts a turn for all mice that are in the wheel. It also
# adds a turn to the totalRevolutions and totalRevolutionsBlock counters.
# The first step in this functions is to check if any mice are in the wheel.
# For each mouse in the wheel, countTurn() adds to the mouses's counters.
# The second step is to update the totalRevolutions and totalRevolutionsBlock
# variables. The program checks to see if 
def countTurn(mice):
	global totalRevolutions
	global totalRevolutionsBlock
	global odometerMode
	doesAdd = False
	for mouse in mice:
		if mouse.inWheel:
			doesAdd = True
			mouse.countTurn()
	if doesAdd:
		if odometerMode:
			totalRevolutions += 1
			totalRevolutionsBlock += 1
		else:
			numMice = 0
			for mouse in mice:
				if mouse.inWheel:
					numMice += 1
			for i in range(numMice):
				totalRevolutions += 1
				totalRevolutionsBlock += 1

# This function updates flags every time a tag is read from the raw data.
def updateMiceFlags(tag, gate, mice):
	for mouse in mice:
		if mouse.tag == tag:
			mouse.switchValue(gate)
	# The script then checks for any typical/atypical cases, and resolves them.
	checkCases(mice)

# The main function which reads a line and parses it.
# It returns two values - the status of the program (if it is done parsing), and
# the endOfBlock variable.
def parseLine():
	global interval
	global endOfBlock
	# Read the next data point from the CSV File
	data = csvfile.readline()
	# If the file is finished, the next line will be blank.
	if data == '':
		return 'done' # We're done here.
	else:
		# If the data point is the wheel turning
		if data[1:6] == "wheel":		
			timeEpoch = float(data[13:26])
			# If this data is still within the current block:
			if timeEpoch < endOfBlock:
				countTurn(mice)
			# If it is not:
			else:
				# First, write the last line and increase endOfBlock by interval.
				writeData(mice)
				endOfBlock += interval
				# Then, check to see if more than one block has passed.
				# While there are still empty blocks, write lines.
				# Then, continue as normal.
				while (timeEpoch > endOfBlock):
					# Write a blank line for endOfBlock
					# This is accomplished by writing a line like normal, since
					# all of the counters for the current empty block are at zero.
					writeData(mice)
					# Then, increase endOfBlock by interval.
					endOfBlock += interval
				# Once the new block has been made, record the data point.
				countTurn(mice)
		# If the data point is a gate being triggered		
		else:
			try:
				timeEpoch = float(data[24:37])
				# If this data is still within the current block:
				if timeEpoch < endOfBlock:
					tag = data[1:17]
					gate = data[20]
					updateMiceFlags(tag, gate, mice)
				# If it is not
				else:
					# First, write the last line and increase endOfBlock
					writeData(mice)
					endOfBlock += interval
					# Then, check to see if more than one block has passed.
					# While there are still empty blocks, write lines.
					# Then, continue as normal.
					while (timeEpoch > endOfBlock):
						# Write a blank line for endOfBlock
						# This is accomplished by writing a line like normal,
						# since all of the counters for the current empty
						# block are at zero.
						writeData(mice)
						# Then, increase endOfBlock by interval.
						endOfBlock += interval
					# Once the new current block has been made, record the data
					tag = data[1:17]
					gate = data[20]
					updateMiceFlags(tag, gate, mice)
			except:
				print "ERROR - LINE: " + data + '\n'
		return 'not done'

def main():

	system('clear')	
	setup()

	done = False
	while not done:
		status = parseLine()
		if status == 'done':
			done = True

	# Save and close all the files for CLOCKLAB.
	for mouse in mice:
		mouse.file.close()
	cageFile.close()

	print "Parsing is complete."

main()
