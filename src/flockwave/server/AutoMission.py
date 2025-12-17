import csv
import simplekml
from geopy.distance import distance
from geopy.point import Point
from .latlon2xy import geoToCart, cartToGeo
import numpy as np
import matplotlib.pyplot as plt


class AutoSplitMission:
    def __init__(
        self, origin, center_lat_lons, num_of_drones, grid_spacing, coverage_area
    ):
        # self.base_dir = os.getcwd()
        self.origin = origin
        self.center_lat_lons = center_lat_lons
        self.num_of_drones = num_of_drones
        self.grid_spacing = grid_spacing
        self.coverage_area = coverage_area
        self.path = []
        self.waypoints = []

        # os.makedirs(self.path_kml, exist_ok=True)
        # os.makedirs(self.path_csv, exist_ok=True)
        # os.makedirs(os.path.dirname(self.search_curve), exist_ok=True)
        # os.makedirs(os.path.dirname(self.curve_csv_file), exist_ok=True)

    def CreateGridsForSpecifiedAreaAndSpecifiedDrones(
        self,
        center_latitude: float,
        center_longitude: float,
        num_of_drones: int,
        grid_space: int,
        coverage_area: int,
        start_index: int,
    ) -> None:

        center_lat = center_latitude
        center_lon = center_longitude
        # print("Number Of Dronessssssssss", num_of_drones)
        num_rectangles = num_of_drones
        grid_spacing = grid_space
        meters_for_extended_lines = 250

        full_width, full_height = coverage_area, coverage_area

        rectangle_height = full_height / num_rectangles

        center_point = Point(center_lat, center_lon)

        west_edge = distance(meters=full_width / 2).destination(center_point, 270)
        index = start_index
        # print("center", center_lat, center_lon)

        for i in range(num_rectangles):

            top_offset = (
                (i * rectangle_height) - (full_height / 2) + (rectangle_height / 2)
            )

            top_center = distance(meters=top_offset).destination(center_point, 0)
            top = distance(meters=rectangle_height / 2).destination(top_center, 0)
            bottom = distance(meters=rectangle_height / 2).destination(top_center, 180)

            kml = simplekml.Kml()

            csv_data = []
            waypoint = []
            current_lat = bottom.latitude
            line_number = 0
            line = kml.newlinestring()
            line.altitudemode = simplekml.AltitudeMode.clamptoground
            line.style.linestyle.color = simplekml.Color.black
            line.style.linestyle.width = 2
            waypoint_number = 1

            while current_lat <= top.latitude:
                line_number += 1
                current_point = Point(current_lat, west_edge.longitude)
                east_point = distance(meters=full_width).destination(current_point, 90)
                if line_number % 2 == 1:
                    csv_data.append((current_point.longitude, current_point.latitude))
                    csv_data.append((east_point.longitude, east_point.latitude))

                    line.coords.addcoordinates(
                        [
                            (current_point.longitude, current_point.latitude),
                            (east_point.longitude, east_point.latitude),
                        ]
                    )
                    kml.newpoint(
                        name=f"{waypoint_number}",
                        coords=[(current_point.longitude, current_point.latitude)],
                    )
                    waypoint_number += 1
                    kml.newpoint(
                        name=f"{waypoint_number}",
                        coords=[(east_point.longitude, east_point.latitude)],
                    )
                    waypoint_number += 1
                else:
                    csv_data.append((east_point.longitude, east_point.latitude))
                    csv_data.append((current_point.longitude, current_point.latitude))

                    line.coords.addcoordinates(
                        [
                            (east_point.longitude, east_point.latitude),
                            (current_point.longitude, current_point.latitude),
                        ]
                    )
                    kml.newpoint(
                        name=f"{waypoint_number}",
                        coords=[(east_point.longitude, east_point.latitude)],
                    )
                    waypoint_number += 1
                    kml.newpoint(
                        name=f"{waypoint_number}",
                        coords=[(current_point.longitude, current_point.latitude)],
                    )
                    waypoint_number += 1
                current_lat = (
                    distance(meters=grid_spacing).destination(current_point, 0).latitude
                )

            index += 1
            self.waypoints.append(csv_data)
        return self.waypoints

    def GroupSplitting(
        self, center_lat_lons, num_of_drones, grid_spacing, coverage_area
    ) -> bool:
        drones_array = [0] * len(center_lat_lons)
        for i in range(num_of_drones):
            drones_array[i % len(center_lat_lons)] += 1
        # print("drone_array", drones_array)
        start = 1
        path = []
        for i in range(len(center_lat_lons)):
            if drones_array[i] == 0:
                continue

            csv_data = self.CreateGridsForSpecifiedAreaAndSpecifiedDrones(
                center_lat_lons[i][0],
                center_lat_lons[i][1],
                drones_array[i],
                grid_spacing,
                coverage_area,
                start,
            )
            # print("csv_data", i, csv_data, len(csv_data[0]))
            path.extend(csv_data)
            start += drones_array[i]
        # print("length of path", len(path), path)
        return path
