from flask import Flask, Response
import cv2
import numpy as np

app = Flask(__name__)

def generate_frames():
cap = cv2.VideoCapture(0)

while cap.isOpened():
ret, frame = cap.read()

frame_encode = cv2.imencode(".jpg", frame)[1]
data_encode = np.array(frame_encode)
byte_encode = data_encode.tobytes()

yield b'--frame\r\nContent-Type: image/jpg\r\n\r\n' + byte_encode + b'\r\n'

if cv2.waitKey(1) & 0xFF == ord('q'):
break

cap.release()
cv2.destroyAllWindows()

@app.route('/video_feed')
def video_feed():
return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
app.run(host='0.0.0.0', port=5000, threaded=True)