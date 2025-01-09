# Import necessary modules for application management and web interactions
from AppOpener import close, open as app_open  # Functions to open and close applications on the system
from webbrowser import open as web_open  # Function to open URLs in a web browser

# Importing functions from pywhatkit for performing web searches and playing YouTube videos
from pywhatkit import search, playonyt

# Import BeautifulSoup for parsing HTML and extracting data from web pages
from bs4 import BeautifulSoup

# Import rich for enhanced printing capabilities in the console (e.g., colored text)
from rich import print

# Import Groq for interacting with the Groq API for AI-driven content generation
from groq import Groq

# Standard library imports
import webbrowser  # Module to interface with the web browser
import subprocess  # Module to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import requests  # Library for making HTTP requests in a simpler way
import keyboard  # Module for detecting and simulating keyboard events
import asyncio  # Library to write concurrent code using the async/await syntax
import os  # Module providing a way of using operating system-dependent functionality like reading or writing to the file system
from dotenv import load_dotenv  # Function to load environment variables from a .env file into the environment


# Load environment variables from the .env file
load_dotenv()

# Retrieve the Groq API key from environment variables
groq_api_key = os.getenv("GroqAPIKey")

# List of CSS classes used for web scraping (specific to certain websites)
css_classes = [
    "zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW",
    "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "05uR6d LTKOO",
    "tw-Data-text tw-text-small tw-ta", "IZ6rdc",
    "vlzY6d", "webanswers-webanswers_table_webanswers-table",
    "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe",
    "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b",
    "A1b2C3", "D4e5F6"
]

# User-Agent string for web requests to mimic a browser
user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/89.0.142.86 Safari/537.36"
)

# Initialize the Groq client with the API key
groq_client = Groq(api_key=groq_api_key)

# Predefined professional responses for user interactions
professional_responses = [
    "Your satisfaction is my top priority; please feel free to reach out if there is anything else I can assist you with.",
    "I am at your service for any additional questions or support you may require. Please don't hesitate to ask."
]

# Message history for the chatbot interaction
message_history = []

# Initial system message for the chatbot context
system_chatbot_context = [
    {'role': 'system',
     'content': f"Hello, I am {os.environ['Username']}, You are a content writer. You have to write content letter, codes applications, notes"}
]


def google_search(topic):
    """Perform a Google search on the given topic."""
    search(topic)
    return True


def content(topic):
    """Generate content based on a topic and save it to a file."""

    def open_notepad(file_path):
        """Open a specified file in Notepad."""
        default_text_editor = 'notepad.exe'
        subprocess.Popen([default_text_editor, file_path])

    def content_writer_ai(prompt):
        """Generate content using AI based on the provided prompt."""
        message_history.append({'role': "user", 'content': f"{prompt}"})

        # Create a chat completion using the Groq API
        completion = groq_client.chat.completions.create(
            model='mixtral-8x7b-32768',
            messages=system_chatbot_context + message_history,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        # Collect the response from the AI in chunks
        response_content = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response_content += chunk.choices[0].delta.content  # Append content from response chunks

        # Clean up the response by removing unwanted markers
        response_content = response_content.replace("</s>", '')

        # Store assistant's response in message history
        message_history.append({'role': "assistant", 'content': response_content})

        return response_content

    # Clean up the topic string and generate content using AI
    cleaned_topic = topic.replace("content", "").strip()
    ai_generated_content = content_writer_ai(cleaned_topic)

    # Save the generated content to a text file
    file_name = f"../Data/{cleaned_topic.lower().replace(' ', '')}.txt"
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(ai_generated_content)

    # Open the generated file in Notepad
    open_notepad(file_name)

    return True


def youtube_search(topic):
    """Open YouTube search results for the specified topic."""
    url = f"https://youtube.com/results?search_query={topic}"
    webbrowser.open(url)
    return True


def play_youtube(query):
    """Play a video on YouTube based on a query."""
    playonyt(query)
    return True


def open_app(app_name, session=requests.session()):
    """Open an application or search for it online if not found locally."""

    try:
        app_open(app_name, match_closest=True, output=True, throw_error=True)
        return True

    except Exception:
        def extract_links(html_content):
            """Extract relevant links from HTML content using BeautifulSoup."""
            if html_content is None:
                return []
            soup = BeautifulSoup(html_content, "html.parser")
            links = soup.find_all('a', {'jsname': "UWckNb"})
            return [link.get('href') for link in links]

        def search_google(query):
            """Perform a Google search and return HTML results."""
            url = f"https://google.com/search?q={query}"
            headers = {"User-Agent": user_agent}
            response = session.get(url=url, headers=headers)

            if response.status_code == 200:
                return response.text

            print("Failed to retrieve search results")
            return None

        # Search Google if the application could not be opened directly
        html_content = search_google(app_name)
        if html_content:
            link = extract_links(html_content)[0]  # Get the first link from search results
            web_open(link)  # Open the link in a web browser

        return True


def close_app(app_name):
    """Close an application by name."""

    if "chrome" in app_name.lower():
        pass  # Skip closing Chrome for now

    else:
        try:
            close(app_name, match_closest=True, output=True, throw_error=True)
            return True

        except Exception:
            return False


def system(command):
    """Control system volume based on command input."""

    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume un-mute")

    def volume_up():
        keyboard.press_and_release("volume up")

    def volume_down():
        keyboard.press_and_release("volume down")

    # Execute commands based on input string
    if command == 'mute':
        mute()

    elif command == 'unmute':
        unmute()

    elif command == 'volume up':
        volume_up()

    elif command == 'volume down':
        volume_down()

    return True


async def translate_and_execute(commands: list[str]):
    """Translate commands into function calls and execute them asynchronously."""

    function_calls = []

    for command in commands:
        if command.startswith("open "):
            if not ("open it" in command or command == 'open file'):
                function_call = asyncio.to_thread(open_app, command.removeprefix("open ").strip())
                function_calls.append(function_call)

        elif command.startswith('close '):
            function_call = asyncio.to_thread(close_app, command.removeprefix('close ').strip())
            function_calls.append(function_call)

        elif command.startswith('play '):
            function_call = asyncio.to_thread(play_youtube, command.removeprefix('play ').strip())
            function_calls.append(function_call)

        elif command.startswith('content '):
            function_call = asyncio.to_thread(content, command.removeprefix('content ').strip())
            function_calls.append(function_call)

        elif command.startswith('google search '):
            function_call = asyncio.to_thread(google_search, command.removeprefix('google search').strip())
            function_calls.append(function_call)

        elif command.startswith('youtube search '):
            function_call = asyncio.to_thread(youtube_search, command.removeprefix('youtube search ').strip())
            function_calls.append(function_call)

        elif command.startswith('system '):
            function_call = asyncio.to_thread(system, command.removeprefix('system ').strip())
            function_calls.append(function_call)

        else:
            print(f"No function found for the command: {command}")

    # Gather and execute all functions concurrently
    results = await asyncio.gather(*function_calls)

    for result in results:
        yield result  # Yield each result back to caller


async def automation(commands: list[str]):
    """Execute a list of commands asynchronously."""

    async for result in translate_and_execute(commands):
        pass  # Process each result (if needed)

    return True

# Uncomment to run all commands at once using asyncio (for testing purposes)
# if __name__ == "__main__":
#     asyncio.run(automation(['open youtube', 'open udemy', 'play natu natu']))
