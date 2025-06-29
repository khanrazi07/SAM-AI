import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import pyttsx3
import requests
import json
import wikipedia
from model import  generate
chat_history = ""

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Female voice & slower rate
voices = engine.getProperty('voices')
for voice in voices:
    if "female" in voice.name.lower() or "zira" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break
engine.setProperty('rate', 150)


def say(text):
    print("SAM:", text)
    engine.say(text)
    engine.runAndWait()


def wish_me():
    hour = datetime.datetime.now().hour
    if 5 <= hour < 12:
        say("Good morning, sir!")
    elif 12 <= hour < 17:
        say("Good afternoon, sir!")
    elif 17 <= hour < 21:
        say("Good evening, sir!")
    else:
        say("Good night, sir! Hope you had a great day.")


def chat(query):
    global chat_history
    openai.api_key = apikey
    chat_history += f"User: {query}\nSAM: "
    try:
        response = openai.Completion.create(
            model="gpt-4.1-2025-04-14",
            prompt=chat_history,
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        answer = response["choices"][0]["text"].strip()
        say(answer)
        chat_history += f"{answer}\n"
        return answer
    except Exception as e:
        say("Sorry, I couldn't process that.")
        print("OpenAI Error:", e)


def ai(prompt):
    openai.api_key = apikey
    try:
        response = openai.Completion.create(
            model="gpt-4.1-2025-04-14",
            temperature=0.7,
            max_tokens=256,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        text = f"OpenAI response for Prompt: {prompt}\n\n{response['choices'][0]['text']}"
        if not os.path.exists("Openai"):
            os.mkdir("Openai")
        filename = f"Openai/{random.randint(1000, 9999)}.txt"
        with open(filename, "w") as f:
            f.write(text)
        say("AI response has been saved.")
    except Exception as e:
        say("There was an error processing the AI prompt.")
        print("AI Error:", e)


def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        say("Listening...")
        try:
            audio = r.listen(source, timeout=5)
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query.lower()
        except Exception as e:
            print("Speech Recognition Error:", e)
            return "Some error occurred"


def get_weather(city="Delhi"):
    # Use a free weather API - OpenWeatherMap example (You need to create free API key)
    api_key = "YOUR_OPENWEATHERMAP_API_KEY"  # Replace with your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(base_url)
        weather_data = response.json()
        if weather_data["cod"] != 200:
            return None
        temp = weather_data["main"]["temp"]
        desc = weather_data["weather"][0]["description"]
        return f"The current temperature in {city} is {temp} degree Celsius with {desc}."
    except Exception as e:
        print("Weather API Error:", e)
        return None


def simple_calculator(expr):
    try:
        # WARNING: Using eval can be risky if input isn't controlled
        result = eval(expr)
        return f"The result of {expr} is {result}."
    except Exception:
        return "Sorry, I couldn't calculate that."


if __name__ == '__main__':
    wish_me()
    say("I am SAM, your intelligent assistant. How can I help you today?")

    while True:
        query = takeCommand()

        if "open youtube" in query:
            say("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        elif "open google" in query:
            say("Opening Google.")
            webbrowser.open("https://www.google.com")

        elif "open wikipedia" in query:
            say("Opening Wikipedia.")
            webbrowser.open("https://www.wikipedia.com")

        elif "play music" in query:
            music_path = "C:\\Users\\YourUsername\\Music\\song.mp3"
            try:
                os.startfile(music_path)
                say("Playing music.")
            except Exception as e:
                say("Sorry, I could not find the music file.")
                print("Music Error:", e)

        elif "the time" in query:
            time = datetime.datetime.now().strftime("%I:%M %p")
            say(f"The time is {time}")

        elif "weather" in query:
            city = "Delhi"  # Default city
            if "in" in query:
                city = query.split("in")[-1].strip()
            weather_report = get_weather(city)
            if weather_report:
                say(weather_report)
            else:
                say("Sorry, I couldn't fetch the weather details right now.")

        elif "introduce yourself" in query:
            intro = (
                "Hello everyone, my name is SAM – your Smart AI Machine. "
                "I am an intelligent voice assistant developed using Python and OpenAI's powerful language model. "
                "I can help you with a variety of tasks like answering your questions, opening websites, "
                "telling you the time, playing music, checking the weather, and even doing basic calculations. "
                "I’m here to make your life easier and more fun."
            )
            say(intro)

        elif "how are you" in query:
            say("I'm doing great, thank you for asking! How can I assist you today?")

        elif "tell me a joke" in query:
            jokes = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "Why did the computer show up at work late? It had a hard drive!",
                "Why do programmers prefer dark mode? Because light attracts bugs!",
            ]
            say(random.choice(jokes))

        elif "what's your favorite color" in query or "what is your favorite color" in query:
            say("I like the color blue. It’s calming and reminds me of the sky.")

        elif "calculate" in query:
            expr = query.replace("calculate", "").strip()
            if expr:
                result = simple_calculator(expr)
                say(result)
            else:
                say("Please tell me the expression to calculate.")

        elif "using artificial intelligence" in query:
            say(generate(prompt=query))

        elif "reset chat" in query:
            chat_history = ""
            say("Chat history reset.")

        elif "shutdown" in query:
            say("Shutting down the system. Goodbye!")
            os.system("shutdown /s /t 1")
            break

        elif "logout" in query:
            say("Logging out. See you soon!")
            os.system("shutdown -l")
            break

        elif "sam quit" in query or "exit" in query:
            say("Goodbye, sir. Have a wonderful day!")
            break

        else:
           say(generate(query))
