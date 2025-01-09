import asyncio  # Import asyncio for asynchronous programming
from random import randint  # Import randint to generate random integers
from PIL import Image  # Import Image from PIL (Pillow) for image processing
import requests  # Import requests for making HTTP requests
from time import sleep  # Import sleep to pause execution for a specified duration
from dotenv import load_dotenv  # Import load_dotenv to load environment variables from a .env file
import os  # Import os module to interact with the operating system

# Load environment variables from the .env file
load_dotenv()

# Retrieve environment variable for Hugging Face API key
huggingface_api = os.getenv('HuggingFaceAPIKey')
# Set up headers for API requests, including authorization token
headers = {'Authorization': f"Bearer {huggingface_api}"}
# Define the URL for the Stable Diffusion API endpoint
url = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"


def open_images(prompt):
    """Open generated images based on a prompt."""
    folder_path = "../Data"  # Define the folder path where images are stored
    prompt = prompt.replace(" ", "_")  # Replace spaces in prompt with underscores

    # Create a list of expected image filenames based on the prompt
    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    # Loop through each expected image file
    for jpg in files:
        image_path = os.path.join(folder_path, jpg)  # Construct full image path using os.path.join

        try:
            img = Image.open(image_path)  # Try to open the image file
            print(f"Opening image: {image_path}")  # Print which image is being opened
            img.show()  # Display the image
            sleep(1)  # Pause for a second before opening the next image
        except IOError:
            print(f"Unable to open {image_path}")  # Handle error if image cannot be opened


async def query(payload):
    """Send an asynchronous POST request to generate an image."""
    response = await asyncio.to_thread(requests.post, url, headers=headers, json=payload)
    return response.content  # Return the content of the response


async def generate_image(prompt: str):
    """Generate images based on a given prompt using asynchronous tasks."""
    tasks = []  # List to hold asynchronous tasks

    for i in range(4):  # Generate four images
        play_load = {
            'inputs': f"{prompt}, quality=4k, sharpness=maximum, Ultra High Details, high resolution, seed={randint(1, 999999)}"
        }
        task = asyncio.create_task(query(play_load))  # Create a task for querying the API
        tasks.append(task)  # Add task to the list

    image_bytes_list = await asyncio.gather(*tasks)  # Wait for all tasks to complete

    # Save each generated image to a file
    for i, image_bytes in enumerate(image_bytes_list):
        output_file_path = os.path.join("../Data", f"{prompt.replace(' ', '_')}{i + 1}.jpg")
        with open(output_file_path, 'wb') as file:
            file.write(image_bytes)  # Write bytes to file


# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    """Generate images and open them."""
    asyncio.run(generate_image(prompt))  # Run asynchronous image generation
    open_images(prompt)  # Open generated images


# Main loop to continuously check for new prompts and generate images
while True:
    try:
        data_file_path = '../Frontend/Files/ImageGeneration.data'  # Define path to data file

        with open(data_file_path, 'r') as f:
            data: str = f.read()  # Read data from file

        prompt, status = data.split(",")  # Split data into prompt and status

        if status.strip() == "True":  # Check if status is "True"
            print("Generating Images...")
            GenerateImages(prompt)  # Generate and open images

            with open(data_file_path, 'w') as f:
                f.write("False, False")  # Reset status after generating images

            break  # Exit loop after processing

        elif status.strip() == "False":
            print("Status is False; exiting loop.")
            break  # Exit loop if status is "False"

        else:
            sleep(1)  # Sleep for a second before checking again

    except Exception as e:
        print("The error is: ", e)  # Print any errors encountered during execution
