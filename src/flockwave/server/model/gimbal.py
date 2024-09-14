import binascii, socket, time, threading, math


class Gimbal:

    def __init__(self, host: str, port: int = 2000) -> None:
        self.host = "192.168.6.121"
        self.port = port
        self.tlat = 0
        self.tlon = 0
        self.connected = False
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.connect_to_gimbal()
        # threading.Thread(target=self.calculate_coords, daemon=True).start()

    def calculate_coords(self):
        while self.connected:
            data, address = self.socket.recvfrom(1024)
            print(data)
            self.get_latlon(data)

    def is_connected(self) -> None:
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

    def hex_to_signed_int(hex_str: str) -> int:
        """
        Converts a little-endian hexadecimal string to a signed integer.
        """
        value = int(hex_str, 16)
        if value >= 2 ** (len(hex_str) * 4 - 1):
            value -= 2 ** (len(hex_str) * 4)
        return value

    def get_latlon(self, data_1) -> tuple:
        response_hex = binascii.hexlify(data_1).decode("utf-8")
        tlat, tlon = 0, 0
        if len(response_hex) == 94:
            tlat, tlon = self.extract_imu_angle(response_hex)
        self.tlat = tlat
        self.tlon = tlon

    def get_target_coords(self) -> tuple:
        return self.tlat, self.tlon

    def get_gps_bearing(self, homeLattitude, homeLongitude):
        destinationLattitude = self.tlat
        destinationLongitude = self.tlon
        rlat1 = homeLattitude * (math.pi / 180)
        rlat2 = destinationLattitude * (math.pi / 180)
        rlon1 = homeLongitude * (math.pi / 180)
        rlon2 = destinationLongitude * (math.pi / 180)

        # formula for bearing
        y = math.sin(rlon2 - rlon1) * math.cos(rlat2)
        x = math.cos(rlat1) * math.sin(rlat2) - math.sin(rlat1) * math.cos(
            rlat2
        ) * math.cos(rlon2 - rlon1)
        bearing = math.atan2(y, x)  # bearing in radians
        bearingDegrees = bearing * (180 / math.pi)
        return bearingDegrees
