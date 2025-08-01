import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import subprocess
import pyautogui
import requests
import psutil
import ctypes
import random
import wikipedia
import json
import platform
import shutil
import time
import socket
import speedtest
import spotipy
import musilib 
from spotipy.oauth2 import SpotifyOAuth

# Initialize TTS
engine = pyttsx3.init()
engine.setProperty("rate", 175)

# NVIDIA API Key
NVIDIA_API_KEY = "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"
NVIDIA_API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
NVIDIA_MODEL = "meta/llama3-8b-instruct"

# Spotify Credentials
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="YOUR_SPOTIFY_CLIENT_ID",
    client_secret="YOUR_SPOTIFY_CLIENT_SECRET",
    redirect_uri="http://localhost:8888/callback",
    scope="user-read-playback-state,user-modify-playback-state"
))

def speak(text):
    print("GYNIUS:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio).lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError:
        speak("Network error.")
        return ""

def get_system_info():
    info = {
        "OS": platform.system(),
        "OS Version": platform.version(),
        "Processor": platform.processor(),
        "CPU Cores": psutil.cpu_count(logical=True),
        "RAM": str(round(psutil.virtual_memory().total / (1024.0 ** 3))) + " GB"
    }
    return info

def get_ip_address():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

def get_weather(city):
    api_key = "f4508c09c6259a2d0c9da8313b4d797b"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if data["cod"] != 200:
            return "Weather info not found."
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"Current temperature in {city} is {temp}°C with {desc}."
    except:
        return "Failed to fetch weather."

def perform_local_tasks(command):
    if "tell me the weather" in command:
        speak("For which city?")
        city = listen()
        weather_report = get_weather(city)
        speak(weather_report)

    elif "play music" in command or "spotify" in command:
        speak("What should I play on Spotify?")
        song = listen()
        results = sp.search(q=song, type='track', limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            sp.start_playback(uris=[track_uri])
            speak(f"Playing {song} on Spotify")
        else:
            speak("Could not find the song on Spotify.")

    elif "open notepad" in command:
        subprocess.Popen(["notepad.exe"])
        speak("Opening Notepad")

    elif "open command prompt" in command or "open cmd" in command:
        subprocess.Popen(["cmd.exe"])
        speak("Opening Command Prompt")

    elif "shutdown" in command:
        os.system("shutdown /s /t 1")
        speak("Shutting down the system")

    elif "restart" in command:
        os.system("shutdown /r /t 1")
        speak("Restarting the system")

    elif "sleep" in command:
        os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
        speak("System going to sleep")

    elif "screenshot" in command:
        screenshot = pyautogui.screenshot()
        filename = f"screenshot_{int(time.time())}.png"
        screenshot.save(filename)
        speak(f"Screenshot saved as {filename}")

    elif "open youtube" in command:
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube")

    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google")

    elif "what time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {now}")

    elif "what date" in command:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {today}")

    elif "open calculator" in command:
        subprocess.Popen(["calc.exe"])
        speak("Opening Calculator")

    elif "take note" in command:
        speak("What should I write?")
        note = listen()
        filename = f"note_{int(time.time())}.txt"
        with open(filename, "w") as f:
            f.write(note)
        speak(f"Note saved as {filename}")

    elif "battery status" in command:
        battery = psutil.sensors_battery()
        percent = battery.percent
        plugged = "Plugged In" if battery.power_plugged else "Not Plugged In"
        speak(f"Battery is at {percent} percent and it is {plugged}")

    elif "lock screen" in command:
        ctypes.windll.user32.LockWorkStation()
        speak("Locking the screen")

    elif "wikipedia" in command:
        speak("What do you want to search on Wikipedia?")
        topic = listen()
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak(summary)
        except:
            speak("I couldn't find anything on that topic.")

    elif "joke" in command:
        jokes = [
            "Why did the computer show up at work late? It had a hard drive!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "What do you call a computer floating in the ocean? A Dell Rolling in the Deep."
        ]
        speak(random.choice(jokes))

    elif "system info" in command:
        info = get_system_info()
        for key, value in info.items():
            speak(f"{key}: {value}")

    elif "disk usage" in command:
        total, used, free = shutil.disk_usage("/")
        speak(f"Disk Total: {total // (2*30)} GB, Used: {used // (230)} GB, Free: {free // (2*30)} GB")

    elif "internet speed" in command:
        speak("Checking internet speed")
        try:
            st = speedtest.Speedtest()
            download = st.download() / 1_000_000
            upload = st.upload() / 1_000_000
            speak(f"Download speed is {download:.2f} megabits per second. Upload speed is {upload:.2f} megabits per second.")
        except:
            speak("Speedtest failed to check the internet speed.")

    elif "ip address" in command:
        ip = get_ip_address()
        speak(f"Your IP address is {ip}")

    elif "open camera" in command:
        subprocess.run("start microsoft.windows.camera:", shell=True)
        speak("Opening Camera")


    elif   "play"  in command:
    
       # command.lower().startswith("play")
        song = command.lower().split("  ")[1] 
        link = musilib.music[song]
        webbrowser.open(link)


    elif "empty recycle bin" in command:
        try:
            os.system("PowerShell.exe -Command Clear-RecycleBin -Force")
            speak("Recycle bin emptied.")


   

                

        except:
            speak("Failed to empty recycle bin.")

    else:
        return False
    return True

def ask_gpt(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {NVIDIA_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "model": NVIDIA_MODEL,
            "temperature": 0.7,
            "top_p": 1,
            "max_tokens": 1024
        }
        response = requests.post(NVIDIA_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content'].strip()
        else:
            return f"NVIDIA API error: {response.status_code}"
    except Exception as e:
        return "Error: " + str(e)

# MAIN LOOP
speak("GYNIUS is now online. How can I help?")
while True:
    command = listen()
    if not command:
        continue

    if "stop" in command or "exit" in command or "goodbye" in command:
        speak("Goodbye!")
        break

    if not perform_local_tasks(command):
        reply = ask_gpt(command)
        speak(reply)