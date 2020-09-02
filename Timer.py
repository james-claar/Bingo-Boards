"""
Timer/stopwatch application.

"""

import time
from winsound import Beep

stopwatch_bool = input("stopwatch? y/n ")


def int_fill(self, depth):
    return str(self).zfill(depth)

def format_seconds(seconds):
    if seconds < 0:
        seconds = abs(seconds)
        negative_result = True
    else:
        negative_result = False

    old_seconds = seconds
    minutes = 0
    hours = 0

    while seconds >= 60:
        seconds -= 60
        minutes += 1
    while minutes >= 60:
        minutes -= 60
        hours += 1

    if old_seconds < 60:
        result = str(seconds) + "s"
    elif 3600 > old_seconds >= 60:
        result = str(minutes) + ":" + str(seconds).zfill(2)
    else:
        result = str(hours) + ":" + str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

    if not negative_result:
        return result
    else:
        return "-" + result

if stopwatch_bool == "y":
    old_time = time.time()
    while True:
        new_time = time.time()
        print(format_seconds(int(new_time - old_time)))
        time.sleep(1)
else:
    duration = input("Example: 2:10:05. Countdown duration in hh:mm:ss, mm:ss, or ss? ")
    duration = duration.split(":")
    duration = list(map(int, duration))
    if len(duration) == 1:
        countdown = duration = int(duration[0])
    elif len(duration) == 2:
        countdown = duration = int((duration[0] * 60) + duration[1])
    elif len(duration) == 3:
        countdown = duration = int((duration[0] * 3600) + (duration[1] * 60) + duration[2])
    else:
        countdown = None
        exit("Duration is not defined.")
    old_time = time.time()
    first_iteration = True
    while True:
        new_time = time.time()
        if countdown > 0:
            countdown = duration - (new_time - old_time)
            if first_iteration:
                print(format_seconds(int(countdown)))
                first_iteration = False
            else:
                print(format_seconds(int(countdown) + 1))
            time.sleep(1)
        else:
            for i in range(10):
                new_time = time.time()
                countdown = duration - (new_time - old_time)
                print(format_seconds(int(countdown)))
                for b in range(4):
                    Beep(2000, 100)
                time.sleep(0.6)
            exit(0)

