from shapely.geometry import Point, Polygon


class FenceValidator:
    def __init__(self, fence_coords, label=None):
        self.polygon = Polygon(fence_coords)
        self.label = label if label else "fence"

    def is_point_inside(self, point):
        point_obj = Point(point)
        return self.polygon.contains(point_obj)

    def are_points_all_inside(self, points):
        """
        Check if all points are inside the fence.

        :param points: List of tuples [(lat1, lon1), (lat2, lon2), ...]
        :return: True if all points are inside, False if any point is outside
        """
        return all(self.is_point_inside(point) for point in points)


# --- Example usage ---
# outer_fence = [
#     [12.769186651249242, 80.00810056995162],
#     [12.703262004262484, 80.00432264717809],
#     [12.698273588867139, 80.11477127426667],
#     [12.780461518409226, 80.1149935184822],
# ]

# validator = FenceValidator(outer_fence, label="outer")

# points = [
#     (12.724293721329502, 80.08189542150944),  # inside
#     (12.73108236823613, 80.13059203109407),  # outside
#     (12.750, 80.050),  # inside
# ]

# result = validator.are_points_all_inside(points)
# print(result)  # False because one point is outside

# from shapely.geometry import Point, Polygon


# class FenceValidator:
#     def __init__(self, fence_coords, label=None):
#         """
#         Initialize the FenceValidator with a polygon fence.

#         :param fence_coords: List of [lat, lon] points defining the fence
#         :param label: Optional label for the fence
#         """
#         self.polygon = Polygon(fence_coords)
#         self.label = label if label else "fence"

#     def is_point_inside(self, point):
#         """
#         Check if the given point is inside the fence.

#         :param point: Tuple (lat, lon) of the point to check
#         :return: True if inside, False if outside
#         """
#         point_obj = Point(point)
#         return self.polygon.contains(point_obj)


# # --- Example usage ---
# # outer_fence = [
# #     [12.769186651249242, 80.00810056995162],
# #     [12.703262004262484, 80.00432264717809],
# #     [12.698273588867139, 80.11477127426667],
# #     [12.780461518409226, 80.1149935184822],
# # ]

# # validator = FenceValidator(outer_fence, label="outer")
# # point1 = (12.724293721329502, 80.08189542150944)  # inside
# # point2 = (12.73108236823613, 80.13059203109407)  # outside

# # print(validator.is_point_inside(point1))  # True
# # print(validator.is_point_inside(point2))  # False
