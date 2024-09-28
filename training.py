import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout

# Load the dataset
with open('dataset/intents.json', 'r') as f:
    data = json.load(f)

# Extract patterns and responses
patterns = []
responses = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        patterns.append(pattern)
    for response in intent['responses']:
        responses.append(response)

# Tokenize the patterns (input)
tokenizer = Tokenizer(oov_token="<OOV>")
tokenizer.fit_on_texts(patterns)
word_index = tokenizer.word_index
sequences = tokenizer.texts_to_sequences(patterns)
padded_sequences = pad_sequences(sequences, padding='post')

# Encode the responses (output)
label_encoder = LabelEncoder()
encoded_responses = label_encoder.fit_transform(responses)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(padded_sequences, encoded_responses, test_size=0.2, random_state=42)

# Get input shape for model
input_shape = X_train.shape[1]
vocab_size = len(word_index) + 1  # Add 1 for padding token
output_size = len(set(encoded_responses))

# Define the LSTM model
model = Sequential([
    Embedding(vocab_size, 128, input_length=input_shape),  # Embedding layer
    LSTM(128, return_sequences=False),                     # LSTM layer
    Dropout(0.5),                                          # Dropout to prevent overfitting
    Dense(64, activation='relu'),                          # Dense layer with ReLU activation
    Dropout(0.5),
    Dense(output_size, activation='softmax')               # Output layer with softmax activation
])

# Compile the model
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# View the model summary
model.summary()

# Train the model
history = model.fit(X_train, y_train, epochs=30, validation_data=(X_test, y_test), batch_size=32)

# Save the model after training
model.save('model/chikitsa_model.h5')
