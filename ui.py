import gradio as gr
import wikipedia
import speech_recognition as sr
from gtts import gTTS

recognizer = sr.Recognizer()

def voice_assistant(audio):
    # Step 1: Convert speech to text
    try:
        with sr.AudioFile(audio) as source:
            audio_data = recognizer.record(source)
            command = recognizer.recognize_google(audio_data)
    except:
        return "Sorry, I could not understand your voice.", None

    command = command.lower()
    response = ""

    # Step 2: Process command
    if "wikipedia" in command:
        query = command.replace("wikipedia", "")
        try:
            response = wikipedia.summary(query, sentences=2)
        except:
            response = "Sorry, I could not find anything on Wikipedia."
    elif "google" in command:
        response = "I can’t search Google directly here, but you can try Wikipedia instead."
    elif "hello" in command:
        response = "Hello! How can I help you?"
    else:
        response = "Sorry, I didn’t understand that."

    # Step 3: Convert response to audio
    tts = gTTS(text=response, lang="en")
    audio_file = "response.mp3"
    tts.save(audio_file)

    return response, audio_file

# Gradio interface
demo = gr.Interface(
    fn=voice_assistant,
    inputs=gr.Audio(source="microphone", type="filepath", label="🎤 Speak Now"),
    outputs=[gr.Textbox(label="Assistant Response"), gr.Audio(label="🔊 Assistant Voice", type="filepath")],
    title="Voice Assistant (Voice I/O)",
    description="Talk to the assistant using your mic. It will reply with both text and speech."
)

if __name__ == "__main__":
    demo.launch()


