# 481_final_project
Quoc Bao Le
Step 1: IDE install.
-pip install SpeechRecognition.
-pip install SpeechRecognition pyttsx3 wikipedia-api requests.
-pip install pyaudio.

Step 2: replace the placeholder "YOUR_API_KEY" with your actual OpenWeatherMap API key.

Step 3: run the Weather_AI.py.

Introduction:
The code uses the speech_recognition library for speech recognition and the pyttsx3 library for speech synthesis.

The search_wikipedia(query) function utilizes the wikipediaapi library to look up information from Wikipedia based on the query.

The get_weather(api_key, city) function uses the OpenWeatherMap API to retrieve weather information for the specified city using the provided api_key.

Within the while True loop, the program listens to audio from the microphone and performs speech recognition using robot_ear.recognize_google(audio, language='en') [NOTE: The program only recognizes the English language.].

If the user's speech matches certain conditions, the program executes corresponding actions.
If the user says "Hello", the program will replies "Hi! Let me know how I can help you today."
If the user says "today", the program will replies the day/month/year.
If the user says "time", the program will replies the time.
If the user says "bye", the program will replies "Goodbye! Let me know when you need help".
If the user says "information the user wants to look up" + "in Wikipedia", the program uses the function search_wikipedia(query) to look up information from Wikipedia and responds with the result or notifies "No information found on Wikipedia".

![image](https://github.com/HenryLe1998/481_final_project/assets/126354428/f7c88ee6-2dee-438e-9c93-5147db8a7805)
