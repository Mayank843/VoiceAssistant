import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
import datetime

# Text to speech
engine = pyttsx3.init()
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Listen to command
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(f"You said: {query}\n")
    except:
        speak("Sorry, I could not understand. Please say again.")
        return "None"
    return query.lower()

# Weather API
def getWeather(city="Haldwani"):
    api_key = "YOUR_OPENWEATHER_API_KEY"  # apna API key daalna
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("main"):
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        return f"{city} weather: {temp}°C, {desc}"
    return "Sorry, couldn't fetch weather."

# News API
def getNews():
    api_key = "YOUR_NEWSAPI_KEY"  # apna API key daalna
    url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={api_key}"
    response = requests.get(url).json()
    articles = response.get("articles")
    if articles:
        headlines = [a["title"] for a in articles[:5]]
        return headlines
    return ["Sorry, no news available."]

# Main loop
if __name__ == "__main__":
    speak("Hello boss, your assistant is ready!")
    while True:
        query = takeCommand()

        if "google" in query:
            speak("Opening Google")
            webbrowser.open("https://www.google.com")

        elif "youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif "weather" in query:
            weather = getWeather("Haldwani")
            speak(weather)
            print(weather)

        elif "news" in query:
            news_list = getNews()
            for i, headline in enumerate(news_list, 1):
                speak(f"Headline {i}: {headline}")
                print(f"{i}. {headline}")

        elif "time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")
            print(strTime)

        elif "exit" in query or "quit" in query:
            speak("Goodbye boss, see you soon!")
            break

        else:
            speak("I can open Google, YouTube, tell weather, news and time. What should I do?")

