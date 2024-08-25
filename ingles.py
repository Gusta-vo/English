import speech_recognition as sr
import pyttsx3
import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
import threading

# Configura el motor TTS
engine = pyttsx3.init()

def set_voice_language():
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'en' in voice.id:
            engine.setProperty('voice', voice.id)
            break

set_voice_language()

recognizer = sr.Recognizer()

WORDS_FILE = 'words.txt'

listening = True
listening_event = threading.Event()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_for_command(callback):
    global listening
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        while listening:
            listening_event.wait(timeout=1)
            if not listening:
                break
            try:
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                command = recognizer.recognize_google(audio, language='es-ES')
                callback(command)
                break
            except sr.UnknownValueError:
                speak("No entendí lo que dijiste.")
                callback(None)
                break
            except sr.RequestError:
                speak("No se pudo conectar al servicio de reconocimiento.")
                callback(None)
                break
            except Exception as e:
                speak(f"Ocurrió un error: {e}")
                callback(None)
                break

class VocabularyApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical')

        self.start_button = Button(text="Iniciar Cuestionario")
        self.start_button.bind(on_press=self.start_quiz)
        layout.add_widget(self.start_button)

        self.add_button = Button(text="Agregar Palabra")
        self.add_button.bind(on_press=self.add_word)
        layout.add_widget(self.add_button)

        self.exit_button = Button(text="Salir")
        self.exit_button.bind(on_press=self.exit_app)
        layout.add_widget(self.exit_button)

        return layout

    def load_words(self):
        words = []
        try:
            with open(WORDS_FILE, 'r', encoding='utf-8') as f:
                for line in f:
                    english, spanish = line.strip().split(',')
                    words.append((english, spanish))
        except FileNotFoundError:
            speak("No se encontró el archivo de palabras.")
        return words

    def start_quiz(self, instance):
        cards = self.load_words()
        if not cards:
            speak("No hay palabras para el cuestionario.")
            return

        def ask_question(index):
            if index >= len(cards):
                speak("Cuestionario terminado.")
                return
            
            english_word, spanish_word = cards[index]
            speak(f"How do you say '{english_word}' in Spanish?")
            
            def on_command_received(command):
                if command and command.strip().lower() == spanish_word.strip().lower():
                    speak("¡Correcto!")
                else:
                    speak(f"Incorrecto. La respuesta correcta es {spanish_word}.")
                ask_question(index + 1)

            # Iniciar el reconocimiento de voz en un hilo separado
            threading.Thread(target=listen_for_command, args=(on_command_received,)).start()
        
        # Empezar el cuestionario con la primera pregunta
        ask_question(0)

    def add_word(self, instance):
        # Aquí puedes implementar la lógica para agregar una nueva palabra al archivo
        speak("Funcionalidad para agregar palabras aún no implementada.")

    def exit_app(self, instance):
        global listening
        listening = False
        listening_event.set()
        self.stop()

if __name__ == "__main__":
    VocabularyApp().run()