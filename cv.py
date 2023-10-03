import cv2

def get_head_coordinates():
    # Initialize the webcam
    cap = cv2.VideoCapture(0)

    # Load the pre-trained Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Capture a single frame
    ret, frame = cap.read()

    # Reverse the frame horizontally
    reversed_frame = cv2.flip(frame, 1)

    # Convert to grayscale
    gray = cv2.cvtColor(reversed_frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Release the webcam
    cap.release()

    # Initialize coordinates
    coordinates = []

    for (x, y, w, h) in faces:
        # Append the coordinates to the list
        coordinates.append((x, y))

    return coordinates

# Get the head coordinates
head_coordinates = get_head_coordinates()
print(f"Head Coordinates: {head_coordinates}")
