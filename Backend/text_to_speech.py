import pygame  # Import the pygame library for audio playback
import random  # Import random for generating random responses
import asyncio  # Import asyncio for asynchronous programming
import edge_tts  # Import edge_tts for text-to-speech functionality
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
import os  # Import os module to interact with the operating system

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables for assistant voice
assistant_voice = os.getenv('AssistantVoice')


async def text_to_audio_file(text: str) -> None:
    """Converts text to an audio file using text-to-speech."""
    file_path = "../Data/speech.mp3"  # Path to the audio file
    if os.path.exists(file_path):  # Check if the file already exists
        os.remove(file_path)  # Remove the existing file

    # Create a Communicate object for TTS with specified parameters
    communicate = edge_tts.Communicate(text, assistant_voice, pitch='+5Hz', rate='+13%')
    await communicate.save(file_path)  # Save the audio file


def tts(text: str, func=lambda r=None: True) -> bool:
    """Converts text to speech functionality."""
    while True:
        try:
            asyncio.run(text_to_audio_file(text))  # Run the TTS conversion asynchronously

            pygame.mixer.init()  # Initialize the mixer module for audio playback

            pygame.mixer.music.load('../Data/speech.mp3')  # Load the audio file
            pygame.mixer.music.play()  # Play the audio

            while pygame.mixer.music.get_busy():  # Wait until the music is finished playing
                if not func():  # Check if any stopping condition is met
                    break
                pygame.time.Clock().tick(10)  # Control playback timing

            return True  # Indicate success

        except Exception as e:
            print(f"Error in tts: {e}")  # Print any errors encountered during TTS

        finally:
            try:
                func(False)  # Call the function with False to indicate completion
                pygame.mixer.music.stop()  # Stop playback
                pygame.mixer.quit()  # Quit the mixer module
            except Exception as e2:
                print("Error in finally block:", e2)  # Print errors in the finally block


def text_to_speech(text: str, func=lambda r=None: True) -> None:
    """Function to manage text-to-speech with additional responses for long text."""
    data_segments = str(text).split(".")  # Split text into segments based on periods
    responses = [
        "The rest of the result has been printed to the chat screen, kindly check it out sir.",
        "The rest of the text is now on the chat screen, sir, please check it.",
        "You can see the rest of the text on the chat screen, sir.",
        "The remaining part of the text is now on the chat screen, sir.",
        "Sir, you'll find more text on the chat screen for you to see.",
        "The rest of the answer is now on the chat screen, sir.",
        "Sir, please look at the chat screen, the rest of the answer is there.",
        "You'll find the complete answer on the chat screen, sir.",
        "The next part of the text is on the chat screen, sir.",
        "Sir, please check the chat screen for more information.",
        "There's more text on the chat screen for you, sir.",
        "Sir, take a look at the chat screen for additional text.",
        "You'll find more to read on the chat screen, sir.",
        "Sir, check the chat screen for the rest of the text.",
        "The chat screen has the rest of the text, sir.",
        "There's more to see on the chat screen, sir, please look.",
        "Sir, the chat screen holds the continuation of the text.",
        "You'll find the complete answer on the chat screen, kindly check it out sir.",
        "Please review the chat screen for the rest of the text, sir.",
        "Sir, look at the chat screen for the complete answer.",
        "The remainder of the content has been displayed in the chat, kindly take a look, sir.",
        "The subsequent information is available on the chat screen, sir; please review it.",
        "You can find the additional text now shown on the chat, sir.",
        "The rest of your query has been answered in the chat, sir; please have a look.",
        "Sir, the chat screen shows more information for your consideration.",
        "The extended response is now visible on the chat screen, sir; please check it.",
        "Sir, you'll discover further details in the chat window.",
        "The chat has the additional response you were seeking, sir.",
        "You can view the next segment of text on the chat screen, sir.",
        "Please check the chat screen, sir; more information is now available.",
        "There's additional information displayed on the chat screen for you, sir.",
        "Sir, kindly consult the chat screen for more details.",
        "You will find the remainder of the information in the chat, sir.",
        "The continuation of your answer has been posted on the chat screen, sir.",
        "For more insights, please evaluate the information on the chat screen, sir.",
        "Sir, the additional text is available for your review on the chat screen.",
        "The chat screen contains further details for your perusal, sir.",
        "You'll find the extended answer on the chat screen, sir; kindly check it.",
        "Please take a moment to look at the chat screen for the rest of the text, sir.",
        "The following information is present in the chat for you, sir."
    ]

    if len(data_segments) > 4 and len(text) >= 250:  # Check if text is long enough for additional responses
        tts(' '.join(text.split('.')[0:2]) + ". " + random.choice(responses), func)  # Read part of the text with a response

    else:
        tts(text, func)  # Read the entire text


if __name__ == "__main__":
    while True:
        user_input = input('Enter the text: ')  # Prompt user for input text
        text_to_speech(user_input)  # Convert input text to speech
        # tts(user_input) call tts you want voice of large text comment above line and uncomment this line

