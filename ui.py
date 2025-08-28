import gradio as gr
import wikipedia
from gtts import gTTS
import os

def assistant(query):
    try:
        result = wikipedia.summary(query, sentences=2)
    except:
        result = "Sorry, I couldn't find anything on that."
    
    # save as speech
    tts = gTTS(result)
    tts.save("response.mp3")
    
    return result, "response.mp3"

demo = gr.Interface(
    fn=assistant,
    inputs=["text"],   # or "mic" if you want microphone
    outputs=["text", "audio"]
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=8080)


