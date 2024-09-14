import math


# Function to convert pixel coordinates to angular displacement (in degrees)
def pixel_to_angle(
    pixel_x,
    pixel_y,
    focal_length_mm,
    sensor_width,
    sensor_height,
    image_width,
    image_height,
    center_x,
    center_y,
    current_pitch,
    current_yaw,
):
    """
    Converts pixel coordinates to angular displacement (degrees) from the center of the image, taking into account the initial gimbal angles.

    Args:
    - pixel_x, pixel_y: Pixel coordinates to be centered.
    - focal_length_mm: Focal length of the camera in millimeters.
    - sensor_width, sensor_height: Physical dimensions of the sensor in millimeters.
    - image_width, image_height: Dimensions of the image in pixels.
    - center_x, center_y: Center pixel coordinates (usually the center of the image).
    - current_pitch, current_yaw: Current pitch and yaw angles of the gimbal.

    Returns:
    - new_pitch, new_yaw: Updated gimbal angles to center the pixel.
    """

    # Convert focal length from mm to pixels
    focal_length_x = (focal_length_mm * image_width) / sensor_width
    focal_length_y = (focal_length_mm * image_height) / sensor_height

    # Calculate normalized coordinates
    norm_x = (pixel_x - center_x) / focal_length_x
    norm_y = (pixel_y - center_y) / focal_length_y

    # Calculate angles in radians
    angle_x_rad = math.atan(norm_x)
    angle_y_rad = math.atan(norm_y)

    # Convert angles to degrees
    angle_x_deg = math.degrees(angle_x_rad)
    angle_y_deg = math.degrees(angle_y_rad)

    # Update gimbal angles
    new_pitch = current_pitch + angle_y_deg
    new_yaw = current_yaw + angle_x_deg

    return new_pitch, new_yaw


# Example usage
if __name__ == "__main__":
    # Example parameters
    focal_length_mm = 21  # Focal length in millimeters
    sensor_width = 7.6  # Sensor width in millimeters
    sensor_height = 5.7  # Sensor height in millimeters
    image_width = 4096  # Image width in pixels
    image_height = 2160  # Image height in pixels
    center_x = image_width // 2  # Image center x-coordinate
    center_y = image_height // 2  # Image center y-coordinate

    # Pixel coordinates that you want to center
    pixel_x = 710
    pixel_y = 442

    # Convert pixel coordinates to angular displacement (degrees)
    yaw_angle, pitch_angle = pixel_to_angle(
        pixel_x,
        pixel_y,
        focal_length_mm,
        sensor_width,
        sensor_height,
        image_width,
        image_height,
        center_x,
        center_y,
        10,
        -20,
    )

    # Print the result
    print(f"Yaw (horizontal angle): {yaw_angle:.2f} degrees")
    print(f"Pitch (vertical angle): {pitch_angle:.2f} degrees")
