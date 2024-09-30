from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('model/chikitsa_model.h5')

# Initialize the Flask app
app = Flask(__name__)

# Define a function to preprocess the user input
def preprocess_input(user_input):
    # Dummy preprocessing function - adjust based on your input data format
    # Tokenization, vectorization, etc., may be required here
    return np.array([user_input])

# Define a function to predict the chatbot's response using the model
def get_response(user_input):
    # Preprocess the input
    processed_input = preprocess_input(user_input)
    
    # Predict using the model
    prediction = model.predict(processed_input)
    
    # Postprocess the prediction - adjust based on your output data format
    # For example, if you have probabilities, select the max one, or decode classes
    response = np.argmax(prediction, axis=1)  # Dummy logic, adjust as per your model's output
    return str(response)

# Route for the chatbot UI
@app.route('/')
def index():
    return render_template('demo.html')

# Route for handling user messages
@app.route('/get_response', methods=['POST'])
def get_bot_response():
    user_message = request.form['message']
    bot_response = get_response(user_message)
    return jsonify({"response": bot_response})

if __name__ == "__main__":
    app.run(debug=True)
