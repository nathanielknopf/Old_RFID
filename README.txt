README FOR PROJECT MUS
Nathaniel Knopf, Samuel Sakhai, Shawn Shirazi

-----------------------------------------------------------------------------------

TABLE OF CONTENTS:

	1. ABOUT
		1a. REQUIRED LIBRARIES
	2. CONVENTIONS
		2a. CAGE LAYOUT AND SETUP
			2ai. GATES
			2aii. WHEEL
		2b. TOTAL REVOLUTIONS
			2bi. ODOMETER MODE VS. SUMMATIVE MODE
			2bii. TOTAL REVOLUTIONS
			2biii. TOTAL REVOLUTIONS PER BLOCK
		2c. SCALING
			2ci. SCALING VARIABLE
		2d. END OF BLOCK VARIABLE
		2e. CONFIG
	3. BASIC DESCRIPTION OF METHODOLOGY
	4. DETAILED DESCRIPTION OF METHODOLOGY
		4a. PART I (COLLECTION OF RAW DATA)
			4ai. TUBECODE
			4aii. WHEELCODE
		4b. PART II (PARSING RAW DATA FOR CLOCKLAB)
			4bi. BACKGROUND
				4bi1. MOUSE OBJECTS
			4bii. GENERAL ALGORITHM OF PART II
				4bii1. READING RAW DATA
				4bii2. RECORDING PARSED DATA
				4bii3. CHECKING FOR SPECIAL CASES	
	5. OTHER NOTES

-----------------------------------------------------------------------------------

1. ABOUT

Project Mus is an open source project for automatically tracking animal activity over long durations of time.

This project is maintained by Nathaniel Knopf, Samuel Sakhai, and Shawn Shirazi.

All of this code can be run with Python 2.7 only.

----------------------------------------

1a. REQUIRED LIBRARIES
	PySerial [https://pypi.python.org/pypi/pyserial]
	time [Builtin]
	os [Builtin]
	sys [Builtin]

-----------------------------------------------------------------------------------

2. CONVENTIONS

This portion of the README contains conventions that are used in Project Mus

----------------------------------------

2a. CAGE LAYOUT AND SETUP

The setup of each cage contains two RFID coils/antennae ("gates") in a tube through which animals pass, and one wheel with a magnetic switch to count turns. The two "gates" connect to an Arduino/RFID housing (one per cage), and the wheel connects to an Arduino which manages the wheels for all of the cages involved in the experiment. In the cage, the wheel should be completely isolated from the rest of the cage in a way such that animals cannot enter it without passing through the tube containing both gates.

--------------------

2ai. GATES

In order to establish whether the mouse is in the wheel or not, and to help resolve ambiguities, Project Mus uses two "gates" to track the direction the mouse is moving in when it passes into or out of the wheel.

By convention, the gate further from the wheel is called "Gate One", and the gate closer to the wheel is called "Gate Two"

Each RFID gate should be connected to an Arduino/RFID housing. Each antenna connects to a corresponding, labeled plug.

In order to optimize readings and thus the accuracy of the data, the two gates should be tuned with the tuners on the Arduino/RFID housing. Optimal tuning ensures the following things:

* There is no overlap between the ranges the two coils read.

* The ranges of both coils meet in the middle of the tube, with no gap between them.

These ranges must be verified through manual testing with an RFID chip.

--------------------

2aii. WHEEL

Each cage contains one wheel which is fitted with a magnetic switch that is triggered for every revolution of the wheel.

Each wheel plugs into the Arduino which manages the wheels for all of the cages involved in the experiment.

Within the WheelCode.py file, it should be specified which output from the Arduino corresponds to which cage. Outputs from the Arduino come in a string, which is composed of the word "wheel" + the number of the Digital IO pin on the Arduino the wheel switch being triggered corresponds to. For example, if a wheel is plugged into pin 4, and the magnetic switch on the wheel is triggered, the Arduino sends "wheel4" to WheelCode.py. WheelCode.py then writes a data point detailing the time at which this revolution occurred to the CSV file specified in the script.

----------------------------------------

2b. TOTAL REVOLUTIONS

There are two variables which exist for the purpose of counting total wheel revolutions in each cage. 

One variable never gets reset and counts the total revolutions for the entire run of the experiment.

The second variable gets reset at the end of each block, and contains the data which is written to the CLOCKLAB file for the entire cage.

--------------------

2bi. ODOMETER MODE VS. SUMMATIVE MODE

There are two modes for each Total Revolutions variable. These two modes are:

* ODOMETER MODE: This mode is for tracking the physical number of times the wheel rotates. For example, if the wheel turned 10 times while two mice were inside of it, the value stored in the Total Revolutions Variable would be 10 rotations.

* SUMMATIVE MODE: This mode is for tracking the sum of all the rotations each animal caused. For example, if the wheel turned 10 times while two mice were inside of it, the value stored in the Total Revolutions Varibale would be 10 + 10 = 20 rotations.

--------------------

2bii. TOTAL REVOLUTIONS VARIABLE

This is the variable which counts the total revolutions in the cage for the duration of the experiment.

By default, the Total Revolutions Variable 

--------------------

2biii. TOTAL REVOLUTIONS PER BLOCK VARIABLE

----------------------------------------

2c. SCALING

--------------------

2ci. SCALING VARIABLE

----------------------------------------

2d. END OF BLOCK

--------------------

2d1. END OF BLOCK VARIABLE

----------------------------------------

2e. CONFIG

-----------------------------------------------------------------------------------

3. BASIC DESCRIPTION OF METHODOLOGY

In Part I, raw data is collected with TubeCode.py and WheelCode.py in conjunction with the Arduino setup. In Part II, raw data is parsed into a format that can be input into CLOCKLAB for generation of actograms.

-----------------------------------------------------------------------------------

4. DETAILED DESCRIPTION OF METHODOLOGY

----------------------------------------

4a. PART I (COLLECTION OF RAW DATA)

--------------------

4ai. TUBECODE

Information about when mice pass through the RFID "gates" is collected by TubeCode.py

Each cage requires a separate instance of TubeCode.py. Each instance of the script should specify the USB Com Port used by the Arduino specific to that cage, as well as a destination CSV file for the raw data collected. This information is used by PySerial to monitor incoming data, which is then recorded to the CSV file specific to that cage.

--------------------

4aii. WHEELCODE

Only one instance of WheelCode.py needs to be run for all cages. In WheelCode.py, the user must specify which USB Com Port is used by the Arduino monitoring wheel activity. WheelCode.py will then manage input from all wheels in use, and will write data to relevant CSV files for each cage. The relevant CSV files should be specified by the user in the WheelCode.py file.

----------------------------------------

4b. PART II (PARSING RAW DATA FOR CLOCKLAB)

--------------------

4bi. BACKGROUND

----------

4bi1. MOUSE OBJECTS

Each mouse in the cage is treated as an object, referred to from this point forward as a "mouse object". Each "mouse object" has several variables associated with it:

* A variable which stores the RFID Tag as a string (tag)

* Three flags (one for the first gate (gateOne), one for the second gate (gateTwo), and one for whether or not the mouse is in the wheel (inWheel))

* A counter of wheel revolutions attributed to that mouse (one counter for each block of time (ranThisBlock) and one for the total duration of time covered by the raw data (ranTotal))

* The file to which all output data for use with CLOCKLAB is written (file)

--------------------

4bii. GENERAL ALGORITHM OF PART II

----------

4bii1. READING RAW DATA

----------

4bii2. RECORDING PARSED DATA

----------

4bii3. CHECKING FOR SPECIAL CASES

--------------------------------------------------------------------------------

5. OTHER NOTES
