from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
from nltk.tokenize import word_tokenize
from tensorflow.keras.preprocessing.text import tokenizer_from_json
import json
from tensorflow.keras.models import load_model

# Load the trained model
model = load_model('model/chikitsa_model.h5')

# Load tokenizer from file
with open('dataset/tokenizer.json', 'r') as f:
    tokenizer_data = f.read()  # Read as a string
    tokenizer = tokenizer_from_json(tokenizer_data)  # Pass the JSON string

def predict_intent(text):
    try:
        # Preprocess the input text
        tokenized_text = word_tokenize(text.lower())  # Tokenize the text
        sequence = tokenizer.texts_to_sequences([tokenized_text])  # Convert tokens to sequence
        
        # Ensure the sequence is padded to the required input shape
        padded_sequence = pad_sequences(sequence, maxlen=model.input_shape[1], padding='post')  # Adjust maxlen as per model input

        # Make prediction
        prediction = model.predict(padded_sequence)
        response_index = np.argmax(prediction)
        
        # Assuming you have a label encoder to map back to the intent
        response = label_encoder.inverse_transform([response_index])[0]
        
        return response
    except Exception as e:
        print(f"Prediction error: {e}")
        return None

# Test the model
user_input = "hi"
predicted_response = predict_intent(user_input)
print("Bot:", predicted_response)

# import json
# from tensorflow.keras.preprocessing.text import Tokenizer
# from tensorflow.keras.preprocessing.sequence import pad_sequences
# from tensorflow.keras.models import load_model

# # Load your intents file
# with open('dataset/intents.json', 'r') as f:
#     intents = json.load(f)

# # Extract texts (patterns) and labels (responses)
# texts = [intent['patterns'][0] for intent in intents['intents']]
# labels = [intent['responses'][0] for intent in intents['intents']]

# # Tokenize the texts
# tokenizer = Tokenizer(oov_token="<OOV>")
# tokenizer.fit_on_texts(texts)
# sequences = tokenizer.texts_to_sequences(texts)

# # Save tokenizer for future use
# with open('dataset/tokenizer.json', 'w') as f:
#     f.write(tokenizer.to_json())

# # Pad sequences
# max_len = max([len(seq) for seq in sequences])
# padded_sequences = pad_sequences(sequences, maxlen=max_len, padding='post')

# # Load the trained model and make predictions
# model = load_model('model/chikitsa_model.h5')
