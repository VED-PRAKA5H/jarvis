from selenium import webdriver  # Import the webdriver module from Selenium
from selenium.webdriver.common.by import By  # Import By for locating elements
from selenium.webdriver.chrome.service import Service  # Import Service for ChromeDriver management
from selenium.webdriver.chrome.options import Options  # Import Options for configuring Chrome
from webdriver_manager.chrome import ChromeDriverManager  # Import ChromeDriverManager for automatic driver management
import mtranslate as mt  # Import mtranslate for translation functionality
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
import os  # Import os module to interact with the operating system

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables for input language
input_language = os.getenv('InputLanguage')

# HTML code for speech recognition interface
html_code = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Speech Recognition</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            background-color: #f0f0f0;
            margin: 0;
        }

        button {
            margin: 10px;
            padding: 10px 20px;
            font-size: 16px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }

        #start {
            background-color: #4CAF50;
            color: white;
        }

        #end {
            background-color: #f44336;
            color: white;
        }

        #output {
            margin-top: 20px;
            width: 80%;
            max-width: 600px;
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <button id="start" onclick="startRecognition()">Start Recognition</button>
    <button id="end" onclick="stopRecognition()">Stop Recognition</button>
    <div id="output"></div>
    <script>
        const output = document.getElementById('output');
        let recognition;

        function startRecognition() {
            recognition = new (window.webkitSpeechRecognition || window.SpeechRecognition)();
            recognition.lang = 'en-US';
            recognition.continuous = true;

            recognition.onresult = function(event) {
                const transcript = event.results[event.results.length - 1][0].transcript;
                output.textContent += transcript;
            };

            recognition.onend = function() {
                recognition.start();
            };
            recognition.start();
        }

        function stopRecognition() {
            recognition.stop();
            output.innerHTML = "";
        }
    </script>
</body>
</html>
'''

# Replace the empty language string in HTML with the input language from environment variables
html_code = str(html_code).replace("recognition.lang = '';", f"recognition.lang = '{input_language}';")

# Write the HTML code to a file
with open("../Data/Voice.html", "w") as file:
    file.write(html_code)

current_directory = os.getcwd()  # Get the current working directory
# Move one level up in the directory structure
parent_directory = os.path.dirname(current_directory)
link_to_html = f"{parent_directory}/Data/Voice.html"  # Path to the HTML file

# Set up Chrome options for Selenium WebDriver
chrome_options = Options()
user_agent_string = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"
chrome_options.add_argument(f"user-agent={user_agent_string}")  # Set user agent
chrome_options.add_argument("--use-fake-ui-for-media-stream")  # Use fake UI for media stream permissions
chrome_options.add_argument("--use-fake-device-for-media-stream")  # Use fake device for media stream
chrome_options.add_argument("--headless=new")  # Run Chrome in headless mode (comment this to make chrome pop up)

# Initialize the Chrome WebDriver using ChromeDriverManager
service_instance = Service(ChromeDriverManager().install())
driver_instance = webdriver.Chrome(service=service_instance, options=chrome_options)

temp_directory_path = rf"{parent_directory}/Frontend/Files"  # Path to temporary directory


def set_assistant_status(status):
    """Set the assistant's status in a data file."""
    with open(f"{temp_directory_path}/status.data", "w", encoding='utf-8') as file:
        file.write(status)


def query_modifier(query):
    """Modify the query to ensure it ends with appropriate punctuation."""
    new_query = query.lower().strip()  # Normalize and strip whitespace from the query
    question_words_list = ['how', 'what', 'who', 'where', 'why', 'which', 'can you', "what's", 'when',
                           'could you', 'would you', 'do you', 'is it', 'are you', 'has anyone',
                           'who is', 'what if', 'why don’t', 'how come', 'what time',
                           'how many', 'how much', 'how long', 'how often',
                           'what kind', 'what type', 'where can', 'whose',
                           'is there', 'what about', 'how does',
                           'where is', 'who are', 'what happened',
                           'can I', 'may I', 'should I',
                           'will you', 'can you tell me',
                           'what would', 'who could',
                           'what do', 'what should']

    if any(word + " " in new_query for word in question_words_list):
        new_query += "?"  # Add a question mark if it contains question words
    else:
        new_query += "."  # Otherwise, add a period

    return new_query.capitalize()  # Return modified query capitalized


def universal_translator(text):
    """Translate text to English using mtranslate."""
    english_translation = mt.translate(text, 'en', 'auto')  # Translate text to English
    return english_translation.capitalize()  # Capitalize the first letter of the translation


def speech_recognition():
    """Perform speech recognition using the HTML interface."""
    driver_instance.get("file:///" + link_to_html)  # Open the local HTML file in the browser
    driver_instance.find_element(by=By.ID, value='start').click()  # Start speech recognition

    while True:
        try:
            recognized_text = driver_instance.find_element(by=By.ID, value='output').text  # Get recognized text from output element

            if recognized_text:  # If there is recognized text
                driver_instance.find_element(by=By.ID, value='end').click()  # Stop recognition

                if input_language.lower() == 'en' or input_language.lower() == '':
                    return query_modifier(recognized_text)  # Modify and return the query if it's in English
                else:
                    set_assistant_status("Translating...")  # Set status to Translating
                    return query_modifier(universal_translator(recognized_text))  # Translate and modify the query

        except Exception as e:
            print(f"Error: {e}")  # Print any exceptions for debugging


if __name__ == "__main__":
    while True:
        text_output = speech_recognition()  # Perform speech recognition and get text
        print(text_output)  # Print recognized or translated text
