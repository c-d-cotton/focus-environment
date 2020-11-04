#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}


def main(stoptime):
    import datetime
    import tempfile
    import time

    if not os.path.isdir(tempfile.gettempdir() + '/' + 'focus-environment/'):
        os.mkdir(tempfile.gettempdir() + '/' + 'focus-environment/')

    if stoptime[-2:] == 'am':
        twentyfourhours = False
        afternoon = False
        stoptime = stoptime[:-2]
    elif stoptime[-2:] == 'pm':
        twentyfourhours = False
        afternoon = True
        stoptime = stoptime[:-2]
    else:
        twentyfourhours = True

    if stoptime.count(':') != 1:
        print('time should contain exactly one colon')
        sys.exit(1)

    stoptimesplit = stoptime.split(':')

    hourend = int(stoptimesplit[0])
    minuteend = int(stoptimesplit[1])

    if twentyfourhours is not True and afternoon is True:
        hourend = hourend + 12

    timenow = datetime.datetime.now()

    # getting timestop as datetime
    timestop = datetime.datetime(timenow.year, timenow.month, timenow.day, hour = hourend, minute = minuteend)

    if hourend < timenow.hour or hourend == timenow.hour and minuteend < timenow.minute:
        timestop = timestop + datetime.timedelta(days = 1)

    secondstogo = (timestop - timenow).seconds

    hourstogo = secondstogo // 3600
    minutestogo = (secondstogo - hourstogo * 3600) // 60

    # start on new line
    print('')
    print('The time now is ' + (timenow + datetime.timedelta(minutes = 1)).strftime('%H:%M'))
    print('Focused time stops at ' + timestop.strftime('%H:%M') + ' (' + timestop.strftime('%I:%M %p') + ')')
    print('This is in ' + str(hourstogo) + ' hours and ' + str(minutestogo) + ' minutes')

    with open(tempfile.gettempdir() + '/' + 'focus-environment/focustime.txt', 'w+') as f:
        f.write(timestop.strftime('%H:%M'))

    importattr(__projectdir__ / Path('submodules/linux-whitenoise/noise_func.py'), 'playsound')(secondstogo)

    time.sleep(secondstogo)
    os.remove(tempfile.gettempdir() + '/' + 'focus-environment/focustime.txt')

    


def main_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("stoptime")
    
    args=parser.parse_args()
    #End argparse:}}}

    importattr(__projectdir__ / Path('focus_func.py'), 'main')(args.stoptime)

