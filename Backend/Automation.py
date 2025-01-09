from AppOpener import close, open as appopeen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
import webbrowser
import subprocess
import requests
import keyboard
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Retrieve the Cohere API key from environment variables
GroqAPIkey = os.getenv("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "05uR6d LTKOO",
            "tw-Data-text tw-text-small tw-ta", "IZ6rdc",  "vlzY6d", "webanswers-webanswers_table_webanswers-table",
            "dDoNo ikb4Bb gsrt", "sXLa0e", "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b", "A1b2C3", "D4e5F6"]

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.142.86 Safari/537.36"

client = Groq(api_key=GroqAPIkey)

professional_responses = [
    "Your satisfaction is my top priority; please feel free to reach out if there is anything else I can assist you with.",
    "I am at your service for any additional questions or support you may require. Please don't hesitate to ask."
]

messages = []
system_chatbot = [{'role': 'system', 'content': f"Hello, I am {os.environ['Username']}, You are a content writer "}]