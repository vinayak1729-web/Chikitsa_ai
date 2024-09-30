import json
import random
import re

# Load the intents file
with open('dataset/intents.json') as file:
    intents = json.load(file)

# Function to find the matching intent
def find_intent(user_input):
    for intent in intents['intents']:
        for pattern in intent['patterns']:
            # Using regular expressions to match user input with patterns
            if re.search(re.escape(pattern), user_input, re.IGNORECASE):
                return random.choice(intent['responses'])
    return "I'm sorry, I don't know how to respond to that."

# Main function for the chatbot
def chatbot_response(user_input):
    response = find_intent(user_input)
    return response

# Running the chatbot
# print("Chatbot is ready! Type 'quit' to exit.")
# while True:
#     user_input = input("You: ")
#     if user_input.lower() == "quit":
#         break
#     response = chatbot_response(user_input)
#     print(f"Chatbot: {response}")
