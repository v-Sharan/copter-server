import socket, time, csv
from math import radians, cos, sin, sqrt, atan2
from .search import SearchGridGenerator, PolygonSearchGrid
from .navigate import NavigationGridGenerator
from .AutoMission import AutoSplitMission
from .latlon2xy import distance_bearing

# from .SpecificSplitMission import SpecificSplitMission
# from .time import TimeCalculation
from .multipoly_specificgrid import PolygonSpecificSplit
from .multipoly_grid import PolygonAutoSplit


def fetch_file_content(file_path):
    lines = []
    try:
        with open(file_path, "r") as file:
            file_content = file.read()
            new_lines = file_content.split("\n")

            # Compare new lines with existing lines and append only unique ones
            unique_new_lines = [line for line in new_lines]
            parsed_messages = []
            for line in unique_new_lines:
                if line == "":
                    continue
                time, message = line.split("\t")
                parsed_messages.append({"timestamp": time, "message": message})

            lines.extend(parsed_messages)
    except IOError as error:
        print("Error reading file:", error)
    return lines


# master_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# adderss = {1: ("192.168.6.200", 12002), 2: ("192.168.6.200", 12008)}


def compute_grid_spacing(uav_altitude, zoom_step, overlap_percentage):
    print(
        "uav_altitude, zoom_step, overlap_percentage",
        uav_altitude,
        zoom_step,
        overlap_percentage,
    )
    sensor_width = 34.6
    sensor_height = 24.9
    focal_length = 21

    dx = (uav_altitude / (focal_length * zoom_step)) * sensor_width
    dy = (uav_altitude / (focal_length * zoom_step)) * sensor_height

    grid_spacing = dx * (1 - (overlap_percentage / 100))

    return int(grid_spacing)


master_num = -1
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address1 = ("192.168.6.151", 12008)
# udp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address2 = ("192.168.6.152", 12008)
# udp_socket3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address3 = ("192.168.6.153", 12008)
# udp_socket4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address4 = ('192.168.6.154', 12008)
# udp_socket5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address5 = ("192.168.6.155", 12008)
# udp_socket6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address6 = ('192.168.6.156', 12008)
# udp_socket7 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address7 = ('192.168.6.157', 12008)
# udp_socket8 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address8 = ('192.168.6.158', 12008)
# udp_socket9 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address9 = ('192.168.6.159', 12008)
# udp_socket10 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address10 = ("192.168.6.160", 12008)

addersses = {
    0: {"control": ("192.168.6.210", 12002), "data": ("192.168.6.210", 12008)},
    1: {"control": ("192.168.6.151", 12002), "data": ("192.168.6.151", 12008)},
    2: {"control": ("192.168.6.154", 12002), "data": ("192.168.6.154", 12008)},
    3: {"control": ("192.168.6.153", 12002), "data": ("192.168.6.153", 12008)},
    4: {"control": ("192.168.6.154", 12002), "data": ("192.168.6.154", 12008)},
    5: {"control": ("192.168.6.155", 12002), "data": ("192.168.6.155", 12008)},
}

origin = (12.58228, 79.865131)  # hanumanthapuram
# origin = (30.351921, 76.852759)  # chandiharh
# origin = (12.961654, 80.041917)  # dce

share_data_udp_socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
share_data_server_address1 = ("192.168.6.151", 12008)
share_data_udp_socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
share_data_server_address2 = ("192.168.6.152", 12008)
share_data_udp_socket3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
share_data_server_address3 = ("192.168.6.153", 12008)
share_data_udp_socket4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
share_data_server_address4 = ("192.168.6.154", 12008)
share_data_udp_socket5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
share_data_server_address5 = ("192.168.6.155", 12008)
# udp_socket6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address6 = ('192.168.6.156', 12008)
# share_data_udp_socket7 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# share_data_server_address7 = ('192.168.6.157', 12008)
# udp_socket8 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address8 = ('192.168.6.158', 12008)
# udp_socket9 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address9 = ('192.168.6.159', 12008)
# share_data_udp_socket10 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# share_data_server_address10 = ("192.168.6.160", 12008)

# socket1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address11 = ("192.168.6.151", 12002)
# socket2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address12 = ("192.168.6.152", 12002)
# socket3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address13 = ("192.168.6.153", 12002)
# socket4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address14 = ('192.168.6.154', 12002)
# socket5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address15 = ("192.168.6.155", 12002)
# socket6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address16 = ('192.168.6.156', 12002)
# socket7 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address17 = ('192.168.6.157', 12002)
# socket8 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address18 = ('192.168.6.158', 12002)
# socket9 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address19 = ('192.168.6.159', 12002)
# socket10 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_address20 = ("192.168.6.160", 12002)

file_sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
file_server_address1 = ("192.168.6.151", 12003)
file_sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
file_server_address2 = ("192.168.6.154", 12003)
file_sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
file_server_address3 = ("192.168.6.153", 12003)
file_sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
file_server_address4 = ("192.168.6.154", 12003)
file_sock5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
file_server_address5 = ("192.168.6.155", 12003)
# file_sock6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# file_server_address6 = ('192.168.6.156', 12003)
# file_sock7 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# file_server_address7 = ('192.168.6.157', 12003)
# file_sock8 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# file_server_address8 = ('192.168.6.158', 12003)
# file_sock9 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# file_server_address9 = ('192.168.6.159', 12003)
# file_sock10 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# file_server_address10 = ("192.168.6.160", 12003)

mavlink_sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mavlink_server_address1 = ("192.168.6.151", 12045)

mavlink_sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mavlink_server_address2 = ("192.168.6.152", 12045)

mavlink_sock3 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mavlink_server_address3 = ("192.168.6.153", 12045)

# mavlink_sock4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# mavlink_server_address4 = ('192.168.6.154', 12045)

# mavlink_sock5 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# mavlink_server_address5 = ("192.168.6.155", 12045)

# mavlink_sock6 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# mavlink_server_address6 = ('192.168.6.156', 12045)

# mavlink_sock7 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# mavlink_server_address7 = ('192.168.6.157', 12045)

# mavlink_sock8 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# mavlink_server_address8 = ('192.168.6.158', 12045)

# mavlink_sock9 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# mavlink_server_address9 = ('192.168.0.159', 12045)

# mavlink_sock10 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# mavlink_server_address10 = ("192.168.6.160", 12045)


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points
    on the Earth's surface using the Haversine formula.

    Parameters:
    - lat1, lon1: Latitude and longitude of the first point (in degrees).
    - lat2, lon2: Latitude and longitude of the second point (in degrees).

    Returns:
    - The distance between the two points (in meters).
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = 6371000 * c  # Radius of Earth in meters

    return distance


def calculate_flight_time():
    global flight_time_var, csv_files
    total_distance = 0
    num_uavs = 0

    for uav, csv_path in csv_files.items():
        lat_lon_points = []
        with open(csv_path, "rt") as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  # Skip the header (first row)
            for row in csv_reader:
                lat, lon = map(float, row)
                lat_lon_points.append((lat, lon))

        total_distance_uav = 0
        for i in range(len(lat_lon_points) - 1):
            lat1, lon1 = lat_lon_points[i]
            lat2, lon2 = lat_lon_points[i + 1]
            distance = haversine(lat1, lon1, lat2, lon2)
            total_distance_uav += distance

        total_distance += total_distance_uav
        num_uavs += 1

    average_total_distance = total_distance / num_uavs
    average_speed = 3  # Assume average speed between 4 m/s and 5 m/s
    flight_time_seconds = average_total_distance / average_speed
    flight_time_minutes = flight_time_seconds / 60

    flight_time_var.set("Flight Time = {:.2f} minutes".format(flight_time_minutes))


def clear_csv():
    print("!!!CSV Cleared!!")
    global udp_socket, udp_socket2, server_address1, server_address2
    # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "clear_csv"

    udp_socket.sendto(str(data).encode(), server_address1)
    time.sleep(0.5)
    udp_socket2.sendto(str(data).encode(), server_address2)
    time.sleep(0.5)

    udp_socket3.sendto(str(data).encode(), server_address3)
    time.sleep(0.5)

    # udp_socket4.sendto(str(data).encode(), server_address4)
    # time.sleep(0.5)
    # udp_socket5.sendto(str(data).encode(), server_address5)
    # time.sleep(0.5)

    # udp_socket6.sendto(str(data).encode(), server_address6)
    # time.sleep(0.5)
    # udp_socket7.sendto(str(data).encode(), server_address7)
    # time.sleep(0.5)
    # udp_socket8.sendto(str(data).encode(), server_address8)
    # time.sleep(0.5)
    # udp_socket9.sendto(str(data).encode(), server_address9)
    # time.sleep(0.5)
    # udp_socket10.sendto(str(data).encode(), server_address10)
    return True


def start_socket():
    print("!!!Start!!")
    global udp_socket, udp_socket2, server_address1, server_address2
    # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "start"

    udp_socket.sendto(str(data).encode(), server_address1)
    time.sleep(0.5)
    udp_socket2.sendto(str(data).encode(), server_address2)
    time.sleep(0.5)

    udp_socket3.sendto(str(data).encode(), server_address3)
    # time.sleep(0.5)

    # udp_socket4.sendto(str(data).encode(), server_address4)
    # time.sleep(0.5)

    # udp_socket5.sendto(str(data).encode(), server_address5)
    # time.sleep(0.5)

    # udp_socket6.sendto(str(data).encode(), server_address6)
    # time.sleep(0.5)

    # udp_socket7.sendto(str(data).encode(), server_address7)
    # time.sleep(0.5)

    # udp_socket8.sendto(str(data).encode(), server_address8)
    # time.sleep(0.5)
    # udp_socket9.sendto(str(data).encode(), server_address9)
    # time.sleep(0.5)

    # udp_socket10.sendto(str(data).encode(), server_address10)
    return True


def start1_socket():
    print("Start1........")
    global udp_socket, server_address1, server_address2, udp_socket2
    # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "start1"

    udp_socket.sendto(str(data).encode(), server_address1)
    time.sleep(0.5)
    udp_socket2.sendto(str(data).encode(), server_address2)
    time.sleep(0.5)

    udp_socket3.sendto(str(data).encode(), server_address3)
    # time.sleep(0.5)
    # udp_socket4.sendto(str(data).encode(), server_address4)
    # time.sleep(0.5)
    # udp_socket5.sendto(str(data).encode(), server_address5)
    # time.sleep(0.5)
    # udp_socket6.sendto(str(data).encode(), server_address6)
    # time.sleep(0.5)
    # udp_socket7.sendto(str(data).encode(), server_address7)
    # time.sleep(0.5)
    # udp_socket8.sendto(str(data).encode(), server_address8)
    # time.sleep(0.5)
    # udp_socket9.sendto(str(data).encode(), server_address9)
    # time.sleep(0.5)
    # udp_socket10.sendto(str(data).encode(), server_address10)
    return True


def home_lock():
    print("Home position Locked....!!!!")
    global udp_socket, server_address1, server_address2, udp_socket2
    # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "home_lock"

    udp_socket.sendto(str(data).encode(), server_address1)
    time.sleep(0.5)
    udp_socket2.sendto(str(data).encode(), server_address2)
    time.sleep(0.5)
    udp_socket3.sendto(str(data).encode(), server_address3)
    # time.sleep(0.5)

    # udp_socket4.sendto(str(data).encode(), server_address4)
    # time.sleep(0.5)
    # udp_socket5.sendto(str(data).encode(), server_address5)
    # time.sleep(0.5)
    # udp_socket6.sendto(str(data).encode(), server_address6)
    # time.sleep(0.5)

    # udp_socket7.sendto(str(data).encode(), server_address7)

    # time.sleep(0.5)
    # udp_socket8.sendto(str(data).encode(), server_address8)
    # time.sleep(0.5)
    # udp_socket9.sendto(str(data).encode(), server_address9)
    # time.sleep(0.5)
    # udp_socket10.sendto(str(data).encode(), server_address10)
    return True


def select_plot(filename):
    if filename != "":

        file_sock1.sendto(str(filename).encode(), file_server_address1)
        time.sleep(0.5)
        file_sock2.sendto(str(filename).encode(), file_server_address2)
        time.sleep(0.5)
        file_sock3.sendto(str(filename).encode(), file_server_address3)
        # time.sleep(0.5)

        # file_sock4.sendto(str(filename).encode(),file_server_address4)
        # time.sleep(0.5)

        # file_sock5.sendto(str(filename).encode(), file_server_address5)
        # time.sleep(0.5)

        # file_sock6.sendto(str(filename).encode(),file_server_address6)
        # time.sleep(0.5)

        # file_sock7.sendto(str(filename).encode(),file_server_address7)
        # time.sleep(0.5)

        # file_sock8.sendto(str(filename).encode(),file_server_address8)
        # time.sleep(0.5)
        # file_sock9.sendto(str(filename).encode(),file_server_address9)
        # time.sleep(0.5)
        # file_sock10.sendto(str(filename).encode(), file_server_address10)
        return True


def share_data_func():
    from flockwave.server.socket.globalVariable import (
        get_goal_table,
        get_return_goal_table,
        get_grid_path_table,
    )

    # global goal_table,return_goal_table,filename,udp_socket,server_address1,server_address2,udp_socket2,grid_path_table
    # goal_table=[]
    grid_path_table = get_grid_path_table()
    goal_table = get_goal_table()

    if get_return_goal_table() is not None:
        combined_goal_table = get_goal_table() + get_return_goal_table()
        print("combined_goal_table", combined_goal_table)
        """
        share_data_udp_socket1.sendto(("share_data" + "," + str(combined_goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address1)
        time.sleep(0.5)
        share_data_udp_socket2.sendto(("share_data" + "," + str(combined_goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address2)
        time.sleep(0.5)
        """
        share_data_udp_socket3.sendto(
            (
                "share_data"
                + ","
                + str(combined_goal_table)
                + ","
                + "grid_path_table"
                + ","
                + str(grid_path_table)
            ).encode(),
            share_data_server_address3,
        )
        time.sleep(0.5)
        """
        share_data_udp_socket4.sendto(("share_data" + "," + str(combined_goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address4)
        time.sleep(0.5)
        """
        share_data_udp_socket5.sendto(
            (
                "share_data"
                + ","
                + str(combined_goal_table)
                + ","
                + "grid_path_table"
                + ","
                + str(grid_path_table)
            ).encode(),
            share_data_server_address5,
        )
        time.sleep(0.5)
        """
        share_data_udp_socket6.sendto(("share_data" + "," + str(combined_goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address6)
        time.sleep(0.5)

        share_data_udp_socket7.sendto(("share_data" + "," + str(combined_goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address7)

        time.sleep(0.5)
        share_data_udp_socket8.sendto(("share_data" + "," + str(combined_goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address8)
        time.sleep(0.5)
        share_data_udp_socket9.sendto(("share_data" + "," + str(combined_goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address9)
        time.sleep(0.5)
        """
        share_data_udp_socket10.sendto(
            (
                "share_data"
                + ","
                + str(combined_goal_table)
                + ","
                + "grid_path_table"
                + ","
                + str(grid_path_table)
            ).encode(),
            share_data_server_address10,
        )

    else:

        """
        share_data_udp_socket1.sendto(("share_data"+","+ str(goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address1)
        time.sleep(0.5)
        share_data_udp_socket2.sendto(("share_data"+","+ str(goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address2)
        time.sleep(0.5)
        """
        share_data_udp_socket3.sendto(
            (
                "share_data"
                + ","
                + str(goal_table)
                + ","
                + "grid_path_table"
                + ","
                + str(grid_path_table)
            ).encode(),
            share_data_server_address3,
        )
        time.sleep(0.5)
        """
        share_data_udp_socket4.sendto(("share_data"+","+ str(goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address4)
        time.sleep(0.5)
        """
        share_data_udp_socket5.sendto(
            (
                "share_data"
                + ","
                + str(goal_table)
                + ","
                + "grid_path_table"
                + ","
                + str(grid_path_table)
            ).encode(),
            share_data_server_address5,
        )
        time.sleep(0.5)
        """
        share_data_udp_socket6.sendto(("share_data"+","+ str(goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address6)
        time.sleep(0.5)

        share_data_udp_socket7.sendto(("share_data"+","+ str(goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address7)

        time.sleep(0.5)
        share_data_udp_socket8.sendto(("share_data"+","+ str(goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address8)
        time.sleep(0.5)
        share_data_udp_socket9.sendto(("share_data"+","+ str(goal_table)+","+"grid_path_table" +","+str( grid_path_table)).encode(), share_data_server_address9)
        time.sleep(0.5)
        """
        share_data_udp_socket10.sendto(
            (
                "share_data"
                + ","
                + str(goal_table)
                + ","
                + "grid_path_table"
                + ","
                + str(grid_path_table)
            ).encode(),
            share_data_server_address10,
        )
    return True


def disperse_socket():
    global udp_socket, master_num
    print("Disperse!!!!!!")
    # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "disperse"
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


def takeoff_socket(alt):
    print("Takeoff...........")
    takeoff_alt = alt
    global udp_socket, master_num
    data = "takeoff" + "," + str(takeoff_alt)
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


def search_socket(points, camAlt, overlap, zoomLevel, coverage, ids):
    global udp_socket, master_num, origin
    # global udp_socket,server_address1,server_address2,udp_socket2
    print("Searching........", points, len(points))
    # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    points = [[float(lon), float(lat)] for lon, lat in points]
    for num in points:
        num.reverse()
    gridspacing = compute_grid_spacing(camAlt, zoomLevel, overlap)
    print("gridspacing", gridspacing)
    if len(points) == 1:
        data = str(
            "search"
            + ","
            + str(points[0][0])
            + ","
            + str(points[0][1])
            + ","
            + str(len(ids))
            + ","
            + str(gridspacing)
            + ","
            + str(coverage)
        )
        print(data, points, len(ids), gridspacing, coverage)
        udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

        curve = SearchGridGenerator(
            origin=origin,
            center_latitude=points[0][0],
            center_longitude=points[0][1],
            coverage_area=coverage,
            grid_spacing=gridspacing,
            num_of_drones=len(ids),
        )
        path = curve.generate_grids()
        print("path", path)
        # return path, 30

    else:
        gridspacing = compute_grid_spacing(camAlt, zoomLevel, overlap)
        print("gridspacing", gridspacing, type(gridspacing), int(gridspacing))
        data = str(
            "searchpolygon"
            + "_"
            + str(points)
            + "_"
            + str(len(ids))
            + "_"
            + str(gridspacing)
        )
        print(points, len(ids), gridspacing, coverage)
        udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

        planner = PolygonSearchGrid(
            polygon_latlon=points,
            origin_gps=origin,
            endDistance=500000,
            num_drones=len(ids),
            grid_spacing=gridspacing,
            rotation_angle=90,
            obstacles_latlon=[],
        )

        planner.generate_paths()
        path = planner.save_paths()
    return path, 30


def aggregate_socket(points):
    global udp_socket, master_num
    print("Aggregation..!!!!", points)
    data = str("aggregate" + "," + str(points[0][1]) + "," + str(points[0][0]))

    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


def home_socket():
    global udp_socket, master_num
    print("Home....******")
    data = "home"
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


# def airport_selection(filename):
#     print(filename)
#     """
#     file_sock1.sendto(str(filename).encode(),file_server_address1)
#     time.sleep(0.5)
#     file_sock2.sendto(str(filename).encode(),file_server_address2)
#     time.sleep(0.5)
#     """
#     file_sock3.sendto(str(filename).encode(), file_server_address3)
#     time.sleep(0.5)
#     """
#     file_sock4.sendto(str(filename).encode(),file_server_address4)
#     time.sleep(0.5)
#     """
#     file_sock5.sendto(str(filename).encode(), file_server_address5)
#     time.sleep(0.5)


def different_alt_socket(initial_alt, alt_diff):
    global udp_socket, master_num
    data = str(initial_alt) + str(",") + str(alt_diff)
    g = str("different" + "," + str(data))
    print(g)
    udp_socket.sendto(g.encode(), addersses[int(master_num)]["data"])

    return True


# def same_alt_socket(alt_same):
#     global udp_socket, master_num
#     print("Same_altitude")
#     data = alt_same
#     print(data, "data")
#     f = "same" + "," + str(data)
#     print(f, "f")

#     udp_socket.sendto(str(f).encode(), server_address1)
#     time.sleep(0.5)
#     udp_socket2.sendto(str(f).encode(), server_address2)
#     time.sleep(0.5)
#     return True


def land_socket():
    global udp_socket, master_num
    data = "land"
    print(data)
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


# def rtl_socket():
#     global socket, udp_socket, master_num
#     data = "rtl"
#     master_udp.sendto(data.encode(), adderss.get(2))
#     return True


def stop_socket():
    print("STOP>>>>>>>>>>>>")
    global master_num, socket
    data = "stop"
    print("master_num", master_num)
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["control"])
    print("addersses[int(master_num)]", addersses[int(master_num)])

    return True


def return_socket():
    global socket, return_flag, udp_socket, server_address1, server_address2, udp_socket2
    # print("&&&&&")
    print("return")
    return_flag = True
    # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    data = "return"
    """
    udp_socket.sendto(str(data).encode(), server_address1)
    time.sleep(0.5)
    udp_socket2.sendto(str(data).encode(), server_address2)
    time.sleep(0.5)
    """
    udp_socket3.sendto(str(data).encode(), server_address3)
    time.sleep(0.5)
    """
    udp_socket4.sendto(str(data).encode(), server_address4)
    time.sleep(0.5)
    """
    udp_socket5.sendto(str(data).encode(), server_address5)
    time.sleep(0.5)
    """
    udp_socket6.sendto(str(data).encode(), server_address6)
    time.sleep(0.5)

    udp_socket7.sendto(str(data).encode(), server_address7)

    time.sleep(0.5)
    udp_socket8.sendto(str(data).encode(), server_address8)
    time.sleep(0.5)
    udp_socket9.sendto(str(data).encode(), server_address9)
    time.sleep(0.5)
    """
    # udp_socket10.sendto(str(data).encode(), server_address10)
    return True


def specific_bot_goal_socket(drone_num, goal_num):
    global master_num, udp_socket
    print("$$$##Specific_bot_goal###")
    goal_num = [[float(lon), float(lat)] for lon, lat in goal_num]
    for num in goal_num:
        num.reverse()
    data = "specificbotgoal" + "_" + str(drone_num[0]) + "_" + str(goal_num)
    print("d", data, addersses[int(master_num)]["data"])
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


def goal_socket(goal_num):
    global master_num, udp_socket
    print("***Group goal*****!!!!!")
    goal_num = [[float(lon), float(lat)] for lon, lat in goal_num]
    for num in goal_num:
        num.reverse()
    data = str("goal" + "_" + str(goal_num))
    print("d", data)
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])
    print("addersses[int(master_num)]", addersses[int(master_num)]["data"])
    return True


def master(master_number):
    global master_num, udp_socket
    master_num = int(master_number)
    data = "master" + "-" + str(master_num)
    print("data", data)
    for uav_id, ports in addersses.items():
        try:
            udp_socket.sendto(data.encode(), ports["control"])
            print(f"✅ Sent to UAV {uav_id}: {ports['control']}")
        except Exception as e:
            print(f"❌ Error sending to UAV {uav_id}: {e}")
    return True


def mavlink_add(uav):
    global master_num, udp_socket
    data = str(str("add") + "," + str(uav))
    print(data)
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


def mavlink_remove(uav):
    global master_num, udp_socket
    data = str("remove" + "," + str(uav))
    print(data)
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


def bot_remove(remove_uav_num):
    global udp_socket, udp_socket2, udp_socket3, server_address1, server_address2, server_address3

    print("!!!bot_remove!!")

    data = "remove_bot" + "," + str(remove_uav_num)
    print("remove_link_num", remove_uav_num)
    udp_socket.sendto(str(data).encode(), server_address1)
    time.sleep(0.5)
    udp_socket2.sendto(str(data).encode(), server_address2)
    time.sleep(0.5)
    udp_socket3.sendto(str(data).encode(), server_address3)
    # time.sleep(0.5)
    # udp_socket4.sendto(str(data).encode(), server_address4)
    # time.sleep(0.5)
    # udp_socket5.sendto(str(data).encode(), server_address5)
    # time.sleep(0.5)
    # udp_socket6.sendto(str(data).encode(), server_address6)
    # time.sleep(0.5)

    # udp_socket7.sendto(str(data).encode(), server_address7)

    # time.sleep(0.5)
    # udp_socket8.sendto(str(data).encode(), server_address8)
    # time.sleep(0.5)
    # udp_socket9.sendto(str(data).encode(), server_address9)
    # time.sleep(0.5)
    # udp_socket10.sendto(str(data).encode(), server_address10)
    return True


def landing_mission_send(mission):
    for num in mission:
        num.reverse()
    global udp_socket

    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    data = str("home,{}".format(mission))
    return True


def navigate(center_latlon, camAlt, overlap, zoomLevel, coverage, ids):
    gridspacing = compute_grid_spacing(camAlt, zoomLevel, overlap)
    global master_num, udp_socket, origin
    latlng = str(str(center_latlon[0][1]) + "," + str(center_latlon[0][0]))
    data = str(
        "navigate"
        + ","
        + str(latlng)
        + ","
        + str(1)
        + ","
        + str(gridspacing)
        + ","
        + str(coverage)
    )

    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    curve = NavigationGridGenerator(
        origin=origin,
        center_latitude=center_latlon[0][1],
        center_longitude=center_latlon[0][0],
        num_of_drones=1,
        grid_spacing=gridspacing,
        coverage_area=coverage,
    )
    path = curve.navigate_grid()
    print("path", path)
    return path


def loiter(center_latlon, direction):
    global udp_socket
    s = str(str(center_latlon[0][1]) + "," + str(center_latlon[0][0]))
    data = str("loiter pointer" + "," + str(s) + "," + str(direction))
    print(data)
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return True


def skip_point(skip_waypoint):
    global udp_socket
    data = str("skip" + "," + str(skip_waypoint))
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])
    return True


def send_alts(alts):
    data = str("alt" + "," + str(alts))
    print(data, adderss.get(2))

    return True


def splitmission(center_latlon, uavs, gridspace, coverage, featureType):
    global master_num, udp_socket, origin
    center_latlon = [[[float(lon), float(lat)]] for [[lon, lat]] in center_latlon]

    print("centerlatlon", center_latlon)
    for latlon in center_latlon:
        latlon.reverse()
    if featureType == "points":
        data = str(
            "split"
            + "_"
            + str(center_latlon)
            + "_"
            + str(len(uavs))
            + "_"
            + str(gridspace)
            + "_"
            + str(coverage)
        )

        udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])
        center_latlon = [coord[0] for coord in center_latlon]
        split = AutoSplitMission(
            origin=origin,
            center_lat_lons=center_latlon,
            num_of_drones=len(uavs),
            grid_spacing=gridspace,
            coverage_area=coverage,
        )
        isDone = split.GroupSplitting(
            center_lat_lons=center_latlon,
            num_of_drones=len(uavs),
            grid_spacing=gridspace,
            coverage_area=coverage,
        )
        # path = split.return_latlon()
        # print("..................................", isDone, len(isDone))
        return isDone
    elif featureType == "polygon":
        print("length..................", center_latlon, len(center_latlon))
        data = str(
            "polyautosplit"
            + "_"
            + str(center_latlon)
            + "_"
            + str(len(uavs))
            + "_"
            + str(gridspace)
            + "_"
            + str(coverage)
        )

        udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

        planner = PolygonAutoSplit(
            polygon_latlon_list=center_latlon,
            origin_gps=origin,
            endDistance=500000,
            num_drones=len(uavs),
            grid_spacing=gridspace,
            rotation_angle=90,
            obstacles_latlon_list=[],
        )

        path1 = planner.generate_paths()
        path = planner.save_paths()
        # print(path, len(path), "SPLIT@")
        return path


def specificsplit(center_latlon, uavs, gridspace, coverage, featureType):
    global master_num, udp_socket, origin
    grid = []
    coverageSpace = []
    for i in range(len(uavs)):
        grid.append(gridspace)
        coverageSpace.append(coverage)
    print(center_latlon, uavs, gridspace, coverage)

    split = AutoSplitMission(
        origin=origin,
        center_lat_lons=center_latlon,
        num_of_drones=len(uavs),
        grid_spacing=gridspace,
        coverage_area=coverage,
    )
    path = split.GroupSplitting(
        center_lat_lons=center_latlon,
        num_of_drones=len(uavs),
        grid_spacing=gridspace,
        coverage_area=coverage,
    )
    data = str(
        "specificsplit"
        + "_"
        + str(center_latlon)
        + "_"
        + str(uavs)
        + "_"
        + str(grid)
        + "_"
        + str(coverageSpace)
    )
    udp_socket.sendto(data.encode(), addersses[int(master_num)]["data"])

    return path


def compute_antenna_az(
    homeLattitude, homeLongitude, destinationLattitude, destinationLongitude
):
    az = distance_bearing(
        homeLattitude, homeLongitude, destinationLattitude, destinationLongitude
    )
    print(az)
    return az
