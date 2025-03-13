from AppOpener import close, open as appopen
from webbrowser import open as webopen
from pywhatkit import search, playonyt
from dotenv import dotenv_values
from bs4 import BeautifulSoup
from rich import print
from groq import Groq
from os import listdir, name as os_name
import webbrowser
import subprocess
import requests
import random
import platform
import keyboard
import asyncio
import os 

env_vars = dotenv_values(".env")
GroqAPIKey = env_vars.get("GroqAPIKey")

classes = ["zCubwf", "hgKElc", "LTKOO sY7ric", "ZOLcW", "gsrt vk_bk FzvWSb YwPhnf", "pclqee", "tw-Data-text tw-text-small tw-ta", 
           "IZ6rdc", "05uR6d LTKOO", "vlzY6d", "webanswers-webanswers_table_webanswers-table", "dDoNo ikb4Bb gsrt", "sXLa0e", 
           "LWkfKe", "VQF4g", "qv3Wpe", "kno-rdesc", "SPZz6b"]

# Define a user-agent for making web requests.

useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'

#Initialize the Groq client with the API key.

client = Groq(api_key=GroqAPIKey)

# Predefined professional responses for user interactions.

professional_responses = [
    "Your satisfaction is my top priority; feel free to reach out if there's anything else I can help you with.", 
    "I'm at your service for any additional questions or support you may need-don't hesitate to ask.",
]
#List to store chatbot messages.

messages = []

# System message to provide context to the chatbot.

SystemChatBot = [{"role": "system", "content": f"Hello, I am {os.environ['Username']}, You're a content writer. You have to write content like letters, codes, applications, essays, notes, songs, poems etc."}]

def GoogleSearch(Topic):
    search(Topic) # Use pywhatkit's search function to perform a Google search.
    return True # Indicate success.

#Function to generate content using AI and save it to a file.
def Content(Topic):

#Nested function to open a file in Notepad.
    def OpenNotepad(File):
        default_text_editor = 'notepad.exe' # Default text editor.
        subprocess.Popen([default_text_editor, File]) # Open the file in Notepad.

#Nested function to generate content using the AI chatbot.
    def ContentWriterAI(prompt):
        messages.append({"role": "user", "content": f"{prompt}"})

# Add the user's prompt to messages.
        completion = client.chat.completions.create(
            model="mixtral-8x7b-32768", #Specify the AI model.
            messages=SystemChatBot + messages, #Include system instructions and chat history.
            max_tokens=2048, # Limit the maximum tokens in the response.
            temperature=0.7, # Adjust response randomness.
            top_p=1, #Use nucleus sampling for response diversity.
            stream=True, # Enable streaming response.
            stop=None # Allow the model to determine stopping conditions.
        )
        Answer = ""

        for chunk in completion:
            if chunk.choices[0].delta.content: # Check for content in the current chunk.
                Answer += chunk.choices[0].delta.content # Append the content to the answer.

        Answer = Answer.replace("</s>", "") # Remove unwanted tokens from the response.
        messages.append({"role": "assistant", "content": Answer}) # Add the AI's response to messages.
        return Answer

    Topic: str = Topic.replace("Content", "") # Remove "Content from the topic.
    ContentByAI = ContentWriterAI(Topic) # Generate content using AI.

#Save the generated content to a text file.

    with open(rf"Data\{Topic.lower().replace('','')}.txt", "w", encoding="utf-8") as file:
        file.write(ContentByAI) #Write the content to the file.
        file.close()

    OpenNotepad(rf"Data\{Topic.lower().replace(' ','')}.txt")
    return True

def YouTubeSearch(Topic):
    Url4Search = f"https://www.youtube.com/results?search_query={Topic}"#Construct the YouTube search URL.
    webbrowser.open(Url4Search) # Open the search URL in a web browser.
    return True # Indicate success.

#Function to play a video on YouTube.

def PlayYoutube(query):
    playonyt(query) # Use pywhatkit's playonyt function to play the video.
    return True # Indicate success.

def OpenApp(app, sess=requests.session()):
    try:
        appopen(app, match_closest=True, output=True, throw_error=True)
        return True # Indicate success.

    except:

        def extract_links(html):
            if html is None:
                return []

            soup = BeautifulSoup(html, 'html.parser') # Parse the HTML content.
            links = soup.find_all('a', {'jsname': 'UWckNb'}) # Find relevant links.
            return [link.get('href') for link in links] # Return the links.

        def search_google(query):
            url = f"https://www.google.com/search?q={query}"
            headers = {"User-Agent": useragent}
            response =  sess.get(url, headers=headers)

            if response.status_code == 200:
                return response.text
            else:
                print("Failed to retrive search results.")
            return None
        
        html = search_google(app)

        if html:
            link = extract_links(html)[0]
            webopen(link)

        return True

def CloseApp(app):

    if "chrome" in app:
        pass #Skip if the app is Chrome.
    else:
        try:
            close(app, match_closest=True, output=True, throw_error=True) # Attempt to close the app.
            return True # Indicate success.
        except:
            return False # Indicate failure.

#Function to execute system-level commands.

def System(command):

#Nested function to mute the system volume.

    def mute():
        keyboard.press_and_release("volume mute")

    def unmute():
        keyboard.press_and_release("volume mute") #Simulate the unmute key press.

#Nested function to increase the system volume.

    def volume_up():
        keyboard.press_and_release("volume up") #Simulate the volume up key press.

#Nested function to decrease the system volume.

    def volume_down():
        keyboard.press_and_release("volume down") # Simulate the volume down key press.

#Execute the appropriate command.

    if command == "mute":
        mute()
    elif command == "unmute":
        unmute()
    elif command == "volume up":
        volume_up()
    elif command == "volume down":
        volume_down()
    
    return True

async def TranslatorAndExecute(commands: list[str]):
    funcs = []
    for command in commands:
        if command.startswith("open "):
            if "open it" in command:
                pass
            if "open file" == command:
                pass
            else:
                fun = asyncio.to_thread(OpenApp, command.removeprefix("open "))
                funcs.append(fun)

        elif command.startswith("general"):
            pass
        elif command.startswith("realtime "):
            pass
        elif command.startswith("close "):
            fun = asyncio.to_thread(CloseApp, command.removeprefix("close "))
            funcs.append(fun)

        elif command.startswith("play "):
            fun = asyncio.to_thread(PlayYoutube, command.removeprefix("play "))
            funcs.append(fun)
        elif command.startswith("Content "):
            fun = asyncio.to_thread(Content, command.removeprefix("content "))
            funcs.append(fun)
        elif command.startswith("google search "):
            fun = asyncio.to_thread(GoogleSearch, command.removeprefix("google search "))
            funcs.append(fun)
        elif command.startswith("youtube search "):
            fun = asyncio.to_thread(YouTubeSearch, command.removeprefix("youtube search "))
            funcs.append(fun)
        elif command.startswith("system "):
            fun = asyncio.to_thread(System, command.removeprefix("system "))
            funcs.append(fun)
        
        else:
            print(f"No Function Found. For {command}")

    results = await asyncio.gather(*funcs)

    for result in results:
        if isinstance(results, str):
            yield result
        else:
            yield result

async def Automation(commands: list[str]):
    async for results in TranslatorAndExecute(commands):
        pass

    return True 

if __name__ =="__main__":
    asyncio.run(Automation([]))