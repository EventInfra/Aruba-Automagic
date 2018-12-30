# Aruba-Automagic
Automagical partial (re)configuration of Aruba AP's

## Requirements
This script requires `python3` and the modules listed in `requirements.txt`.
Speech synthesis _(to let the user know which AP has just been reconfigured)_ is optional and requires `espeak`.

Run this on a machine that has python3 installed to install the modules:
```
pip install -r requirements
```

## Usage
The idea is that each instance has it's own serial cable and to parallise the user can open multiple terminals and thus instances.

First find out which tty the serial cable has been assigned to with:
```
ls /dev/ttyUSB*
```

and pass that to the script by running it like this:
```
./aruba-automagic/__init.py__ /dev/ttyUSB0
```

## Normal output
For each (re)configured device this should be in the terminal:
```
Waiting for power... done!
Waiting for boot... done!
Entering the bootloader...done!
Asking for name... PY-AP215-116
Purging all variables... done!
Setting original name... done!
Saving variables... done!
```
