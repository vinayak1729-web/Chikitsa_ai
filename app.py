from flask import Flask, render_template, request, jsonify, redirect, url_for, session
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

@app.route('/thank_you')
def thank_you():
    
    close_ended_str = csv_to_string("responses/close_end_questions_responses.csv")
    open_ended_str = csv_to_string("responses/open_end_questions_responses.csv")
    default=" this is my assesment of close ended questions and open ended questions , give feed back on me "
    judge_gemini = gemini_chat(default+" "+close_ended_str+" "+open_ended_str)
    #default_txt = "tell me how i am i what kind of man ? , and write in I am ___ for not in you are a __  , you can get to know by a assesment test : " 
    #tell_me_about_me = gemini_chat(default_txt+""+close_ended_str+" "+open_ended_str)
    return render_template('thank_you.html', judge_gemini=judge_gemini)



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
        print(f"Error during chat: {e}")
        # Optionally log the error to a file
        with open('error.log', 'a') as log_file:
            log_file.write(f"{str(e)}\n")
        return "An error occurred. Please try again."
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

if __name__ == "__main__":
    app.run(debug=True)
