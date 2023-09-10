import cv2
import socket
import time

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam
cap = cv2.VideoCapture(0)  # 0 indicates the default camera

host, port = "127.0.0.1", 25001
base_coordinate = [0, 2, 1]


# # Number of times you want to connect
# num_connections = 5

while True:
    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally (mirror image)
    mirrored_frame = cv2.flip(frame, 1)

    # Convert the mirrored frame to grayscale for face detection
    gray_frame = cv2.cvtColor(mirrored_frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the mirrored frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:

        center_x = x + w // 2
        center_y = y + h // 2
        z_coordinate = w  # Assuming z-coordinate is proportional to the width of the face box

        # Display the coordinates and z-coordinate near the center of the face rectangle
        data = f"{center_x/100}, {center_y/100}, {z_coordinate/100}"

    # data = f"{base_coordinate[0]+i},{base_coordinate[1]},{base_coordinate[2]}"
    print(data)
    
    # SOCK_STREAM means TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server and send the data
        sock.connect((host, port))
        sock.sendall(data.encode("utf-8"))
        response = sock.recv(1024).decode("utf-8")
        print(response)

    finally:
        sock.close()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    # Optional: wait for a short duration before the next connection
    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()
