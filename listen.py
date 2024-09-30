import speech_recognition as sr
from googletrans import Translator

def listen(timeout=5, phrase_time_limit=10, mic_index=None, language='hi-IN'):
    """
    Listens to speech from the microphone and recognizes it in specified language.
    
    Args:
        timeout (int): Maximum time to wait for speech.
        phrase_time_limit (int): Maximum time for a phrase to be spoken.
        mic_index (int, optional): Index of the microphone to use.
        language (str): Language code for recognition ('hi-IN', 'mr-IN', or 'en-US').
        
    Returns:
        str: Recognized speech as text.
    """
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone(device_index=mic_index) as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            print("Processing...")

        # Recognize speech using Google Web Speech API with specified language
        text = recognizer.recognize_google(audio, language=language)
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


from deep_translator import GoogleTranslator

def translate_text(text, target_language='en'):
    try:
        translation = GoogleTranslator(source='auto', target=target_language).translate(text)
        return translation
    except Exception as e:
        print(f"Translation error: {e}")
        return text

def MicExecution():
    translated_query = listen(language="en-US")
    if translated_query:
        data = translate_text(translated_query)
        return data

if __name__ == "__main__":
    result = MicExecution()
    if result:
        print(f"Translated Text: {result}")
