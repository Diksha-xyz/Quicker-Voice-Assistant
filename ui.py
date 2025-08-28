import gradio as gr
from gtts import gTTS
import datetime
import wikipedia
import webbrowser
import pyjokes
import tempfile
import os
import speech_recognition as sr

# ----------------- Core Assistant Functions -----------------

def speak_text(text):
    """Convert text to speech and return audio file path."""
    try:
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        tts = gTTS(text=text, lang='en')
        tts.save(tmp_file.name)
        return tmp_file.name
    except Exception as e:
        return None

def tell_time():
    now = datetime.datetime.now().strftime("%H:%M:%S")
    return f"The current time is {now}"

def tell_date():
    today = datetime.datetime.now().strftime("%A, %d %B %Y")
    return f"Today is {today}"

def search_wikipedia(query):
    if not query.strip():
        return "Please provide a topic to search on Wikipedia."
    try:
        result = wikipedia.summary(query, sentences=2)
        return f"According to Wikipedia:\n{result}"
    except Exception as e:
        return "Sorry, I could not find anything on Wikipedia."

def tell_joke():
    return pyjokes.get_joke()

def open_youtube():
    webbrowser.open("https://youtube.com")
    return "Opening YouTube..."

def google_search(query):
    if not query.strip():
        return "Please provide a search query."
    webbrowser.open(f"https://www.google.com/search?q={query}")
    return f"Searching Google for '{query}'"

# ----------------- Gradio Assistant Handler -----------------

def assistant(query, action):
    """Handles the assistant logic for Gradio UI."""
    query = query or ""  # handle empty input

    if action == "Time":
        response = tell_time()
    elif action == "Date":
        response = tell_date()
    elif action == "Wikipedia":
        response = search_wikipedia(query)
    elif action == "Joke":
        response = tell_joke()
    elif action == "YouTube":
        response = open_youtube()
    elif action == "Google":
        response = google_search(query)
    else:
        response = "Unknown action."

    audio_file = speak_text(response)
    return response, audio_file

# ----------------- Gradio UI -----------------

with gr.Blocks() as demo:
    gr.Markdown("## Quicker Assistant 🤖\nInput your query via text or mic. Output is text + speech.")

    with gr.Row():
        query_input = gr.Textbox(label="Type your query here")
        # Updated mic input for latest Gradio
        mic_input = gr.Audio(sources=["microphone"], type="filepath", label="Or speak here")

    action_dropdown = gr.Dropdown(
        choices=["Time", "Date", "Wikipedia", "Joke", "YouTube", "Google"],
        label="Select Action"
    )

    output_text = gr.Textbox(label="Assistant Response")
    output_audio = gr.Audio(label="Audio Response", type="filepath")

    def process_input(text_input, mic_file, action):
        """Combine text and mic input; prioritize mic if available."""
        if mic_file:
            r = sr.Recognizer()
            with sr.AudioFile(mic_file) as source:
                audio_data = r.record(source)
            try:
                query = r.recognize_google(audio_data)
            except sr.UnknownValueError:
                return "Could not understand the audio.", None
            except sr.RequestError:
                return "Network error while recognizing audio.", None
        else:
            query = text_input or ""
        return assistant(query, action)

    submit_btn = gr.Button("Submit")
    submit_btn.click(
        process_input,
        inputs=[query_input, mic_input, action_dropdown],
        outputs=[output_text, output_audio]
    )

# ----------------- Launch for Render -----------------
if __name__ == "__main__":
    # Render provides PORT via environment variable
    demo.launch(server_name="0.0.0.0", server_port=int(os.environ.get("PORT", 8080)))


