import cv2
import socket
import time

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the webcam
cap = cv2.VideoCapture(0)  # 0 indicates the default camera

host, port = "127.0.0.1", 25001

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

    if len(faces) > 0:
        # Take the first detected face (you can modify this logic if needed)
        x, y, w, h = faces[0]

        center_x = x + w // 2
        center_y = y + h // 2
        z_coordinate = w  # Assuming z-coordinate is proportional to the width of the face box

        # Display the coordinates and z-coordinate near the center of the face rectangle
        data = [center_x/100, center_y/100, z_coordinate/100]

        print(data)

        # You can break here if you only want to capture the initial face coordinates
        break

    # Add a delay to avoid excessive CPU usage
    time.sleep(0.1)
    

while True:
    start_time = time.time()

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
        shift = [center_x/100-data[0], (center_y/100-data[1])*-1, (z_coordinate/100-data[2])*-1]
        data = [center_x/100, center_y/100, z_coordinate/100]
    
    shiftString = f"{shift[0]},{shift[1]},{shift[2]}"
    print(shiftString)

    # SOCK_STREAM means TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Connect to the server and send the data
        sock.connect((host, port))
        sock.sendall(shiftString.encode("utf-8"))
        response = sock.recv(1024).decode("utf-8")
        print(response)

    finally:
        sock.close()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"Time taken: {time_taken:.6f} seconds")
    
    # Optional: wait for a short duration before the next connection
    time.sleep(0.1)

cap.release()
cv2.destroyAllWindows()
