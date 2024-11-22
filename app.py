from flask import Flask, render_template, request, jsonify, redirect, url_for, session,Response
import json
import os
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import google.generativeai as genai
from close_end_questionaire import get_random_close_questions
import csv
from open_end_questions import get_random_open_questions
import pandas as pd
from csv_extracter import csv_to_string
import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from gemini_ai import gemini_chat
from image_analysis import analyze_image
from werkzeug.utils import secure_filename
from trained_chikitsa import chatbot_response
import cv2
# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secret_key'

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'image_analysis/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    """
    Checks if the file has an allowed extension.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# Initialize Gemini AI
genai.configure(api_key=os.getenv("API_KEY"))

# Define User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, email, password, name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

# Create database tables
with app.app_context():
    db.create_all()

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

# Registration Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Check for existing user
        if User.query.filter_by(email=email).first():
            return render_template('register.html', error='Email already exists.')

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/closed_ended')
        else:
            return render_template('login.html', error='Invalid credentials.')

    return render_template('login.html')

@app.route('/closed_ended')
def close_ended():
    random_questions = get_random_close_questions()  # Get random 5 questions
    return render_template('closed_ended.html', questions=random_questions)

@app.route('/submit_close_end', methods=['POST'])
def submit_close_ended():
    if request.method == 'POST':
        responses = []
        for question in request.form:
            answer = request.form[question]
            responses.append((question, answer))
        
        # Save responses to CSV
        save_to_csv(responses)
        
        return redirect(url_for('submit_opended'))  # Corrected here

def save_to_csv(responses):
    file_exists = os.path.isfile('responses/close_end_questions_responses.csv')

    with open('responses/close_end_questions_responses.csv', mode='w', newline='') as file:  # Changed to 'a'
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Question', 'Answer'])  # Write header if the file doesn't exist
        
        for response in responses:
            writer.writerow(response)


@app.route('/open_ended', methods=['GET', 'POST'])
def submit_opended():
    if request.method == 'POST':
        responses = {key: value for key, value in request.form.items()}
        save_responses_to_csv(responses)
        return redirect(url_for('thank_you'))  # Corrected here
    else:
        random_questions = get_random_open_questions()  # Call the function from the imported file
        return render_template('open_ended.html', questions=random_questions)
def save_responses_to_csv(responses):
    file_exists = os.path.isfile('responses/open_end_questions_responses.csv')

    # Prepare the data to be saved
    data_to_save = [(question, responses[question]) for question in responses]

    # Create a DataFrame from the prepared data
    df = pd.DataFrame(data_to_save, columns=['Question', 'Response'])
    
    # Save to CSV
    df.to_csv('responses/open_end_questions_responses.csv', mode='w', header=not file_exists, index=False)

# @app.route('/thank_you')
# def thank_you():
    
#     close_ended_str = csv_to_string("responses/close_end_questions_responses.csv")
#     open_ended_str = csv_to_string("responses/open_end_questions_responses.csv")
#     default=" this is my assesment of close ended questions and open ended questions , give feed back on me "
#     judge_gemini = gemini_chat(default+" "+close_ended_str+" "+open_ended_str)
#     summarize = gemini_chat("summarize this in 200 words "+judge_gemini)
#     return render_template('thank_you.html', judge_gemini=summarize)
@app.route('/thank_you')
def thank_you():
    # Get the email from the session
    email = session.get('email')

    if email:
        # Retrieve user data from the database using the email
        user = User.query.filter_by(email=email).first()
        user_name = user.name if user else "User"  # Default to "User" if not found
    else:
        user_name = "Guest"  # Default to "Guest" if email is not in the session

    # Generate the Gemini feedback
    close_ended_str = csv_to_string("responses/close_end_questions_responses.csv")
    open_ended_str = csv_to_string("responses/open_end_questions_responses.csv")
    default = "This is my assessment of close-ended questions and open-ended questions. Please provide feedback on me."
    judge_gemini = gemini_chat(default + " " + close_ended_str + " " + open_ended_str)
    mainprompt="Please summarize the following content in 150 words. Analyze my strengths and weaknesses, identify areas for improvement, and provide actionable suggestions on how to improve. Also, give an honest assessment of my mental health and well-being based on the content provided. Keep in mind that you are my digital psychiatrist, my best friend, and a well-rounded expert in various fields of knowledge. Your feedback should be constructive, empathetic, and based on your understanding of the information provided. Help me grow by offering insights on how I can become a better version of myself, both personally and professionally. at last summarize in only 150 words or less then it add some emogies for representing more connection "
    summarize = gemini_chat(mainprompt+judge_gemini)
    return render_template('thank_you.html', judge_gemini=summarize, user_name=user_name ,completejudege=judge_gemini)



from gemini_ai import gemini_chat
from gemini_ai import model

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


chat_session = model.start_chat()

# Chat function to handle user input
def gemini_chat(user_input, history_file="dataset/intents.json"):
    try:
        # Load intents from JSON or initialize
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                intents_data = json.load(f)
        else:
            intents_data = {"intents": []}

        # Send user input to the model
        response = chat_session.send_message(user_input)

        # Create a new intent object for the conversation
        new_intent = {
            "patterns": [user_input],
            "responses": [response.text.strip()],
        }

        # Append the new intent to the intents list
        intents_data['intents'].insert(1, new_intent)

        # Save the updated intents JSON file
        with open(history_file, 'w') as f:
            json.dump(intents_data, f, indent=4)

        return response.text

    except Exception as e:
       
        response = chatbot_response(user_input)
        # Optionally log the error to a file
        with open('error.log', 'a') as log_file:
            log_file.write(f"{str(e)}\n")
        return response
# in excecption the pretained model so if error occurs then it can use the pretrained model 
# Chat Route
@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('main.html')
    elif request.method == 'POST':
        user_input = request.form['user_input']
        response = gemini_chat(user_input)  # Call gemini_chat function here
        return jsonify({'response': response})
    else:
        return "Unsupported request method", 405  # Handle other methods if needed


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining images for a renowned hospital. Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.
you have to analayse the image but and predict the cause or whats that 
Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."
3. Your insights are invaluable in guiding clinical decisions. Please proceed with analysis, adhering to the structured approach outlined above.
"""
@app.route('/image_analysis', methods=['GET', 'POST'])
def image_analysis():
    analysis = None
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)

        uploaded_file = request.files['file']
        if uploaded_file.filename == '':
            return redirect(request.url)

        if uploaded_file:
            # Process the uploaded image
            image_data = uploaded_file.read()

            # Prepare image parts
            image_parts = [{
                "mime_type": "image/jpeg",
                "data": image_data
            }]
            
            # Prepare the prompt parts
            prompt_parts = [
                image_parts[0],
                system_prompt,
            ]

            # Generate a response based on the prompt and image
            response = model.generate_content(prompt_parts)
            analysis = response.text
    return render_template('image_analysis.html', analysis=analysis)


from fer import FER
# # Initialize emotion detection model
emotion_detector = FER(mtcnn=True)


# Initialize global variables
attention_status = "Not Paying Attention"
dominant_emotion = "neutral"  # Default value

def is_paying_attention(emotions_dict, threshold=0.5):
    """ Checks if the user is paying attention based on emotion scores. """
    dominant_emotion = max(emotions_dict, key=emotions_dict.get)
    emotion_score = emotions_dict[dominant_emotion]
    return emotion_score > threshold, dominant_emotion

def detect_emotion_and_attention(frame):
    """ Detects emotion and attention from the frame. """
    global attention_status, dominant_emotion

    results = emotion_detector.detect_emotions(frame)

    for result in results:
        bounding_box = result["box"]
        emotions_dict = result["emotions"]

        # Update attention status and dominant emotion
        paying_attention, dominant_emotion = is_paying_attention(emotions_dict)
        attention_status = "Paying Attention" if paying_attention else "Not Paying Attention"

        # Draw bounding box and display emotion info
        x, y, w, h = bounding_box
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        emotion_text = ", ".join([f"{emotion}: {prob:.2f}" for emotion, prob in emotions_dict.items()])
        cv2.putText(frame, f"{dominant_emotion} ({attention_status})", (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.putText(frame, emotion_text, (x, y + h + 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

    return frame

# Video feed generator
def generate_frames():
    """ Captures frames from the webcam and detects emotion and attention. """
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = detect_emotion_and_attention(frame)
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()

# Flask route for the chatbot interaction
@app.route('/talk_to_me', methods=['GET', 'POST'])
def talk_to_me():
    """ Handles the user's input and sends it to the chatbot along with emotion and attention. """
    global attention_status, dominant_emotion

    if request.method == 'GET':
        return render_template('talk_to_me.html')

    elif request.method == 'POST':
        user_input = request.form.get('user_input', '')

        # Create the prompt with the attention status and emotion
        prompt = f"The user is in a {dominant_emotion} mood and is {'paying attention' if attention_status == 'Paying Attention' else 'not paying attention'}."

        # Call the gemini_chat function with the user input and the generated prompt
        bot_response = gemini_chat(user_input + " " + prompt)

        return jsonify({'response': bot_response})

    else:
        return "Unsupported request method", 405

def log_conversation(user_input, bot_response, history_file="dataset/intents.json"):
    # Load or initialize intents data
    if os.path.exists(history_file):
        with open(history_file, 'r') as f:
            intents_data = json.load(f)
    else:
        intents_data = {"intents": []}

    # Create a new intent object
    new_intent = {
        "patterns": [user_input],
        "responses": [bot_response],
    }

    # Append the new intent
    intents_data['intents'].append(new_intent)

    # Save the updated intents JSON file
    with open(history_file, 'w') as f:
        json.dump(intents_data, f, indent=4)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(debug=True)
    