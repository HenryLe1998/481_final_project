import speech_recognition as sr
import pyttsx3
from datetime import date, datetime
import wikipediaapi
import requests

def search_wikipedia(query):
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        extract_format=wikipediaapi.ExtractFormat.WIKI,
        user_agent='MyCoolBot/1.0'
    )
    page = wiki_wiki.page(query)
    if page.exists():
        return page.summary
    else:
        return "No information found on Wikipedia."

def get_weather(api_key, city):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric"
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    if response.status_code == 200:
        temperature = weather_data["main"]["temp"]
        description = weather_data["weather"][0]["description"]
        print(f"Current weather in {city}:")
        print(f"Temperature: {temperature}°C")
        print(f"Description: {description}")
    else:
        print("Unable to get weather information.")

def respond_to_query(query):
    if "hello" in query:
        return "Hi! Let me know how I can help you today."
    elif "today" in query:
        today = date.today()
        return today.strftime("%B %d, %Y.")
    elif "time" in query:
        now = datetime.now()
        if now.strftime("%H") < "13":
            return now.strftime("%H am %M minutes and %S seconds.")
        else: return now.strftime("%H pm %M and %S seconds.")
    elif "bye" in query:
        return "Goodbye! Let me know when you need help."
    elif "in Wikipedia" in query:
        search_query = query.split("in Wikipedia")[0].strip()
        result = search_wikipedia(search_query)
        return result if result != "No information found on Wikipedia." else "Sorry, I haven't been programmed to answer this question."
    elif query.startswith("weather in"):
        city = query.split("weather in")[1].strip()
        api_key = "Use your API"
        get_weather(api_key, city)
        return None
    else:
        return "Sorry, I haven't been programmed to answer this question."

def main():
    robot_ear = sr.Recognizer()
    robot_mouth = pyttsx3.init()

    while True:
        with sr.Microphone() as mic:
            print("AI: I'm listening...")
            audio = robot_ear.listen(mic)
        
        print("AI: ...")
        try:
            user_input = robot_ear.recognize_google(audio, language='en')
            print("You: " + user_input)
        except sr.UnknownValueError:
            user_input = ""
            print("You: (Unable to recognize speech)")

        if user_input == "":
            robot_brain = "I can't hear you, please try again!"
        else:
            robot_brain = respond_to_query(user_input)

        if robot_brain is not None:
            print("AI: " + robot_brain)
            robot_mouth.say(robot_brain)
            robot_mouth.runAndWait()

if __name__ == "__main__":
    main()
