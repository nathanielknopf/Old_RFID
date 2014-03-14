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

<do this bit later>
