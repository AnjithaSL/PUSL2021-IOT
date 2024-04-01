import cv2
import numpy as np
import time
import serial
import sys

# Function to calculate speed
def calculate_speed(distance, time_diff):
    speed = distance / time_diff
    return speed

# Constants
LEFT_LINE_X = 100     # x-coordinate of the left line
RIGHT_LINE_X = 500    # x-coordinate of the right line
LINE_Y = 50           # y-coordinate of the line

# Initialize variables
object_passed_left = False
object_passed_right = False
start_time = None

# Function to detect when the object passes the line
def check_object_passed(x):
    global object_passed_left, object_passed_right
    if x < LEFT_LINE_X:
        object_passed_left = True
    elif x > RIGHT_LINE_X:
        object_passed_right = True

# Function to draw lines on the frame
def draw_lines(frame):
    cv2.line(frame, (LEFT_LINE_X, 0), (LEFT_LINE_X, frame.shape[0]), (0, 255, 0), 2)
    cv2.line(frame, (RIGHT_LINE_X, 0), (RIGHT_LINE_X, frame.shape[0]), (0, 255, 0), 2)

try:
    # Initialize serial communication with ESP32
    ser = serial.Serial('COM4', 9600)  # Adjust port name and baud rate as needed
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    sys.exit(1)

# Capture video from the webcam
# cap = cv2.VideoCapture(0)
# Capture video from the USB webcam
cap = cv2.VideoCapture(1)  # Change index to 1 if the USB webcam is recognized as the second camera

# Main loop
while True:
    ret, frame = cap.read()
    if not ret:
        break

    draw_lines(frame)

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect objects in the frame
    detector = cv2.SimpleBlobDetector_create()
    keypoints = detector.detect(gray)

    for keypoint in keypoints:
        x = int(keypoint.pt[0])
        y = int(keypoint.pt[1])

        cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

        check_object_passed(x)

    if object_passed_left and object_passed_right:
        if start_time is None:
            start_time = time.time()
        else:
            end_time = time.time()
            time_diff = end_time - start_time
            distance = RIGHT_LINE_X - LEFT_LINE_X
            speed = calculate_speed(distance, time_diff)
            print("Speed:", speed, "pixels per second")
            # Send speed data to ESP32
            try:
                ser.write(f"Speed: {speed} pixels per second\n".encode())
            except serial.SerialException as e:
                print(f"Error writing to serial port: {e}")
            start_time = None
            object_passed_left = False
            object_passed_right = False

    cv2.imshow('Frame', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
