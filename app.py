from flask import Flask, send_from_directory, jsonify
import cv2
from screeninfo import get_monitors

app = Flask(__name__)

# Get screen dimensions
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

cap = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

@app.route('/')
def home():
    return send_from_directory(app.static_folder, path="index.html")

@app.route('/face')
def face():
    ret, frame = cap.read()
    reversed_frame = cv2.flip(frame, 1)
    resized_frame = cv2.resize(reversed_frame, (screen_width, screen_height))
    gray = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        xCoord, yCord = int(x + w/2), int(y + h/2)  # Update coordinates

    return jsonify(x=xCoord, y=yCord)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # Changed port to 8000
