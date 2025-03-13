import asyncio

from random import randint

from PIL import Image

import requests

from dotenv import get_key

import os

from time import sleep

#Function to open and display images based on a given prompt

def open_images(prompt):

    folder_path = r"Data" # Folder where the images are stored

    prompt = prompt.replace("", "") # Replace spaces in prompt with underscores

#Generate the filenames for the images

    Files = [f"{prompt}{i}.jpg" for i in range(1, 5)]

    for jpg_file in Files:

        image_path = os.path.join(folder_path, jpg_file)

        try:

#Try to open and display the image

            img = Image.open(image_path)

            print(f"Opening image: {image_path}")

            img.show()

            sleep(1) #Pause for 1 second before showing the next image

        except IOError:

            print(f"Unable to open {image_path}")

#API details for the Hugging Face Stable Diffusion model

API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0" 
headers = {"Authorization": f"Bearer {get_key('.env', 'HuggingFaceAPIKey')}"}

async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

async def generate_images(prompt: str):

    tasks = []

#Create 4 image generation tasks

    for _ in range(4):

        payload = {
            "inputs": f"(prompt), quality=4K, sharpness-maximum, Ultra High details, high resolution, seed {randint(0, 1000000)}",
        }
        task = asyncio.create_task(query(payload))

        tasks.append(task)

# Wait for all tasks to complete

    image_bytes_list = await asyncio.gather(*tasks)

    for i, image_bytes in enumerate(image_bytes_list):

#Save the generated images to files 
        with open(fr"Data\{prompt.replace('','')}{1+1}.jpg", "wb") as f: 

            f.write(image_bytes)

#Wrapper Function to generate and open images

def GenerateImages(prompt : str):

    asyncio.run(generate_images(prompt)) # Run the async image generation

    open_images(prompt) # Open the generated images

#Main loop to monitor for image generation requests

while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:

            Data: str = f.read()

        Prompt, Status = Data.split(",")

# If the status indicates an image generation request

        if Status == "True":

            print("Generating Images...")

            ImageStatus = GenerateImages(prompt=Prompt)

#Reset the status in the file after generating images 
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:

                f.write("False, False")

                break 

        else:

            sleep(1) # Wait for 1 second before checking again

    except:
        pass