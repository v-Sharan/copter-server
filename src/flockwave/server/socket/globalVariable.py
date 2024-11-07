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
mission_index = 0
alts: dict[int, int] = {
    1: 100,
    3: 110,
    5: 120,
    # 1: 100,
    # 2: 110,
    # 3: 120,
    # 5: 100,
    # 6: 140,
    # 7: 150,
    # 8: 160,
    # 10: 110,
    # 11: 180,
    # 12: 190,
    # 13: 200,
    # 14: 210,
    # 15: 220,
    # 16: 230,
    # 18: 240,
    # 20: 250,
    # 22: 260,
    # 23: 270,
    # 24: 280,
    # 25: 290,
}

drone = {1: 1, 3: 2, 5: 3}

past_distance: int | float = 0.0
plat: float = 0.0
plon: float = 0.0

# batch_wise_location = {
#     ("01", "02", "03", "05", "06"): (13.21, 10),
#     ("07", "08", "10", "11", "12"): (12.22, 10),
#     ("13", "14", "15", "16", "18"): (12.22, 10),
#     ("20", "22", "23", "24", "25"): (12.22, 10),
# }


# def find_value_in_dict(value_to_find: str) -> tuple[float] | None:
#     global batch_wise_location
#     locations = batch_wise_location
#     for key, values in locations.items():
#         if value_to_find in key:
#             return values
#     return None
trail: bool = False


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
