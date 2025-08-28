import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import pyjokes


def speak(text):
    """Convert text to speech and print it."""
    print(f"Assistant: {text}")
    try:
        engine = pyttsx3.init(driverName='sapi5')   
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)  
        engine.say(text)
        engine.runAndWait()
        engine.stop()
    except Exception as e:
        print("⚠️ Speech output not supported:", e)


def take_command():
    """Listen to user command and return as text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("📝 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except sr.UnknownValueError:
        speak("Sorry, I could not understand. Please say that again.")
        return "None"
    except sr.RequestError:
        speak("Network error. Please check your internet connection.")
        return "None"

    return query.lower()


def tell_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    speak(f"The current time is {now}")

def tell_date():
    today = datetime.datetime.now().strftime("%A, %d %B %Y")
    speak(f"Today is {today}")

def search_wikipedia(query=None):
    """Search Wikipedia based on query or ask user for topic."""
    if not query or query.strip() == "":
        speak("What should I search on Wikipedia?")
        query = take_command()

    if query == "None":
        return
    
    try:
        result = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia:")
        speak(result)
    except Exception as e:
        speak("Sorry, I could not find anything on Wikipedia.")
        print("Error:", e)

def tell_joke():
    joke = pyjokes.get_joke()
    speak(joke)

def wish_user():
    hour = int(datetime.datetime.now().hour)
    if hour < 12:
        speak("Good Morning!")
    elif hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("Hello! I am your assistant Quicker. How can I help you today?")


if __name__ == "__main__":
    wish_user()
    while True:
        query = take_command()

        if "time" in query:
            tell_time()
        elif "date" in query:
            tell_date()
        elif "wikipedia" in query:
            
            topic = query.replace("wikipedia", "").strip()
            if topic == "":
                search_wikipedia("")   
            else:
                search_wikipedia(topic)
      
        elif "joke" in query:
            tell_joke()
        elif "open youtube" in query:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "google" in query:
            topic = query.replace("google", "").replace("search", "").strip()
            if topic == "":
                speak("What do you want me to search on Google?")
                topic = take_command()
    
            if topic != "None":
                speak(f"Searching Google for {topic}")
                webbrowser.open(f"https://www.google.com/search?q={topic}")

        elif "exit" in query or "bye" in query:
            speak("Goodbye! Have a nice day!")
            break