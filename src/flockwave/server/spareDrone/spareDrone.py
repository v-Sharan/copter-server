#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function

from dronekit import LocationGlobalRelative, LocationGlobal, Command, connect
import math
from pymavlink import mavutil
import csv

error_flag = 0

distance = [0 for _ in range(20)]
turns = [0 for _ in range(20)]
times = [0 for _ in range(20)]
points = [0 for _ in range(20)]


def get_location_metres(original_location, dNorth, dEast):

    earth_radius = 6378137.0
    dLat = dNorth / earth_radius
    dLon = dEast / (earth_radius * math.cos(math.pi * original_location.lat / 180))

    newlat = original_location.lat + (dLat * 180 / math.pi)
    newlon = original_location.lon + (dLon * 180 / math.pi)
    return LocationGlobal(newlat, newlon, original_location.alt)


def get_distance_metres(aLocation1, aLocation2):

    dlat = aLocation2.lat - aLocation1.lat
    dlong = aLocation2.lon - aLocation1.lon
    return math.sqrt((dlat * dlat) + (dlong * dlong)) * 1.113195e5


def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0  # Earth radius in meters

    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    # Calculate differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad

    # Haversine formula
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c

    return distance


def distance_to_current_waypoint(vehicle):

    nextwaypoint = vehicle.commands.next
    if nextwaypoint == 0:
        return None
    missionitem = vehicle.commands[nextwaypoint - 1]
    lat = missionitem.x
    lon = missionitem.y
    alt = missionitem.z
    targetWaypointLocation = LocationGlobalRelative(lat, lon, alt)
    distancetopoint = get_distance_metres(
        vehicle.location.global_frame, targetWaypointLocation
    )
    return distancetopoint


def download_mission(vehicle):

    cmds = vehicle.commands
    cmds.download()
    cmds.wait_ready()


def adds_square_mission(mission=1, uav=1, altitude=30):
    ip_address = {
        1: [
            "14561",
            "C:/Users/vshar/OneDrive/Documents/sharan/DCE/dec-8drones/csv_15/dec_d2.csv",
        ]
    }

    try:
        vehicle = connect(
            "udpin:192.168.0.127:" + str(ip_address[uav][0]), heartbeat_timeout=3
        )
    except Exception as e:
        raise Exception(e)

    cmds = vehicle.commands

    cmds.clear()

    cmds.add(
        Command(
            0,
            0,
            0,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            altitude,
        )
    )
    cmds.add(
        Command(
            0,
            0,
            0,
            mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            0,
            altitude,
        )
    )

    with open(ip_address[mission][1], "r") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if len(row) == 2 and row[0] != "" and row[1] != "":
                wp_lat = row[0]
                wp_lon = row[1]
                cmds.add(
                    Command(
                        0,
                        0,
                        0,
                        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                        16,
                        0,
                        0,
                        0,
                        0,
                        0,
                        0,
                        float(wp_lat),
                        float(wp_lon),
                        altitude,
                    )
                )

    # cmds.add(
    #     Command(
    #         0,
    #         0,
    #         0,
    #         mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    #         16,
    #         0,
    #         0,
    #         0,
    #         0,
    #         0,
    #         0,
    #         lat,
    #         lon,
    #         altitude,
    #     )
    # )

    cmds.upload()

    vehicle.close()

    print("Mission is uploaded for Drone")

    return True


# adds_square_mission()
