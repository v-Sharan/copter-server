#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
from flockwave.server.ext.mavlink.automission import AutoMissionManager
from flockwave.server.ext.mavlink.enums import MAVCommand
from flockwave.gps.vectors import GPSCoordinate
from flockwave.server.model import UAV
import csv
from typing import List


async def add_mavlink_mission(i: int, alt: int, uav: UAV) -> None:
    manager = AutoMissionManager.for_uav(uav)
    await manager.set_automission_areas([])
    search_file = "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/search-drone-"
    flag = 0
    points_coordinate = [
        [
            GPSCoordinate(uav.status.position.lat, uav.status.position.lon, 0, 30, 0),
            MAVCommand.NAV_VTOL_TAKEOFF,
        ],
        [
            GPSCoordinate(0, 0, 0, 30, 0),
            MAVCommand.NAV_VTOL_TAKEOFF,
        ],
    ]
    with open(
        "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/forward-drone-"
        + str(i + 1)
        + ".csv",
        "r",
    ) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            lat = float(row[0])
            lon = float(row[1])
            if not flag:
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, alt, 0), MAVCommand.NAV_WAYPOINT],
                )
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, alt, 0), MAVCommand.NAV_LOITER_UNLIM],
                )
            else:
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, alt, 0), MAVCommand.NAV_WAYPOINT],
                )
            prev_lat = lat
            prev_lon = lon
            flag = 1
    with open(
        search_file + str(i + 1) + ".csv",
        "r",
    ) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            lat = float(row[0])
            lon = float(row[1])
            points_coordinate.append(
                [GPSCoordinate(lat, lon, 0, alt, 0), MAVCommand.NAV_WAYPOINT]
            )
            prev_lat = lat
            prev_lon = lon
    points_coordinate.append(
        [GPSCoordinate(prev_lat, prev_lon, 0, alt, 0), MAVCommand.NAV_LOITER_UNLIM]
    )
    with open(
        "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/reverse-drone-"
        + str(i + 1)
        + ".csv",
        "r",
    ) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            lat = float(row[0])
            lon = float(row[1])
            points_coordinate.append(
                [GPSCoordinate(lat, lon, 0, alt, 0), MAVCommand.NAV_WAYPOINT]
            )
            prev_lat = lat
            prev_lon = lon
    points_coordinate.append(
        [GPSCoordinate(prev_lat, prev_lon, 0, alt, 0), MAVCommand.NAV_LOITER_UNLIM]
    )
    points_mission = convert_to_missioncmd(points_coordinate)
    await manager.set_automission_areas(points_mission)


def convert_to_missioncmd(
    points_coordinate: List[list[GPSCoordinate, MAVCommand]]
) -> List[tuple[MAVCommand, dict[str, int]]]:
    points_mission = [
        (
            (point[1]),
            {
                "x": int(point[0].lat * 1e7),
                "y": int(point[0].lon * 1e7),
                "z": int(point[0].ahl),
            },
        )
        for point in points_coordinate
    ]
    return points_mission


async def main(uavs: List[UAV]) -> None:
    index = 0
    alt = 100
    for uav in uavs:
        if uav:
            await add_mavlink_mission(index, alt, uav)
            index += 1
            alt += 25
