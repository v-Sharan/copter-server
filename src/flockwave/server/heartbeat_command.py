import socket
import time
import logging

# from modules.utils import *

# Initialize logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
heartbeat = [0xEB, 0x90, 0x07, 0x55, 0xAA, 0xDC, 0x04, 0x10, 0x00, 0x14, 0x3]
get_zoom = [0x55, 0xAA, 0xDC, 0x01, 0x14, 0x20]
HOST = "192.168.6.121"  # The server's hostname or IP address
PORT = 2000  # The port used by the server


def connect_to_server(host, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        logging.info(f"Connected to server {host}:{port}")
        return s
    except Exception as e:
        logging.error(f"Error connecting to server: {e}")
        return None


def hex_to_decimal(hex_str):
    return int(hex_str, 16)


def send_command(socket, heartbeat):
    packet = bytearray(heartbeat)
    bytePacket = bytes(packet)
    try:
        socket.sendall(bytePacket)
        logging.info(f"Command sent: {heartbeat}")

        # Receive response
        response = socket.recv(1024)  # Adjust the buffer size as needed
        logging.info(f"Response received: {response}")

        # Convert response to a list of hex values
        hex_response = [f"{byte:02x}" for byte in response]
        logging.info(f"Response in hex: {hex_response}")

        hex_sequence = "".join(hex_response)
        # Output the results
        # print('Hex Sequence:', hex_sequence)
        hex_sequence = hex_sequence[24:]
        # print('hex_sequence',hex_sequence)

        # # Drone Latitude (3 ~ 6 bytes)
        # drone_latitude = hex_to_decimal(hex_sequence[4:12])

        # # # Drone Longitude (7 ~ 10 bytes)
        # drone_longitude = hex_to_decimal(hex_sequence[12:20])

        # # # Drone Altitude (11 ~ 12 bytes)
        # drone_altitude = hex_to_decimal(hex_sequence[20:24])

        # # Target Latitude (13 ~ 16 bytes)
        target_latitude = hex_to_decimal(hex_sequence[24:32])

        # # Target Longitude (17 ~ 20 bytes)
        target_longitude = hex_to_decimal(hex_sequence[32:40])

        # # # # Target Altitude (21 ~ 22 bytes)
        # # target_altitude = hex_to_decimal(hex_sequence[40:44])
        print("hex_sequence[101:108]", hex_sequence[-6:-2])
        zoom_value = hex_to_decimal(hex_sequence[-6:-2])
        print("zoom_value", zoom_value * 0.1)
        # # # Output the values
        # print(f"Drone Latitude: {drone_latitude}")
        # print(f"Drone Longitude: {drone_longitude}")
        # print(f"Drone Altitude: {drone_altitude}")
        print(f"Target Latitude: {target_latitude}")
        print(f"Target Longitude: {target_longitude}")
        # print(f"Target Altitude: {target_altitude}")
        # Further interpretation can be done here based on protocol
        # For example, if the first byte indicates a status:
        status = response[0]  # Example: first byte as status
        logging.info(f"Status: {status}")

    except Exception as e:
        logging.error(f"Error sending command: {e}")


def main():
    s = connect_to_server(HOST, PORT)
    if s is None:
        return
    try:
        while 1:
            time.sleep(0.08)
            send_command(s, heartbeat)  # Send the command
            logging.info("Command sent and response received")
    except KeyboardInterrupt:
        logging.info("Program interrupted by user")
    finally:
        s.close()
        logging.info("Socket closed")


if __name__ == "__main__":
    main()
