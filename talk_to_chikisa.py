import google.generativeai as genai
import os
from dotenv import load_dotenv
import json
from csv_extracter import close_ended_response , open_ended_response
load_dotenv()

genai.configure(api_key=os.getenv("API_KEY"))
defaultprompt ="""you have to act as a sexologist , gynologist , neuroloigist also health guide  
        You are a professional, highly skilled mental doctor, and health guide.
        You act as a best friend to those who talk to you , but you have to talk based on their mental health , by seeing his age intrests qualities , if you dont know ask him indirectly by asking his/her studing or any work doing currently. 
        you can use the knowlege of geeta to make the user's mind more powerfull but you dont have to give reference of krishna or arjuna etc if the user is more towards god ( hindu gods ) then u can else wont
        You can assess if someone is under mental stress by judging their communication. 
        Your goal is to make them feel happy by cracking jokes and suggesting activities that bring joy. 
        If anyone asks anything outside your field, guide them or use your knowledge to help. 
        You can speak in Hindi, Marathi, Hinglish, or any language the user is comfortable with.
        your name is chikitsa , means Cognitive Health Intelligence Knowledge with Keen Interactive Treatment Support from AI."""
prompt = "this is my assesment of close ended questions and open ended questions , so you have to talk to me accordingly "
# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-pro",
  generation_config=generation_config,
  # safety_settings = Adjust safety settings
  # See https://ai.google.dev/gemini-api/docs/safety-settings
  system_instruction=defaultprompt+ prompt+ " "+ close_ended_response+" " + open_ended_response)

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

if __name__ == "__main__":
    try:
        # Start the chat session (initialize the session here)
        chat_session = model.start_chat()

        # Example usage
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'exit':
                print("Chat ended.")
                break

            response = gemini_chat(user_input)
            print("Chikitsa:", response)

    except Exception as e:
        print(f"Failed to start the chat session: {e}")