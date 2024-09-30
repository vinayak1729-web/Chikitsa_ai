import speech_recognition as sr
from langdetect import detect
from gtts import gTTS
import io
from playsound import playsound

# Function to listen and detect speech
def listen(timeout=5, phrase_time_limit=10, mic_index=None):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Processing...")

        # Recognize speech using Google Web Speech API
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text

    except sr.UnknownValueError:
        print("Could not understand audio")
        return "Sorry, I didn't catch that. Could you please repeat?"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return "There was an issue with the speech service. Please try again."
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        return "An unexpected error occurred. Please try again."

# Function to detect the language of the spoken text
def detect_language(text):
    try:
        language = detect(text)
        print(f"Detected language: {language}")
        return language
    except Exception as e:
        print(f"Error in language detection: {e}")
        return "en"  # Default to English if detection fails

# Function to speak the response in the detected language
def speak_response(text, language_code):
    try:
        # Generate the response using gTTS
        tts = gTTS(text=text, lang=language_code)
        tts_io = io.BytesIO()
        tts.write_to_fp(tts_io)
        tts_io.seek(0)
        
        # Play the audio from memory
        playsound(tts_io)
        print(f"Response: {text} (in {language_code})")
    except Exception as e:
        print(f"Error in speaking the response: {e}")

# Main function
def main():
    # Step 1: Listen for user input
    user_input = listen()

    if user_input:
        # Step 2: Detect the language of the input
        detected_language = detect_language(user_input)

        # Step 3: Prepare the response in the same language
        if detected_language == 'hi':  # Hindi
            response_text = "आपने हिंदी में बात की है।"
        elif detected_language == 'mr':  # Marathi
            response_text = "तुम्ही मराठीत बोललात."
        elif detected_language == 'en':  # English
            response_text = "You spoke in English."
        else:
            response_text = "I detected your language."

        # Step 4: Speak the response in the detected language
        speak_response(response_text, detected_language)

if __name__ == "__main__":
    main()
