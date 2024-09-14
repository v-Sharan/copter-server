home_pos = []
goal_points = []
goal_table = []
return_goal_table = []
grid_path_table = []
Takeoff_Alt = 2.5
logCounter = 0
log_file_path = ""
area_covered, minutes, seconds = 0, 0, 0
removed_uav_grid_file_name = []
removed_uav_grid_path_length = []
gimbal_target = []


def update_coverage_time(area_covered1, minutes1, seconds1):
    global area_covered, minutes, seconds
    area_covered = area_covered1
    minutes = minutes1
    seconds = seconds1


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
