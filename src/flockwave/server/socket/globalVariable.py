from flockwave.gps.vectors import GPSCoordinate

home_pos: list = []
goal_points: list = []
goal_table: list = []
return_goal_table: list = []
grid_path_table: list = []
Takeoff_Alt: str = 2.5
logCounter: int = 0
log_file_path: str = ""
area_covered: int = 0
minutes: int = 0
seconds: int = 0
removed_uav_grid_file_name = []
removed_uav_grid_path_length = []
gimbal_target = []
mission = []
mission_index: int = 0
speed_match = False
reached_height = False

vtol_takeoff_height = {
    1: 30,
    2: 30,
    3: 30,
    4: 30,
    5: 30,
    20: 40,
    22: 35,
    24: 30,
    # 5: 30,
    # 6: 35,
    # 7: 40,
    # 8: 45,
    # 10: 30,
    # 11: 35,
    # 14: 40,
    # 15: 45,
    # 20: 30,
    # 22: 35,
    # 24: 40,
    # 25: 45,
}
alts: dict[int, int] = {
    20: 100,
    22: 110,
    24: 120,
    1: 300,
    2: 310,
    3: 300,
    4: 310,
    5: 300,
    # 5: 210,
    # 6: 200,
    # 7: 190,
    # 8: 180,
    # 10: 170,
    # 11: 160,
    # 14: 150,
    # 15: 140,
    # 20: 130,
    # 22: 120,
    # 24: 110,
    # 25: 100,
}

drone = {
    20: 1,
    1: 1,
    2: 2,
    3: 3,
    4: 4,
    5: 5,
    22: 2,
    24: 3,
    8: 4,
    10: 5,
    11: 6,
    14: 7,
    15: 8,
    # 20: 9,
    # 22: 10,
    # 24: 11,
    # 25: 12,
}


vtol_rtl_height = {20: 50, 22: 60, 24: 70, 1: 30, 2: 30}
# vtol_takeoff_height = {7: 50, 14: 45, 22: 40, 24: 35, 25: 30}
# alts: dict[int, int] = {7: 100, 14: 110, 22: 120, 24: 130, 25: 140}

# drone = {7: 1, 14: 2, 22: 3, 24: 4, 25: 5}

past_distance: int | float = 0.0
plat: float = 0.0
plon: float = 0.0

trail: bool = False
target_confirmation = GPSCoordinate(lat=0, lon=0, amsl=None, ahl=None, agl=None)

airspeed_failure_ms = 26

def changeReachHeight(value:bool):
    global  reached_height
    reached_height = value

def get_target_confirm():
    global target_confirmation
    return


def update_target_confirmation(lat, lon):
    global target_confirmation
    target_confirmation.lat = lat
    target_confirmation.lon = lon


def update_trail() -> None:
    global trail
    trail = True


def get_trail() -> bool:
    global trail
    return trail


def update_past_distance(dis: int | float, plat1: float, plon1: float) -> None:
    global past_distance, plat, plon
    past_distance = dis
    plat = plat1
    plon = plon1


def get_past_distance() -> tuple[int | float]:
    global past_distance, plat, plon
    return (past_distance, plat, plon)


def update_coverage_time(area_covered1, minutes1, seconds1) -> None:
    global area_covered, minutes, seconds
    area_covered = area_covered1
    minutes = minutes1
    seconds = seconds1


def update_mission_index():
    global mission_index
    mission_index += 1


def get_mission_index():
    global mission_index
    return mission_index


def update_mission(add_mission):
    global mission
    mission.append(add_mission)


def empty_mission():
    global mission
    mission = []


def get_mission():
    global mission
    return mission


def get_coverage_time():
    return [area_covered, minutes, seconds]


def update_logCounter():
    global logCounter
    logCounter = 1


def get_logCounter():
    global logCounter
    return logCounter


def update_log_file_path(file_path):
    global log_file_path
    log_file_path = file_path


def get_log_file_path():
    global log_file_path
    return log_file_path


def update_home(home_pos_val):
    global home_pos
    home_pos = home_pos_val


def get_home():
    global home_pos
    return home_pos


def update_goal_points(goal_ponits_val):
    global goal_points
    goal_points = goal_ponits_val


def get_goal_points():
    global goal_points
    return goal_points


def update_goal_table(goal_table_val):
    global goal_table
    goal_table.append(goal_table_val)


def get_goal_table():
    global goal_table
    return goal_table


def update_return_goal_table(return_goal_table_val):
    global return_goal_table
    return_goal_table.append(return_goal_table_val)


def get_return_goal_table():
    global return_goal_table
    return return_goal_table


def update_grid_path_table(grid_path_table_val):
    global grid_path_table
    grid_path_table = grid_path_table_val


def get_grid_path_table():
    global grid_path_table
    return grid_path_table


def update_Takeoff_Alt(alt):
    global Takeoff_Alt
    Takeoff_Alt = alt


def getTakeoffAlt():
    global Takeoff_Alt
    return Takeoff_Alt


def update_RemovedUAVfilename(filename, grid_path_length):
    global removed_uav_grid_file_name, removed_uav_grid_path_length
    removed_uav_grid_file_name = filename
    removed_uav_grid_path_length = grid_path_length


def getRemovedUAVfilename():
    global removed_uav_grid_file_name
    return removed_uav_grid_file_name


def getRemovedUAVgridpathlength():
    global removed_uav_grid_path_length
    return removed_uav_grid_path_length


def find_value_in_dict(value_to_find, data_dict):
    for key, values in data_dict.items():
        if value_to_find in values:
            return key
    return None
