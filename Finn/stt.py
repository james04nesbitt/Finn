import speech_recognition as sr
import tkinter as tk

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        text_output.delete(1.0, tk.END)  # Clear previous text
        text_output.insert(tk.END, recognized_text)
    except sr.UnknownValueError:
        text_output.delete(1.0, tk.END)  # Clear previous text
        text_output.insert(tk.END, "Sorry, could not understand the audio.")
    except sr.RequestError:
        text_output.delete(1.0, tk.END)  # Clear previous text
        text_output.insert(tk.END, "Sorry, there was an error processing the audio.")

