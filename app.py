from flask import Flask, render_template, Response
import cv2
import urllib.request
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')

app = Flask(__name__, template_folder='templates')  # Đảm bảo Flask tìm đúng thư mục templates

# 🔹 Địa chỉ camera IP
CAMERA_URL = 'http://192.168.43.243/cam-hi.jpg'

def generate_frames():
    while True:
        try:
            # Lấy ảnh từ camera IP
            img_resp = urllib.request.urlopen(CAMERA_URL, timeout=1)
            imgnp = np.array(bytearray(img_resp.read()), dtype=np.uint8)
            frame = cv2.imdecode(imgnp, -1)

            if frame is None:
                continue

            # Mã hóa frame thành JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            # Trả về frame dưới dạng streaming
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

        except Exception as e:
            print("Lỗi:", e)
            continue

@app.route('/')
def index():
    return render_template('camera.html')  # Flask sẽ render đúng file trong "templates/"

@app.route('/video')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace;
