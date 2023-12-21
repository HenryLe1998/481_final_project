import speech_recognition as sr
import pyttsx3
from datetime import date, datetime
import wikipediaapi
import requests
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense

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

def build_lstm_model(vocabulary_size, embedding_dim, input_length):
    model = Sequential()
    model.add(Embedding(input_dim=vocabulary_size, output_dim=embedding_dim, input_length=input_length))
    model.add(LSTM(units=100))
    model.add(Dense(units=1, activation='linear'))  # Assuming regression for weather temperature
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def respond_to_query(query, lstm_model):
    if "hello" in query:
        return "Hi! Let me know how I can help you today."
    elif "today" in query:
        today = date.today()
        return today.strftime("%B %d, %Y.")
    elif "time" in query:
        now = datetime.now()
        return now.strftime("%H hours %M minutes and %S seconds.")
    elif "bye" in query:
        return "Goodbye! Let me know when you need help."
    elif "in Wikipedia" in query:
        search_query = query.split("in Wikipedia")[0].strip()
        result = search_wikipedia(search_query)
        return result if result != "No information found on Wikipedia." else "Sorry, I haven't been programmed to answer this question."
    elif query.startswith("weather in"):
        city = query.split("weather in")[1].strip()
        api_key = "YOUR_API_KEY"
        get_weather(api_key, city)
        return None
    else:
        # Use LSTM for generating a response based on the query
        processed_query = preprocess_input_sequence(query)
        predicted_response = lstm_model.predict(processed_query)
        return f"My prediction: {predicted_response}"

def preprocess_input_sequence(sequence):
    # You may need to implement tokenization and padding based on your specific requirements
    # For simplicity, let's convert the sequence to lowercase and split into words
    tokens = sequence.lower().split()
    # Assuming a fixed input length, pad or truncate the sequence as needed
    processed_sequence = pad_or_truncate(tokens, max_sequence_length)
    # Convert words to indices using a vocabulary
    indices = [word_to_index[word] for word in processed_sequence]
    return np.array(indices)

def pad_or_truncate(sequence, length):
    if len(sequence) < length:
        return sequence + ['<PAD>'] * (length - len(sequence))
    else:
        return sequence[:length]

def main():
    # Set parameters for LSTM model
    vocabulary_size = 10000  # Choose an appropriate vocabulary size based on your data
    embedding_dim = 50
    max_sequence_length = 20  # Choose an appropriate sequence length based on your data
    lstm_model = build_lstm_model(vocabulary_size, embedding_dim, max_sequence_length)

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
            robot_brain = respond_to_query(user_input, lstm_model)

        if robot_brain is not None:
            print("AI: " + robot_brain)
            robot_mouth.say(robot_brain)
            robot_mouth.runAndWait()

if __name__ == "__main__":
    main()
