PROJECT MUS
Nathaniel Knopf, Samuel Sakhai, Shawn Shirazi

-----------------------------------------------------------------------------------

TABLE OF CONTENTS:

	1. ABOUT
		1a. REQUIRED LIBRARIES
	2. CONVENTIONS
	3. BASIC DESCRIPTION OF METHODOLOGY
	4. DETAILED DESCRIPTION OF METHODOLOGY
		4a. PART I (COLLECTION OF RAW DATA)
			4ai. TUBECODE
			4aii. WHEELCODE
		4b. PART II (PARSING RAW DATA FOR CLOCKLAB)
			4bi. BACKGROUND
				4bi1. MOUSE OBJECTS
			4bii. GENERAL ALGORITHM OF PART II
				4bii1. READING DATA
				4bii2. RECORDING DATA
				4bii3. CHECKING FOR SPECIAL CASES
					
	5. OTHER NOTES

-----------------------------------------------------------------------------------

1. ABOUT

Project Mus is an open source project for automatically tracking animal activity 
over long durations of time.

This project is maintained by Nathaniel Knopf, Samuel Sakhai, and Shawn Shirazi

All code must be run with Python 2.7

-----------------------------------------------------------------------------------

1a. REQUIRED LIBRARIES
	PySerial [https://pypi.python.org/pypi/pyserial]
	time [Builtin]
	os [Builtin]
	sys [Builtin]

-----------------------------------------------------------------------------------

2. CONVENTIONS

-----------------------------------------------------------------------------------

3. BASIC DESCRIPTION OF METHODOLOGY

In Part I, raw data is collected with TubeCode.py and WheelCode.py in conjunction 
with the Arduino setup. In Part II, raw data is parsed into a format that can be 
input into CLOCKLAB for generation of actograms.

-----------------------------------------------------------------------------------

4. DETAILED DESCRIPTION OF METHODOLOGY

4a. PART I (COLLECTION OF RAW DATA)

4ai. TUBECODE

Information about when mice pass through the RFID "gates" is collected by 
TubeCode.py

Each cage requires a separate instance of TubeCode.py. Each instance of the script 
should specify the USB Com Port used by the Arduino specific to that cage, as well 
as a destination CSV file for the raw data collected. This information is used by 
PySerial to monitor incoming data, which is then recorded to the CSV file specific 
to that cage.

4aii. WHEELCODE

Only one instance of WheelCode.py needs to be run for all cages. In WheelCode.py, 
the user must specify which USB Com Port is used by the Arduino monitoring wheel 
activity. WheelCode.py will then manage input from all wheels in use, and will write 
data to relevant CSV files for each cage. The relevant CSV files should be specified 
by the user in the WheelCode.py file.

4b. PART II (PARSING RAW DATA FOR CLOCKLAB)

4bi. BACKGROUND

4bi1. MOUSE OBJECTS

Each mouse in the cage is treated as an object, referred to from this point forward 
as a "mouse object". Each "mouse object" has several variables associated with it:

* A variable which stores the RFID Tag as a string (tag)

* Three flags (one for the first gate (gateOne), one for the second gate (gateTwo), 
  and one for whether or not the mouse is in the wheel (inWheel))

* A counter of wheel revolutions attributed to that mouse (one counter for each block 
  of time (ranThisBlock) and one for the total duration of time covered by the raw data (ranTotal))

* The file to which all output data for use with CLOCKLAB is written (file)


