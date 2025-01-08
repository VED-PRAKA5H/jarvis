import pygame
import random
import asyncio
import edge_tts
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
import os  # Import os module to interact with the operating system

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variables for input language
assistant_voice = os.getenv('AssistantVoice')
