import csv,os,sys
import simplekml
from geopy.distance import distance
from geopy.point import Point
from geopy.point import Point
from .latlon2xy import geoToCart, cartToGeo
import numpy as np
import matplotlib.pyplot as plt


class SpecificSplitMission():
    def __init__(self, origin,center_lat_lons, drone_array, grid_spacing, coverage_area):
        self.base_dir = os.getcwd()
        self.origin = origin
        self.center_lat_lons = center_lat_lons
        self.drone_array = drone_array
        self.grid_spacing = grid_spacing
        self.coverage_area = coverage_area
        self.path_kml = os.path.join(self.base_dir, "group_split")
        self.path_csv = os.path.join(self.base_dir, "group_split")
        self.search_curve = os.path.join(self.base_dir, "group_split", "bezier", "search_{}.kml")
        self.curve_csv_file = os.path.join(self.base_dir, "group_split", "bezier", "d{}.csv")
        self.initial_heading = np.radians(0)  # Initial heading angle in radians
        self.G = 9.81  # Gravity (m/s²)
        self.MAX_BANK_ANGLE = np.radians(40)  # 40 degrees in radians
        self.SPEED = 18  # Aircraft speed in m/s
        self.TURN_RATE = (self.G * np.tan(self.MAX_BANK_ANGLE)) / self.SPEED  # rad/s
        self.sample_points = []
        self.path = []
        self.waypoints = []
        
        os.makedirs(self.path_kml, exist_ok=True)
        os.makedirs(self.path_csv, exist_ok=True)
        os.makedirs(os.path.dirname(self.search_curve), exist_ok=True)
        os.makedirs(os.path.dirname(self.curve_csv_file), exist_ok=True)

    def CreateGridsForSpecifiedAreaAndSpecifiedDrones(
            self,
            center_latitude: float,
            center_longitude: float,
            drone_array: int,
            grid_space: int,
            coverage_area: int,
    ) -> None:
        
        center_lat = center_latitude
        center_lon = center_longitude

        num_rectangles = drone_array
        grid_spacing = grid_space
        # meters_for_extended_lines = 250
        full_width, full_height = coverage_area, coverage_area

        rectangle_height = full_height / len(num_rectangles)

        center_point = Point(center_lat, center_lon)

        west_edge = distance(meters=full_width / 2).destination(center_point, 270)

        for i in range(len(num_rectangles)):
            top_offset = (i * rectangle_height) - (full_height / 2) + (rectangle_height / 2)

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
                    csv_data.append((current_point.latitude, current_point.longitude))
                    csv_data.append((east_point.latitude, east_point.longitude))

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
                    csv_data.append((east_point.latitude, east_point.longitude))
                    csv_data.append((current_point.latitude, current_point.longitude))

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
        waypoint.append(csv_data)
        return waypoint
            # kml_filename = f"search-drone-{num_rectangles[i]}.kml"
            # kml.save(os.path.join(self.path_kml, kml_filename))
            # csv_filename = f"grid_{num_rectangles[i]}.csv"
            # xy = []
            # for data in csv_data:
            #     x,y = geoToCart(self.origin,500000,data)
            #     xy.append((x/2.0,y/2.0))
            # with open(
            #         os.path.join(self.path_csv, csv_filename),
            #         mode="w",
            #         newline="",
            # ) as file:
            #     writer = csv.writer(file)
            #     writer.writerows(xy)
            #     #self.generate_bezier_curve(xy,num_rectangles[i])
            
    # def write_kml(self,data,num):
    #     kml = simplekml.Kml()
    #     line = kml.newlinestring()
    #     line.altitudemode = simplekml.AltitudeMode.clamptoground
    #     line.style.linestyle.color = simplekml.Color.blue
    #     line.style.linestyle.width = 2
    #     kml_data = []
    #     if len(data) == 0:
    #         print("No Mission Data")
    #         return
    #     for i,cmd in enumerate(data):
    #         lat,lon = cartToGeo(self.origin,5000000,[cmd[0]*2,cmd[1]*2])
    #         kml_data.append([lat,lon])
    #     for i in range(len(kml_data)-1):
    #         line.coords.addcoordinates(
    #                 [
    #                     (kml_data[i][1], kml_data[i][0]),
    #                     (kml_data[i+1][1],kml_data[i+1][0]),
    #                 ]
    #             )
    #         kml.newpoint(name="{}".format(i),coords=[(kml_data[i][1], kml_data[i][0])])
    #     kml.save(self.search_curve.format(num))

        # def get_heading_to_target(self,current_pos, target_pos):
        #     """Compute the heading angle required to face the target waypoint."""
        #     dx, dy = target_pos[0] - current_pos[0], target_pos[1] - current_pos[1]
        #     return np.arctan2(dy, dx)

        # def normalize_angle(self,angle):
        #     """Ensure angles stay within -π to π range."""
        #     return (angle + np.pi) % (2 * np.pi) - np.pi


    def GroupSplitting(
            self,
            center_lat_lons,
            drone_array,
            grid_spacing,
            coverage_area
    ) -> bool:
        path = [] 
        for i in range(len(center_lat_lons)):
            if len(drone_array[i]) == 0:
                continue
            waypoint = self.CreateGridsForSpecifiedAreaAndSpecifiedDrones(
                center_lat_lons[i][0],
                center_lat_lons[i][1],
                drone_array[i],
                grid_spacing[i],
                coverage_area[i],
            )
            path.extend(waypoint)
        print('path',path)
        return path


# center_latlon = [
#     [13.391341, 80.236145],
#     [13.386840, 80.257992],
#     [13.393423, 80.224792],
#     [13.383977, 80.236774],
#     [13.373029, 80.236966],
# ]
# origin = ( 13.210665, 80.099739) #[13.375812,80.225549]
# drone_array = [[2,4],[5,7],[1],[6],[3,8]]
# grid_spacing = [50,100,50,100,50]
# coverage_area = [1000,2000,2000,1000,1000]
# split = SpecificSplitMission(origin=origin,center_lat_lons=center_latlon, drone_array=drone_array, grid_spacing=grid_spacing,
#                          coverage_area=coverage_area)
# isDone = split.GroupSplitting(
#     center_lat_lons=center_latlon,
#     drone_array=drone_array,
#     grid_spacing=grid_spacing,
#     coverage_area=coverage_area,
# )

