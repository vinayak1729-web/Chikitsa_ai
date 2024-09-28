from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import json
import os
import bcrypt
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'secret_key'

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
            return redirect('/about')
        else:
            return render_template('login.html', error='Invalid credentials.')

    return render_template('login.html')

# Dashboard Route
@app.route('/about')
def about():
    return render_template ('about.html')

@app.route('/submit_about', methods=['POST'])
def submit_about():
    user_about = request.form['user_about']

    # Save the user's input to a text file
    with open('prompt.txt', 'w') as f:
        f.write(user_about)

    return redirect(url_for('chat'))
from gemini_ai import gemini_chat
from gemini_ai import model 

@app.route('/logout')
def logout():
    session.pop('email', None)
    return redirect('/login')


from gemini_ai import load_prompt

prompt = load_prompt("prompt.txt")

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

if __name__ == "__main__":
    app.run(debug=True)
