import cv2
import socket
import time
import csv
import struct

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Open the webcam
cap = cv2.VideoCapture(0)

host, port = "127.0.0.1", 25001

# Create a persistent socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        mirrored_frame = cv2.flip(frame, 1)
        gray_frame = cv2.cvtColor(mirrored_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        if len(faces) > 0:
            x, y, w, h = faces[0]
            center_x = x + w // 2
            center_y = y + h // 2
            z_coordinate = w
            data = [center_x/100, center_y/100, z_coordinate/100]
            break

        time.sleep(0.1)

    for i in range(100):
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            break

        mirrored_frame = cv2.flip(frame, 1)
        gray_frame = cv2.cvtColor(mirrored_frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            center_x = x + w // 2
            center_y = y + h // 2
            z_coordinate = w
            shift = [center_x/100-data[0], (center_y/100-data[1])*-1, (z_coordinate/100-data[2])*-1]
            data = [center_x/100, center_y/100, z_coordinate/100]

        packed_data = struct.pack('!fff', shift[0], shift[1], shift[2])
        sock.sendall(packed_data)

        binary_response = sock.recv(1024)
    
        # If the server is sending back the same packed floats:
        if len(binary_response) == 12:  # 3 floats * 4 bytes each
            x, y, z = struct.unpack('!fff', binary_response)
            print(f"Received from server: x={x}, y={y}, z={z}")

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        end_time = time.time()
        time_taken = end_time - start_time
        print(f"Time taken: {time_taken:.6f} seconds")

        with open('benchmark_times.csv', 'a', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            if i == 0:
                csvwriter.writerow(['Iteration', 'Time Taken (seconds)'])
            csvwriter.writerow([i, f"{time_taken:.6f}"])

        # time.sleep(0.1)

finally:
    sock.close()
    cap.release()
    cv2.destroyAllWindows()
