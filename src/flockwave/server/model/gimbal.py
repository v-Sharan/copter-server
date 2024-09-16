import binascii, socket, time, math, threading
from functools import lru_cache
from flockwave.gps.vectors import GPSCoordinate


class Gimbal:
    host: str
    port: int
    position: GPSCoordinate

    def __init__(
        self, host="192.168.6.121", port=2000, position=GPSCoordinate()
    ) -> None:
        self.host = "192.168.6.121"
        self.port = port
        self.tlat = -35.3663932
        self.tlon = 149.1625786
        self.connected = False
        self.position = position
        self.bearing = 0
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread(target=self.get_gps_bearing_loop, daemon=True).start()

    def calculate_coords(self):
        while self.connected:
            data, address = self.socket.recvfrom(1024)
            print(data)
            self.get_latlon(data)

    def is_connected(self) -> bool:
        try:
            self.socket.send(b"")
        except socket.error:
            return False
        return True

    def connect_to_gimbal(self) -> None:
        try:
            self.socket.connect((self.host, self.port))
            time.sleep(2)
            print("Connected to gimbal")
            self.connected = True
        except socket.error as e:
            print(f"Connection failed: {e}")
            self.connected = False

    @staticmethod
    @lru_cache(maxsize=None)
    def hex_to_signed_int(hex_str: str) -> int:
        """
        Converts a little-endian hexadecimal string to a signed integer.
        """
        value = int(hex_str, 16)
        if value >= 2 ** (len(hex_str) * 4 - 1):
            value -= 2 ** (len(hex_str) * 4)
        return value

    def extract_imu_angle(self, data: str) -> tuple | None:
        """
        Extracts and calculates the IMU angles from the provided data string.
        """
        if len(data) == 94:
            tlat = data[34:42]
            tlon = data[42:50]
            tlat = self.hex_to_signed_int(tlat)
            tlon = self.hex_to_signed_int(tlon)

            return tlat * 10 * -7, tlon * 10 * -7

    def get_latlon(self, data_1) -> tuple:
        response_hex = binascii.hexlify(data_1).decode("utf-8")
        tlat, tlon = 0, 0
        if len(response_hex) == 94:
            tlat, tlon = self.extract_imu_angle(response_hex)
        self.tlat = tlat
        self.tlon = tlon
        self.get_gps_bearing()  # Recalculate bearing

    def get_target_coords(self) -> tuple:
        return self.tlat, self.tlon

    def get_gps_bearing_loop(self) -> None:
        while True:
            self.bearing = self.get_gps_bearing(
                self.position.lat, self.position.lon, self.tlat, self.tlon
            )
            time.sleep(0.5)  # Reduce the frequency of recalculations

    @lru_cache(maxsize=None)
    def get_gps_bearing(
        self, lat1: float, lon1: float, lat2: float, lon2: float
    ) -> float:
        """
        Calculate and cache the GPS bearing based on coordinates.
        """
        rlat1 = lat1 * (math.pi / 180)
        rlat2 = lat2 * (math.pi / 180)
        rlon1 = lon1 * (math.pi / 180)
        rlon2 = lon2 * (math.pi / 180)

        # formula for bearing
        y = math.sin(rlon2 - rlon1) * math.cos(rlat2)
        x = math.cos(rlat1) * math.sin(rlat2) - math.sin(rlat1) * math.cos(
            rlat2
        ) * math.cos(rlon2 - rlon1)
        bearing = math.atan2(y, x)  # bearing in radians
        bearing_degrees = bearing * (180 / math.pi)
        return bearing_degrees
