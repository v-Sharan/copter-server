#!/usr/bin/python

import os
import datetime

from cuav.lib import cuav_util, mav_position
from datetime import timedelta

# from timestrap import formated_timeStrap


def increment_timestamp_by_seconds(timestamp):
    dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    dt += timedelta(seconds=1)
    return dt.strftime("%Y-%m-%d %H:%M:%S.%f")


def process(timestamp):
    """process a set of files"""
    # count = 0

    mpos = mav_position.MavInterpolator(gps_lag=(0.0))
    mpos.set_logfile(os.path.join(os.getcwd(), "mav3.tlog"))

    frame_time = 0

    start_frame_time = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")
    frame_time = cuav_util.datetime_to_float(start_frame_time)
    try:
        if False:
            roll = 0
        else:
            roll = None
        pos = mpos.position(frame_time, 0.0, roll=0)
    except mav_position.MavInterpolatorException as e:
        print("{0} - {1} ".format(os.path.basename("mav3.tlog"), e))
        # count += 1
        pos = None
    if pos:
        lat_deg = pos.lat
        lng_deg = pos.lon

    print(
        frame_time,
        lat_deg,
        lng_deg,
    )


# main program
if __name__ == "__main__":
    timestamp = "2024-06-29 09:08:29.507528"
    # timestamp = "2024-06-27 16:00:54.334700"
    # timestamp = formated_timeStrap()

    while True:
        process(timestamp)
        timestamp = increment_timestamp_by_seconds(timestamp)
