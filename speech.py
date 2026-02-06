from __future__ import annotations

import speech_recognition as sr
import pyttsx3


class SpeechIO:
    """Input/output abstraction for speech and text fallback."""

    def __init__(self, locale: str, text_mode: bool = False):
        self.locale = locale
        self.text_mode = text_mode
        self.recognizer = sr.Recognizer()
        self.tts = pyttsx3.init()
        self.tts.setProperty("rate", 175)

    def speak(self, message: str) -> None:
        print(f"Jarvis: {message}")
        self.tts.say(message)
        self.tts.runAndWait()

    def listen(self) -> str:
        if self.text_mode:
            return input("Tú> ").strip()

        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=0.4)
            print("Escuchando...")
            audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=10)

        try:
            return self.recognizer.recognize_google(audio, language=self.locale).strip()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
