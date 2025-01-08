from googlesearch import search  # Import the search function from the googlesearch library
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
Provide Answers In a Professional Way, make sure to add full stops, commas, question marks, and use proper grammar.***
*** Just answer the question from the provided data in a professional way. ***"""

# Attempt to load existing chat logs from a JSON file; create a new file if it doesn't exist
try:
    with open('../Data/ChatLog.json', 'r') as f:
        messages = load(f)  # Load existing messages from the file
except FileNotFoundError:
    with open('../Data/ChatLog.json', 'w') as f:
        dump([], f)  # Create an empty JSON file if it doesn't exist


def google_search(query):
    """Perform a Google search and return formatted results."""
    results = list(search(query, num_results=5, advanced=True))  # Perform a Google search for the query
    answer = f"The search results for '{query}' are:\n[start]"
    for result in results:
        answer += f"Title: {result.title}\nDescription: {result.description}\n\n"  # Format each result

    return answer + "[end]"  # Return formatted results


def answer_modifier(answer):
    """Remove empty lines from the chatbot's answer."""
    lines = answer.split('\n')  # Split answer into lines
    non_empty_lines = [line for line in lines if line.strip()]  # Filter out empty lines
    return "\n".join(non_empty_lines)  # Join non-empty lines back into a single string


# Initialize system chatbot messages with initial conversation context
system_chatbot = [
    {'role': 'system', 'content': system_message},
    {'role': 'user', 'content': "Hi"},
    {'role': 'assistant', 'content': "Hello, how can I help you?"}
]


def information():
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


def realtime_searchengine(prompt):
    """Process user prompt and perform Google search if needed."""
    global system_chatbot, messages

    with open('../Data/ChatLog.json', 'r') as f:
        messages = load(f)  # Load existing messages from chat log

    messages.append({"role": "user", "content": f"{prompt}"})  # Append user query to messages list

    system_chatbot.append({"role": "system", "content": google_search(prompt)})  # Append search results to context

    # Send request to Groq API for a chat completion based on user input and previous messages
    completion = client.chat.completions.create(
        model='llama3-70b-8192',
        messages=system_chatbot + [{'role': 'system', 'content': information()}] + messages,
        max_tokens=1024,
        temperature=0.7,
        top_p=1,
        stream=True,
        stop=None
    )

    answer = ""  # Initialize an empty string to accumulate responses

    for chunk in completion:
        if chunk.choices[0].delta.content:
            answer += chunk.choices[0].delta.content  # Append content from response chunks

    answer = answer.replace("</s>", '')  # Remove any unwanted end-of-sequence markers

    messages.append({'role': "assistant", 'content': answer})  # Append assistant's response to messages list

    with open('../Data/ChatLog.json', 'w') as f:
        dump(messages, f, indent=4)  # Save updated messages back to chat log file

    return answer_modifier(answer=answer)  # Return modified answer without empty lines


# Main loop for continuous interaction with the user
if __name__ == "__main__":
    while True:
        question = input("Enter Your Questions: ")  # Prompt user for input questions
        if question.lower() == 'quit':  # Check if user wants to exit
            break  # Exit loop if user types 'quit'
        else:
            print(realtime_searchengine(question))  # Print chatbot's response to user's question
