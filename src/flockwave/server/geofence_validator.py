from shapely.geometry import Point, Polygon
from shapely.prepared import prep
import math


# -----------------------------
# Base fence class (geometry owner)
# -----------------------------
class Fence:
    def __init__(self, fence_coords, label=None):
        """
        :param fence_coords: List of (lat, lon) tuples
        """
        # Convert (lat, lon) -> (lon, lat) for Shapely
        polygon = Polygon([(lon, lat) for lat, lon in fence_coords])

        if not polygon.is_valid:
            raise ValueError(f"Invalid fence polygon: {label or 'fence'}")

        self.polygon = prep(polygon)
        self.label = label or "fence"

    def contains_point(self, lat, lon):
        """
        Check if a point is inside or on the boundary of the fence.
        """
        return self.polygon.covers(Point(lon, lat))


# -----------------------------
# Goal validator (simple point checks)
# -----------------------------
class GoalFenceValidator:
    def __init__(self, fence: Fence):
        self.fence = fence

    def is_point_inside(self, point):
        """
        Check if a single point is inside the fence.
        """
        lat, lon = point
        return self.fence.contains_point(lat, lon)

    def are_points_all_inside(self, points):
        """
        Check if all points are inside the fence.
        """
        return all(self.is_point_inside(p) for p in points)


# -----------------------------
# Search / coverage validator (area-aware)
# -----------------------------
class SearchAreaValidator:
    def __init__(self, fence: Fence):
        self.fence = fence

    def _offset_point(self, lat, lon, dx_m, dy_m):
        """
        Offset a lat/lon point by meters.
        dx_m: east (+) / west (-)
        dy_m: north (+) / south (-)
        """
        meters_per_deg_lat = 111_320
        meters_per_deg_lon = meters_per_deg_lat * math.cos(math.radians(lat))

        new_lat = lat + (dy_m / meters_per_deg_lat)
        new_lon = lon + (dx_m / meters_per_deg_lon)

        return new_lat, new_lon

    def is_point_with_coverage_inside(self, point, coverage_area_m):
        """
        Check if a point and its coverage area (diameter in meters) are fully inside the fence.
        """
        lat, lon = point
        radius = coverage_area_m / 2

        # Points to check: center + top/bottom/left/right edges
        check_points = [
            (lat, lon),  # center
            self._offset_point(lat, lon, 0, radius),  # top
            self._offset_point(lat, lon, 0, -radius),  # bottom
            self._offset_point(lat, lon, radius, 0),  # right
            self._offset_point(lat, lon, -radius, 0),  # left
        ]

        return all(self.fence.contains_point(p[0], p[1]) for p in check_points)

    def are_points_with_coverage_inside(self, points, coverage_diameter_m):
        """
        Check if ALL points (with coverage area) are fully inside the fence.

        :param points: list of (lat, lon)
        :param coverage_diameter_m: coverage diameter in meters
        :return: True if all points are valid
        """
        return all(
            self.is_point_with_coverage_inside(p, coverage_diameter_m) for p in points
        )


# -----------------------------
# Example usage
# -----------------------------
# if __name__ == "__main__":
#     polygon = [
#         (13.392158, 80.228117),
#         (13.392747, 80.236340),
#         (13.386209, 80.235990),
#         (13.386442, 80.229049),
#         (13.392158, 80.228117),
#     ]

#     fence = Fence(polygon, label="mission_fence")

#     goal_validator = GoalFenceValidator(fence)
#     search_validator = SearchAreaValidator(fence)

#     point = (13.390043, 80.229374)

#     # Single-point goal validation
#     print("Single point inside:", goal_validator.is_point_inside(point))

#     # Multiple points goal validation
#     points_to_check = [(13.390043, 80.229374), (13.391, 80.230)]
#     print("All points inside:", goal_validator.are_points_all_inside(points_to_check))

#     # Search area / coverage validation
#     coverage_area = 500  # meters
#     print(
#         f"Point with {coverage_area}m coverage inside:",
#         search_validator.is_point_with_coverage_inside(point, coverage_area),
#     )

#     # Larger coverage example
#     coverage_area = 1000  # meters
#     print(
#         f"Point with {coverage_area}m coverage inside:",
#         search_validator.is_point_with_coverage_inside(point, coverage_area),
#     )
# if search_validator.are_points_with_coverage_inside(points, coverage_diameter_m):
#     print("All coverage areas are inside fence")
# else:
#     print("One or more coverage areas exceed fence")
# from shapely.geometry import Point, Polygon


# class FenceValidator:
#     def __init__(self, fence_coords, label=None):
#         self.polygon = Polygon(fence_coords)
#         self.label = label if label else "fence"

#     def is_point_inside(self, point):
#         point_obj = Point(point)
#         return self.polygon.contains(point_obj)

#     def are_points_all_inside(self, points):
#         """
#         Check if all points are inside the fence.

#         :param points: List of tuples [(lat1, lon1), (lat2, lon2), ...]
#         :return: True if all points are inside, False if any point is outside
#         """
#         return all(self.is_point_inside(point) for point in points)


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
