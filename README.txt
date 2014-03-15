ABOUT:

This code is developed and maintained by Nathaniel Knopf, Samuel Sakhai, and Shawn Shirazi

It must be run with Python 2.7

Required Libraries:
	PySerial [https://pypi.python.org/pypi/pyserial]
	decimal [Builtin]
	time [Builtin]
	os [Builtin]
	sys [Builtin]

These three scripts are used to collect data about mouse activity over month long periods of time.

GENERAL METHODOLOGY:

PART I:
	TubeCode.py and WheelCode.py are used in conjunction with each other to gather raw data.

PART II:
	Parsing.py is used to prepare files for use with CLOCKLAB, which generates actograms.

DESCRIPTION OF METHODOLOGY:

PART I:

TubeCode.py:

Each cage requires a separate instance of TubeCode.py to be run. Each version of the script should specify the USB Com Port used by the Arduino specific to that cage, as well as a destination CSV file for the raw data collected. This information is used by PySerial to monitor incoming data, which is then recorded to the CSV file specific to that cage.

WheelCode.py:

One instance of WheelCode.py should be run to cover all cages. In WheelCode.py, the user must specify which USB Com Port is used by the Arduino monitoring Wheel activity. WheelCode.py will then manage wheel revolutions from all cages in use, and will write data to relevant CSV files for each cage. The relevant CSV files should be specified by the user in the WheelCode.py file.

PART II:

We have a variable which tracks the end of the current block (endOfBlock).

We also have a variable which stores the length of time of each block (interval).

When a data point is read from the raw data CSV file, its time is compared to endOfBlock. If it is less than endOfBlock, the data is recorded and the next data point is read. If it is greater than endOfBlock, a line is written to the CLOCKLAB files for the time endOfBlock. The endOfBlock variable is then increased by the value of interval, setting the next endOfBlock. The time from the data point is then checked against the next endOfBlock, to see if there were any lapsed block-periods with no activity. If this is the case, the script continues to write lines and increase the endOfBlock variable to the next endOfBlock until the time from the raw data point is less than the value of endOfBlock (in other words, the data point fits inside the range of the current block).

SPECIAL CASES:


