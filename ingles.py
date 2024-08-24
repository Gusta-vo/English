import speech_recognition as sr
import pyttsx3
import tkinter as tk
from tkinter import simpledialog, messagebox

# Configura el motor TTS
engine = pyttsx3.init()

# Configura el reconocimiento de voz
recognizer = sr.Recognizer()

# Archivo de almacenamiento de palabras
WORDS_FILE = 'words.txt'

def speak(text):
    """Función para hablar texto"""
    engine.say(text)
    engine.runAndWait()

def listen_for_command():
    """Función para escuchar y reconocer voz"""
    with sr.Microphone() as source:
        print("Escuchando...")
        recognizer.adjust_for_ambient_noise(source)  # Ajusta el reconocimiento al ruido ambiental
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            command = recognizer.recognize_google(audio)
            print(f"Has dicho: {command}")
            return command
        except sr.UnknownValueError:
            print("No entendí lo que dijiste.")
            speak("No entendí lo que dijiste.")
            return None
        except sr.RequestError:
            print("No se pudo conectar al servicio de reconocimiento.")
            speak("No se pudo conectar al servicio de reconocimiento.")
            return None
        except Exception as e:
            print(f"Ocurrió un error: {e}")
            speak(f"Ocurrió un error: {e}")
            return None

def start_quiz():
    """Función para manejar el flujo de tarjetas"""
    cards = load_words()
    if not cards:
        speak("No hay palabras para el cuestionario.")
        return
    for question, answer in cards:
        speak(f"¿Cómo se dice {question}?")
        response = listen_for_command()
        if response and response.lower() == answer.lower():
            speak("¡Correcto!")
        else:
            speak(f"Incorrecto. La respuesta correcta es {answer}.")

def load_words():
    """Función para cargar las palabras desde el archivo"""
    try:
        with open(WORDS_FILE, 'r') as file:
            return [tuple(line.strip().split(',')) for line in file if len(line.strip().split(',')) == 2]
    except FileNotFoundError:
        return []

def add_word():
    """Función para agregar palabras al archivo"""
    question = simpledialog.askstring("Agregar Palabra", "Introduce la palabra en español:")
    if question:
        answer = simpledialog.askstring("Agregar Palabra", "Introduce la traducción en inglés:")
        if answer:
            try:
                with open(WORDS_FILE, 'a') as file:
                    file.write(f"{question},{answer}\n")
                messagebox.showinfo("Éxito", "Palabra añadida con éxito.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {e}")

def create_app():
    """Configura la interfaz gráfica"""
    root = tk.Tk()
    root.title("Aplicación de Vocabulario")

    start_button = tk.Button(root, text="Iniciar", command=start_quiz)
    start_button.pack(pady=10)

    add_button = tk.Button(root, text="Agregar Palabra", command=add_word)
    add_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_app()