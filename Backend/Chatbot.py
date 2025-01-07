from groq import Groq  # Import the Groq library for accessing its API
from json import load, dump  # Import load and dump functions for handling JSON files
import datetime  # Import datetime module to work with dates and times
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
import os  # Import os module to interact with the operating system

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables for username, assistant name, and API key
username = os.getenv('Username')
assistant_name = os.getenv('Assistantname')
groq_api_key = os.getenv('GroqAPIKey')

# Initialize the Groq client with the API key
client = Groq(api_key=groq_api_key)

# Initialize an empty list to store chat messages
messages = []

# Define the system message that sets the context for the chatbot
system_message = f"""Hello, I am {username}. You are a very accurate and advanced AI chatbot named {assistant_name}, which also has real-time up-to-date information from the internet.
*** Do not tell time until I ask, do not talk too much, just answer the question.***
*** Reply in only English, even if the question is in Hindi, reply in English.***
*** Do not provide notes in the output, just answer the question and never mention your training data. ***
"""

# Create a list containing the system message formatted for the chatbot
system_chatbot = [
    {'role': 'system', 'content': system_message}
]

# Attempt to load existing chat logs from a JSON file; create a new file if it doesn't exist
try:
    with open('../Data/ChatLog.json', 'r') as f:
        messages = load(f)  # Load existing messages from the file
except FileNotFoundError:
    with open('../Data/ChatLog.json', 'w') as f:
        dump([], f)  # Create an empty JSON file if it doesn't exist


def get_realtime_information():
    """Retrieve current date and time information."""
    current_datetime = datetime.datetime.now()  # Get the current date and time
    second = current_datetime.strftime('%S')  # Extract seconds
    minute = current_datetime.strftime('%M')  # Extract minutes
    hour = current_datetime.strftime('%H')  # Extract hours (corrected from '%M' to '%H')
    day = current_datetime.strftime('%A')  # Extract day of the week
    date = current_datetime.strftime('%d')  # Extract day of the month
    month = current_datetime.strftime('%B')  # Extract month name
    year = current_datetime.strftime('%Y')  # Extract year

    # Format the real-time information into a string
    data = (f"Please use this real-time information if needed,\nDay: {day}\nDate: {date}\nMonth: {month}\nYear: {year}"
            f"\nTime: {hour} Hours: {minute} minutes: {second} seconds.\n")

    return data


def answer_modifier(answer):
    """Remove empty lines from the chatbot's answer."""
    lines = answer.split('\n')  # Split answer into lines
    non_empty_lines = [line for line in lines if line.strip()]  # Filter out empty lines
    return "\n".join(non_empty_lines)  # Join non-empty lines back into a single string


def chatbot(query):
    """This function sends the user's query to the chatbot and returns the AI's response."""
    try:
        # Load existing messages from chat log file
        with open('../Data/ChatLog.json', 'r') as f:
            messages = load(f)

        # Append user query to messages list
        messages.append({"role": "user", "content": f"{query}"})

        # Send request to Groq API for a chat completion based on user input and previous messages
        completion = client.chat.completions.create(
            model='llama3-70b-8192',
            messages=system_chatbot + [{'role': 'user', 'content': get_realtime_information()}] + messages,
            max_tokens=1024,
            temperature=0.7,
            top_p=1,
            stream=True,
            stop=None
        )

        answer = ""  # Initialize an empty string to accumulate responses

        # Process each chunk of response from the API stream
        for chunk in completion:
            if chunk.choices[0].delta.content:  # Check if there is content in the chunk
                answer += chunk.choices[0].delta.content  # Append content to answer

        answer = answer.replace("</s>", '')  # Remove any unwanted end-of-sequence markers

        # Append assistant's response to messages list for maintaining conversation history
        messages.append({'role': "assistant", 'content': answer})

        # Save updated messages back to chat log file
        with open('../Data/ChatLog.json', 'w') as f:
            dump(messages, f, indent=4)

        return answer_modifier(answer=answer)  # Return modified answer without empty lines

    except Exception as e:
        print("Error: ", e)  # Print any errors encountered during processing

        # Reset chat log file on error by creating an empty list in JSON format
        with open('../Data/ChatLog.json', 'w') as f:
            dump([], f, indent=4)

        return chatbot(query)  # Retry sending the query after resetting


# Main loop for continuous interaction with the user
if __name__ == "__main__":
    while True:
        question = input("Enter Your Questions: ")  # Prompt user for input questions
        if question.lower() == 'quit':  # Check if user wants to exit
            break  # Exit loop if user types 'quit'
        else:
            print(chatbot(question))  # Print chatbot's response to user's question
