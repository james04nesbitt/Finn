import tkinter as tk
import speech_recognition as sr

class SpeechToTextApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Continuous Speech to Text")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.start_button = tk.Button(self.frame, text="Start Recording", command=self.start_recording)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = tk.Button(self.frame, text="Stop Recording", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.grid(row=0, column=1, padx=5, pady=5)

        self.text_entry = tk.Text(self.frame, height=10, width=50)
        self.text_entry.grid(row=1, columnspan=2, padx=5, pady=5)

        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        self.is_listening = False

    def start_recording(self):
        self.is_listening = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.text_entry.delete(1.0, tk.END)
        while self.is_listening:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                try:
                    audio = self.recognizer.listen(source)
                    text = self.recognizer.recognize_google(audio)
                    self.text_entry.delete(1.0, tk.END)
                    if(text=="goodbye"):
                        self.stop_recording()
                        self.text_entry.insert(tk.END, "bye bye")

                    else:
                        self.text_entry.insert(tk.END, text)
                    self.text_entry.update_idletasks()
                except sr.UnknownValueError:
                    pass

    def stop_recording(self):
        self.is_listening = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = SpeechToTextApp(root)
    root.mainloop()
