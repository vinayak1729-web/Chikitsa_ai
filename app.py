from flask import Flask, render_template, request, jsonify, redirect, url_for,session
import json
import os
from gemini_ai import gemini_chat
import google.generativeai as genai
app = Flask(__name__)
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from models import User 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'secret_key'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __init__(self,email,password,name):
        self.name = name
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))

with app.app_context():
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # handle request
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        new_user = User(name=name,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/login')



    return render_template('register.html')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['email'] = user.email
            return redirect('/dashboard')
        else:
            return render_template('login.html',error='Invalid user')

    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if session['email']:
        user = User.query.filter_by(email=session['email']).first()
        return render_template('dashboard.html',user=user)
    
    return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('email',None)
    return redirect('/login')


@app.route('/questions')
def questions():
    if 'email' not in session:  # Check if user is logged in
        return redirect('/login')

    # Fetch open-ended and closed-ended questions from a database or list (replace with your actual logic)
    open_ended_questions = ["What is the most interesting thing you heard this week?"]
    closed_ended_questions = ["Have you been feeling depressed or sad lately?"]

    return render_template('questions.html', open_ended_questions=open_ended_questions, closed_ended_questions=closed_ended_questions)
# Create the model
generation_config = {
    "temperature": 2,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Apply safety settings
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "NEGLIGIBLE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "NEGLIGIBLE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "NEGLIGIBLE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "NEGLIGIBLE"
    }
]

default_prompt = " You are a professional mental doctor and health guide. You act as a best friend to those who talk to you. You can speak in Hindi, Marathi, Hinglish, or any language the user is comfortable with.You have to act as a sexologist, gynologist, neurologist, and health guide."
def load_prompt(file_path):
    with open(file_path, 'r') as file:
        return file.read().strip()

# Read prompt from the text file
@app.route('/')
def index():
    return render_template('about.html')

@app.route('/submit_about', methods=['POST'])
def submit_about():
    user_about = request.form['user_about']

    # Save the user's input to a text file
    with open('prompt.txt', 'w') as f:
        f.write(user_about)

    return redirect(url_for('chat'))

prompt = load_prompt("prompt.txt")
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=default_prompt + prompt
)
chat_session = model.start_chat()

def gemini_chat(user_input, history_file="dataset/intents.json"):
    try:
        # Load the intents JSON or create an empty structure if not found
        if os.path.exists(history_file):
            with open(history_file, 'r') as f:
                intents_data = json.load(f)
        else:
            intents_data = {"intents": []}

        # Send the user input to the model
        response = chat_session.send_message(user_input)

        # Create a new intent object for the conversation
        new_intent = {
            # "tag": [predicted_tag],  # Assuming greeting here, adjust based on logic
            "patterns": [user_input],
            "responses": [response.text.strip()],
        }

        # Append the new intent to the intents list at position 2 (index 1)
        intents_data['intents'].insert(1, new_intent)

        # Save the updated intents JSON file
        with open(history_file, 'w') as f:
            json.dump(intents_data, f, indent=4)

        return response.text

    except Exception as e:
        print(f"Error during chat: {e}")
        return "An error occurred. Please try again."

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        return render_template('main.html')
    elif request.method == 'POST':
        user_input = request.form['user_input']
        response = gemini_chat(user_input)  # Call your gemini_chat function here
        return jsonify({'response': response})
    else:
        return "Unsupported request method", 405  # Handle other methods if needed

if __name__ == "__main__":
    app.run(debug=True)