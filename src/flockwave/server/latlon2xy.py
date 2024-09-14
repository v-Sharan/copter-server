import math, csv, os
from scipy import interpolate


def destination_location(homeLattitude, homeLongitude, distance, bearing):
    R = 6371e3  # Radius of earth in metres
    rlat1 = homeLattitude * (math.pi / 180)
    rlon1 = homeLongitude * (math.pi / 180)
    d = distance
    bearing = bearing * (math.pi / 180)  # Converting bearing to radians
    rlat2 = math.asin(
        (math.sin(rlat1) * math.cos(d / R))
        + (math.cos(rlat1) * math.sin(d / R) * math.cos(bearing))
    )
    rlon2 = rlon1 + math.atan2(
        (math.sin(bearing) * math.sin(d / R) * math.cos(rlat1)),
        (math.cos(d / R) - (math.sin(rlat1) * math.sin(rlat2))),
    )
    rlat2 = rlat2 * (180 / math.pi)  # Converting to degrees
    rlon2 = rlon2 * (180 / math.pi)  # converting to degrees
    location = [rlat2, rlon2]
    return location


def distance_bearing(
    homeLattitude, homeLongitude, destinationLattitude, destinationLongitude
):
    R = 6371e3  # Radius of earth in metres
    rlat1 = homeLattitude * (math.pi / 180)
    rlat2 = destinationLattitude * (math.pi / 180)
    rlon1 = homeLongitude * (math.pi / 180)
    rlon2 = destinationLongitude * (math.pi / 180)
    dlat = (destinationLattitude - homeLattitude) * (math.pi / 180)
    dlon = (destinationLongitude - homeLongitude) * (math.pi / 180)
    # haversine formula to find distance
    a = (math.sin(dlat / 2) * math.sin(dlat / 2)) + (
        math.cos(rlat1) * math.cos(rlat2) * (math.sin(dlon / 2) * math.sin(dlon / 2))
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # distance in metres
    # formula for bearing
    y = math.sin(rlon2 - rlon1) * math.cos(rlat2)
    x = math.cos(rlat1) * math.sin(rlat2) - math.sin(rlat1) * math.cos(
        rlat2
    ) * math.cos(rlon2 - rlon1)
    bearing = math.atan2(y, x)  # bearing in radians
    bearingDegrees = bearing * (180 / math.pi)
    out = [distance, bearingDegrees]
    return out


def geoToCart(origin, endDistance, geoLocation):
    # The initial point of rectangle in (x,y) is (0,0) so considering the current
    # location as origin and retreiving the latitude and longitude from the GPS
    # origin = (12.948048, 80.139742) Format

    # Calculating the hypot end point for interpolating the latitudes and longitudes
    rEndDistance = math.sqrt(2 * (endDistance**2))

    # The bearing for the hypot angle is 45 degrees considering coverage area as square
    bearing = 45

    # Determining the Latitude and Longitude of Middle point of the sqaure area
    # and hypot end point of square area for interpolating latitude and longitude
    lEnd, rEnd = destination_location(
        origin[0], origin[1], rEndDistance, 180 + bearing
    ), destination_location(origin[0], origin[1], rEndDistance, bearing)

    # Array of (x,y)
    x_cart, y_cart = [-endDistance, 0, endDistance], [-endDistance, 0, endDistance]

    # Array of (latitude, longitude)
    x_lon, y_lat = [lEnd[1], origin[1], rEnd[1]], [lEnd[0], origin[0], rEnd[0]]

    # Latitude interpolation function
    f_lat = interpolate.interp1d(y_lat, y_cart)

    # Longitude interpolation function
    f_lon = interpolate.interp1d(x_lon, x_cart)

    # Converting (latitude, longitude) to (x,y) using interpolation function
    y, x = f_lat(geoLocation[0]), f_lon(geoLocation[1])
    return (y, x)


def cartToGeo(origin, endDistance, cartLocation):
    # The initial point of rectangle in (x,y) is (0,0) so considering the current
    # location as origin and retreiving the latitude and longitude from the GPS
    # origin = (12.948048, 80.139742) Format

    # Calculating the hypot end point for interpolating the latitudes and longitudes
    rEndDistance = math.sqrt(2 * (endDistance**2))

    # The bearing for the hypot angle is 45 degrees considering coverage area as square
    bearing = 45

    # Determining the Latitude and Longitude of Middle point of the sqaure area
    # and hypot end point of square area for interpolating latitude and longitude
    lEnd, rEnd = destination_location(
        origin[0], origin[1], rEndDistance, 180 + bearing
    ), destination_location(origin[0], origin[1], rEndDistance, bearing)

    # Array of (x,y)
    x_cart, y_cart = [-endDistance, 0, endDistance], [-endDistance, 0, endDistance]

    # Array of (latitude, longitude)
    x_lon, y_lat = [lEnd[1], origin[1], rEnd[1]], [lEnd[0], origin[0], rEnd[0]]

    # Latitude interpolation function
    f_lat = interpolate.interp1d(y_cart, y_lat)

    # Longitude interpolation function
    f_lon = interpolate.interp1d(x_cart, x_lon)

    # Converting (latitude, longitude) to (x,y) using interpolation function
    lat, lon = f_lat(cartLocation[1]), f_lon(cartLocation[0])
    return (lat, lon)


async def write_to_csv(filename, data):
    with open(filename, "w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        for row in data:
            csv_writer.writerow(row)


# a, b = cartToGeo([12.924801, 80.042719], 3000, [225, 550])
# print(a, b)
# if __name__ == "__main__":
#     endDistance = 3000
#     origin = (12.929028, 80.045107)
#     # arr = [[12.9093106,80.1219986],[12.9092763,80.1219466],[12.9092298,80.1219081],[12.9091872,80.1218708],[12.9091328,80.1218269]]
#     # for i in range(len(arr)):
#     #     b,a = geoToCart(origin, endDistance, arr[i])
#     #     x,y=float(b), float(-a)
#     #     print(x,y)

#     # lat,lon = cartToGeo(origin,endDistance,[71,186])
#     # print(lat,lon)
#     y, x = geoToCart(origin, endDistance, [12.9300747, 80.0475099])
#     print(y, -x)

# # "C:/Users/vshar/OneDrive/Documents/blenderfiles/10-drones/A8mini/a8mini-path-{}.kml"
# -1.2031520051268958,-7.573107442949441,5.0
# -2.0875201441611875,-0.8340426701929009,5.0
# -3.177555294992016,10.451312771712765,5.0
# -6.28312713658592,-8.462752957663836,5.0
# -2.6633877713460823,5.225656385856382,5.0
# -7.907896510780984,4.591906568928152,5.0
# -7.455429090674011,-1.312227134342011,5.0
# -9.203598670485645,10.12887865445964,5.0

# ar = [
#     [-1.2031520051268958, -7.573107442949441],
#     [-2.0875201441611875, -0.8340426701929009],
#     [-3.177555294992016, 10.451312771712765],
#     [-6.28312713658592, -8.462752957663836],
#     [-2.6633877713460823, 5.225656385856382],
#     [-7.907896510780984, 4.591906568928152],
#     [-7.455429090674011, -1.312227134342011],
#     [-9.203598670485645, 10.12887865445964],
# ]

# for arr in ar:
#     # print(arr)
#     lat, lon = cartToGeo((22.333525, 87.218054), 3000, (-arr[0], -arr[1]))
#     y, x = geoToCart((22.334220, 87.217763), 3000, (lat, lon))
#     print(-x, -y)

# path = os.listdir("C:/Users/vshar/OneDrive/Desktop/output")
# print(path)
# dis = distance_bearing(13.389387, 80.229761, 13.412900, 80.314072)
# print("dis...........", dis)

# 13.400562, 80.246590 -- test 1
# [2204.062957040227, 55.68053994642359]

# 13.402347, 80.2747666 -- test 2
# test 2  [5077.053142702974, 73.50508296101127]

# 13.412900, 80.314072 -- test 3
# test 3 [9487.066970522823, 73.99314633603083]
