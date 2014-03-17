# Nathaniel Knopf
# 3/17/2014
#
# This script loads a GUI for entering info into the CONFIG file.
# The CONFIG file is then saved in the local directory as config.txt

from Tkinter import *

root = Tk()

leftFrame = Frame(root)
rightFrame = Frame(root)
bottomFrame = Frame(root)

def writeToFile(tag1, tag2, tag3, tag4, csv, scale, interval, odometer):
	if odometer == 'y':
		odometer = '1'
	elif odometer == 'n':
		odometer = '0'
	configFile = open('config.txt', 'w')
	configFile.write('ENTER INFORMATION AFTER DESCRIPTOR. LEAVE SPACE AFTER DESCRIPTOR BEFORE RELEVANT INPUT.\n')
	configFile.write('TAG ONE  : ' + tag1 + '\n')
	configFile.write('TAG TWO  : ' + tag2 + '\n')
	configFile.write('TAG THREE: ' + tag3 + '\n')
	configFile.write('TAG FOUR : ' + tag4 + '\n')
	configFile.write('CSV FILE : ' + csv + '\n')
	configFile.write('INTERVAL : ' + interval + '\n')
	configFile.write('SCALE    : ' + scale + '\n')
	configFile.write('ODOMETER : ' + odometer + '\n')
	configFile.close()

def done():
	isGood = True
	errors = []
	tag1 = tag1Entry.get()
	tag2 = tag2Entry.get()
	tag3 = tag3Entry.get()
	tag4 = tag4Entry.get()
	csv = csvEntry.get()
	if csv[-4:] != '.csv':
		csv += '.csv'
	scale = scaleEntry.get()
	interval = intervalEntry.get()
	odometer = odometerEntry.get()
	if (tag1 == '' and tag2 == '' and tag3 == '' and tag4 == ''):
		errors.append("You must enter at least one RFID Tag")
		isGood = False
	if csv == '':
		errors.append("You must enter the CSV file storing the raw data.")
		isGood = False
	if scale == '':
		errors.append("You must enter a value for the Scaling Variable")
		isGood = False
	if interval == '':
		errors.append("You must enter a value for the interval")
		isGood = False
	if (odometer != 'y' and odometer != 'n'):
		errors.append("You must input either 'y' or 'n' for the Odometer Mode")
		isGood = False
	if isGood:
		print "Writing to file"
		writeToFile(tag1, tag2, tag3, tag4, csv, scale, interval, odometer)
		print "Done!"
		root.destroy()
	else:
		for error in errors:
			print error
		
tag1Label = Label(leftFrame, text="Mouse One Tag")
tag1Label.pack()

tag1Entry = Entry(leftFrame)
tag1Entry.pack()

tag3Label = Label(leftFrame, text="Mouse Three Tag")
tag3Label.pack()

tag3Entry = Entry(leftFrame)
tag3Entry.pack()

csvLabel = Label(leftFrame, text="CSV File")
csvLabel.pack()

csvEntry = Entry(leftFrame)
csvEntry.pack()

scaleLabel = Label(leftFrame, text="Scaling Variable")
scaleLabel.pack()

scaleEntry = Entry(leftFrame)
scaleEntry.pack()

tag2Label = Label(rightFrame, text="Mouse Two Tag")
tag2Label.pack()

tag2Entry = Entry(rightFrame)
tag2Entry.pack()

tag4Label = Label(rightFrame, text="Mouse Four Tag")
tag4Label.pack()

tag4Entry = Entry(rightFrame)
tag4Entry.pack()

intervalLabel = Label(rightFrame, text="Interval")
intervalLabel.pack()

intervalEntry = Entry(rightFrame)
intervalEntry.pack()

odometerLabel = Label(rightFrame, text = "Odometer Mode (y/n)")
odometerLabel.pack()

odometerEntry = Entry(rightFrame)
odometerEntry.pack()

doneButton = Button(bottomFrame, text="DONE", command=done)
doneButton.pack()

leftFrame.pack(side=LEFT)
rightFrame.pack(side=RIGHT)
bottomFrame.pack(side=BOTTOM)

mainloop()
