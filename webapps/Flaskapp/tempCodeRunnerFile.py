from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory(directory=app.static_folder, path='bio.html')

@app.route('/schedule')
def bio():
    return send_from_directory(directory=app.static_folder, path='schedule.html')

@app.route('/links')
def bio():
    return send_from_directory(directory=app.static_folder, path='links.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)  # Use a different port, such as 8000
