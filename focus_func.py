#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')


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

    sys.path.append(str(__projectdir__ / Path('submodules/linux-whitenoise/')))
    from noise_func import playsound
    playsound(secondstogo)

    time.sleep(secondstogo)
    os.remove(tempfile.gettempdir() + '/' + 'focus-environment/focustime.txt')

    


def main_ap():
    #Argparse:{{{
    import argparse
    
    parser=argparse.ArgumentParser()
    parser.add_argument("stoptime")
    
    args=parser.parse_args()
    #End argparse:}}}

    main(args.stoptime)

