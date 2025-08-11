import csv
import os
import simplekml
from geopy.distance import distance
from geopy.point import Point
from .latlon2xy import geoToCart, cartToGeo
from geopy.point import Point

class NavigationGridGenerator:
    def __init__(self, origin, center_latitude,center_longitude, num_of_drones, grid_spacing, coverage_area):
        self.center_lat = center_latitude
        self.center_lon = center_longitude
        self.num_of_drones = num_of_drones
        self.grid_spacing = grid_spacing  # in meters
        self.coverage_area = coverage_area  # in meters (width and height)
        self.origin = origin
        self.search_csv_file = os.path.join(os.getcwd(), "d{}.csv")


    def navigate_grid(self):
        center_point = Point(self.center_lat, self.center_lon)
        full_width = full_height = self.coverage_area
        rectangle_height = full_height / self.num_of_drones

        west_edge = distance(meters=full_width / 2).destination(center_point, 270)
        east_edge = distance(meters=full_width / 2).destination(center_point, 90)
        csv_datas = []
        for i in range(self.num_of_drones):
            top_offset = (i * rectangle_height) - (full_height / 2) + (rectangle_height / 2)
            top_center = distance(meters=top_offset).destination(center_point, 0)
            top = distance(meters=rectangle_height / 2).destination(top_center, 0)
            bottom = distance(meters=rectangle_height / 2).destination(top_center, 180)

            kml = simplekml.Kml()
            csv_data = []

            current_lat = bottom.latitude
            line_number = 0
            line = kml.newlinestring()
            line.altitudemode = simplekml.AltitudeMode.clamptoground
            line.style.linestyle.color = simplekml.Color.red
            line.style.linestyle.width = 2
            waypoint_number = 1

            while current_lat <= top.latitude:
                line_number += 1
                current_point = Point(current_lat, west_edge.longitude)
                east_point = distance(meters=full_width).destination(current_point, 90)

                if line_number % 2 == 1:
                    csv_data.extend([(current_point.longitude, current_point.latitude),
                                     (east_point.longitude, east_point.latitude)])
                    line.coords.addcoordinates([(current_point.longitude, current_point.latitude),
                                                (east_point.longitude, east_point.latitude)])
                    kml.newpoint(name=str(waypoint_number), coords=[(current_point.longitude, current_point.latitude)])
                    waypoint_number += 1
                    kml.newpoint(name=str(waypoint_number), coords=[(east_point.longitude, east_point.latitude)])
                    waypoint_number += 1
                else:
                    csv_data.extend([(east_point.longitude, east_point.latitude),
                                     (current_point.longitude, current_point.latitude)])
                    line.coords.addcoordinates([(east_point.longitude, east_point.latitude),
                                                (current_point.longitude, current_point.latitude)])
                    kml.newpoint(name=str(waypoint_number), coords=[(east_point.longitude, east_point.latitude)])
                    waypoint_number += 1
                    kml.newpoint(name=str(waypoint_number), coords=[(current_point.longitude, current_point.latitude)])
                    waypoint_number += 1

                current_lat = distance(meters=self.grid_spacing).destination(current_point, 0).latitude

            # kml_filename = os.path.join(os.getcwd(), f"search-drone-{i+1}.kml")
            # #csv_filename = os.path.join(self.output_dir, f"d{i+1}.csv")

            # kml.save(kml_filename)
            csv_datas.append(csv_data)
        
        # minimum_waypoints = len(min(csv_datas, key=len))
        # for i in range(len(csv_datas)):
        #     number_of_waypoints = 0
        #     with open(
        #         self.search_csv_file.format(i+1),
        #         mode="w",
        #         newline="",
        #     ) as file:
        #         for j in range(len(csv_datas[i])):
        #             if number_of_waypoints < minimum_waypoints:
        #                 writer = csv.writer(file)
        #                 x,y = geoToCart(self.origin,500000,csv_datas[i][j])
        #                 writer.writerow((x/2,y/2))
        #             number_of_waypoints += 1
        return csv_datas
