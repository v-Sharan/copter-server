from flockwave.server.ext.mavlink.automission import AutoMissionManager
from flockwave.server.ext.mavlink.enums import MAVCommand
from flockwave.gps.vectors import GPSCoordinate
from flockwave.server.model import UAV
import csv
from typing import List


async def add_mavlink_mission1(i: int, alt: int, uav: UAV) -> None:
    manager = AutoMissionManager.for_uav(uav)
    await manager.clear_mission()
    search_file = "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/search-drone-"
    flag = 0
    points_coordinate = [
        [
            GPSCoordinate(0, 0, 0, 30, 0),
            MAVCommand.NAV_VTOL_TAKEOFF,
        ],
        [
            GPSCoordinate(0, 0, 0, 30, 0),
            MAVCommand.NAV_VTOL_TAKEOFF,
        ],
    ]
    print(
        "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/forward-drone-{}.csv".format(
            i
        )
    )
    with open(
        "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/forward-drone-{}.csv".format(
            i
        ),
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
                # lat = 13.3945042
                # lon = 80.2309012
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
        search_file + str(i) + ".csv",
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
        + str(i)
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
    print(points_coordinate)
    points_mission = convert_to_missioncmd(points_coordinate)
    await manager.set_automission_areas(points_mission)


async def add_mavlink_mission(i: int, alt: int, uav: UAV, altitude: int) -> None:
    manager = AutoMissionManager.for_uav(uav)
    await manager.clear_mission()
    search_file = "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/search-drone-"
    flag = 0
    prev_lat, prev_lon = 0, 0
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
                    [GPSCoordinate(lat, lon, 0, altitude, 0), MAVCommand.NAV_WAYPOINT]
                )
                points_coordinate.append(
                    [
                        GPSCoordinate(lat, lon, 0, altitude, 0),
                        MAVCommand.NAV_LOITER_UNLIM,
                    ]
                )
            elif flag == 1 or flag == 2:
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, altitude, 0), MAVCommand.NAV_WAYPOINT]
                )
            else:
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, alt, 0), MAVCommand.NAV_WAYPOINT]
                )
            prev_lat = lat
            prev_lon = lon
            flag = 1
    count = 1
    search_waypoints = 0
    with open(
        search_file + str(i + 1) + ".csv",
        "r",
    ) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            search_waypoints += 1
    search_waypoints -= 1
    with open(
        search_file + str(i + 1) + ".csv",
        "r",
    ) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if count >= search_waypoints:
                lat = float(row[0])
                lon = float(row[1])
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, altitude, 0), MAVCommand.NAV_WAYPOINT]
                )
            else:
                lat = float(row[0])
                lon = float(row[1])
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, alt, 0), MAVCommand.NAV_WAYPOINT]
                )
            prev_lat = lat
            prev_lon = lon
    points_coordinate.append(
        [GPSCoordinate(prev_lat, prev_lon, 0, altitude, 0), MAVCommand.NAV_LOITER_UNLIM]
    )
    flag = 0
    reverse_waypoints = 0
    with open(
        "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/reverse-drone-"
        + str(i + 1)
        + ".csv",
        "r",
    ) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            reverse_waypoints += 1
    reverse_waypoints -= 2
    count = 0
    with open(
        "C:/Users/vshar/OneDrive/Documents/fullstack/skybrush-server/src/flockwave/server/VTOL/csvs/reverse-drone-"
        + str(i + 1)
        + ".csv",
        "r",
    ) as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            if not flag or count >= reverse_waypoints:
                lat = float(row[0])
                lon = float(row[1])
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, altitude, 0), MAVCommand.NAV_WAYPOINT]
                )
                prev_lat = lat
                prev_lon = lon
            else:
                lat = float(row[0])
                lon = float(row[1])
                points_coordinate.append(
                    [GPSCoordinate(lat, lon, 0, alt, 0), MAVCommand.NAV_WAYPOINT]
                )
                prev_lat = lat
                prev_lon = lon
            flag = 1
            count += 1
    points_coordinate.append(
        [GPSCoordinate(prev_lat, prev_lon, 0, altitude, 0), MAVCommand.NAV_LOITER_UNLIM]
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


async def main(uavs: dict[str, UAV]) -> bool:
    from ..socket.globalVariable import alts, drone

    alt = 0
    drone_id = drone
    for i, uav in enumerate(uavs):
        alt = alts[int(uav)]
        print("mission:", i + 1, alt)
        vehicle = uavs[uav]
        if vehicle:
            await add_mavlink_mission1(i + 1, alt, vehicle)
        # await add_mavlink_mission(index, alt, uav, altitudes[i])
    print("Uploaded")
    return True
