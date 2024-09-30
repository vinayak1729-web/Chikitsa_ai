import pyttsx3

def speak(text, accent="en-IN"):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            
                engine.setProperty('voice', voice.id[7])
                break

        engine.setProperty('rate', 150)  # Adjust the speaking rate
        engine.setProperty('pitch', 200)  # Adjust the pitch
        engine.setProperty('volume', 1.0)  # Adjust the volume

        engine.say(text)
        engine.runAndWait()

    except Exception as e:
        print(f"pyttsx3 failed: {e}")


speak(" GANPATI BAPPA MORYA ")
# from selenium import webdriver
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from time import sleep

# chrome_options = Options()
# chrome_options.add_argument('--log-level=3')
# chrome_options.headless = True

# # Corrected line: Pass options instead of chrome_options
# Path = "driver/chromedriver.exe"
# driver = webdriver.Chrome(Path, options=chrome_options)  # Use 'options' here
# driver.maximize_window()

# website = r"https://ttsmp3.com/text-to-speech/British%2English/"  # Corrected typo
# driver.get(website)

# butonselection = Select(driver.find_element(by=By.XPATH, value='/html/body/div[4]/div[2]/form/select'))
# butonselection.select_by_visible_text('Indian English / Aditi')

# def speak(text):
#     length_of_text = len(str(text))

#     if not length_of_text:
#         return  # Handle empty text case

#     print(f"mag: {text}.")

#     Data = str(text)
#     xpath_of_sec = '/html/body/div[4]/div[2]/form/textarea'
#     driver.find_element(By.XPATH, value=xpath_of_sec).send_keys(Data)
#     driver.find_element(By.XPATH, value='//*[@id="vorlesenbutton"]').click()

#     # Wait for processing to finish (adjust sleep time as needed)
#     sleep(5)

#     # Clear the input field for the next text
#     driver.find_element(By.XPATH, value='/html/body/div[4]/div[2]/form/textarea').clear()


# speak("This is a text with an Indian accent.")  # Example usage

# # Close the browser after use
# driver.quit()
