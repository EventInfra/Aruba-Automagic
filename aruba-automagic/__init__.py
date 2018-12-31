#!/usr/bin/env python

import sys, time
import serial
from pexpect import fdpexpect

# Speech synthesis is optional and requires espeak (for Linux)
try:
    import pyttsx3
    enable_speech = True
except ImportError:
    enable_speech = False
    

def check_prompt(AP):
    time.sleep(0.1)
    AP.send('\n')
    time.sleep(0.1)
    AP.expect('apboot>')
    time.sleep(0.1)
    AP.send('\n')
    time.sleep(0.1)
    AP.expect('apboot>')


# Create serial connection
AP_serial = serial.Serial(sys.argv[-1], 9600)
AP = fdpexpect.fdspawn(AP_serial)

# Setup TTS
if enable_speech:
    tts = pyttsx3.init()
    tts.say('Started')
    tts.runAndWait()

# Keep on listening, untill the expect timesout (1h)
while True:

    print('\n\n\n\n')

    print('Waiting for power... ', end='', flush=True)
    AP.expect('APBoot ', timeout=3600)
    time.sleep(0.1)
    print('done!')

    # Enter the bootloader
    print('Waiting for boot... ', end='', flush=True)
    AP.expect('Hit <Enter>')
    time.sleep(0.1)
    print('done!')
    time.sleep(0.1)

    print('Entering the bootloader...', end='', flush=True)
    check_prompt(AP)
    print('done!')
    time.sleep(0.1)

    # Get the AP name
    print('Asking for name... ', end='', flush=True)
    AP.send('printenv name\n') # PY-AP215-074
    time.sleep(0.1)
    name = ''
    while name == '':
        input_string = AP.readline().decode("utf-8")
        if input_string[:5] == 'name=':
            name = input_string[5:].strip('\r\n')
            print(name)
    check_prompt(AP)
    time.sleep(0.1)

    # Purge all the variables in one go
    print('Purging all variables... ', end='', flush=True)
    AP.send('purgeenv\n')
    check_prompt(AP)
    print('done!')
    time.sleep(0.1)

    # Put back the name
    print('Setting original name... ', end='', flush=True)
    AP.send('setenv name ' + name + '\n')
    check_prompt(AP)
    print('done!')
    time.sleep(0.1)

    # Save the new variables
    print('Saving variables... ', end='', flush=True)
    AP.send('saveenv\n')
    check_prompt(AP)
    print('done!')
    time.sleep(0.1)

    # Say the number of the AP
    if enable_speech:
        tts.say(str(int(name.split('-')[-1])) + ' done')
        tts.runAndWait()
