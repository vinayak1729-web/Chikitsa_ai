from flask import Flask, request, jsonify, render_template, Response
from gemini_ai import gemini_chat  # Ensure this exists in your gemini_ai module
import cv2
from fer import FER

app = Flask(__name__)

# Initialize emotion detection model
emotion_detector = FER(mtcnn=True)

# Route for "Talk to Me" functionality
@app.route('/talk_to_me', methods=['POST'])
def talk_to_me():
    try:
        user_input = request.form['user_input']
        bot_response = gemini_chat(user_input)  # Fetch response using your function
        return jsonify({'response': bot_response})
    except Exception as e:
        print(f"Error during chat: {e}")
        return jsonify({'response': 'An error occurred. Please try again.'})

# Video feed for emotion detection
def detect_emotion_and_attention(frame):
    attention_status = "Not Paying Attention"
    results = emotion_detector.detect_emotions(frame)

    for result in results:
        bounding_box = result["box"]
        emotions_dict = result["emotions"]
        x, y, w, h = bounding_box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        dominant_emotion = max(emotions_dict, key=emotions_dict.get)
        attention_status = "Paying Attention" if emotions_dict[dominant_emotion] > 0.5 else "Not Paying Attention"
        cv2.putText(frame, f"{dominant_emotion} ({attention_status})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    return frame, attention_status

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        frame, _ = detect_emotion_and_attention(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    cap.release()

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# Home route
@app.route('/')
def index():
    return render_template('Mindex.html')

if __name__ == '__main__':
    app.run(debug=True)
