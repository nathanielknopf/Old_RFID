DOCUMENTATION FOR PROJECT MUS
Nathaniel Knopf, Samuel Sakhai, Shawn Shirazi
3/16/2014

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
		2d. INTERVAL AND END OF BLOCK
			2di. INTERVAL VARIABLE
			2dii. END OF BLOCK VARIABLE
		2e. OTHER TERMINOLOGY
		2f. CONFIG
	3. BASIC DESCRIPTION OF METHODOLOGY
		3a. PART I (COLLECTION OF RAW DATA)
		3b. PART II (PARSING RAW DATA FOR CLOCKLAB)
	4. DETAILED DESCRIPTION OF METHODOLOGY
		4a. PART I (COLLECTION OF RAW DATA)
			4ai. TUBECODE
			4aii. WHEELCODE
		4b. PART II (PARSING RAW DATA FOR CLOCKLAB)
			4bi. BACKGROUND
				4bi1. MOUSE OBJECTS
				4bi2. GLOBAL VARIABLES
			4bii. GENERAL ALGORITHM OF PART II
				4bii1. SETUP
				4bii2. READING RAW DATA
				4bii3. RECORDING PARSED DATA
			4biii. SPECIAL CASES
				4biii1. MULTIPLE BLOCKS OF INACTIVITY
				4biii2. SPECIAL CASES OF MOUSE FLAGS
	5. BEFORE RUNNING
	6. OTHER NOTES

-----------------------------------------------------------------------------------

1. ABOUT

Project Mus is an open source project for automatically tracking animal activity over long durations of time.

This project is maintained by Nathaniel Knopf, Samuel Sakhai, and Shawn Shirazi.

Python 2.7 is required to run all of the code from Project Mus.

----------------------------------------

1a. REQUIRED LIBRARIES
	
The following Python 2.7 libraries are required to run code from Project Mus

* PySerial [https://pypi.python.org/pypi/pyserial]

* time [Builtin]

* os [Builtin]

* sys [Builtin]

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

By default, the Total Revolutions counters function in Odometer mode. This can be changed in the CONFIG file. For details on how to change this, check section 2f. CONFIG.

--------------------

2bii. TOTAL REVOLUTIONS VARIABLE

This is the variable which counts the total revolutions in the cage for the duration of the experiment.

By default, the Total Revolutions Variable functions in Odometer mode.

--------------------

2biii. TOTAL REVOLUTIONS PER BLOCK VARIABLE

This is the variable which counts the total revolutions in the cage for each block of time. The value stored in this variable is what gets written to the CLOCKLAB file for the entire cage.

By default, the Total Revolutions per Block variable functions in Odometer mode.

----------------------------------------

2c. SCALING

In order to accommodate for CLOCKLAB's ignoring of values >999, Project Mus includes a Scaling function. This function scales all wheel rotation values down to a value which CLOCKLAB will not ignore.

When writing to a file, Parsing.py will divide each value by the Scaling variable. For example, if the Total Revolutions Per Block variable reports 1543 rotations in the block being written to the CLOCKLAB files, and the Scaling variable stores the value "10.0", Parsing.py will write 154.3 rotations to the CLOCKLAB file for the entire cage.

--------------------

2ci. SCALING VARIABLE

When writing to a file, Parsing.py will divide each value by the Scaling variable. For example, if the Total Revolutions Per Block variable reports 1543 rotations in the block being written to the CLOCKLAB files, and the Scaling variable stores the value "10.0", Parsing.py will write 154.3 rotations to the CLOCKLAB file for the entire cage.

The value of the Scaling variable can be changed in the CONFIG file.

----------------------------------------

2d. INTERVAL AND END OF BLOCK

Parsing.py records parsed data in blocks of time specified by the user. Each block of time's duration is expressed in seconds by the Interval variable.

--------------------

2di. INTERVAL VARIABLE

This is the variable which expresses the duration of each block of time. It can be changed in the CONFIG file.

--------------------

2dii. END OF BLOCK VARIABLE

This is a variable used by the Parsing.py script to determine whether each raw data point that it reads falls within the current block of time. 

When Parsing.py reads a raw data point from the CSV file which occurred at a time before the time stored in the End of Block variable, it extracts the relevant information from the raw data and updates whatever the raw data dictates. If the raw data point occurred at a time after the time stored in the End of Block variable, Parsing.py will interpret this as meaning that the block it was working in has come to its conclusion. It will then record the parsed data to the files for CLOCKLAB. If several blocks of time have passed with no activity, Parsing.py will account for this in the CLOCKLAB files as well. To see a detailed description of how Parsing.py does this, check section 4biii1. MULTIPLE BLOCKS OF INACTIVITY.

----------------------------------------

2e. OTHER TERMINOLOGY

Various other terminology used in Project Mus:

* BLOCK - The duration of time for each data point for the CLOCKLAB files. Determined by the Interval variable in the CONFIG file.

* RAW DATA - The data produced by the scripts in PART I (TubeCode.py and WheelCode.py). This raw data is then parsed by Parsing.py in preparation for use with CLOCKLAB.

* PARSED DATA - The files which are created by Parsing.py for use with CLOCKLAB.

----------------------------------------

2f. CONFIG

The CONFIG file contains prerequisite settings and data which Parsing.py needs to parse the data for CLOCKLAB. This includes:

* The RFID tags for each animal in the cage

* The name of the CSV file containing raw data (must include .csv extension)

* The desired interval (length of each block) for the data to be recorded in.

* The desired scaling variable for the data to be recorded with, as described in section 2c. SCALING.

* Whether the Total Revolutions counters should function in Odometer mode or Summative mode. A value of '1' in the CONFIG sets the counters to Odometer mode. A value of '0' sets them to Summative mode.

The format of the CONFIG file must be exactly as follows:

ENTER INFORMATION AFTER DESCRIPTOR. LEAVE SPACE AFTER DESCRIPTOR BEFORE RELEVANT INPUT.
TAG ONE  : RFID TAG
TAG TWO  : RFID TAG
TAG THREE: RFID TAG
TAG FOUR : RFID TAG
CSV FILE : FILE NAME WITH .CSV EXTENSION
INTERVAL : INTERVAL TIME IN SECONDS
SCALE    : SCALE VALUE
ODOMETER : 1 FOR ODOMETER MODE, 0 FOR SUMMATIVE MODE

Replace the text after the colon with your specific information. Make sure to leave a space between the colon and your information. 

-----------------------------------------------------------------------------------

3. BASIC DESCRIPTION OF METHODOLOGY

----------------------------------------

3a. PART I (COLLECTION OF RAW DATA)

In Part I, raw data is collected with TubeCode.py and WheelCode.py in conjunction with the Arduino setup. This raw data includes the triggering of gates by specific mice (differentiated by their RFID tags), rotations of the wheels in each cage, and the times at which such events occurred.

----------------------------------------

3b. PART II (PARSING RAW DATA FOR CLOCKLAB)

In Part II, raw data is parsed into a format that can be input into CLOCKLAB for generation of actograms.

-----------------------------------------------------------------------------------

4. DETAILED DESCRIPTION OF METHODOLOGY

In this section, the workings of Project Mus are described in detail.

Section 4a. PART I details the process by which Project Mus collects raw data.

Section 4b. PART II details the process by which Project Mus processes the raw data collected in PART I in preparation for use with CLOCKLAB.

----------------------------------------

4a. PART I (COLLECTION OF RAW DATA)

Raw data is collected by two scripts - TubeCode.py, and WheelCode.py. These two scripts create a CSV file for each cage which contains raw data which is then parsed by Parsing.py for use with CLOCKLAB. Each CSV file begins with a line that includes the time at which data collection began for that cage. This line is then used by Parsing.py as the beginning of the first block.

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

This section contains background information that is useful for understanding the methodology implemented by PART II of Project Mus.

Includes:

* Mouse Objects

* Global Variables

----------

4bi1. MOUSE OBJECTS

Each mouse in the cage is treated as an object, referred to from this point forward as a "mouse object". Each "mouse object" has several variables associated with it:

* A variable which stores the RFID Tag for the specific mouse as a string (tag).

* Three flags (one for the first gate (gateOne), one for the second gate (gateTwo), and one for whether or not the mouse is in the wheel (inWheel)) These flag variables are booleans, and their status is switched whenever the RFID gate they correspond to is triggered.

* A counter of wheel revolutions attributed to that mouse (one counter for each block of time (ranThisBlock) and one for the total duration of time covered by the raw data (ranTotal)).

* The file to which all output data for use with CLOCKLAB is written (file). This file is opened when Parsing.py begins, and is saved and closed when Parsing.py finishes.

Parsing.py maintains a list of these mouse objects called "mice", which it uses to iterate through all mouse objects when running functions.

----------

4bi2. GLOBAL VARIABLES

Parsing.py establishes the following global variables when it is run, and uses/updates them throughout the code.

* "mouseOne", "mouseTwo", "mouseThree", "mouseFour" - Mouse objects.

* "mice" - A list of mouse objects, used for iterating through all mouse objects.

* "csvfile" - The CSV file containing raw data.

* "interval" - The length of each block of time.

* "endOfBlock" - The time at which the current block ends.

* "scale" - The factor by which each value written to the CLOCKLAB files is scaled.

* "odometerMode" - Whether or not Total Revolutions counters function in Odometer mode. This is a boolean (True or False)

* "cageFile" - Similar to the files opened by each mouse object, except it tracks the activity for the entire cage using the Total Revolutions counters.

--------------------

4bii. GENERAL ALGORITHM OF PART II

PART II consists of the execution of Parsing.py, which parses the raw data created in PART I, and prepares it for use with CLOCKLAB.

The Parsing script is split into three parts:

* Setup

* Reading Raw Data

* Recording Parsed Data

The second and third steps are repeated until all raw data has been parsed.

----------

4bii1. SETUP

The setup of PART II includes:

* The extraction of configurations from the CONFIG file.

* The creation of mouse objects and other global variables described in section 4bi2. GLOBAL VARIABLES.

Extracting configurations:

Parsing.py will check for configurations stored in 'config.txt' in the local directory. If no such file can be found, Parsing.py will prompt the user for the name of the CONFIG file.

----------

4bii2. READING RAW DATA

----------

4bii3. RECORDING PARSED DATA

--------------------

4biii. SPECIAL CASES

----------

4biii1. MULTIPLE BLOCKS OF INACTIVITY

----------

4biii2. SPECIAL CASES OF MOUSE FLAGS

--------------------------------------------------------------------------------

5. BEFORE RUNNING

--------------------------------------------------------------------------------

6. OTHER NOTES

Please send all questions and/or comments to nathanielknopf@gmail.com. We will get back to you as quickly as possible.
