from flask import Flask, render_template, Response
from flask_cors import CORS  # Import CORS
import cv2
import urllib.request
import numpy as np

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Camera URL (Use public IP or domain if accessing remotely)
CAMERA_URL = 'http://192.168.43.243/cam-hi.jpg'  # Replace with public IP if needed

def generate_frames():
    while True:
        try:
            # Fetch frame from IP camera
            img_resp = urllib.request.urlopen(CAMERA_URL, timeout=1)
            img_np = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(img_np, -1)

            if frame is None:
                continue

            # Encode frame to JPEG format
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Yield frame as part of the HTTP response stream
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print(f"Error fetching camera feed: {e}")
            continue

@app.route('/')
def index():
    """ Render the HTML page """
    return render_template('camera.html')

@app.route('/video')
def video_feed():
    """ Stream video frames """
    return Response(generate_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
